from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 page=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 for filename,selector,out in [('index.html','.hero','hero'),('index.html','.statement-section','profile'),('index.html','.research-showcase','research-home'),('research.html','.research-index','research-index'),('talks.html','#sys2025','talk-science'),('resources.html','#training','training')]:
  page.goto(base+filename);page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')");page.wait_for_function("[...document.images].every(i=>i.complete)");page.locator(selector).evaluate('(e)=>e.scrollIntoView({block:"start"})');page.screenshot(path=str(root/'.site-work'/(out+'.png')))
 page.goto(base+'research/spatial-extremes.html');page.locator('[data-bgev]').scroll_into_view_if_needed();page.select_option('[data-language-select]','pt');page.screenshot(path=str(root/'.site-work/bgev-pt.png'))
 print('BGEV Portuguese title',page.locator('.bgev h2').inner_text())
 b.close()
server.shutdown()
