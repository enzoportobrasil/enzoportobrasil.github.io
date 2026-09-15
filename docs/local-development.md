# Local preview and checks

This is a mostly static HTML site with a Jekyll source page at
`research/spatial-extremes.html`. Its opening YAML is intentional and valid.
Opening source files using `file://`, or serving the source directory with a
plain HTTP server, does not process that YAML.

Install Ruby (on Windows, use RubyInstaller with DevKit) and Bundler, then run
from the repository root:

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open `http://127.0.0.1:4000/` and
`http://127.0.0.1:4000/research/spatial-extremes.html`.
The Gemfile pins Jekyll 3.10.0, the engine listed by
[GitHub Pages](https://pages.github.com/versions/).

For a build without live reload:

```sh
bundle exec jekyll build
python -m http.server 4000 --bind 127.0.0.1 --directory _site
```

Serve the generated `_site` directory, not the source directory. The deployment
is a user site at `https://enzoportobrasil.github.io/`, with an empty base URL;
the existing relative asset and navigation paths resolve from that root.
Keep Jekyll enabled when publishing the source. This local copy contains no
`.git` directory or GitHub Actions configuration, so the remote Pages settings
cannot be verified from this copy.

## Verification

```sh
python tests/site-check.py
python -m pip install playwright
python tests/site-browser.py
```

The browser check uses installed Chrome on Windows and tests the generated
`_site` directory at 360, 390, 430, 768, 1024, 1280, 1440 and 1600 pixels in
English, Portuguese and Spanish. To test a different generated directory, set
`SITE_ROOT`; both check scripts support it. In PowerShell:

```powershell
$env:SITE_ROOT = (Resolve-Path '.site-work/generated').Path
python tests/site-check.py
python tests/site-browser.py .site-work/screenshots
```

QA artifacts and local runtime dependencies belong in `.site-work`, which is
excluded from both Git and the Jekyll output.

## Selected event photo decks

Run `python3 tools/build-event-photo-decks.py` after adding or renumbering photos
in the three configured `photos_selected` directories. Pillow is required;
HEIC decoding uses macOS `sips` or optional `pillow-heif` on other platforms.
The leading positive integer followed by `_` is authoritative (1, 2, …, 10).
Unnumbered images are reported and excluded; duplicate numbers stop the build.
Source files are never renamed or overwritten.

The builder updates only marked deck blocks in `talks.html` and records their
order, source hashes, alt text and enlargement targets in
`assets/data/event-photo-decks.json`. Unchanged WebPs are reused. Edit existing
alt text in that manifest before rebuilding. HEIC sources get a full-resolution
WebP for browser enlargement. The Huntsville postcard retains its individual
transparent-margin trim and sizing. Scientific plates and PDFs are independent
of the builder.
