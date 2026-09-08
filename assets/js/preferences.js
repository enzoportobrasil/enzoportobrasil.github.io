/* Run before CSS: an explicit saved preference takes priority over the dark default. */
(() => {
  let theme = 'dark';
  try {
    const saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') theme = saved;
  } catch { /* Storage may be unavailable; the site still works. */ }
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
})();
