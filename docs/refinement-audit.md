# Refinement and functional audit

Website copy preserved.

## Files changed

- `assets/css/styles.css`: research image proportions, balanced titles, small labels, publication rows, reading widths and accessible caption presentation.
- `assets/css/spatial-extremes.css`: balanced thesis heading, readable metadata and caption styling.
- `assets/css/bgev-animation.css`: 12px minimum for small UI labels and reduced tracking; mathematical code unchanged.
- `publications.html`: one external PDF URL replaced; no text changed.
- `tests/site-check.py`: supports `SITE_ROOT` to audit generated output.
- `tests/site-browser.py`: defaults to generated output, adds viewport widths, checks front-matter processing and local HTTP failures, waits for image decoding.
- `_config.yml`: excludes dependency files and existing QA screenshots from published output.
- `.gitignore`: excludes local builds, runtime dependencies and QA artifacts.
- `Gemfile` (new): Jekyll 3.10.0 and WEBrick for the preview workflow.
- `docs/local-development.md` (new): source/build distinction, preview and checks.
- `docs/refinement-audit.md` (new): this report.

## Visual findings and fixes

The homepage map combined `object-fit: contain` with a minimum-height wrapper, creating dark bands. Its wrapper now follows the native 1672:941 ratio and uses cover, without editing the image or losing the edge legend. Scientific figures on the research index retain their complete intrinsic proportions without empty container bands.

The SORCE/XPS grid previously allocated 67.5% of column space to the image. It now allocates 47.5% to copy and 52.5% to the image, with a fluid 32–72px gap and a 3:2 desktop frame, switching to 16:9 when stacked. Its unchanged title fits two balanced lines at 1280px.

Research image captions and number badges are visually suppressed. Scientific caption context remains available to screen readers; alt attributes and image links are unchanged. Duplicate links within hidden captions are excluded from keyboard navigation; each destination remains available through its linked image. Portrait captions and the hero credit are preserved.

Small editorial labels use a shared 0.75rem scale and reduced uppercase tracking. Body copy uses the existing 72ch reading measure. The research-practice heading has fluid sizing, a 26ch maximum, 1.08 line height and balanced wrapping. Page hero titles also wrap with balance. Publication rows have consistent year/content/CTA tracks, fluid gaps, 30px vertical padding and mobile stacking.

## Functional findings

All 431 local references on all 11 generated pages pass checks for files, fragments, path case and excluded assets. Navigation, research links, breadcrumbs, active state, PDFs, language/theme preferences, mobile menu, certificate filters and talk controls passed browser checks.

One publication URL returned 404 after the publisher's site migration. Its replacement is the [official issue PDF](https://www.gov.br/hubrasil/pt-br/ensino-e-pesquisa/revista-juridica-da-hu-brasil/numero-atual/revista-juridica-da-ebserh-v2n2-dez2025.pdf#page=72), opening at printed page 71 (PDF page 72). Button wording, title, author list and year are unchanged.

Four distinct arXiv links and the event/YouTube/GitHub links responded with 200. The UnB repository responded with 200 in Chrome; Python's certificate store could not verify its chain. LinkedIn returned automation-block status 999, so it remains unverified rather than being treated as a broken URL.

## Front matter diagnosis

Diagnosis B: valid Jekyll source opened without Jekyll processing. The file starts with the correct delimiter, without BOM or stray characters. `layout: null` is appropriate for complete standalone HTML; the permalink matches the public route. No Liquid syntax requires correction.

A real Jekyll 3.10.0 safe-mode build produced HTML beginning with `<!doctype html>`, tested over localhost. This is the engine version listed by [GitHub Pages](https://pages.github.com/versions/). See the [Jekyll front matter documentation](https://jekyllrb.com/docs/front-matter/). No front matter was deleted; direct `file://` preview remains inappropriate.

Ruby was initially absent. Validation used an isolated Ruby installation and the unmodified Jekyll build API. Native live-reload dependencies required unavailable MSYS2, so the generated output was served with Python HTTPServer. This does not claim a successful `bundle exec jekyll serve` run. The normal Ruby+DevKit and Bundler workflow is documented separately.

## Validation and limits

- Jekyll build completed without errors.
- 597 browser assertions passed across 11 pages, three languages and widths 360, 390, 430, 768, 1024, 1280, 1440 and 1600px.
- No horizontal page overflow, JavaScript exceptions or failed local HTTP responses in the final run.
- Images loaded; screenshots were inspected for homepage features and every research page. Both BGEV numerical/reference suites passed.
- All text nodes in all 11 HTML pages match the initial snapshot. Homepage and research HTML remain byte-identical. Only a publication URL changed in HTML; translations and scientific assets are untouched.
- Evidence: `.site-work/polish-qa`. Generated site: `.site-work/generated`. Source snapshots: `.site-work/polish-baseline`.

No copy changes are recommended or awaiting approval. No design decision remains open. This supplied directory lacks `.git` metadata and a deployment workflow, so remote GitHub Pages configuration and deployment were not verified or changed.
