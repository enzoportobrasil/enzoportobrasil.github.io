# Asset migration report

27 asset files moved; all original bytes preserved. Six active images, 20 reserve assets, and one unknown text file. No exact SHA-256 duplicates found. Finder metadata was also retained at `assets/reserve/metadata/img-ds-store`. No Git metadata is present, so filesystem renames were used.

## Moves, renames, and usage

Old paths and filenames below are intentional historical references, not production URLs. Formats were inspected by file signatures and image decoding; renaming did not transcode images.

| Old path | New path | Classification / usage |
| --- | --- | --- |
| `assets/img/2.1_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/satellite-coast.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/2.2_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/satellite-river.webp` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/2.3_MSc_research.webp.png` | `assets/reserve/research/02-spatial-extremes/2-3-msc-research.png` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. Spatial plots; scientific scenario unspecified, so original identifiers retained. |
| `assets/img/2.4_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/2-4-msc-research.png` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. Spatial plots; scientific scenario unspecified, so original identifiers retained. |
| `assets/img/2.5_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/spatial-parameter-panels.webp` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/2.6_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/spatial-fields.webp` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/2.7_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/amazon-map.png` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/2.8_MSc_research.webp` | `assets/reserve/research/02-spatial-extremes/amazon-map-wide.png` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/2_MSc_research.webp` | `assets/img/research/02-spatial-extremes/hero.png` | ACTIVE; index.html, research.html |
| `assets/img/3.2_imputation_extremes.webp` | `assets/reserve/research/03-imputation-extremes/scatter-density-panels.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/3.3_imputation_extremes.webp` | `assets/reserve/research/03-imputation-extremes/density-contours-alternative.webp` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/3_imputation_extremes.webp` | `assets/img/research/03-imputation-extremes/density-contours.jpg` | ACTIVE; index.html, research.html |
| `assets/img/4_sorce_mission_IA.webp` | `assets/img/research/04-sorce/hero.webp` | ACTIVE; index.html, research.html |
| `assets/img/5.1_compound_extremes.webp` | `assets/reserve/research/05-compound-extremes/copula-surfaces.png` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/5.2_compound_extremes.webp` | `assets/reserve/research/05-compound-extremes/copula-panels.png` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/5.4_compound_extremes.webp` | `assets/reserve/research/05-compound-extremes/volcano-alternative.webp` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/5_compound_extremes.webp` | `assets/img/research/05-compound-extremes/hero.webp` | ACTIVE; index.html, research.html |
| `assets/img/Enzo e Jéssica - 12-03-25 - 753.jpg` | `assets/reserve/personal/enzo-e-jessica-12-03-25-753.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/capa_nasa_1.webp` | `assets/img/site/hero-nebula.jpg` | ACTIVE; index.html |
| `assets/img/capa_nasa_3.webp` | `assets/reserve/site/nebula-alternative.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/favicon.svg` | `assets/reserve/site/favicon.svg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/profile._reserva.webp` | `assets/reserve/profile/profile-lakeside-portrait.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/profile.webp` | `assets/img/profile/profile-main.png` | ACTIVE; index.html |
| `assets/img/profile_2.webp` | `assets/reserve/profile/profile-courtyard.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/profile_3.webp` | `assets/reserve/profile/profile-with-dogs-original.jpg` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |
| `assets/img/profile_4.jpeg` | `assets/reserve/unknown/profile-4.txt` | ORPHAN / UNKNOWN; No references; file contains only CRLF bytes, not a photograph. |
| `assets/img/profile_5.webp` | `assets/reserve/profile/profile-with-dogs.webp` | RESERVE; No repository references; visual inspection confirms retained alternative or site artwork. |

## References updated

`index.html`, `research.html`. Only image URLs changed in these pages. CSS, JavaScript, text, layout, image sizing, and crop rules are unchanged. The existing files README was updated to match the new structure.

## Review notes

- `reserve/unknown/profile-4.txt` was named `profile_4.jpeg` but consists only of CRLF bytes. The original photograph is not present in that file; retain or replace it when its intended source is known.
- `2-3-msc-research.png` and `2-4-msc-research.png` are spatial plots, but their exact scenario labels are undocumented. Their identifiers are retained; descriptive scientific names can be supplied later.
- `profile-with-dogs-original.jpg` and `profile-with-dogs.webp` show the same photographic composition at different resolutions; they are not byte-for-byte duplicates and both are retained.
- The favicon was not referenced by any page; it remains in reserve. `profile-courtyard.jpg` is a JPEG with MPO metadata, preserved byte-for-byte.

## Integrity checksums

| New path | SHA-256 before and after |
| --- | --- |
| `assets/reserve/research/02-spatial-extremes/satellite-coast.jpg` | `49427d804f740bb9607b3511f3223a99562e12fa3854a6c34a71f83b40cc54fd` |
| `assets/reserve/research/02-spatial-extremes/satellite-river.webp` | `6b4911b121b2b2c64409b329eae2e8f15d948c8ffd0664f298e6af716989f935` |
| `assets/reserve/research/02-spatial-extremes/2-3-msc-research.png` | `d058933494de53f5bda4f2d486ddb113c7ee8b00cc24db7d2a5b5240e5d851e7` |
| `assets/reserve/research/02-spatial-extremes/2-4-msc-research.png` | `4f14f94772206aff26142e32f98c8fc117e97f342ea68c32419e24adf007bd5d` |
| `assets/reserve/research/02-spatial-extremes/spatial-parameter-panels.webp` | `355ac1a5a6a7825741e77162ba31df603899ec8b74c907fac8ccefa23bb6c359` |
| `assets/reserve/research/02-spatial-extremes/spatial-fields.webp` | `15e203d5e9cca91180699a825f086720838acbff182ef636e1d5708e7a969d52` |
| `assets/reserve/research/02-spatial-extremes/amazon-map.png` | `13912188db928390d40374ff95e5cfd79ba0e597c3c962a3bf0759be81676bd3` |
| `assets/reserve/research/02-spatial-extremes/amazon-map-wide.png` | `08fae55567e6812907f538ff75958d6df2270cf287b4454b64856830c6fbbe49` |
| `assets/img/research/02-spatial-extremes/hero.png` | `cf3a3197018603c0f4fac6d432986913faafd826c9df3f992486ad1de071d311` |
| `assets/reserve/research/03-imputation-extremes/scatter-density-panels.jpg` | `9425435a9ec764c927f0122b025e3a427bf6a471309e8cd967d286ba1292870f` |
| `assets/reserve/research/03-imputation-extremes/density-contours-alternative.webp` | `29c9266e5575e6dfb97bc74856f89fa1b66bba9c19a9c8eb815cd7bf5d105137` |
| `assets/img/research/03-imputation-extremes/density-contours.jpg` | `4472e6af716ad8a1e3d20b41c63b0cdc1a516062179ffac9f62f5ab53e3c06d9` |
| `assets/img/research/04-sorce/hero.webp` | `5b4956684e4f198adc854f4c8c7bb25588c84420eeeb5c93e2f7d967e2d7a4c9` |
| `assets/reserve/research/05-compound-extremes/copula-surfaces.png` | `280247aa7e1da040bda510e29a730e080d21d4ed3126d74296be33f90f9dd530` |
| `assets/reserve/research/05-compound-extremes/copula-panels.png` | `9d07e39425559586b5b80bbe044d2136b6e8e3dbc6590f46d2718858ea34d4d7` |
| `assets/reserve/research/05-compound-extremes/volcano-alternative.webp` | `e52aa73915155053e35cae4805b0d204caac3a92ee3341ac468146f6f91f3bc0` |
| `assets/img/research/05-compound-extremes/hero.webp` | `b16026e699d35811ea9d959cd1cd903f770740859f8d50e428620e119acdb92c` |
| `assets/reserve/personal/enzo-e-jessica-12-03-25-753.jpg` | `afa8d3e26b4c331f98a380f6f174bac75b62ac86c5f4f0f7f1ee05da4956a748` |
| `assets/img/site/hero-nebula.jpg` | `676e6dafcfc4bc83fc156a474883fe0aa9fbc8c652eef930baf246646987e3ea` |
| `assets/reserve/site/nebula-alternative.jpg` | `d11cf031492d95d62c39065ca0eae0fd3e1829dfa4ae4c3d39584a8184247cc7` |
| `assets/reserve/site/favicon.svg` | `29cf1996ac70023f8616cd1753190de774d0712680e1db404c335940de9b4bae` |
| `assets/reserve/profile/profile-lakeside-portrait.jpg` | `55e05d86a644312bbeb177855209ab97bef721a5291e3e8033edcfd7ef3511f9` |
| `assets/img/profile/profile-main.png` | `6e3b2e2399c26d75c455bf3747d7dca5f556d9833531bff1f7808695d75c2b76` |
| `assets/reserve/profile/profile-courtyard.jpg` | `fdfa9672a22ed45b5a5cffacfa3fe68453050780cbadf324a82c56ad301bb341` |
| `assets/reserve/profile/profile-with-dogs-original.jpg` | `20a92e23769aafb9caa09c7dccebdd0da1dc05fe18d71837fe8a19b733a9dfa9` |
| `assets/reserve/unknown/profile-4.txt` | `7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6` |
| `assets/reserve/profile/profile-with-dogs.webp` | `19411826c07a209afa60185e32d62f3e86f6566bc959d5a9107ae9d639733ae7` |

## Document structure created

All four canonical projects now have `papers/`, `preprints/`, `slides/`, `posters/`, `presentation-photos/`, `certificates/`, and `supplementary/`. General `assets/files/cv/` and `assets/files/certificates/` are also prepared: 30 directories with `.gitkeep`. No local PDFs or other academic documents were present to migrate, and no dummy documents were created.

## Validation

- Audited 15 production text files and resolved 143 local HTML/CSS references with exact path case: zero missing files.
- All six files in `assets/img/` are actively referenced; no unused production images remain.
- Zero production references to `assets/reserve/` or any migrated old path. Old names remain only in this historical report.
- Zero broken local document paths introduced; no local document downloads existed before migration (`cvPdf` remains empty).
- All 27 asset SHA-256 checksums match their pre-migration values; no exact byte duplicates found or deleted.
- Chrome HTTP check: all 11 HTML pages loaded; all 10 image instances decoded successfully; zero JavaScript errors.
- Only image path strings changed in `index.html` and `research.html`; CSS and JavaScript were not modified.
