# Asset architecture

## Production images
`assets/img/` contains only images referenced by production pages. Site-wide imagery lives in `site/`, the active portrait in `profile/`, and project imagery in `research/[project]/`.

## Research documents
`assets/files/research/[project]/` groups locally hosted academic materials. Each project has `papers/`, `preprints/`, `slides/`, `posters/`, `presentation-photos/`, `certificates/`, and `supplementary/`. Empty directories contain `.gitkeep`, not dummy documents. No research PDFs were present during migration.

| Project | Canonical directory slug |
| --- | --- |
| Bayesian spatial extremes / MSc thesis | `02-spatial-extremes` |
| Multiple imputation under extreme values | `03-imputation-extremes` |
| SORCE/XPS solar spectral irradiance | `04-sorce` |
| Dependence and compound climate extremes | `05-compound-extremes` |

The same slugs apply to research images, documents, and reserve images when present. Folder numbering is archival organization; page project order is unchanged.

Original presentation photographs belong in `files/research/[project]/presentation-photos/`; web images actively displayed belong in `img/research/[project]/`. General CVs go in `files/cv/`, and unrelated academic certificates in `files/certificates/`.

## Reserve assets
`assets/reserve/` retains unused alternatives, historical imagery, personal photographs, unused site artwork, and unresolved files. Production HTML/CSS/JS must never reference this tree. These files are unlinked, not access-controlled; a static deployment may still publish their URLs. No content was deleted or converted.

## Naming and maintenance
Use lowercase-kebab-case directories and `lowercase-kebab-case.ext` filenames, with one extension matching the actual format. Use `YYYY-event-description.ext` for dated documents, e.g. `2025-uah-astrostatistics-slides.pdf`, `2025-rbras-compound-extremes-poster.pdf`, `2025-uah-presentation-01.jpg`, and `2025-uah-certificate.pdf`.

Use descriptive reserve suffixes such as `-wide`, `-portrait`, `-detail`, `-alternative`, or `-original`; avoid `final2`, `new`, `copy`, or `test`. Two spatial plot identifiers were retained because their precise scientific scenarios are not documented.

Before moving assets, search HTML, CSS, JS and data for direct and dynamic references. Move rather than copy, update every reference with exact case, then verify local URLs and ensure every production image is referenced. Compare checksums when moving originals. Use `git mv` in a Git checkout; this working copy has no `.git` directory.

See [ASSET_MIGRATION_REPORT.md](ASSET_MIGRATION_REPORT.md) for the complete old-to-new map, active/reserve inventory, format corrections, checksums, and validation results.
