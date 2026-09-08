from pathlib import Path
from PIL import Image,ImageOps
import re
root=Path(__file__).resolve().parents[1]
def variants(source,stem,widths,quality):
 im=ImageOps.exif_transpose(Image.open(root/source)).convert('RGB')
 for width in widths:
  copy=im.copy();copy.thumbnail((width,round(width*im.height/im.width)),Image.Resampling.LANCZOS)
  output=root/(stem+f'-{width}.webp');copy.save(output,'WEBP',quality=quality,method=6)
  print(output.relative_to(root),copy.size,output.stat().st_size)
variants('assets/img/site/hero-nebula.jpg','assets/img/site/hero-nebula',[1600,2400,3200],92)
variants('assets/img/profile/profile-main.png','assets/img/profile/profile-main',[640,1024],91)
for name in ['index.html','research.html']:
 p=root/name;s=p.read_text(encoding='utf-8')
 s=s.replace('src="assets/img/site/hero-nebula.jpg"','src="assets/img/site/hero-nebula-2400.webp" srcset="assets/img/site/hero-nebula-1600.webp 1600w, assets/img/site/hero-nebula-2400.webp 2400w, assets/img/site/hero-nebula-3200.webp 3200w" sizes="(max-width: 820px) 1650px, 100vw"').replace('width="2999" height="2999"','width="2400" height="1193"')
 s=s.replace('src="assets/img/profile/profile-main.png"','src="assets/img/profile/profile-main-1024.webp" srcset="assets/img/profile/profile-main-640.webp 640w, assets/img/profile/profile-main-1024.webp 1024w" sizes="(max-width: 560px) 640px, 700px"')
 s=s.replace('width="2066" height="1788"','width="1672" height="941"')
 # The scientific overview uses evidence. Homepage keeps illustrative direction with honest labels.
 if name=='index.html':
  s=s.replace('class="project-image" href="research/spatial-extremes.html"','class="project-image evidence-preview" href="research/spatial-extremes.html"')
  for href,label in [('spatial-extremes','Spatial research overview'),('solar-irradiance','Editorial illustration'),('missing-data-extremes','Illustrative density contours'),('climate-dependence','Illustrative photograph')]:
   pattern=r'(<a class="project-image[^>]*href="research/'+href+r'\.html"[^>]*>.*?)(<span class="project-number">)'
   s=re.sub(pattern,lambda m:m[1]+f'<span class="image-caption">{label}</span>'+m[2],s,flags=re.S)
 else:
  replacements=[('assets/img/research/02-spatial-extremes/hero.png','assets/img/research/02-spatial-extremes/web/spatial-parameters-1600.webp','Two rows of maps comparing true and estimated BGEV parameter surfaces.',1600,636),('assets/img/research/04-sorce/hero.webp','assets/img/apresentacoes/sys2025/web/maxima-workflow-1600.webp','Workflow from the related solar and atmospheric study presented at sys2025.',1600,1011),('assets/img/research/03-imputation-extremes/density-contours.jpg','assets/img/apresentacoes/cobipe-2024/web/imputation-mse-1600.webp','Mean squared error comparison from the coBIPE 2024 imputation study.',1600,690),('assets/img/research/05-compound-extremes/hero.webp','assets/img/apresentacoes/rbras-seagro-2025/web/temperature-humidity-poster-1200.webp','Earlier temperature and humidity study: complete 2025 poster.',1200,1697)]
  for old,new,alt,w,h in replacements:
   s=re.sub(r'<img src="'+re.escape(old)+r'"[^>]*>',f'<img src="{new}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">',s)
  s=s.replace('class="research-entry-image','class="evidence-preview research-entry-image')
 p.write_text(s,encoding='utf-8')
p=root/'resources.html';s=p.read_text(encoding='utf-8');s=s.replace('</body>','<script src="assets/js/certificates.js"></script></body>');p.write_text(s,encoding='utf-8')
