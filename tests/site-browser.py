"""Behavioural QA with Playwright + installed Chrome.
Requires playwright in the Python environment. Screenshots go to a supplied directory.
python tests/site-browser.py [screenshot-directory]
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json, sys

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'.site-work/screenshots'
OUT.mkdir(parents=True,exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
BASE=f'http://127.0.0.1:{server.server_port}/'
pages=['index.html','research.html','publications.html','talks.html','cv.html','resources.html','research/spatial-extremes.html','research/missing-data-extremes.html','research/solar-irradiance.html','research/climate-dependence.html','404.html']
failures=[]; checks=0
def check(value,message):
    global checks
    checks+=1
    if not value: failures.append(message)
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light',reduced_motion='reduce')
    page=context.new_page(); errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    for name in pages:
        page.goto(BASE+name,wait_until='networkidle')
        check(page.locator('html').get_attribute('data-theme')=='dark',name+': dark default')
        check(page.locator('html').get_attribute('lang')=='en',name+': English default')
        for width in [360,390,768,1024,1440]:
            page.set_viewport_size({'width':width,'height':900})
            for lang in ['en','pt','es']:
                page.evaluate('(lang)=>window.SITE_I18N.setLanguage(lang)',lang)
                page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
                check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'{name}/{width}/{lang}: horizontal overflow')
                check(page.evaluate("[...document.querySelectorAll('h1,h2,h3,a.button')].every(el=>el.getBoundingClientRect().right <= innerWidth+2)"),f'{name}/{width}/{lang}: content outside viewport')
        page.evaluate("window.SITE_I18N.setLanguage('en')")
        page.evaluate("document.querySelectorAll('img').forEach(img=>img.loading='eager')")
        page.wait_for_function("[...document.images].every(i=>i.complete)")
        check(page.evaluate("[...document.images].every(i=>i.naturalWidth>0)"),name+': image failed')
        if name in ['index.html','research.html','resources.html','talks.html']:
            page.screenshot(path=str(OUT/(name.replace('.html','')+'-desktop.png')),full_page=True)
        print('Checked',name,flush=True)
    check(not errors,'JavaScript errors: '+repr(errors))
    page.goto(BASE+'index.html'); page.set_viewport_size({'width':390,'height':844})
    page.locator('[data-language-select]').select_option('pt')
    check(page.locator('html').get_attribute('lang')=='pt-BR','Portuguese document language')
    check('Inferência' in page.locator('h1').inner_text(),'Portuguese hero')
    page.locator('[data-theme-toggle]').click()
    check(page.locator('html').get_attribute('data-theme')=='light','Theme switch')
    page.locator('[data-nav-toggle]').click()
    check(page.locator('[data-nav]').is_visible(),'Mobile menu opens')
    page.keyboard.press('Escape')
    check(not page.locator('[data-nav]').is_visible(),'Mobile menu closes with Escape')
    check(page.locator('[data-nav-toggle]').evaluate('(el)=>el===document.activeElement'),'Escape restores focus')
    page.locator('[data-nav-toggle]').click();page.locator('[data-nav] a[href="research.html"]').click()
    check(page.locator('html').get_attribute('data-theme')=='light','Theme persists across navigation')
    check(page.locator('html').get_attribute('lang')=='pt-BR','Language persists across navigation')
    page.locator('[data-language-select]').select_option('es');page.reload()
    check(page.locator('html').get_attribute('lang')=='es','Spanish persists across reload')
    page.goto(BASE+'resources.html');page.locator('#certificate-search').fill('regressao')
    check(page.locator('[data-certificate-category]:visible').count()==1,'Accent-insensitive certificate search')
    page.locator('#certificate-search').fill('');page.locator('#certificate-category').select_option('astronomy')
    check(page.locator('[data-certificate-category]:visible').count()==1,'Certificate category filter')
    page.locator('#certificate-search').fill('no-such-record')
    check(page.locator('[data-certificate-category]:visible').count()==0,'Empty filter state')
    check('No se encontraron' in page.locator('[data-certificate-count]').inner_text(),'Translated empty state')
    page.goto(BASE+'talks.html')
    check(page.locator('iframe').count()==0,'Video does not load initially')
    check(not page.locator('.event-archive').get_attribute('open'),'Album starts collapsed')
    page.locator('.event-archive summary').click();page.locator('[data-album-next]').click()
    page.wait_for_function("document.querySelector('[data-album-counter]').textContent.startsWith('2')")
    page.locator('[data-language-select]').select_option('pt')
    check('outono' in page.locator('[data-album-caption]').inner_text(),'Album caption responds to language change')
    page.route('https://www.youtube-nocookie.com/**',lambda route:route.fulfill(status=200,body='<html><body>Player request intercepted for QA</body></html>'))
    page.locator('button.video-preview').click()
    check('youtube-nocookie.com/embed/ZFK-9LS7n0A' in page.locator('iframe').get_attribute('src'),'Correct on-demand video source')
    check('autoplay' not in page.locator('iframe').get_attribute('src'),'No video autoplay')
    page.goto(BASE+'index.html');page.locator('[data-theme-toggle]').click();page.screenshot(path=str(OUT/'home-mobile-pt.png'),full_page=True)
    # Storage exceptions must not stop theme, navigation, links or text rendering.
    blocked=browser.new_context(viewport={'width':360,'height':800})
    blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
    b=blocked.new_page(); b.goto(BASE+'index.html');b.locator('[data-language-select]').select_option('es');b.locator('[data-theme-toggle]').click()
    check(b.locator('html').get_attribute('lang')=='es','Localization works with blocked storage')
    check(b.locator('html').get_attribute('data-theme')=='light','Theme works with blocked storage')
    # No-JS progressive fallback: content, navigation and certificate archive stay readable.
    plain=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    n=plain.new_page();n.goto(BASE+'index.html')
    check(n.locator('[data-reveal]').first.evaluate('(el)=>getComputedStyle(el).opacity')=='1','No-JS research content is visible')
    check(n.locator('[data-nav]').is_visible(),'No-JS navigation is visible')
    n.goto(BASE+'resources.html');check(n.locator('[data-certificate-category]').count()==6,'No-JS certificates are present')
    n.goto(BASE+'talks.html');check(n.locator('a.video-preview').get_attribute('href').startswith('https://www.youtube.com/'),'No-JS video link works')
    browser.close()
finally:server.shutdown()
result={'checks':checks,'failures':failures}
(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
assert not failures,'Browser QA failed'
