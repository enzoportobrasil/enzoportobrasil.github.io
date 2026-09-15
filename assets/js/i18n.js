/* Curated text-node translations. English HTML remains the canonical, usable fallback.
   No HTML strings are inserted and no third-party requests are made. */
(() => {
  const rows = window.SITE_TRANSLATIONS || [];
  const dictionaries = { en: new Map(), pt: new Map(), es: new Map() };
  const canonical = new Map();
  const normalize = value => value.replace(/\s+/g, ' ').trim();
  rows.forEach(([en, pt, es]) => {
    [en, pt, es].forEach(value => canonical.set(normalize(value), en));
    dictionaries.pt.set(en, pt);
    dictionaries.es.set(en, es);
  });
  let language = 'en';
  const originals = new WeakMap();
  const attrOriginals = new WeakMap();
  const text = (value, parameters = {}) => {
    const key = canonical.get(normalize(value)) || normalize(value);
    let translated = dictionaries[language].get(key);
    if (!translated && key.includes(': ')) {
      const colon = key.indexOf(': ');
      const prefix = key.slice(0, colon);
      const suffix = key.slice(colon + 2);
      if (dictionaries[language].has(prefix)) translated = dictionaries[language].get(prefix) + ': ' + text(suffix);
    }
    return (translated || key).replace(/\{(\w+)\}/g, (match, name) => parameters[name] ?? match);
  };
  function translate(scope = document.body) {
    const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!node.nodeValue.trim() || node.parentElement.closest('script,style,[data-no-i18n],[lang]:not(html)')) continue;
      const current = normalize(node.nodeValue);
      let record = originals.get(node);
      if (!record || current !== record.last) record = { en: canonical.get(current) || current, last: current };
      const translated = dictionaries[language].get(record.en) || record.en;
      node.nodeValue = node.nodeValue.replace(/\S[\s\S]*\S|\S/, translated);
      record.last = translated;
      originals.set(node, record);
    }
    scope.querySelectorAll('[aria-label],[alt],[placeholder]').forEach(element => {
      if (element.closest('[data-no-i18n]')) return;
      let cache = attrOriginals.get(element) || {};
      for (const attr of ['aria-label','alt','placeholder']) {
        if (!element.hasAttribute(attr)) continue;
        const current = element.getAttribute(attr);
        if (!cache[attr] || current !== cache[attr].last) cache[attr] = { en: canonical.get(normalize(current)) || current };
        const value = text(cache[attr].en);
        element.setAttribute(attr, value);
        cache[attr].last = value;
      }
      attrOriginals.set(element, cache);
    });
  }
  function setLanguage(next, save = false) {
    language = ['en','pt','es'].includes(next) ? next : 'en';
    document.documentElement.lang = language === 'pt' ? 'pt-BR' : language;
    document.querySelectorAll('[data-language-select]').forEach(select => { select.value = language; });
    translate();
    if (save) { try { localStorage.setItem('language', language); } catch {} }
    document.dispatchEvent(new CustomEvent('site:language', { detail: { language } }));
  }
  window.SITE_I18N = { text, translate, setLanguage, get language() { return language; } };
  document.querySelectorAll('[data-language-select]').forEach(select => select.addEventListener('change', () => setLanguage(select.value, true)));
  let saved = 'en';
  try { saved = localStorage.getItem('language') || 'en'; } catch {}
  setLanguage(saved);
})();
