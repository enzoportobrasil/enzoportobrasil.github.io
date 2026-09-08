# Presentation materials

The site uses static HTML in `talks.html` and the shared stylesheet plus
`assets/css/talks.css`. No build step or dependencies are required. The Huntsville album uses the small progressive-enhancement script `assets/js/photo-album.js`.

## Event folders

- `workshop-pgest-unb-2026/`: invited talk, 11 June 2026.
- `sys2025/`: contributed oral presentation, 15 November 2025; workshop 14–17 November.

Each event uses:

```text
event-slug/
  documents/  complete slide deck and available certificates (PDF)
  photos/     original photographs, including those not selected
  figures/    original figures and one-page PDF excerpts
  web/        selected, re-encoded WebP photos and rendered PDF previews
```

`file-manifest.json` maps all 29 original filenames to their new paths, with SHA-256
checksums, material type and selection status. Files were renamed without changing
their bytes; no originals or unselected materials were deleted or overwritten.
Finder's `.DS_Store` files are not research materials and were left untouched.
There were no pre-existing site references to the old asset paths.

Web photos have their original proportions, are not cropped or enlarged beyond
the source resolution, and contain no inherited EXIF metadata. The 480/1024 suffixes
are target width limits; `srcset` uses the actual pixel widths. Scientific previews
use 800/1600/2400 pixels, WebP quality 94. Images open directly at larger resolution,
following the existing research page convention. The sys2025 diagram also links to
its original vector PDF; that one-page file is **not** the complete slides.

## Sources and curation

### UnB

- Title, date and event: slide 1 of `documents/extremos-na-natureza-slides.pdf`
  (26 pages). Original title: “Extremos na Natureza: estatística, incerteza e
  previsão diante de fenômenos extremos”.
- Institution: Universidade de Brasília, as named on the title slide.
- Invited-speaker role: supplied by the site owner; not inferred from photos.
- Description: slides 4–12 and 23–24.
- Selected: presenting-models photo; workshop-conversation photo; preview of slide 5.
- No certificate was supplied. No empty certificate link is rendered.

### sys2025

- Full title, presentation date and city: slide 1 of
  `documents/joint-extremes-slides.pdf` (35 pages).
- Full workshop name, 14–17 November dates, Huntsville, and contributed-talk role:
  `documents/participation-certificate.pdf` (1 page), issued by UAH.
- Description: slides 18–20. The figure is the supplied block-maxima workflow
  used in slide 29, not an independently inferred result.
- Selected: a seven-photo album (Morton Hall portrait, campus autumn, Cramer Research Hall, gravitational-wave session, UAH research centre portrait, Space & Rocket Center, Huntsville postcard), plus the unchanged maxima workflow figure. The previous two selected photos and their web copies are preserved but no longer displayed.
  No photo of Enzo delivering the Alabama talk was present, so captions do not
  claim that any of the selected photos shows that presentation.
- Certificate reviewed visually and as text: professional participation details,
  institutional contact information and the issuer's signature; no personal ID,
  private address or private contact details requiring a public redacted copy.
  PDFs remain byte-for-byte original, including the signed certificate.

## Add the next presentation

1. Create a short lowercase event folder, e.g. `event-name-2027`, with the same
   subfolders as needed. Use lowercase, hyphenated filenames. Keep a manifest entry
   for renamed originals; never overwrite files. Do not put sensitive originals
   into the published site: retain those in a private archive and use a genuinely
   redacted public copy after checking both PDF text and rendered pages.
2. Read the complete slides and available certificate to confirm title, event,
   participation, date and place. Do not infer a talk date from a photo timestamp.
3. Select roughly three images. Preserve aspect ratios, faces and scientific labels.
   Convert unsupported photo formats to genuine browser-compatible copies; strip
   metadata from public photo copies. Render selected PDF pages to WebP previews;
   keep complete slides separate from figure excerpts.
4. Copy one `<article class="talk-event">` in `talks.html`, placing the newest first.
   Update its unique `id`, heading ID and `aria-labelledby`, date (`datetime`), text,
   captions, alt text, image dimensions, `srcset` and links. Add its jump link at the
   top if useful. Reuse the existing CSS; the text is English, with original titles
   marked using `lang` where appropriate.
5. The two primary links must point to the **same complete slide PDF**. Give the
   download link a descriptive `download` filename. Update language, page count
   and size (decimal MB). Omit the certificate anchor, optional photo or any other
   missing resource entirely. Never add disabled placeholder buttons.
6. Check at desktop, 390 px and 320 px widths: no horizontal overflow, all images
   load, faces and plots remain intact, and menu/theme controls work. Open the
   slide PDF and certificate; download the slides and compare the downloaded file
   to the original. Check every local `href`, `src` and `srcset` path.

