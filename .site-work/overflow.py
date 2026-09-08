from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[1]
cases=[('index.html',768,'pt'),('research.html',360,'en'),('publications.html',360,'en'),('resources.html',360,'pt'),('research/solar-irradiance.html',360,'en')]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 page=b.new_page(reduced_motion='reduce')
 for name,width,lang in cases:
  page.set_viewport_size({'width':width,'height':850});page.goto((root/name).as_uri());page.evaluate('(l)=>SITE_I18N.setLanguage(l)',lang)
  print(name,width,lang,json.dumps(page.evaluate("[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&getComputedStyle(e).position!=='absolute').map(e=>({tag:e.tagName,cls:e.className,width:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,100)})).slice(0,20)"),ensure_ascii=False))
  page.screenshot(path=str(root/'.site-work'/('qa-'+name.replace('/','-')+'.png')))
 b.close()
