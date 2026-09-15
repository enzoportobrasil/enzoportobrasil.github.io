/* Resources-only filtering; the static document remains complete without JS. */
(() => {
  const archive = document.querySelector('.academic-resources');
  const search = archive?.querySelector('#certificate-search');
  if (!search) return;
  const category = archive.querySelector('#certificate-category');
  const activity = archive.querySelector('#certificate-type');
  const records = [...archive.querySelectorAll('[data-certificate-category]')];
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function filter() {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    records.forEach(record => {
      const text = normalize(record.textContent + ' ' + record.dataset.searchAlias);
      record.hidden = !(category.value === 'all' || category.value === record.dataset.certificateCategory)
        || !(activity.value === 'all' || activity.value === record.dataset.certificateType)
        || !words.every(word => text.includes(word));
      if (!record.hidden) visible++;
    });
    archive.querySelectorAll('[data-certificate-group]').forEach(group => {
      group.hidden = !group.querySelector('[data-certificate-category]:not([hidden])');
    });
    const lang = document.documentElement.lang;
    const labels = lang === 'pt-BR' ? ['registros', 'Nenhum registro encontrado.'] : lang === 'es' ? ['registros', 'No se encontraron registros.'] : ['records', 'No matching records.'];
    archive.querySelector('[data-certificate-count]').textContent = visible ? `${visible} / ${records.length} ${labels[0]}` : labels[1];
  }
  search.addEventListener('input', filter);
  category.addEventListener('change', filter);
  activity.addEventListener('change', filter);
  document.addEventListener('site:language', filter);
  archive.querySelector('[data-certificate-controls]').hidden = false;
  filter();
})();
