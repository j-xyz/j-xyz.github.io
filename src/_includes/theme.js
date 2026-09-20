(() => {
  const key = 'swiftlabs-theme';
  const root = document.documentElement;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = (value) => value === 'light' || value === 'dark';
  let preference = null;
  let button;

  try {
    const saved = window.localStorage.getItem(key);
    if (valid(saved)) preference = saved;
  } catch {
    // The switch remains usable when browser storage is unavailable.
  }

  function apply() {
    const theme = preference || (system.matches ? 'dark' : 'light');
    root.dataset.theme = theme;
    document.getElementById('theme-color-light').media = theme === 'light' ? 'all' : 'not all';
    document.getElementById('theme-color-dark').media = theme === 'dark' ? 'all' : 'not all';
    if (button) {
      const label = `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`;
      button.setAttribute('aria-label', label);
      button.setAttribute('title', label);
    }
  }

  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', (event) => {
    if (event.key !== key && event.key !== null) return;
    preference = valid(event.newValue) ? event.newValue : null;
    apply();
  });

  document.addEventListener('DOMContentLoaded', () => {
    button = document.getElementById('theme-toggle');
    if (!button) return;
    apply();
    button.hidden = false;
    button.addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      apply();
      try {
        window.localStorage.setItem(key, preference);
      } catch {
        // Keep the chosen theme for this page even if it cannot be saved.
      }
    });
  });
})();
