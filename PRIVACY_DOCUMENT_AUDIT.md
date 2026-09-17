# Privacy Audit — Public Documents

**Date:** 2026-09-17 · **Scope:** the website repository and the repository that publishes it
**Status:** sanitization and withdrawal complete in both working trees; **Git-history remediation pending human approval**

This report contains **no personal identifier values and no verification credentials**.
Identifiers are referred to only by type. Where a count appears it counts occurrences,
never values.

Repositories covered:

| Role | Path | Remote |
|---|---|---|
| Working source | `6. site_enzo_porto_brasil_v1` | none |
| **Publishing** | `0_site_enzo/enzoportobrasil.github-3.io-dev_correto` | `github.com/enzoportobrasil/enzoportobrasil.github.io` |

Both trees now hold byte-identical public documents.

---

## Summary

| | |
|---|---|
| Documents and text assets scanned | 209 documents + 59 text/code assets |
| Safe as-is (Class A, unmodified) | 175 |
| Sanitized (Class B) | 24 |
| Withdrawn from the public repositories (Class C) | 96 |
| Manual review (Class D) | 7 items, all now resolved to a recommendation |
| High-confidence identifiers in either working tree | **0** |
| Verification credentials on public certificates | **0** |
| **Sensitive data in published Git history** | **YES — unresolved, see below** |

### What was found

Two findings dominated.

**1. A CPF in selectable body text, not in an image.** The University of Brasília
SIGAA extension-certificate template prints the holder's CPF inline in the certifying
sentence. It appeared in 76 PDFs, 24 of them linked from the live site.

**2. Other people's personal data.** One archived file — a university provisional PIBIC
results list — carried the **CPF of six other people and the academic registration
numbers of 278 other students**, plus several phone numbers. It was tracked by Git and
present in the published repository, though never linked from a page. Two further
archived certificates belong to other named individuals, and four spreadsheets held
family and friends' emails and phone numbers.

### Method

- Text layers read with `pdftotext -layout` and PyMuPDF; OOXML unzipped and stripped of
  markup; images checked for EXIF/GPS with Pillow.
- Redaction uses PyMuPDF `add_redact_annot` + `apply_redactions(PDF_REDACT_TEXT_REMOVE)`,
  which **deletes glyphs from the content stream**. No black rectangles, no overlays,
  nothing recoverable by selection, copy-paste or `pdftotext`.
- Redaction rectangles are built from **tight per-glyph bounding boxes clipped against
  neighbouring text lines**. This matters: the certificate template's line boxes overlap
  vertically by 2.35 pt, and a naive rectangle silently destroys words on the line below.
- Every public file is then re-verified against its own **fully decompressed** byte
  stream (`qpdf --stream-data=uncompress --decode-level=all`), including a search for the
  target characters separated by arbitrary text operators, which is how a naive check
  misses kerned text.
- A word-for-word comparison against the pristine original proves that **no character
  other than the redacted values was removed**.

---

## Public documents

### Class B — sanitized in place (24 files)

All 24 are UnB extension certificates, in two template families: 19 upright
(SIGAA) and 5 on 90°-rotated pages (SIEX).

**Removed irreversibly from the public copies:**

| Value | Why | Occurrences |
|---|---|---|
| CPF | personal identifier | 24 |
| `Código de verificação` value | SIGAA retrieval credential | 19 |
| `Número do Documento` value | SIGAA retrieval credential | 19 |
| SIEX 32-character validation hash | SIEX retrieval credential | 10 |

Total: **72 redactions across 24 files.** The verification credentials are removed
because together they are a route back to the original document, and the institutional
verification view of that document displays the CPF. Redacting the CPF alone would have
left that route open.

**Preserved unchanged:** holder's name, activity or course title, coordinator,
department, role, dates, attendance figure, institution, issuers' signatures,
institutional logo, ornamental border, and the generic (credential-free) instruction URL.

**Public URLs are unchanged. No HTML, JSON, CSS or JavaScript file was edited in either
repository.**

