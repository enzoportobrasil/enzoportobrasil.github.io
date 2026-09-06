(() => {
  document.documentElement.classList.add('js');
  const config = window.SITE_CONFIG || {};

  // Theme
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) root.dataset.theme = savedTheme;

  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      localStorage.setItem('theme', next);
      button.setAttribute('aria-label', next === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    });
  });

  // Mobile navigation
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (navToggle && nav) {
    const closeNavigation = () => {
      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-label', 'Open navigation');
    };

    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    });

    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeNavigation();
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) {
        closeNavigation();
        navToggle.focus();
      }
    });
  }

  // Quietly strengthen orientation on long pages.
  const header = document.querySelector('[data-site-header]') || document.querySelector('.site-header');
  const progress = document.querySelector('[data-scroll-progress]');
  const updateScrollState = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    if (header) header.classList.toggle('is-scrolled', scrollTop > 24);
    if (progress) {
      const distance = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${distance > 0 ? Math.min(scrollTop / distance, 1) : 0})`;
    }
  };
  updateScrollState();
  window.addEventListener('scroll', updateScrollState, { passive: true });

  // Populate contact / social links from one config file.
  const mapping = {
    email: config.email ? `mailto:${config.email}` : '',
    linkedin: config.linkedin,
    github: config.github,
    orcid: config.orcid,
    scholar: config.scholar,
    cv: config.cvPdf
  };

  Object.entries(mapping).forEach(([key, href]) => {
    document.querySelectorAll(`[data-link="${key}"]`).forEach((el) => {
      if (href) {
        el.href = href;
        el.classList.remove('is-hidden');
      } else {
        el.classList.add('is-hidden');
      }
    });
  });

  document.querySelectorAll('[data-email-text]').forEach((el) => {
    if (config.email) el.textContent = config.email;
  });

  // Footer year
  document.querySelectorAll('[data-current-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // Reveal motion, respecting reduced motion.
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const items = document.querySelectorAll('[data-reveal]');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach((item) => observer.observe(item));
  }
})();
