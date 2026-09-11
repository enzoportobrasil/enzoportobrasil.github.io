/* A small, finite album. Its first photo and enlargement link work without JS. */
(() => {
  document.querySelectorAll('[data-photo-album]').forEach((album) => {
    const t = (value) => window.SITE_I18N?.text(value) || value;
    const photos = JSON.parse(album.querySelector('[data-album-photos]').textContent);
    const previous = album.querySelector('[data-album-prev]');
    const next = album.querySelector('[data-album-next]');
    const link = album.querySelector('.album-image-link');
    const status = album.querySelector('[data-album-status]');
    const photoId = link.querySelector('img').id;
    const cache = new Map();
    const thumbnails = [...album.querySelectorAll("[data-album-select]")];
    const markSelection = () => thumbnails.forEach((a, i) => a.setAttribute("aria-current", String(i === index)));
    let index = 0;
    let busy = false;
    let start = null;
    let suppressClick = false;
    const load = (position) => {
      if (!cache.has(position)) {
        const photo = photos[position];
        const image = new Image(photo.width, photo.height);
        image.alt = t(photo.alt);
        image.decoding = 'async';
        image.sizes = link.querySelector('img').sizes;
        image.srcset = photo.srcset;
        image.src = photo.src;
        const ready = image.decode().then(() => image).catch((error) => {
          cache.delete(position);
          throw error;
        });
        cache.set(position, ready);
      }
      return cache.get(position);
    };
    const preloadNext = () => {
      if (index + 1 < photos.length && !navigator.connection?.saveData) {
        load(index + 1).catch(() => {});
      }
    };
    const show = async (position) => {
      if (busy || position < 0 || position >= photos.length || position === index) return;
      busy = true;
      album.setAttribute('aria-busy', 'true');
      try {
        const image = await load(position);
        image.id = photoId;
        image.classList.remove('album-enter');
        link.replaceChildren(image);
        image.classList.add('album-enter');
        index = position;
        markSelection();
        image.alt = t(photos[index].alt);
        album.querySelector('[data-album-caption]').textContent = t(photos[index].caption);
        album.querySelector('[data-album-counter]').textContent = `${index + 1} / ${photos.length}`;
        album.querySelectorAll('[data-album-enlarge]').forEach((a) => { a.href = photos[index].src; });
        previous.disabled = index === 0;
        next.disabled = index === photos.length - 1;
        status.textContent = `${index + 1} / ${photos.length}. ${t(photos[index].caption)}`;
        preloadNext();
      } catch {
        status.textContent = t('This photograph could not be loaded. Please try again.');
      } finally {
        busy = false;
        album.removeAttribute('aria-busy');
      }
    };
    previous.hidden = next.hidden = false;
    markSelection();
    thumbnails.forEach(a => a.addEventListener("click", event => { event.preventDefault(); show(Number(a.dataset.albumSelect)); }));
    document.addEventListener('site:language', () => {
      album.querySelector('[data-album-caption]').textContent = t(photos[index].caption);
      link.querySelector('img').alt = t(photos[index].alt);
    });
    album.classList.add('album-ready');
    previous.addEventListener('click', () => show(index - 1));
    next.addEventListener('click', () => show(index + 1));
    album.addEventListener('keydown', (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      const target = { ArrowLeft: index - 1, ArrowRight: index + 1, Home: 0, End: photos.length - 1 }[event.key];
      if (target !== undefined) {
        event.preventDefault();
        show(target);
      }
    });
    // Allow vertical page scrolling and pinch zoom; only horizontal gestures change photos.
    link.addEventListener('pointerdown', (event) => {
      suppressClick = false;
      if (event.pointerType !== 'touch' || !event.isPrimary) return;
      start = { x: event.clientX, y: event.clientY, id: event.pointerId };
      link.setPointerCapture(event.pointerId);
    });
    link.addEventListener('pointerup', (event) => {
      if (!start || event.pointerId !== start.id) return;
      const dx = event.clientX - start.x;
      const dy = event.clientY - start.y;
      start = null;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.4) {
        suppressClick = true;
        show(index + (dx < 0 ? 1 : -1));
      }
    });
    link.addEventListener('pointercancel', () => { start = null; });
    link.addEventListener('click', (event) => {
      if (suppressClick) { event.preventDefault(); suppressClick = false; }
    });
    link.addEventListener('dragstart', (event) => event.preventDefault());
    // Do not fetch the rest of this below-the-fold album on initial page load.
    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        preloadNext();
        observer.disconnect();
      }
    });
    observer.observe(album);
  });
})();
