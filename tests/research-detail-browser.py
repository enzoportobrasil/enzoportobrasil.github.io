"""Research-detail browser checks. Requires Playwright and Chrome.
Run after Jekyll build; SITE_ROOT and CHROME_PATH can override defaults.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import json,re,os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.site-work/research-detail-qa'; OUT.mkdir(parents=True,exist_ok=True)
SERVE=Path(os.environ.get('SITE_ROOT',ROOT/'_site')).resolve()
if not (SERVE/'index.html').is_file(): raise SystemExit('Build with Jekyll first; set SITE_ROOT to the generated directory.')
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SERVE)))
Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
errors=[]; checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(**({'executable_path': os.environ['CHROME_PATH']} if os.environ.get('CHROME_PATH') else {'channel':'chrome'}),headless=True)
 ctx=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce');page=ctx.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.url.startswith(base) and r.status>=400 else None)
 for name in ['spatial-extremes','solar-irradiance','missing-data-extremes','climate-dependence']:
  page.goto(base+'research/'+name+'.html',wait_until='networkidle')
  assert not page.locator('body').inner_text().lstrip().startswith('---'), 'Unprocessed front matter'
  page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
  page.wait_for_function('[...document.images].every(i=>i.complete)')
  for width in [1440,1200,1024,768,430]:
   page.set_viewport_size({'width':width,'height':1000})
   for lang in ['en','pt','es']:
    page.evaluate('(lang)=>window.SITE_I18N.setLanguage(lang)',lang)
    info=page.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth, broken:[...document.images].filter(i=>!i.naturalWidth).length, captions:[...document.querySelectorAll('main figcaption')].every(e=>getComputedStyle(e).position==='static' && e.getBoundingClientRect().height>20), outside:[...document.querySelectorAll('main h1,main h2,main figure,main .button')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).length})''')
    checks.append({'page':name,'width':width,'lang':lang,**info})
   page.evaluate("window.SITE_I18N.setLanguage('en')")
   page.evaluate("async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode()));}")
   for img in page.locator('main figure img').all(): img.scroll_into_view_if_needed()
   page.evaluate('scrollTo(0,0)')
   if width in [1440,768,430]:page.screenshot(path=str(OUT/f'{name}-{width}.png'),full_page=True)
  # Verify focus and light theme as well.
  page.locator('[data-theme-toggle]').click()
  page.set_viewport_size({'width':1440,'height':1000})
  page.screenshot(path=str(OUT/f'{name}-light.png'),full_page=True)
  page.locator('[data-theme-toggle]').click()
  print('Checked',name,flush=True)
 browser.close()
server.shutdown()
(OUT/'browser-results.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2))
assert not errors,errors
assert all(not x['overflow'] and not x['broken'] and x['captions'] and not x['outside'] for x in checks)
print('PASS',len(checks),'responsive/language combinations; no console or local HTTP errors')