Other existing presentations remain in the compact list. Their unavailable
material buttons were removed; existing titles/statuses were not re-researched.

## Huntsville album

The album lives only inside `#sys2025` in `talks.html`. Its ordered photo records
are in the adjacent `<script type="application/json" data-album-photos>` block.
To change the sequence, update those records (`src`, `srcset`, dimensions, `alt`,
`caption`). Keep the first static image, caption, enlargement links and counter
consistent with the first record; these work without JavaScript. The counter
uses the record count after navigation. Maintain `file-manifest.json` selection
flags when changing the curation.

`web/album/` contains fresh WebP copies at target widths 480 and 1200, never
upscaled beyond original resolution, quality 89, without inherited metadata.
The actual widths are used in `srcset`. No original files were modified.
Only the first photo is in the initial HTML; the next image is prefetched when
the album enters the viewport (unless Save-Data is enabled). Subsequent images
are decoded on demand before replacing the current photo. A failed load leaves
the current photo visible and announces a retry message.

Controls stop at the first/last image. Arrow keys, Home and End work only while
focus is inside the album. Horizontal touch swipes change photos; vertical page
scrolling and pinch zoom remain available. There is no autoplay or wrapping.
The frame uses `object-fit: contain`, so both portrait and landscape photographs
remain complete. The short fade is disabled for reduced motion. Enlargement
opens the larger WebP directly, as elsewhere on the site.

## coBIPE 2024

`cobipe-2024/` contains five preserved originals from
`1s_workshop_prob_est_brasil_colombia/`: two JPEG photographs of the oral talk,
one HEIC panorama, the complete 27-page slide deck, and a separate one-page MSE
figure. Their old/new paths and hashes are recorded in `file-manifest.json`.
The HEIC was decoded to PNG before generating real WebP copies; it was not merely
renamed. All three photographs are in the album, opening with the audience-facing
portrait, followed by the scenario discussion and the panorama. The panoramic
location is not named because the supplied materials do not identify it.

Title, authors and talk date (18 September 2024) come from slide 1. The title uses
“techniques”, correcting the former short entry's “methods”. The description is
based on slides 13–20. The standalone figure is labelled 20% and is presented as a
separate result graphic, not as the complete slides or as an exact slide extract.
No certificate was supplied. No certificate button is rendered.

The event's name, UFRN/Natal location and 16–18 September dates are also confirmed
by the Associação Brasileira de Estatística's August 2024 bulletin, page 11:
https://www.redeabe.org.br/wp-content/uploads/2025/02/Boletim-ABE-110-Agosto.pdf

The existing album component is reused. Each static photo needs a unique ID;
controls reference that ID and the shared script preserves it on photo changes.
The JSON record count determines album length, so a three-photo event needs no
special code. All original files and existing event content remain intact.

## Latest coBIPE and Huntsville layout refinement

coBIPE now displays only the two presentation photos, as large static images with
normal enlargement links. Its panorama and generated copies remain archived but
are no longer selected. The new text is a concise paraphrase of the supplied
`cobipe-2024/documents/imputation-abstract.pdf`, excluding author email footnotes.
That PDF is retained as a source and is not linked from the page.
`oral-presentation-certificate.pdf` is linked as the certificate of oral presentation;
both original pages are intact, including the verification sheet. The personnel
number was already masked in the supplied document. Renaming preserves hashes.
These decisions supersede the earlier three-photo album/no-certificate notes.

Huntsville retains its seven-photo carousel and scientific figure, but the album
now occupies a full-width row below the text, with a taller stable frame and
responsive source sizing inherited by the gallery script. The figure also uses
more of the desktop width. Other events retain their previous layout.


## Complete event update — September 2026

The current page has featured oral/invited talks, a static poster/research archive, and a separate accepted-presentations list. Existing UnB, SYS2025 and coBIPE materials remain in place.

### New events and sources

- `emr-epbest-2025`: two complete Portuguese posters, two presentation certificates and two separately labelled participation certificates. Dates in the certificates: EPBEST 27–28 October; EMR 29–31 October 2025, João Pessoa. Selected photos: `between-posters` and `poster-session-group`.
- `rbras-seagro-2025`: three complete coauthored posters and their presentation certificates, 4–8 August 2025, Vitória. Certificates establish that the works were presented, not who personally presented each one; the page uses “Coauthored posters”. The two supplied abstracts are preserved but not linked redundantly. The temperature/humidity abstract and final poster differ numerically, so the description covers methods without reproducing their differing estimates.
- `wasa-2024`: full poster, abstract, presentation certificate and all photographs. The original folder said 2025, but the abstract and certificate both confirm 23–25 October **2024**, UnB, Brasília. Selected photos: `poster-selfie` and `auditorium-group`.
- `pibic-2022`: full 12-page Portuguese report, complete 15-page slides and **research programme** certificate. The certificate covers September 2021–August 2022 and does not certify an oral presentation. The slides and recording are dated 1 September 2022. The page describes the recorded presentation without inventing a congress name/date. The summary preserves the report's distinction between recovery accuracy, mean prediction error and its variability.

