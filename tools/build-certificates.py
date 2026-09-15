"""Build CV training/events, Resources archive and page-only i18n from shared data.

Run: python3 tools/build-certificates.py
Only CV/Resources outputs are written. English HTML works without JavaScript.
"""
from pathlib import Path
from html import escape
from datetime import date
import json
import re

ROOT = Path(__file__).resolve().parents[1]
E = lambda value: escape(str(value), quote=True)

def replace_marker(content, name, body):
    content, count = re.subn(r'<!-- '+name+r':start -->.*?<!-- '+name+r':end -->', lambda m: '<!-- '+name+':start -->\n'+body+'\n<!-- '+name+':end -->', content, flags=re.S)
    assert count == 1, f'Missing {name} markers'
    return content

def build():
    records = json.loads((ROOT/'assets/data/certificates.json').read_text())
    labels = json.loads((ROOT/'assets/data/academic-archive-labels.json').read_text())
    categories=labels['categories'];groups=labels['groups'];translations=labels['strings']+list(categories.values())+list(groups.values())
    seen=set();files=set()
    months=[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']]
    def date_label(item):
        d=item['date'];year=d[:4]
        if len(d)==4:return year
        triple=[f'{m[int(d[5:7])-1]} {year}' for m in months]
        translations.append(triple);return triple[0]
    def duration(item):
        if item.get('duration'):return item['duration']
        h=item.get('hours');return f'{h:g} h' if h is not None else ''
    def link(item,label):
        assert item['public'] and item['file']
        return f'<a href="{E(item["file"])}" target="_blank" rel="noopener noreferrer">{E(label)}</a>'
    for item in records:
        assert item['id'] not in seen;seen.add(item['id']);assert item['category'] in categories
        d=item['date'];date.fromisoformat(d+('-01-01' if len(d)==4 else '-01' if len(d)==7 else ''))
        translations.append([item['title'],item['title_pt'],item['title_es']])
        if item.get('notes'):translations.append([item['notes'],item['notes_pt'],item['notes_es']])
        if item['public']:
            assert item['file'] and '_archive' not in item['file']
            target=(ROOT/item['file']).resolve();assert target.is_relative_to(ROOT) and target.is_file(),item['file']
            assert item['file'] not in files;files.add(item['file'])
        else:assert item['file'] is None, 'Nonpublic source path must not enter the public manifest'
        if item.get('related'):assert (ROOT/item['related'].split('#')[0]).is_file()
    def training_row(item):
        status={'in-progress':'In progress','completed':'Completed','participated':item['role'],'recorded':''}[item['status']]
        meta=f'<span>{E(item["institution"])}</span>'
        if duration(item):meta+=' · <span>'+E(duration(item))+'</span>'
        if status:meta+=' · <span>'+E(status)+'</span>'
        if item['type']=='course':
            when=f'<time datetime="{item["date"]}">{date_label(item)}</time>'
            certificate=link(item,'Certificate ↗') if item['public'] else ''
            detail=''
            if item.get('notes'):
                detail='<div class="cv-course-detail"><p>'+E(item['notes'])+'</p><p><span>Published workload: 20 h</span> · <a href="'+E(item['course_url'])+'" target="_blank" rel="noopener noreferrer">Course syllabus ↗</a></p></div>'
            return f'<li id="cv-record-{E(item["id"])}"><h4>{E(item["title"])}</h4><p class="cv-course-meta">{meta} · {when}</p><div class="cv-course-link">{certificate}</div>{detail}</li>'
        extra=''
        if item.get('notes'):extra='<p>'+E(item['notes'])+'</p><p><span>Published workload: 20 h</span> · <a href="'+E(item['course_url'])+'" target="_blank" rel="noopener noreferrer">Course syllabus ↗</a></p>'
        if item['public']:extra+='<p class="cv-record-link">'+link(item,'Certificate ↗')+'</p>'
        return f'<li id="cv-record-{E(item["id"])}"><div><h4>{E(item["title"])}</h4><p>{meta}</p>{extra}</div><time class="cv-doc-training-date" datetime="{item["date"]}">{date_label(item)}</time></li>'
    cv=[]
    for cat,triple in categories.items():
        items=sorted([x for x in records if x['type']=='course' and x.get('cv') and x['category']==cat],key=lambda x:x['date'],reverse=True)
        if not items:continue
        cv.append(f'<details class="cv-record-group" open><summary><span>{E(triple[0])}</span><span class="cv-record-count" aria-hidden="true">{len(items):02}</span></summary><ul class="cv-doc-training cv-course-list">'+''.join(training_row(x) for x in items)+'</ul></details>')
    events=[]
    items=sorted([x for x in records if x['type']=='event' and x.get('cv')],key=lambda x:x['date'],reverse=True)
    # Recent participation is visible; older university activities can be expanded with a native summary.
    recent=[x for x in items if x['year']>=2021];older=[x for x in items if x['year']<2021]
    events.append('<ul class="cv-doc-training">'+''.join(training_row(x) for x in recent)+'</ul>')
    translations.append(['Earlier academic events · 2018–2020','Eventos acadêmicos anteriores · 2018–2020','Eventos académicos anteriores · 2018–2020'])
    events.append('<details class="cv-record-group"><summary><span>Earlier academic events · 2018–2020</span><span class="cv-record-count" aria-hidden="true">'+str(len(older))+'</span></summary><ul class="cv-doc-training">'+''.join(training_row(x) for x in older)+'</ul></details>')
    cvpath=ROOT/'cv.html';content=cvpath.read_text();content=replace_marker(content,'cv-training','\n'.join(cv));content=replace_marker(content,'cv-events','\n'.join(events));cvpath.write_text(content)
    sections=[]
    for kind,triple in groups.items():
        items=sorted([x for x in records if x['public'] and x['type']==kind],key=lambda x:x['date'],reverse=True)
        if not items:continue
        rows=[]
        for x in items:
            status=x.get('type_label') or {'course':'Course certificate','event':'Participation certificate','service':'Academic service certificate','research':'Research programme certificate'}[kind]
            meta=f'<span>{E(status)}</span>'
            if kind!='course':meta+=' · <span>'+E(x['role'])+'</span>'
            if duration(x):meta+=' · <span>'+E(duration(x))+'</span>'
            links=link(x,'View certificate ↗')
            if x.get('related'):links+='<a href="'+E(x['related'])+'">Related presentation →</a>'
            rows.append(f'<article id="certificate-{E(x["id"])}" data-certificate-category="{E(x["category"])}" data-certificate-type="{kind}" data-search-alias="{E(x["title"]+" "+x["title_pt"]+" "+x["title_es"])}"><div class="output-year"><time datetime="{x["date"]}">{date_label(x)}</time> · <span>{E(categories[x["category"]][0])}</span></div><h4>{E(x["title"])}</h4><p>{E(x["institution"])}</p><p>{meta}</p><div class="document-links">{links}</div></article>')
        sections.append(f'<section class="resource-record-group" data-certificate-group aria-labelledby="archive-{kind}"><h3 id="archive-{kind}">{E(triple[0])}</h3><div class="archive-list">'+''.join(rows)+'</div></section>')
    path=ROOT/'resources.html';content=replace_marker(path.read_text(),'certificates','<div id="certificate-list">\n'+'\n'.join(sections)+'\n</div>')
    options='<option value="all">All categories</option>'+''.join(f'<option value="{key}">{E(value[0])}</option>' for key,value in categories.items() if any(x['public'] and x['category']==key for x in records))
    content=re.sub(r'(<select id="certificate-category"[^>]*>).*?(</select>)',lambda m:m[1]+options+m[2],content,flags=re.S)
    if 'id="certificate-type"' not in content:
        control='<label for="certificate-type">Activity</label><select id="certificate-type" aria-controls="certificate-list"><option value="all">All activities</option>'+''.join(f'<option value="{key}">{E(value[0])}</option>' for key,value in groups.items())+'</select>'
        content=content.replace('</select></div><p data-certificate-count','</select>'+control+'</div><p data-certificate-count')
    path.write_text(content)
    # Append after the global dictionary only on these two pages.
    unique={row[0]:row for row in translations}
    (ROOT/'assets/i18n/cv-resources.js').write_text('/* Generated by tools/build-certificates.py; loaded only by CV and Resources. */\nwindow.SITE_TRANSLATIONS.push(...'+json.dumps(list(unique.values()),ensure_ascii=False,indent=2)+');\n')
    print(f'Built {len(records)} records: {len(files)} public documents; {len(items)} records in final group.')

if __name__=='__main__':build()
