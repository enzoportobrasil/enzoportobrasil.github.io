/* Publications: a click on a cover opens the first page at reading size.
   Without JavaScript the link opens the same image directly. */
(() => {
  const links = document.querySelectorAll('[data-cover-viewer]');
  if (!links.length || typeof HTMLDialogElement !== 'function') return;
  const dialog = document.createElement('dialog');
  dialog.className = 'cover-viewer';
  dialog.innerHTML = '<button type="button" class="cover-viewer-close">×</button><figure><img alt="" decoding="async"><figcaption></figcaption></figure>';
  document.body.append(dialog);
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');
  const close = dialog.querySelector('button');
  const label = text => (window.SITE_I18N ? window.SITE_I18N.text(text) : text);
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { image.removeAttribute('src'); image.removeAttribute('srcset'); });
  links.forEach(link => link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const title = document.getElementById(link.getAttribute('aria-describedby'));
    const name = title ? title.textContent.trim() : '';
    image.sizes = 'min(92vw, calc((100dvh - 120px) * 0.707))';
    image.srcset = link.dataset.coverSrcset;
    image.src = link.href;
    image.alt = name ? `${label('First page')}: ${name}` : label('First page');
    caption.textContent = name;
    close.setAttribute('aria-label', label('Close'));
    dialog.setAttribute('aria-label', label('First page'));
    dialog.showModal();
  }));
})();
