"""Build the accessible static archive from JSON; no runtime fetch is required.

Run from any directory: python tools/build-certificates.py
"""
from pathlib import Path
from html import escape
from datetime import date
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'statistics': 'Statistics & Data Science', 'astronomy': 'Astronomy & Space Science', 'research': 'Research Practice', 'mathematics': 'Probability & Mathematics', 'physics': 'Physics', 'climate': 'Climate & Environment', 'computing': 'Computing', 'education': 'Education & Social Sciences', 'other': 'Other interdisciplinary training'}

def build():
    records = json.loads((ROOT / 'assets/data/certificates.json').read_text(encoding='utf-8'))
    ids = set()
    rows = []
    for item in sorted(records, key=lambda r: r['date'], reverse=True):
        assert item['id'] not in ids, 'Duplicate certificate id'
        ids.add(item['id'])
        assert item['category'] in CATEGORIES, 'Unknown category'
        date.fromisoformat(item['date'] + ('-01' if len(item['date']) == 7 else ''))
        for key in ['certificate', 'related']:
            target = (ROOT / item[key].split('#')[0]).resolve()
            assert target.is_relative_to(ROOT) and target.is_file(), f'Missing local {key}: {item[key]}'
        e = {key: escape(str(value), quote=True) for key, value in item.items()}
        title_lang = f' lang="{e["titleLang"]}"' if 'titleLang' in e else ''
        rows.append(f'''<article id="certificate-{e['id']}" data-certificate-category="{e['category']}">
<div class="output-year"><time datetime="{e['date']}">{e['date'][:4]}</time> · <span>{escape(CATEGORIES[item['category']])}</span></div>
<h3{title_lang}>{e['title']}</h3><p>{e['institution']}</p><p>{e['type']}</p>
<div class="document-links"><a href="{e['certificate']}">Certificate (PDF) ↗</a><a href="{e['related']}">Related presentation →</a></div>
</article>''')
    path = ROOT / 'resources.html'
    content = path.read_text(encoding='utf-8')
    archive = '<!-- certificates:start --><div id="certificate-list" class="archive-list">\n' + '\n'.join(rows) + '\n</div><!-- certificates:end -->'
    content, count = re.subn(r'<!-- certificates:start -->.*?<!-- certificates:end -->', lambda m: archive, content, flags=re.S)
    assert count == 1, 'Archive markers missing'
    options = '<option value="all">All categories</option>' + ''.join(f'<option value="{key}">{escape(label)}</option>' for key, label in CATEGORIES.items() if any(x['category'] == key for x in records))
    content = re.sub(r'(<select id="certificate-category"[^>]*>).*?(</select>)', lambda m: m[1] + options + m[2], content, flags=re.S)
    path.write_text(content, encoding='utf-8')
    print(f'Built {len(rows)} certificate records.')

if __name__ == '__main__':
    build()
