# CV sources

This directory holds the website's public **Academic CV** — a general,
non-application-specific CV meant for the CV page and public download.

- `academic_cv.tex` — LaTeX source for the general Academic CV. Built from the
  same master template/macro architecture as Enzo's targeted PhD-application
  CVs (identical `\documentclass`, packages, geometry, colours, typography,
  section/entry macros, footer and page-numbering system). Only the
  application-specific positioning block (headline, keywords, profile text)
  and the curated section content were changed — no macro, spacing length, or
  layout definition was touched.
- `Enzo_Porto_Brasil_Academic_CV.pdf` — compiled output, linked from
  `cv.html`.

## Compiling

The template supports both engines (`\ifPDFTeX` branch uses `tgpagella`;
the `\else` branch uses `fontspec`). The approved reference CV this template
was copied from was itself built with **pdfTeX** and TeX Gyre Pagella — the
`fontspec` branch requires "Charis SIL" or "TeX Gyre Pagella" registered as
*system* fonts (not just TeX packages), which is often not the case outside
Overleaf. To guarantee byte-identical typography with the approved template
and avoid any accidental font substitution, compile with:

```sh
pdflatex academic_cv.tex
pdflatex academic_cv.tex   # second pass resolves lastpage/pageref
mv academic_cv.pdf Enzo_Porto_Brasil_Academic_CV.pdf
```

If your environment has "Charis SIL" or "TeX Gyre Pagella" installed as
system fonts, `xelatex academic_cv.tex` (run twice) also works and should
render identically.

Targeted, application-specific CV variants (e.g. for a particular PhD
programme) are kept outside this repository and are not affected by this
file.
