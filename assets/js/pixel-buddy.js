/* Optional pixel-art signature experiment (Talks page only).
   To disable: set ENABLE_PIXEL_BUDDY to false, or delete this file, its <script>
   tag, the assets/css/pixel-buddy.css <link>, and the .pixel-buddy markup block
   in talks.html. Nothing else on the site depends on this component. */
(function () {
  var ENABLE_PIXEL_BUDDY = true;
  if (!ENABLE_PIXEL_BUDDY) return;

  var el = document.querySelector('[data-pixel-buddy]');
  if (!el) return;
  el.hidden = false;

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) {
    el.classList.add('is-visible');
    return;
  }

  if (!('IntersectionObserver' in window)) {
    el.classList.add('is-visible');
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        el.classList.add('is-visible');
        observer.disconnect();
      }
    });
  }, { threshold: 0.4 });
  observer.observe(el);
})();