`file-manifest.json` records all renamed originals and SHA-256 values, including paths outside this folder. All 43 originals handled during this update retained their exact bytes. One older record, `cobipe-2024/photos/waterside-panorama.heic`, was already absent when audited; its available web derivatives remain preserved and unused. The manifest retains its original hash and records its current availability.

### Upcoming entries

Only the two education/financing works remain: ANPOCS and the Panamerican Meeting on the Economics of Education. Complete titles and event dates come from the newly supplied acceptance letters. ANPOCS confirms GT70 and online/in-person event periods; it does not list all coauthors or an individual presentation slot. The Panamerican letter lists four authors and the submission category “Resumo”; it does not identify an oral/poster format. Do not invent those details.

The previously advertised Bayesian and workforce SINAPE presentations were removed following the author's explicit cancellation, without recategorising them as presented. Their former entries remain in Git history. The new letters are preserved in `_source-materials` at project root, outside publication; the Panamerican original includes a participant-print URL. Public entries link to official event pages instead.

### Video and web copies

YouTube's public oEmbed endpoint returned HTTP 200 and an embed URL for `ZFK-9LS7n0A`, confirming the supplied title. `talk-video.js` progressively enhances a working YouTube link into a button that creates a `youtube-nocookie.com` iframe only after clicking. There is no autoplay parameter or initial player request. The direct YouTube link remains available below the frame. The preview is an actual frame from the local recording at 15 seconds, exported as 640/1280px WebP. The unchanged MP4 is in `_source-materials/pibic-2022`, ignored by Git and excluded from the Pages build; maintain a separate backup.

New photos have 480/1200/1800px WebP copies; posters have 600/1200/2200px copies and always link to the original vector PDF for reading. Photos retain their complete frame, carry no EXIF metadata, and use lazy loading. Poster previews are generated from the supplied PDF, never treated as complete slides. Existing Huntsville album behaviour is unchanged.

`_config.yml` excludes original-photo folders, unused source documents, personal extra photos and the local archive from GitHub Pages output. If deploying by a manual copy instead, respect the same exclusions. The five extra personal photographs were renamed under `assets/img/fotos-extras-estilo/photos`; none is inserted as decoration or associated with an unrelated event.

### Reference checks

Consulted: official SYS2025, RBras/SEAGRO and UnB workshop pages; official ANPOCS page; Panamerican Even3 event page; all supplied local certificates/posters/letters. Selected verified official links appear in their entries. Instagram, the UFRN repository item and the EMR/EPBEST page did not return usable content during the checks, so no proceedings membership or additional details are inferred from them.

### Add the next event

1. Use an `event-year/` folder with `documents/`, `photos/` for unchanged originals and `web/` for browser copies. Add old/new paths and hashes to the manifest.
2. Copy the matching static `talk-event` or `poster-work` block in `talks.html`. Fill only confirmed metadata, identify Portuguese documents, and omit unavailable resources.
3. Generate responsive WebP copies, set real dimensions, `srcset`, descriptive alt text, lazy loading and a brief caption. Link poster/slide previews to their complete PDF; photo enlargement links to the largest web copy.
4. Keep certificates secondary and label their exact purpose. For a future accepted work, use the `#upcoming .output-item` pattern until the presentation is confirmed as delivered.
5. Add unused original material to the Pages exclusions, keep private/heavy local sources in `_source-materials`, and check desktop/mobile, local paths and downloads.


### Verification performed

- Chrome at 1440, 390 and 320 CSS pixels: reviewed new event layouts, all images decoded and no horizontal overflow.
- Huntsville: manual arrows, Home/End, finite boundaries and a touch swipe. The existing seven-photo album remains intact.
- 24 distinct linked PDFs returned HTTP 200 with `application/pdf`; all 11 download controls produced byte-identical copies of their source PDFs using real browser clicks.
- PIBIC: no initial iframe; clicking loads the YouTube player, visually confirmed with its play control and without autoplay. Blocking both enhancement scripts preserves the first album photograph and the external YouTube preview link.
- All local HTML resource paths and fragment targets checked, and all 43 newly handled originals matched their recorded hashes. No public HTML link points into a Pages-excluded source path.
