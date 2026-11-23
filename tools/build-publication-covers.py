"""Render the document covers on publications.html from the vector PDFs.

Run: python tools/build-publication-covers.py [name ...]   (requires PyMuPDF and Pillow)
     With names, only those covers are rebuilt; without, all of them.

Two outputs per document, in assets/img/research/area-hubs/:
  <name>-cover-<w>.webp  thumbnail, exactly 160 x 226 CSS px (96 x 136 on phones), one
                         file per common screen density (1x, 1.25x, 1.5x, 2x, 3x), so the
                         browser never rescales it; strokes are darkened slightly so small
                         type keeps its contrast.
  <name>-page-<w>.webp   the whole first page at reading size, opened when the cover is
                         clicked (assets/js/cover-viewer.js).

Remote PDFs are downloaded once into _source-materials/covers/ (kept out of git).
Documents that are not online are kept there as a single-page PDF holding only the
cover page (<name>-p1.pdf); the full texts are not stored in the site folder.
To add a cover: add a line to COVERS, run this script, and copy the markup of an
existing cover on publications.html, changing only the name.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import io

import pymupdf
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/img/research/area-hubs'
CACHE = ROOT / '_source-materials/covers'
RATIO = 113 / 80                                   # thumbnail frame height / width (160 x 226)
THUMBS = [96, 160, 192, 200, 240, 288, 320, 480]   # phone 1x-3x and desktop 1x-3x
PAGES = [900, 1400, 2000]                          # reading view
COVERS = {
    'sorce-preprint': ('https://arxiv.org/pdf/2608.30878', 1),
    'imputation-preprint': ('https://arxiv.org/pdf/2602.04751', 1),
    'compound-preprint': ('https://arxiv.org/pdf/2608.10252', 1),
    'conditional-copula': ('https://arxiv.org/pdf/2607.26256', 1),
    'bsc': ('https://bdm.unb.br/bitstream/10483/38509/1/2023_EnzoPortoBrasil_tcc.pdf', 1),
    'pibic': ('assets/img/apresentacoes/pibic-2022/documents/dichotomous-imputation-full-text.pdf', 1),
    'ipea-td3261': ('assets/img/apresentacoes/panamerican-education-2026/documents/full-time-education-expansion-discussion-paper.pdf', 1),
    'hu-labor-relations': ('https://www.gov.br/hubrasil/pt-br/ensino-e-pesquisa/revista-juridica-da-hu-brasil/numero-atual/revista-juridica-da-ebserh-v2n2-dez2025.pdf', 72),
    'msc-dissertation': ('_source-materials/covers/msc-dissertation-p1.pdf', 1),
    'ipea-eti-dashboard': ('_source-materials/covers/ipea-eti-dashboard-p1.pdf', 1),
    'ipea-ppa-indicators': ('_source-materials/covers/ipea-ppa-indicators-p1.pdf', 1),
    'ipea-fundeb-chapter': ('_source-materials/covers/ipea-fundeb-chapter-p1.pdf', 1),
}


def pdf_bytes(source):
    if not source.startswith('http'):
        return (ROOT / source).read_bytes()
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / (hashlib.sha256(source.encode()).hexdigest()[:16] + '.pdf')
    if not cached.exists():
        request = Request(source, headers={'User-Agent': 'Mozilla/5.0 (site cover builder)'})
        with urlopen(request, timeout=120) as response:
            cached.write_bytes(response.read())
    return cached.read_bytes()


def raster(page, scale, oversample):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale * oversample, scale * oversample), alpha=False)
    image = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    return image.resize((round(page.rect.width * scale), round(page.rect.height * scale)), Image.LANCZOS)


def thumbnail(page, width):
    height = round(width * RATIO)
    # Fill the frame like CSS object-fit: cover, anchored to the top of the page.
    scale = max(width / page.rect.width, height / page.rect.height)
    image = raster(page, scale, 4)
    left = max(0, (image.width - width) // 2)
    image = image.crop((left, 0, left + width, height))
    # Darken antialiased strokes (gamma on the tones only; white stays white), then sharpen lightly.
    image = image.point(lambda v: round(255 * (v / 255) ** 1.6))
    return image.filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=0))


def full_page(page, width):
    image = raster(page, width / page.rect.width, 2)
    return image.filter(ImageFilter.UnsharpMask(radius=0.5, percent=40, threshold=0))


def build(names=()):
    unknown = set(names) - set(COVERS)
    if unknown:
        raise SystemExit(f'unknown cover name(s): {", ".join(sorted(unknown))}')
    for name, (source, page_number) in COVERS.items():
        if names and name not in names:
            continue
        page = pymupdf.open(stream=pdf_bytes(source), filetype='pdf')[page_number - 1]
        for width in THUMBS:
            thumbnail(page, width).save(OUT / f'{name}-cover-{width}.webp', 'WEBP', quality=95, method=6)
        for width in PAGES:
            full_page(page, width).save(OUT / f'{name}-page-{width}.webp', 'WEBP', quality=90, method=6)
        print(f'{name}: page {page_number}')


if __name__ == '__main__':
    import sys
    build(sys.argv[1:])
