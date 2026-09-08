from pathlib import Path
from bs4 import BeautifulSoup, Comment
import json,re
root=Path(__file__).resolve().parents[1]
seen=set(); rows=[]
for file in list(root.glob('*.html'))+list((root/'research').glob('*.html')):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for node in soup.body.find_all(string=True):
  if isinstance(node,Comment) or node.parent.name in ['script','style'] or any(p.has_attr('lang') and p.name!='html' for p in node.parents):continue
  value=re.sub(r'\s+',' ',str(node)).strip()
  if not re.search('[a-zA-Z]{2}',value) or value in seen:continue
  seen.add(value);rows.append([file.relative_to(root).as_posix(),value])
(root/'.site-work/texts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows),'unique text nodes')
