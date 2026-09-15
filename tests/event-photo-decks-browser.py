"""Focused event-deck QA. Run against a local server with Python + Playwright.
SITE_URL defaults to http://127.0.0.1:8765; CHROME_PATH may override Chrome.
"""
from pathlib import Path
from urllib.parse import unquote
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
import json, os, re
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.site-work/event-decks-qa'
OUT.mkdir(parents=True, exist_ok=True)
BASE = os.environ.get('SITE_URL', 'http://127.0.0.1:8765')
manifest = json.loads((ROOT / 'assets/data/event-photo-decks.json').read_text())

class Paths(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'href') and value and not value.startswith(('https:', 'http:', 'mailto:', '#')):
                assert (ROOT / unquote(value.split('#')[0])).is_file(), value
Paths().feed((ROOT / 'talks.html').read_text())
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROME_PATH', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'), headless=True)
    page = browser.new_page(viewport={'width':1440, 'height':1000}, reduced_motion='reduce')
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda r: errors.append(f'{r.status} {r.url}') if r.status >= 400 else None)
    page.goto(BASE + '/talks.html')
    for event, data in manifest.items():
        deck = page.locator(f'#{event} [data-photo-deck]')
        photos = data['photos']; cards = deck.locator('.event-photo-card')
        assert cards.count() == len(photos)
        numbers = [int(Path(r['source']).name.split('_')[0]) for r in photos]
        assert numbers == sorted(numbers) and len(set(numbers)) == len(numbers)
        assert len({r['source'] for r in photos}) == len(photos)
        sources = [q for q in (ROOT / 'assets/img/apresentacoes' / event / 'photos_selected').iterdir() if re.match(r'^\d+_', q.name)]
        assert set(r['source'] for r in photos) == set(q.relative_to(ROOT).as_posix() for q in sources)
        for i, record in enumerate(photos):
            assert unquote(cards.nth(i).get_attribute('href')) == record['enlarge']
            assert cards.nth(i).locator('img').get_attribute('src') == record['src']
        deck.focus();page.keyboard.press('Home')
        for i in range(len(photos)):
            assert deck.locator('.event-photo-counter').inner_text() == f'{i+1:02} / {len(photos):02}'
            assert unquote(deck.locator('.event-photo-enlarge').get_attribute('href')).endswith(photos[i]['enlarge'])
            deck.locator('.event-photo-enlarge').click()
            page.locator('dialog img').evaluate('e=>e.decode()')
            assert page.locator('dialog').evaluate('e=>e.open')
            page.keyboard.press('Escape')
            assert deck.locator('.event-photo-enlarge').evaluate('e=>e===document.activeElement')
            deck.locator('[data-deck-next]').click()
        deck.locator('[data-deck-prev]').click()
        assert deck.locator('.event-photo-counter').inner_text().startswith(f'{len(photos):02}')
        deck.focus();page.keyboard.press('Home');page.keyboard.press('ArrowRight')
        assert deck.locator('.event-photo-counter').inner_text().startswith('02')
        deck.locator('.event-photo-card[data-position="1"]').focus();page.keyboard.press('Enter')
        assert deck.locator('.event-photo-counter').inner_text().startswith('03')
        deck.focus();page.keyboard.press('Home')
    assert page.locator('[data-photo-deck]').count() == 3
    page.locator('#sys2025 [data-deck-next]').click()
    assert page.locator('#wasa-2024 .event-photo-counter').inner_text() == '01 / 06'
    assert page.locator('#emr-epbest-2025 .event-photo-counter').inner_text() == '01 / 06'
    page.locator('#sys2025 [data-photo-deck]').focus();page.keyboard.press('Home')
    page.eval_on_selector_all('img', 'es=>es.forEach(e=>e.loading="eager")')
    page.wait_for_function('[...document.images].every(e=>e.complete)')
    assert page.eval_on_selector_all('img[src]', 'es=>es.every(e=>e.naturalWidth>0)')
    for width in [320,390,768,820,1024,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        page.wait_for_timeout(200)
        for theme in ['dark','light']:
            page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(width,theme)
            if width in [390,1024,1440]:
                for event in manifest:
                    page.locator(f'#{event}').screenshot(path=str(OUT/f'{event}-{width}-{theme}.png'),style='.site-header,.skip-link { visibility:hidden; }')
        if width==390:
            for event in manifest:
                deck=page.locator(f'#{event} [data-photo-deck]');deck.focus();page.keyboard.press('Home')
                deck.locator('.event-photo-cards').evaluate('e=>e.scrollLeft=e.clientWidth*.88+16')
                page.wait_for_timeout(300)
                assert deck.locator('.event-photo-counter').inner_text().startswith('02')
                deck.focus();page.keyboard.press('Home')
    page.set_viewport_size({'width':1440,'height':1000})
    assert float(page.locator('.event-photo-card').first.evaluate('e=>parseFloat(getComputedStyle(e).transitionDuration)')) < .001
    page.emulate_media(reduced_motion='no-preference')
    assert page.locator('.event-photo-card').first.evaluate('e=>getComputedStyle(e).transitionDuration').startswith('0.45s')
    assert page.locator('#emr-epbest-2025 .poster-preview').count()==2
    assert page.locator('#wasa-2024 .poster-preview').count()==0
    stages=page.locator('#emr-epbest-2025 .poster-preview > a').evaluate_all('es=>es.map(e=>{const r=e.getBoundingClientRect();return [r.width,r.height,r.top,r.bottom]})')
    assert stages[0]==stages[1]
    for event in ['emr-epbest-2025','wasa-2024']:
        assert page.locator(f'#{event} .event-photo-pair').count()==0
        for href in page.locator(f'#{event} .poster-preview > a').evaluate_all('es=>es.map(e=>e.href)'):
            assert href.endswith('.pdf') and page.request.get(href).ok
    assert not errors,errors
    browser.close()
print('PASS: numeric ordering, 21 unique sources, independent controls, all enlargement targets, keyboard/focus, mobile snap, six widths, both themes, motion preferences, PDFs/links and console.')
