/* In-page PDF viewer for certificate/document links on the CV and Resources
   pages. Intercepts same-origin PDF links and opens them in a native <dialog>
   instead of a new tab. Isolated and reversible: remove this file, its
   <script> tag, and assets/css/certificate-viewer.css (plus its <link>) to
   fully restore plain "open in a new tab" links; nothing else references it. */
(() => {
  const main = document.querySelector('main');
  if (!main || typeof HTMLDialogElement === 'undefined') return;

  const links = [...main.querySelectorAll('a[href$=".pdf"][target="_blank"]')];
  if (!links.length) return;

  const lang = document.documentElement.lang;
  const L = {
    open: lang === 'pt-BR' ? 'Abrir original ↗' : lang === 'es' ? 'Abrir original ↗' : 'Open original ↗',
    close: lang === 'pt-BR' ? 'Fechar' : lang === 'es' ? 'Cerrar' : 'Close'
  };

  let dialog = null;
  let lastTrigger = null;

  function buildDialog() {
    const el = document.createElement('dialog');
    el.className = 'certificate-viewer';
    el.innerHTML = `
      <div class="certificate-viewer-head">
        <h2 class="certificate-viewer-title"></h2>
        <a class="certificate-viewer-open" target="_blank" rel="noopener noreferrer"></a>
        <button type="button" class="certificate-viewer-close" aria-label="${L.close}">&times;</button>
      </div>
      <div class="certificate-viewer-body"></div>
    `;
    document.body.appendChild(el);
    el.querySelector('.certificate-viewer-close').addEventListener('click', () => el.close());
    el.addEventListener('click', event => {
      if (event.target === el) el.close();
    });
    el.addEventListener('close', () => {
      el.querySelector('.certificate-viewer-body').innerHTML = '';
      document.body.classList.remove('has-certificate-viewer');
      if (lastTrigger) lastTrigger.focus();
    });
    return el;
  }

  function openViewer(link) {
    if (!dialog) dialog = buildDialog();
    lastTrigger = link;
    const href = link.getAttribute('href');
    const title = link.closest('article, li')?.querySelector('h3, h4')?.textContent?.trim() || link.textContent.trim();
    dialog.querySelector('.certificate-viewer-title').textContent = title;
    const openLink = dialog.querySelector('.certificate-viewer-open');
    openLink.href = href;
    openLink.textContent = L.open;
    dialog.querySelector('.certificate-viewer-body').innerHTML =
      `<iframe src="${href}" title="${title}" loading="eager"></iframe>`;
    document.body.classList.add('has-certificate-viewer');
    dialog.showModal();
  }

  links.forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      openViewer(link);
    });
  });
})();
