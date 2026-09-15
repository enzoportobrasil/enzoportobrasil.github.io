/* One DOM card per selected photograph. Native scroll/snap remains the no-JS fallback. */
(() => {
  const dialog = document.querySelector('.event-photo-lightbox');
  if (!dialog) return;
  const open = (link, alt) => {
    dialog.querySelector('img').src = link.href;
    dialog.querySelector('img').alt = alt;
    dialog.showModal();
  };
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  document.querySelectorAll('[data-photo-enlarge]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); open(link, link.querySelector('img').alt);
  }));
  document.querySelectorAll('[data-photo-deck]').forEach((deck) => {
    const track = deck.querySelector('.event-photo-cards');
    const cards = [...track.children];
    const mobile = matchMedia('(max-width: 820px)');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    let index = 0;
    let gesture = null;
    let suppressClick = false;
    const mark = (announce = true) => {
      cards.forEach((card, i) => {
        const position = (i - index + cards.length) % cards.length;
        const visible = mobile.matches || position < 4;
        card.dataset.position = position;
        card.dataset.visible = visible;
        card.tabIndex = visible ? 0 : -1;
        card.setAttribute('aria-hidden', String(!visible));
        card.setAttribute('aria-current', String(i === index));
      });
      const count = `${String(index + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
      deck.querySelector('.event-photo-counter').textContent = count;
      if (announce) deck.querySelector('[data-deck-status]').textContent = `${count}. ${cards[index].querySelector('img').alt}`;
    };
    const show = (next) => {
      index = (next + cards.length) % cards.length;
      mark();
      if (mobile.matches) track.scrollTo({ left: cards[index].offsetLeft - track.offsetLeft - 8, behavior: reduced.matches ? 'instant' : 'smooth' });
      if (cards.includes(document.activeElement) && document.activeElement.tabIndex < 0) cards[index].focus({ preventScroll: true });
    };
    cards.forEach((card, i) => card.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (suppressClick) { suppressClick = false; return; }
      if (i !== index) show(i);
      else open(card, card.querySelector('img').alt);
    }));
    deck.querySelector('[data-deck-prev]').addEventListener('click', () => show(index - 1));
    deck.querySelector('[data-deck-next]').addEventListener('click', () => show(index + 1));
    deck.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      const next = { ArrowLeft: index - 1, ArrowRight: index + 1, Home: 0, End: cards.length - 1 }[event.key];
      if (next !== undefined) { event.preventDefault(); show(next); }
    });
    // Desktop drag only; touch screens at the mobile breakpoint use native horizontal scrolling.
    track.addEventListener('dragstart', event => event.preventDefault());
    track.addEventListener('pointerdown', event => {
      suppressClick = false;
      if (mobile.matches || !event.isPrimary || event.button !== 0) return;
      gesture = { x: event.clientX, y: event.clientY, id: event.pointerId };
    });
    window.addEventListener('pointerup', event => {
      if (!gesture || event.pointerId !== gesture.id) return;
      const dx = event.clientX - gesture.x, dy = event.clientY - gesture.y;
      gesture = null;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.4) { suppressClick = true; show(index + (dx < 0 ? 1 : -1)); }
    });
    window.addEventListener('pointercancel', () => { gesture = null; });
    let scrollTimer;
    track.addEventListener('scroll', () => {
      if (!mobile.matches) return;
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(() => {
        index = cards.reduce((best, card, i) => Math.abs(card.offsetLeft - track.offsetLeft - 8 - track.scrollLeft) < Math.abs(cards[best].offsetLeft - track.offsetLeft - 8 - track.scrollLeft) ? i : best, 0);
        mark();
      }, 120);
    }, { passive: true });
    mobile.addEventListener('change', () => { mark(false); if (mobile.matches) show(index); else track.scrollLeft = 0; });
    deck.classList.add('is-ready');
    deck.querySelector('.event-photo-controls').hidden = false;
    mark(false);
  });
})();
