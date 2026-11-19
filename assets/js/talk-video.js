/* PIBIC uses the same native-dialog interaction as the event photo lightboxes. */
(() => {
  const section = document.querySelector('#pibic-2022');
  const dialog = section?.querySelector('.talk-video-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const video = dialog.querySelector('video');
  let opener;
  section.querySelector('.talk-pibic-inline').hidden = true;
  section.querySelector('.talk-pibic-preview').hidden = false;
  section.querySelectorAll('[data-pibic-open]').forEach(control => {
    control.setAttribute('aria-haspopup', 'dialog');
    control.setAttribute('aria-controls', dialog.id);
    control.addEventListener('click', event => {
      event.preventDefault();
      opener = control;
      dialog.showModal();
      // Playback starts only after an explicit visitor action.
      video.play().catch(() => { /* Native controls remain available. */ });
    });
  });
  const close = () => { video.pause(); dialog.close(); };
  dialog.addEventListener('cancel', () => video.pause());
  dialog.querySelector('.talk-video-close').addEventListener('click', close);
  dialog.addEventListener('click', event => {
    const box = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) close();
  });
  dialog.addEventListener('close', () => {
    video.pause();
    opener?.focus({ preventScroll: true });
  });
})();

/* sys2025: the YouTube link becomes a player only after a click; nothing is requested from YouTube on page load. */
(() => {
  document.querySelectorAll('[data-youtube-embed]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const frame = document.createElement('iframe');
      frame.src = link.dataset.youtubeEmbed + '&autoplay=1';
      frame.title = link.getAttribute('aria-label') || 'YouTube video';
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      link.replaceWith(frame);
      frame.focus();
    });
  });
})();
