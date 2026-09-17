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
            ".js", ".ts", ".css", ".scss", ".xml", ".tex", ".svg"}

# ---------------------------------------------------------------------------
# HIGH confidence: a match is a failure.
# ---------------------------------------------------------------------------
HIGH = [
    ("CPF",              re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("CPF_CONTEXT",      re.compile(r"(?i)\bCPF\b[^0-9\n]{0,24}\d[\d.\- ]{9,16}\d")),
    ("RG_CONTEXT",       re.compile(r"(?i)\bRG\b[ \t]*[:nº.\-]{0,4}[ \t]*\d[\d.\-/ ]{4,14}\d")),
    ("STUDENT_ID",       re.compile(r"(?<!\d)1801\d{5}(?!\d)")),
    ("PASSPORT_CONTEXT", re.compile(r"(?i)\b(?:passaporte|passport)\b[ \t]*[:nº.\-]{0,4}[ \t]*[A-Z]{0,2}\d{6,9}\b")),
    ("VOTER_CONTEXT",    re.compile(r"(?i)t[ií]tulo[ \t]+de[ \t]+eleitor[ \t]*[:nº.\-]{0,4}[ \t]*\d{4}")),
    ("CNH_CONTEXT",      re.compile(r"(?i)\bCNH\b[ \t]*[:nº.\-]{0,4}[ \t]*\d{9,11}\b")),
]

# ---------------------------------------------------------------------------
# REVIEW: reported for a human to look at, does not fail the run.
# ---------------------------------------------------------------------------
REVIEW = [
    ("BIRTHDATE_LABEL", re.compile(r"(?i)\bdata\s+de\s+nascimento\b|\bdate\s+of\s+birth\b")),
    ("MATRICULA_LABEL", re.compile(r"(?i)\bmatr[ií]cula\b[ \t]*[:nº.\-]{0,4}[ \t]*\d{4,}")),
    ("CEP",             re.compile(r"(?<!\d)\d{5}-\d{3}(?!\d)")),
    ("LOCAL_PATH",      re.compile(r"(?i)(?:/Users/[a-z0-9._-]+|[A-Z]:\\Users\\[^\s\\]+)")),
    ("VERIFY_TOKEN",    re.compile(r"(?i)https?://\S*(?:token|validar|autentic)\S*")),
]


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


def iter_files():
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            ext = os.path.splitext(name)[1].lower()
            if ext in DOC_EXT or ext in TEXT_EXT:
                full = os.path.join(dirpath, name)
                yield full, os.path.relpath(full, REPO), ext


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true",
                    help="also list files scanned with no findings")
    args = ap.parse_args()

    if not shutil.which("pdftotext"):
        print("note: pdftotext not found, PDF text-layer coverage is reduced "
              "(install poppler for full coverage)", file=sys.stderr)

    failures, reviews, scanned = [], [], 0
    for full, rel, ext in iter_files():
        # never scan our own pattern definitions
        if os.path.abspath(full) == os.path.abspath(__file__):
            continue
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

    print(f"scanned {scanned} document and text assets under {REPO}")

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
