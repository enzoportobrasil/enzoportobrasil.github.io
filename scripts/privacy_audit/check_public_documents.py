#!/usr/bin/env python3
"""Privacy safety check for the public website assets.

Scans the documents and text assets that ship with the site and fails when it
finds a high-confidence personal identifier. Detected values are always masked
before being printed, so the output is safe to paste into an issue or a CI log.

Usage:
    python3 scripts/privacy_audit/check_public_documents.py [--verbose]

Exit status:
    0  no high-confidence sensitive data found
    1  high-confidence sensitive data found (details, masked, on stdout)
    2  could not run (missing dependency)

Dependencies: none beyond the standard library. PDF text is read via `pdftotext`
(poppler) when available; without it, PDFs are still scanned as raw bytes, which
catches uncompressed text but is weaker. Install poppler for full coverage:
    brew install poppler
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Directories that are not published or not document assets.
SKIP_DIRS = {
    ".git", ".site-work", ".jekyll-cache", "_site", ".bundle",
    "no-ai-slop-main_SKILL", "__pycache__", "node_modules", "venv",
    "_source-materials",
}

DOC_EXT = {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".csv",
           ".xls", ".xlsx", ".xlsm", ".ppt", ".pptx"}
TEXT_EXT = {".html", ".md", ".markdown", ".json", ".yml", ".yaml",
            ".js", ".ts", ".css", ".scss", ".xml", ".tex", ".svg",
            # source files leak identifiers too - including this script, which
            # is deliberately not exempt from its own content rules.
            ".py", ".mjs", ".sh", ".rb", ".txt"}

# ---------------------------------------------------------------------------
# Registration-number machinery, shared by the content and path rules.
#
# Only the 4-digit intake-year PREFIXES appear in this file. No complete
# registration number is ever written literally here, in a fixture, a comment
# or a regex example - an earlier version of this script did exactly that and
# leaked the real values into the public repository.
# ---------------------------------------------------------------------------
_REG_PREFIXES = ("1801", "2411")                     # undergraduate, postgraduate
_REG_NUMBER = r"(?<!\d)(?:" + "|".join(_REG_PREFIXES) + r")\d{5}(?!\d)"

# Separator run for CONTENT rules. Deliberately excludes newlines: allowing \s
# here made "patrones de matrícula\n2nd Pan-American..." a false positive.
_SEPC = r"[ \t_.:\-]{0,4}"


# ---------------------------------------------------------------------------
# HIGH confidence: a match is a failure.
# ---------------------------------------------------------------------------
HIGH = [
    ("CPF",              re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("CPF_CONTEXT",      re.compile(r"(?i)\bCPF\b[^0-9\n]{0,24}\d[\d.\- ]{9,16}\d")),
    ("RG_CONTEXT",       re.compile(r"(?i)\bRG\b[ \t]*[:nº.\-]{0,4}[ \t]*\d[\d.\-/ ]{4,14}\d")),
    ("REG_KNOWN_PREFIX", re.compile(_REG_NUMBER)),
    ("REG_MATRICULA",    re.compile(r"(?i)matr[ií]cula" + _SEPC + r"n?[o\u00ba]?" + _SEPC + r"\d{4,}")),
    ("REG_REGISTRATION", re.compile(r"(?i)registration" + _SEPC + r"(?:number|no|nr)?" + _SEPC + r"\d{4,}")),
    ("REG_STUDENT_ID",   re.compile(r"(?i)student" + _SEPC + r"(?:id|number|no)" + _SEPC + r"\d{4,}")),
    ("REG_ENROLLMENT",   re.compile(r"(?i)enrol{1,2}ment" + _SEPC + r"(?:number|no|nr)?" + _SEPC + r"\d{4,}")),
    ("PASSPORT_CONTEXT", re.compile(r"(?i)\b(?:passaporte|passport)\b[ \t]*[:nº.\-]{0,4}[ \t]*[A-Z]{0,2}\d{6,9}\b")),
    ("VOTER_CONTEXT",    re.compile(r"(?i)t[ií]tulo[ \t]+de[ \t]+eleitor[ \t]*[:nº.\-]{0,4}[ \t]*\d{4}")),
    ("CNH_CONTEXT",      re.compile(r"(?i)\bCNH\b[ \t]*[:nº.\-]{0,4}[ \t]*\d{9,11}\b")),
]

# ---------------------------------------------------------------------------
# REVIEW: reported for a human to look at, does not fail the run.
# ---------------------------------------------------------------------------
REVIEW = [
    ("BIRTHDATE_LABEL", re.compile(r"(?i)\bdata\s+de\s+nascimento\b|\bdate\s+of\s+birth\b")),
    ("CEP",             re.compile(r"(?<!\d)\d{5}-\d{3}(?!\d)")),
    ("LOCAL_PATH",      re.compile(r"(?i)(?:/Users/[a-z0-9._-]+|[A-Z]:\\Users\\[^\s\\]+)")),
    ("VERIFY_TOKEN",    re.compile(r"(?i)https?://\S*(?:token|validar|autentic)\S*")),
]


# ---------------------------------------------------------------------------
# PATH rules: applied to file names and directory names, not to file contents.
#
# A registration number leaks just as effectively through a path as through a
# document body, and a path is visible in every directory listing, every commit
# and every URL. These rules therefore run over EVERY file in the tree, not only
# the ones whose contents we can parse.
#
# They are label-driven on purpose. Flagging any long number in a filename would
# fire on research output like "..._S20_T200_rep001.pdf", so a match needs an
# explicit academic-registration label next to the digits.
# ---------------------------------------------------------------------------
_SEP = r"[\s._:\-]*"          # space, dot, underscore, colon or hyphen, any run

PATH_HIGH = [
    ("PATH_MATRICULA",
     re.compile(r"(?i)matr[ií]cula" + _SEP + r"n?[o\u00ba]?" + _SEP + r"\d{4,}")),
    ("PATH_REGISTRATION_NO",
     re.compile(r"(?i)registration" + _SEP + r"(?:number|no|nr)?" + _SEP + r"\d{4,}")),
    ("PATH_STUDENT_ID",
     re.compile(r"(?i)student" + _SEP + r"(?:id|number|no)" + _SEP + r"\d{4,}")),
    ("PATH_ENROLLMENT_NO",
     re.compile(r"(?i)enrol{1,2}ment" + _SEP + r"(?:number|no|nr)?" + _SEP + r"\d{4,}")),
    # Known-value rule. These are the registration-number prefixes this person's
    # institution issues (intake-year based), so a bare 9-digit run with one of
    # them is high confidence even with no label beside it - which is exactly how
    # it appeared in "Ficha_ENZO BRASIL_<number>.pdf". Extend this list if another
    # prefix turns up; it is deliberately narrow to avoid matching dates or sizes.
    ("PATH_KNOWN_REG_PREFIX", re.compile(_REG_NUMBER)),
]

# Conservative contextual rule: a long digit run in a document path is flagged
# only when the path also carries academic-registration context.
PATH_CONTEXT = re.compile(
    r"(?i)matr[ií]cula|registration|enrol|student|aluno|discente"
    r"|disserta|tese|thesis|diploma|hist[oó]rico|transcript|certificad")
PATH_LONG_DIGITS = re.compile(r"(?<!\d)\d{6,}(?!\d)")
# Runs that are almost always dates or sizes, not identifiers.
PATH_DIGIT_BENIGN = re.compile(
    r"^(?:(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])"   # YYYYMMDD
    r"|(?:0[1-9]|[12]\d|3[01])(?:0[1-9]|1[0-2])(?:19|20)\d{2})$")   # DDMMYYYY


def path_findings(rel_path: str):
    """Return [(label, masked_sample)] for a repo-relative path. Never the raw value."""
    out = []
    for label, rx in PATH_HIGH:
        m = rx.search(rel_path)
        if m:
            out.append((label, mask(m.group())))
    if not out and PATH_CONTEXT.search(rel_path):
        for m in PATH_LONG_DIGITS.finditer(rel_path):
            if not PATH_DIGIT_BENIGN.match(m.group()):
                out.append(("PATH_DIGITS_WITH_ACADEMIC_CONTEXT", mask(m.group())))
                break
    return out


def mask(value: str) -> str:
    """Replace every alphanumeric character, so no real identifier is printed."""
    return re.sub(r"[0-9A-Za-z]", "*", value)


def pdf_text(path: str) -> str:
    if shutil.which("pdftotext"):
        try:
            r = subprocess.run(["pdftotext", "-layout", "-q", path, "-"],
                               capture_output=True, text=True, timeout=180)
            if r.stdout.strip():
                return r.stdout
        except (subprocess.SubprocessError, OSError):
            pass
    try:                                      # weaker fallback: raw bytes
        with open(path, "rb") as fh:
            return fh.read().decode("latin-1", "replace")
    except OSError:
        return ""


def ooxml_text(path: str) -> str:
    parts = []
    try:
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.endswith((".xml", ".rels")):
                    try:
                        parts.append(z.read(name).decode("utf-8", "replace"))
                    except (KeyError, OSError):
                        continue
    except (zipfile.BadZipFile, OSError):
        return ""
    return re.sub(r"<[^>]+>", " ", "\n".join(parts))


def plain_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def extract(path: str, ext: str) -> str:
    if ext == ".pdf":
        return pdf_text(path)
    if ext in (".docx", ".xlsx", ".xlsm", ".pptx"):
        return ooxml_text(path)
    return plain_text(path)


def iter_all_paths():
    """Every file in the tree, for path-based checks."""
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            yield os.path.relpath(full, REPO)


def iter_files():
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            ext = os.path.splitext(name)[1].lower()
            if ext in DOC_EXT or ext in TEXT_EXT:
                full = os.path.join(dirpath, name)
                yield full, os.path.relpath(full, REPO), ext


def self_test() -> int:
    """Regression test for the path rules. Standard library only, no fixtures file.

    Fixture identifiers are BUILT AT RUNTIME so that no complete registration
    number exists as a contiguous literal anywhere in this source file.
    """
    # EVERY fixture number is assembled at runtime. Because this script is not
    # exempt from its own content rules, a literal "label + digits" sequence in
    # this source would make the scanner fail on itself - correctly.
    tail    = "9" * 5
    fake_ug = _REG_PREFIXES[0] + tail          # synthetic undergraduate value
    fake_pg = _REG_PREFIXES[1] + tail          # synthetic postgraduate value
    n6      = "8" * 6                          # synthetic 6-digit id
    n9      = "7" * 9                          # synthetic 9-digit id

    must_flag = [
        f"assets/img/x/dissertacao NAME - matricula {fake_pg} - final.pdf",
        f"assets/docs/Ficha_NAME_{fake_ug}.pdf",
        f"a/Matrícula: {fake_pg} relatorio.pdf",
        f"a/student-id-{n6}.pdf",
        f"a/registration_number_{n6}.pdf",
        f"a/enrollment no {n6}.pdf",
        f"a/historico-escolar-{n9}.pdf",
    ]
    must_not_flag = [
        "assets/img/research/02-spatial-extremes/fig_C3_scn_S20_T200_rep001.pdf",
        "assets/img/research/03-imputation/n_20_40_graficos.1_mesclado.pdf",
        "assets/other_certificates/events/2024_sinape-participation.pdf",
        "assets/other_certificates/courses/2021_datacamp-intro-r.pdf",
        "assets/img/apresentacoes/sys2025/web/album/waterside-panorama-1600.webp",
        "assets/files/cv/Enzo_Porto_Brasil_Academic_CV.pdf",
        "assets/certificado_20260917.pdf",
        "assets/img/profile/profile-main-1024.webp",
        "docs/transcript-notes.md",
    ]
    # content rules must fire on a label followed by digits, and must not fire
    # across a line break
    content_flag = [
        f"Matrícula: {fake_ug}",
        f"student id {fake_pg}",
        f"registration number {n6}",
        f"enrolment no {n6}",
    ]
    content_ok = [
        "padrões de matrícula\n2nd Pan-American Meeting on the Economics of Education",
        "his registration was confirmed in 2024",
        "students enrolled: 278",
    ]

    bad = []
    for p in must_flag:
        if not path_findings(p):
            bad.append(("MISSED PATH", p))
    for p in must_not_flag:
        f = path_findings(p)
        if f:
            bad.append(("FALSE POSITIVE PATH", p, [x[0] for x in f]))
    for t in content_flag:
        if not any(rx.search(t) for _, rx in HIGH):
            bad.append(("MISSED CONTENT", t[:40]))
    for t in content_ok:
        hit = [n for n, rx in HIGH if rx.search(t)]
        if hit:
            bad.append(("FALSE POSITIVE CONTENT", t[:40], hit))

    total = len(must_flag) + len(must_not_flag) + len(content_flag) + len(content_ok)
    print(f"self-test: {total - len(bad)}/{total} cases correct")
    for b in bad:
        print("  FAIL", b)
    if bad:
        return 1
    print("self-test OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true",
                    help="also list files scanned with no findings")
    ap.add_argument("--self-test", action="store_true",
                    help="check the path rules against known cases and exit")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if not shutil.which("pdftotext"):
        print("note: pdftotext not found, PDF text-layer coverage is reduced "
              "(install poppler for full coverage)", file=sys.stderr)

    failures, reviews, scanned = [], [], 0

    # path/filename scan first: it covers files whose contents we cannot parse
    paths_scanned = 0
    for rel in iter_all_paths():
        paths_scanned += 1
        for label, sample in path_findings(rel):
            failures.append((rel, label, 1, sample))
    for full, rel, ext in iter_files():
        # This script is NOT exempt. Its rules are written so that the pattern
        # definitions cannot match themselves, and it must be able to catch a
        # real identifier accidentally pasted into its own source.
        blob = extract(full, ext)
        scanned += 1
        for label, rx in HIGH:
            hits = rx.findall(blob)
            if hits:
                failures.append((rel, label, len(hits), mask(str(hits[0])[:40])))
        for label, rx in REVIEW:
            hits = rx.findall(blob)
            if hits:
                reviews.append((rel, label, len(hits)))

    print(f"scanned {scanned} document and text assets "
          f"and {paths_scanned} paths under {REPO}")

    if reviews:
        print(f"\nREVIEW ({len(reviews)} findings, not failures):")
        for rel, label, n in reviews:
            print(f"  {label:16} x{n:<4} {rel}")

    if failures:
        print(f"\nFAIL: {len(failures)} high-confidence sensitive finding(s):")
        for rel, label, n, sample in failures:
            print(f"  {label:16} x{n:<4} {rel}   e.g. {sample}")
        print("\nValues above are masked. Do not commit these files.")
        return 1

    if args.verbose:
        print("\nno high-confidence sensitive data found in any scanned asset")
    print("\nOK: no high-confidence personal identifiers found.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
