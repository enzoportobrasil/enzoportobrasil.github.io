"""Dependency-free static site checks: python tests/site-check.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import os
import re

ROOT = Path(os.environ.get('SITE_ROOT', Path(__file__).resolve().parents[1])).resolve()
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.refs, self.images, self.errors = path, set(), [], [], []
        self.h1 = 0
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('Duplicate ID: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'img':
            self.images.append(a)
            if 'alt' not in a: self.errors.append('Missing image alt')
        for name in ['href', 'src', 'poster']:
            if name in a: self.refs.append(a[name])
        if 'srcset' in a: self.refs.extend(part.strip().split()[0] for part in a['srcset'].split(','))
        if 'aria-controls' in a: self.refs.extend('#' + i for i in a['aria-controls'].split())

def check():
    pages = {p.resolve(): Page(p) for p in list(ROOT.glob('*.html')) + list((ROOT/'research').glob('*.html'))}
    failures, count = [], 0
    for path, page in pages.items():
        failures.extend(f'{path.name}: {error}' for error in page.errors)
        if page.h1 != 1: failures.append(f'{path.name}: expected one h1, got {page.h1}')
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc or not ref or ref == '#': continue
            target = (ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)).resolve() if url.path else path
            count += 1
            if not target.is_relative_to(ROOT): failures.append(f'{path.name}: outside root: {ref}')
            elif not target.is_file(): failures.append(f'{path.name}: missing {ref}')
            elif any(part in ['reserve', '_source-materials'] for part in target.relative_to(ROOT).parts): failures.append(f'{path.name}: excluded asset {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids: failures.append(f'{path.name}: missing fragment {ref}')
            if target.is_file():
                # Windows is case insensitive, GitHub Pages is not.
                current = ROOT
                for part in target.relative_to(ROOT).parts:
                    if part not in {child.name for child in current.iterdir()}: failures.append(f'{path.name}: incorrect case {ref}'); break
                    current = current / part
    catalog = (ROOT/'assets/i18n/translations.js').read_text(encoding='utf-8').split('`',2)[1]
    seen = {}
    for line in catalog.strip().splitlines():
        row = line.split('|')
        if len(row) != 3 or not all(row): failures.append('Incomplete translation: ' + line[:70]); continue
        if row[0] in seen and seen[row[0]] != row: failures.append('Conflicting translation: '+row[0])
        seen[row[0]] = row
    for path in pages:
        text = path.read_text(encoding='utf-8')
        if re.search('add later|Add the strongest|Generelized|Prbabolity|enviromental|Configure GitHub',text): failures.append(f'{path.name}: provisional or misspelled copy')
    print(json.dumps({'pages':len(pages),'local_references':count,'translation_entries':len(seen),'failures':failures},indent=2))
    assert not failures, 'Static site validation failed'

if __name__ == '__main__': check()