| Public file | Sensitive elements removed | Redactions | Public replacement | Validation |
|---|---|---|---|---|
| `courses/social-education-humanities/2021_study-autonomy.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2018_ie-2018.pdf` | CPF ×1, SIEX hash ×2 | 3 | same path | PASS (18/18) |
| `events/2018_science-beyond.pdf` | CPF ×1, SIEX hash ×2 | 3 | same path | PASS (18/18) |
| `events/2019_galaxies-guide.pdf` | CPF ×1, SIEX hash ×2 | 3 | same path | PASS (18/18) |
| `events/2019_ie-2019.pdf` | CPF ×1, SIEX hash ×2 | 3 | same path | PASS (18/18) |
| `events/2019_professional-choice.pdf` | CPF ×1, SIEX hash ×2 | 3 | same path | PASS (18/18) |
| `events/2020_black-women-scientists.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_career-guidance.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_chomsky.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_complexity-art.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_creativity.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_indian-trigonometry.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_math-degree.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_personal-agenda.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_psychopathy.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_pythagoras.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_science-religion.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_scientific-writing.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2020_social-media.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2021_quantum-concept.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2021_unb-python.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2021_unb-r.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2022_sbpc-2022.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |
| `events/2023_brands.pdf` | CPF ×1, verif. code, doc. number | 3 | same path | PASS (18/18) |

No QR codes or barcodes exist on any of the 24 — the embedded images are template and
logo rasters only, so there is nothing encoded left to decode.

Measured impact: **0.160 %–0.381 % of page area changed** per file. All pages kept their
original dimensions. Each file carries a discreet label, **verified by reopening the
saved file and confirming the text lies inside the page box**:

> Cópia pública - identificadores pessoais e credenciais de verificação suprimidos por privacidade.

The same statement is recorded in each file's PDF `Subject` metadata. These files are
**not** presented as untouched official originals.

### Class C — withdrawn from both public repositories (96 files)

None were used by the website; the only reference was `_archive/inventory.json`, an
internal bookkeeping file, withdrawn with them. Every file was copied to a private store
outside both repositories and checksum-verified before removal. All 96 copies in the
publishing clone were confirmed byte-identical to the private originals first.

| Group | Files | Why |
|---|---|---|
| `_archive/academic-record/` | 2 | own registration number (also in the filename); one file holds **278 other students' registration numbers and 6 other people's CPF** |
| `_archive/compiled-records/` | 3 | own CPF, RG, date of birth |
| `_archive/professional-record/` | 3 | internship records: own CPF, RG, date of birth |
| `_archive/obsolete-cv/` | 3 | superseded CVs |
| `_archive/temporary-working-file/` | 8 | mailing lists with **other people's** emails and phone numbers |
| `_archive/duplicate/` | 43 | duplicate certificates, 36 with the own CPF; includes **two certificates belonging to other named individuals**. 16 were byte-identical to clean live certificates, which is expected and harmless |
| `_archive/event/` | 19 | duplicate certificates with the own CPF |
| `_archive/course/` | 5 | duplicate certificates with the own CPF |
| `_archive/research-document/` | 2 | duplicate of a published proceedings volume |
| `_archive/` metadata | 4 | `inventory.json` repeated the own registration number in filename strings |
| `other_certificates/` strays | 2 | unlinked; one carried the own CPF |
| `assets/reserve/personal/` | 1 | **not a privacy issue — see correction below.** Unlinked byte-identical duplicate of the published profile portrait; withdrawn only as a redundant 5 MB copy |

#### Correction — the `assets/reserve/personal/` file

The first pass of this audit described this file as a private photograph of the author
and one other person, inferred from its filename. **That was wrong.** Byte-comparison
during the publishing-repository validation showed it is SHA-256-identical to
`assets/img/profile/profile-main.png`, and visual inspection confirms both are the same
**solo portrait of the site owner** already published on the site as
`profile-main-1024.webp` / `profile-main-640.webp`. The filename carries the photo
session's name, not the photo's contents.

Consequences, stated plainly:

- Withdrawing this file was **not** a privacy fix. It removed an unreferenced duplicate
  of an already-public image. The original is preserved privately and can be restored.
- The three references listed below as containing this path therefore contain the
  **published profile photo**, not private content. Their history risk is downgraded
  accordingly.

Related observation, not a privacy finding and **not acted on**: four full-resolution
profile source images remain unreferenced in the public repositories
(`profile-main.png`, `profile-main-2.png`, `profile-main - Copia.png`,
`profile-main - Copia_jpeg.jpg`, together roughly 12 MB, 3610×5415). They are the same
published portrait, so there is no disclosure concern; removing them would be a
housekeeping choice, outside the scope of this audit.

### Class A — safe as-is, unmodified (175 files)

- `assets/files/cv/` — published academic CV and LaTeX source. Only the public
  professional email, GitHub, LinkedIn and city. (A `Nascimento` match was a co-author's
  surname.)
- All research figures, posters, slides, abstracts and full texts.
- All presentation photographs. **No GPS data in any image in either repository.**
- 46 certificates with no identifier: DataCamp, Coursera, ADBI, EMR, STAMPS, SINAPE,
  COBIPE, UAH, and the UnB colloquium monitor and coordinator certificates.
- No PDF contains an embedded file, attachment, form value or local filesystem path.

---

## Manual review — final recommendations

| # | Item | Recommendation |
|---|---|---|
| 1 | `academic-service/2021_colloquium-reviewer.pdf` — the 216-page official *Livro de Resumos* of the VI Colóquio, with 96 author correspondence emails | **SAFE TO PUBLISH.** Published scholarly proceedings; the `CEP` matches are institutional addresses in author affiliations. Content unmodified. **But the site description is inaccurate — see below.** |
| 2 | SIGAA / SIEX verification credentials on the 24 certificates | **SANITIZED.** Resolved in this pass: all 72 credential and identifier instances removed. |
| 3 | `courses/climate-earth-ocean/2025_climate-sovereign-risk.pdf` — ADBI verifier URL with a short numeric course code | **SAFE TO PUBLISH.** The code identifies the *course*, not the holder, and the page returns no personal data. Distinct from the UnB case, where the credential retrieves a CPF-bearing document. |
| 4 | `cobipe-2024/.../oral-presentation-certificate.pdf` — the *signing official's* employee registration number, already partly masked by the issuing university | **SAFE TO PUBLISH.** Third-party, system-generated, published that way by UFRN. Not the site owner's data. |
| 5 | Issuers' handwritten signatures on certificates | **SAFE TO PUBLISH.** They belong to the issuing officials and are integral to the documents as the institutions published them. Removing them would damage authenticity for no privacy gain. |
| 6 | Co-authors' personal email addresses on posters and abstracts | **SAFE TO PUBLISH.** Published by the conferences in that form; standard scholarly correspondence data. Removing them would misrepresent the published record. |
| 7 | Image EXIF: camera make/model and capture timestamps on 46 images; no GPS. Three profile photographs also carry `Artist` / `Copyright` naming the photographer | **SAFE TO PUBLISH.** Recommend explicitly **not** stripping the photographer attribution — it is a copyright credit, not personal data of the site owner. Camera model and timestamps are low-risk; strip only if you want the extra tidiness. |

### Item 1 — proposed site-description correction (NOT applied)

The entry's **title is accurate**: Enzo appears in the PDF as *Comitê do Livro de
Resumos — Revisão*. What is inaccurate is how the **linked file** is described. The card
renders `Academic service certificate` and the link reads `View certificate ↗`, but the
target is a 216-page proceedings volume, not a certificate.

Referenced in exactly two places: the `colloquium-reviewer` entry in
`assets/data/certificates.json`, and the generated card in `resources.html`.

The label is data-driven — `tools/build-certificates.py` uses
`x.get('type_label') or {…}[kind]` — so the type label is a one-field data change:

```json
"id": "colloquium-reviewer",
"type_label": "Abstract booklet (proceedings volume)",
```

The link text is currently hardcoded. Making it per-entry needs a one-line tool change,
`links = link(x, x.get('link_label') or 'View certificate ↗')`, plus:

```json
"link_label": "View abstract booklet ↗",
```

Then regenerate with `python3 tools/build-certificates.py`. A trilingual site will also
need translation rows for any new label string. **None of this has been applied** — it is
presentation accuracy, not privacy, and it is your call.

---

## Automated safety check

`scripts/privacy_audit/check_public_documents.py` — present in both repositories. Scans
every document and text asset, reads PDF text layers, masks everything it reports, and
exits non-zero on a high-confidence identifier. Standard library only.

Verified in both directions: exits `0` on both clean working trees, and exits `1` with
masked output when pointed at known-positive originals held privately.

The one remaining `REVIEW` line is item 1 above — institutional addresses in a published
proceedings volume, not personal data.

### Publishing-repository validation, 2026-09-17

Re-verified against the publishing repository after the migration, by checksum against
the private manifest rather than by filename:

- 24 sanitized certificates match their expected SHA-256 in **both** repositories (24/24
  identical), and all 24 open with academic text intact.
- 96 Class C files absent from both working trees; 120 private originals verified intact
  outside both repositories.
- 0 private originals, pre-redaction copies or private manifests present in either repo.
- Independent sweep of 117 PDFs (decompressed streams, text, metadata, annotations, form
  values), 273 images (EXIF) and 71 text assets: **0 findings** across CPF, RG,
  registration number, phone, CEP, date of birth, address, SIGAA code, document number,
  SIEX hash, embedded attachments, annotation text, form values, EXIF GPS and filenames.
- The repository's own checker, `tests/site-check.py`, reports 7 pages, 462 local
  references, `failures: []`. `node --test tests/*.test.mjs` passes 2/2. 379 asset
  references resolve, 0 broken, 0 references to withdrawn files.
- A local Jekyll build could **not** be run: the Jekyll gems are not installed in either
  repository and installing them was out of scope. GitHub Pages builds server-side, and
  this change touches no layout, template or content file, so the build surface is
  unchanged. This is stated as a limitation, not a pass.

---

## Git history

### URGENT — SENSITIVE FILES REMAIN IN PUBLISHED GIT HISTORY

Removing a file from a working tree does not remove it from history. Until the history of
`github.com/enzoportobrasil/enzoportobrasil.github.io` is rewritten, the pre-sanitization
versions of the documents described in this report remain fetchable from earlier commits.
This includes the archived material described under Class C — among it personal data
belonging to **other people**, not only to the site owner.

Scope, in aggregate: **95 withdrawn file paths (77 distinct blobs)** and the **24
pre-redaction certificates**, reachable from the two active branches and from one tag.
Three further branches contain only the published profile photo and need no rewrite.

**This report intentionally does not list the specific commits, paths or reference names.**
While the data is still reachable, publishing a precise map of where it sits would make it
easier to retrieve, and this report is itself a public file. The full technical detail —
affected commits, every reference, the exact `git filter-repo` invocation, verification
commands, rollback procedure, GitHub Pages implications and cache-invalidation steps —
is held **outside both repositories**, at:

```
enzoportobrasil-private-documents/HISTORY_REMEDIATION_PLAN.md
```

That plan has **not been executed**. History rewriting is destructive, changes every
commit ID from the earliest affected commit onward, requires a force-push and a re-clone
of every working copy, and needs explicit owner approval.

Two points that are easy to get wrong and are worth stating here:

- A force-push alone does not evict the old objects from GitHub. They can remain
  retrievable by commit SHA until GitHub garbage-collects, and **forks are not rewritten**.
  A support request and a fork check are part of the remediation, not optional extras.
- The underscore-prefixed archive directory was skipped by Jekyll and so never appeared
  in the built site, but it was fully readable through the repository itself. The Jekyll
  exclusion protected nothing.

Because the material was publicly reachable, the other people's identifiers should be
treated as disclosed regardless of remediation.

---

## Remaining actions

1. **Commit both repositories** (nothing is committed yet).
2. **Push the publishing repository**, so the live site stops serving the affected files.
3. **Git-history rewrite** — see above. Highest-priority remaining risk.
4. Optional, non-privacy: the item 1 site-description correction.
