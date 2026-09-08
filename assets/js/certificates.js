(() => {
  const search = document.querySelector('#certificate-search');
  if (!search) return;
  const category = document.querySelector('#certificate-category');
  const records = [...document.querySelectorAll('[data-certificate-category]')];
  const normalize = (text) => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function filter() {
    const query = normalize(search.value.trim());
    let visible = 0;
    records.forEach((record) => {
      record.hidden = !(category.value === 'all' || category.value === record.dataset.certificateCategory) || !normalize(record.textContent).includes(query);
      if (!record.hidden) visible++;
    });
    const lang = document.documentElement.lang;
    const labels = lang === 'pt-BR' ? ['registros', 'Nenhum registro encontrado.'] : lang === 'es' ? ['registros', 'No se encontraron registros.'] : ['records', 'No matching records.'];
    document.querySelector('[data-certificate-count]').textContent = visible ? `${visible} / ${records.length} ${labels[0]}` : labels[1];
  }
  search.addEventListener('input', filter);
  category.addEventListener('change', filter);
  document.addEventListener('site:language', filter);
  document.querySelector('[data-certificate-controls]').hidden = false;
  filter();
})();
