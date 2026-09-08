/* The static preview remains a working YouTube link when JavaScript is absent. */
(() => {
  const preview = document.querySelector('[data-video-load]');
  if (!preview) return;
  const t = (value) => window.SITE_I18N?.text(value) || value;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = preview.className;
  button.setAttribute('aria-label', t('Load the PIBIC video player'));
  while (preview.firstChild) button.appendChild(preview.firstChild);
  button.querySelector('[data-video-label]').textContent = t('Load video');
  preview.replaceWith(button);
  document.addEventListener('site:language', () => {
    if (!button.isConnected) return;
    button.setAttribute('aria-label', t('Load the PIBIC video player'));
    button.querySelector('[data-video-label]').textContent = t('Load video');
  });
  button.addEventListener('click', () => {
    const player = document.createElement('iframe');
    player.src = 'https://www.youtube-nocookie.com/embed/ZFK-9LS7n0A';
    player.title = 'PIBIC UnB 2021/22: Técnicas de Imputação para Variáveis Dicotômicas';
    player.allow = 'encrypted-media; picture-in-picture; fullscreen';
    player.referrerPolicy = 'strict-origin-when-cross-origin';
    player.allowFullscreen = true;
    button.replaceWith(player);
    player.focus();
  }, { once: true });
})();
