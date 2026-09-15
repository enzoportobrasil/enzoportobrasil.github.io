"""Build static event decks in numeric source-filename order.

Run: python3 tools/build-event-photo-decks.py (requires Pillow).
HEIC decoding uses macOS sips; elsewhere install pillow-heif.
Unnumbered images are reported and omitted; duplicate numbers are errors.
The manifest records source hashes to avoid recompressing unchanged images.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import quote
from PIL import Image, ImageOps
import hashlib
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'assets/img/apresentacoes'
MANIFEST = ROOT / 'assets/data/event-photo-decks.json'
EVENTS = {
    'sys2025': ('Huntsville', 'Huntsville, in photographs'),
    'emr-epbest-2025': ('EPBEST / EMR', 'EPBEST / EMR'),
    'wasa-2024': ('WASA', 'WASA'),
}
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif'}


def ordered_photos(directory):
    numbered, unnumbered = [], []
    for source in directory.iterdir():
        if not source.is_file() or source.suffix.lower() not in EXTENSIONS:
            continue
        match = re.match(r'^([1-9][0-9]*)_(.+)$', source.name)
        if match:
            numbered.append((int(match[1]), source))
        else:
            unnumbered.append(source.name)
    numbers = [n for n, _ in numbered]
    if len(set(numbers)) != len(numbers):
        raise ValueError(f'Duplicate numeric prefixes in {directory}')
    return [p for _, p in sorted(numbered, key=lambda item: item[0])], unnumbered


class ExistingAlts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.alts = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img' and attrs.get('alt') and attrs.get('src'):
            stem = re.sub(r'-\d+$', '', Path(attrs['src']).stem)
            self.alts[stem] = attrs['alt']


def build():
    page = ROOT / 'talks.html'
    html = page.read_text()
    known = ExistingAlts()
    known.feed(html)
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    manifest = {}
    for event, (label, heading) in EVENTS.items():
        sources, unnumbered = ordered_photos(BASE / event / 'photos_selected')
        if not sources:
            raise ValueError(f'No numbered photos for {event}')
        records = []
        old = {r['source']: r for r in previous.get(event, {}).get('photos', [])}
        for position, source in enumerate(sources):
            source_path = source.relative_to(ROOT).as_posix()
            stem = re.sub(r'^\d+_', '', source.stem)
            postcard = event == 'sys2025' and 'huntsville-postcard' in stem
            slug = 'huntsville-postcard' if postcard else stem
            target = BASE / event / 'web/deck' / (slug + '.webp')
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            cached = old.get(source_path) or next((r for r in old.values() if r['sha256'] == digest), {})
            enlarge = source_path
            # Original HEIC is retained; a full-resolution browser-readable copy is used for enlargement.
            if source.suffix.lower() in {'.heic', '.heif'}:
                enlarge = target.with_name(slug + '-original.webp').relative_to(ROOT).as_posix()
            reuse = target.exists() and (ROOT / enlarge).exists() and (cached.get('sha256') == digest or (not previous and event == 'sys2025'))
            if not reuse:
                with tempfile.TemporaryDirectory() as temp:
                    decoded = source
                    if source.suffix.lower() in {'.heic', '.heif'}:
                        try:
                            import pillow_heif
                            pillow_heif.register_heif_opener()
                        except ImportError:
                            decoded = Path(temp) / 'decoded.png'
                            subprocess.run(['sips', '-s', 'format', 'png', str(source), '--out', str(decoded)], check=True, capture_output=True)
                    image = ImageOps.exif_transpose(Image.open(decoded))
                    if enlarge != source_path:
                        image.save(ROOT / enlarge, 'WEBP', quality=95, method=6)
                    if postcard:
                        bounds = image.getchannel('A').getbbox()
                        image = image.crop((max(0, bounds[0]-8), max(0, bounds[1]-8), min(image.width, bounds[2]+8), min(image.height, bounds[3]+8)))
                    image.thumbnail((1200, 1200))
                    image.save(target, 'WEBP', quality=85, lossless=postcard, method=6)
            with Image.open(target) as image:
                width, height = image.size
            alt = cached.get('alt') or known.alts.get(slug) or known.alts.get(slug.replace('-photo', '')) or f'{label} event photograph {position + 1}.'
            records.append(dict(source=source_path, sha256=digest, src=target.relative_to(ROOT).as_posix(), enlarge=enlarge, width=width, height=height, alt=alt, postcard=postcard))
        cards = []
        for i, r in enumerate(records):
            cls = 'event-photo-card' + (' event-photo-card--postcard' if r['postcard'] else '')
            cards.append(f'<a class="{cls}" href="{quote(r["enlarge"], safe="/")}" data-position="{i}" aria-label="{escape(r["alt"], quote=True)}"><img src="{quote(r["src"], safe="/")}" alt="{escape(r["alt"], quote=True)}" width="{r["width"]}" height="{r["height"]}" loading="lazy" decoding="async" draggable="false"></a>')
        track_id = f'{event}-cards'
        deck = f'''<section class="event-photo-deck" data-photo-deck aria-label="{label} photo album" aria-roledescription="carousel" tabindex="0">
<div class="event-photo-deck-heading"><span class="eyebrow">{heading}</span><span class="event-photo-counter" aria-hidden="true">01 / {len(records):02}</span></div>
<div class="event-photo-cards" id="{track_id}">{chr(10).join(cards)}</div>
<div class="event-photo-controls" hidden><button type="button" data-deck-prev aria-label="Previous photograph" aria-controls="{track_id}">←</button><a class="event-photo-enlarge" href="{quote(records[0]['enlarge'], safe='/')}">Enlarge ↗</a><button type="button" data-deck-next aria-label="Next photograph" aria-controls="{track_id}">→</button></div>
<p class="sr-only" data-deck-status aria-live="polite" aria-atomic="true"></p>
</section>'''
        pattern = f'(<!-- photo-deck:{event}:start -->).*?(<!-- photo-deck:{event}:end -->)'
        html, count = re.subn(pattern, lambda m: m[1] + '\n' + deck + '\n' + m[2], html, flags=re.S)
        if count != 1:
            raise ValueError(f'Expected one pair of deck markers for {event}')
        manifest[event] = dict(photos=records, unnumbered=unnumbered)
        print(f'{event}: {len(records)} photos: ' + ', '.join(p.name for p in sources))
        for name in unnumbered:
            print(f'UNNUMBERED (omitted): {event}/{name}')
    page.write_text(html)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    build()
