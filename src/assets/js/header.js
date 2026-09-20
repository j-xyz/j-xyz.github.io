(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;

  // Measure instead of hard-coding: font loading, text zoom and both mobile rows
  // must all leave enough room above anchor targets and keyboard focus.
  const measure = () => {
    document.documentElement.style.setProperty('--header-height', `${header.getBoundingClientRect().height}px`);
  };
  measure();
  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(header);
  else window.addEventListener('resize', measure);

  document.addEventListener('focusin', (event) => {
    const target = event.target;
    if (header.contains(target) || target.classList.contains('skip-link')) return;
    const top = target.getBoundingClientRect().top;
    const clearance = header.getBoundingClientRect().bottom + 16;
    if (top < clearance) window.scrollBy(0, top - clearance);
  });
})();
