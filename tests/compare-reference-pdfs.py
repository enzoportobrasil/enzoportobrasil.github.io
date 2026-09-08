"""Extract original vector paths; compare in PDF coordinates (0.01 pt rounding)."""
import json, re, sys
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream
base=Path(sys.argv[1]);out=[]
for suffix,xi,xmin,xmax in [('MENOS_1',-1,-3,2),('0',0,-3,3),('MAIS_1',1,-2,6)]:
 r=PdfReader(base/f'bgev_xi_igual_{suffix}.pdf');paths=[];points=[];ticks=[[],[]]
 for args,op in ContentStream(r.pages[0].get_contents(),r).operations:
  if op==b'm':points=[list(map(float,args))]
  if op==b'l':points.append(list(map(float,args)))
  if op==b'S' and len(points)>100:paths.append(points);points=[]
 def visitor(t,cm,tm,f,size):
  if re.fullmatch(r'\d+\.\d+|\d+',t.strip()) and tm[4]>0:
   if tm[4]<40:ticks[0].append((float(t),tm[5]))
   elif 350<tm[4]<400:ticks[1].append((float(t),tm[5]))
 r.pages[0].extract_text(visitor_text=visitor)
 for k,points in enumerate(paths[:6]):
  panel=k//3;tt=ticks[panel];scale=(tt[-1][1]-tt[0][1])/(tt[-1][0]-tt[0][0]);zero=tt[0][1]+3.95
  left=min(p[0] for p in points);right=max(p[0] for p in points)
  out.append(dict(xi=xi,delta=[0,1,3][k%3],panel=panel,scale=scale,zero=zero,points=[[(x-left)/(right-left)*(xmax-xmin)+xmin,y] for x,y in points[::10]]))
Path(__file__).with_name('bgev-reference-vectors.json').write_text(json.dumps(out,separators=(',',':')))
