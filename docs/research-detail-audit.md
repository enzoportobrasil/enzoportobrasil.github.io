# Research-detail refinement

## Scope and architecture

Four standalone HTML routes share the existing site shell:

- `research/spatial-extremes.html`
- `research/solar-irradiance.html`
- `research/missing-data-extremes.html`
- `research/climate-dependence.html`

No Liquid includes or Markdown layout are used by these essays. The dissertation
route has intentional Jekyll front matter (`layout: null`, explicit permalink).
Jekyll 3.10 processes it correctly. A raw HTTP server or `file://` shows the YAML;
preview the generated site as documented in `local-development.md`.

The original detail styles came from `styles.css`, an additional thesis stylesheet,
and two inline sidebar spacing rules. Global CSS also visually hid research captions.
The new `research-detail.css` replaces the thesis-only stylesheet and scopes every
selector to `.research-detail` on `main`. It restores captions, sets reading widths,
and provides common hero, metadata, figure, output-row and related-research patterns.
No global stylesheet, navigation, overview, homepage, Publications, Talks, CV or
Applied Research Outputs content was edited in this task.

## Scientific sources and figure selection

The local final dissertation is the canonical source for the spatial page. The
abstract, model formulation, simulation discussion, application and conclusions
support the account. Five figures form the narrative: dissertation Figures 2.2,
4.17, 5.5, 5.9 and 5.10. Existing distribution, simulation and return-level images
are reused. Station and posterior-field figures are cropped directly from PDF
pages 122 and 129 (printed pages 98 and 105).

The page distinguishes descriptive gridded summaries from full Bayesian prediction
at unobserved sites. It reports the 11-station domain, quarterly construction,
location-parameter mixing limitations, residual temporal dependence and the absence
of formal prior-sensitivity analysis. It does not claim operational forecasting.

Other sources, read alongside existing repository presentations:

- Solar: <https://arxiv.org/abs/2608.30878>, Figures 1 and 4. The mission record
  and tail diagnostics replace a workflow from a separate solar–atmospheric study.
- Missing data: <https://arxiv.org/abs/2602.04751>, Figures 1 and 2. The clean and
  contaminated benchmarks support the simulation setup; the prose distinguishes
  predictive performance from interval coverage and restricts claims to the design.
- Dependence: <https://arxiv.org/abs/2608.10252>, Figures 12 and 13. The fitted
  contours and marginal-model comparison replace the dominant poster. The earlier
  RBras/SEAGRO poster is retained as a small output preview.
- Related theory: <https://arxiv.org/abs/2607.26256>, retained as a separate output.

`assets/img/research/detail-figures/sources.json` records source URLs/paths, PDF page
numbers and crop rectangles in PDF points. WebP derivatives preserve axes, legends,
data and geometry; no scientific figures were generated or redrawn. Original PDFs
and original images are unchanged. Source PDFs for the preprints and working
renders remain in the ignored local QA directory.

## Verification

- Source-site static check: all 599 local references pass.
- Real Jekyll 3.10 build succeeds; the generated dissertation begins with a doctype,
  and contains no visible front matter.
- Chrome: all four generated routes pass at 1440, 1200, 1024, 768 and 430 pixels,
  in EN/PT/ES (60 combinations), with no horizontal overflow, broken images or
  JavaScript/local HTTP errors. Existing localization is retained; newly authored
  scientific prose uses English.
- Visual review covers desktop/mobile pages, light theme and source-figure crops.
- Main-page files and global CSS/JavaScript match the task-start hashes. Existing
  unrelated working-tree changes are preserved.
- `git diff --check` passes.

The full generated-site static check also exposed an existing, out-of-scope issue:
Jekyll excludes some `photos_selected` files referenced by Talks. Source-file links
pass, but those photo originals are absent from the build. The research-detail
routes do not reference them. Talks and `_config.yml` were intentionally untouched.

Run focused browser checks with `python tests/research-detail-browser.py` after a
Jekyll build. `SITE_ROOT` selects another generated directory; `CHROME_PATH` can
select a Chrome executable. Screenshots and results go to `.site-work`.
