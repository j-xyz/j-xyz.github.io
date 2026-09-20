const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

function boot({ saved = null, dark = false, blocked = false } = {}) {
  const events = {};
  const storage = { value: saved };
  const root = { dataset: {} };
  const button = {
    hidden: true,
    attributes: {},
    setAttribute(name, value) { this.attributes[name] = value; },
    addEventListener(name, callback) { events[name] = callback; },
  };
  const meta = { light: {}, dark: {} };
  const media = { matches: dark, addEventListener(name, callback) { events.system = callback; } };
  const document = {
    documentElement: root,
    getElementById(id) {
      if (id === 'theme-toggle') return button;
      if (id === 'theme-color-light') return meta.light;
      if (id === 'theme-color-dark') return meta.dark;
    },
    addEventListener(name, callback) { events[name] = callback; },
  };
  const window = {
    matchMedia() { return media; },
    localStorage: {
      getItem() { if (blocked) throw Error('Storage disabled'); return storage.value; },
      setItem(key, value) { if (blocked) throw Error('Storage disabled'); storage.value = value; },
    },
    addEventListener(name, callback) { events[name] = callback; },
  };
  vm.runInNewContext(readFileSync('src/_includes/theme.js', 'utf8'), { window, document });
  const initialTheme = root.dataset.theme;
  events.DOMContentLoaded();
  return { root, button, meta, storage, initialTheme,
    click: () => events.click(),
    system(value) { media.matches = value; events.system({ matches: value }); },
    stored(value) { events.storage({ key: 'swiftlabs-theme', newValue: value }); },
  };
}

test('applies system preference before DOM ready, without saving a choice', () => {
  for (const dark of [false, true]) {
    const page = boot({ dark });
    assert.equal(page.initialTheme, dark ? 'dark' : 'light');
    assert.equal(page.storage.value, null);
    assert.equal(page.button.hidden, false);
  }
});
test('saved choice overrides system; invalid values fall back to system', () => {
  assert.equal(boot({ saved: 'light', dark: true }).initialTheme, 'light');
  assert.equal(boot({ saved: 'dark' }).initialTheme, 'dark');
  assert.equal(boot({ saved: 'invalid', dark: true }).initialTheme, 'dark');
});
test('toggle changes theme, accessible action, browser chrome and persisted choice', () => {
  const page = boot();
  page.click();
  assert.equal(page.root.dataset.theme, 'dark');
  assert.equal(page.storage.value, 'dark');
  assert.equal(page.button.attributes['aria-label'], 'Switch to light theme');
  assert.equal(page.meta.dark.media, 'all');
  assert.equal(page.meta.light.media, 'not all');
  assert.equal(boot({ saved: page.storage.value }).initialTheme, 'dark');
  page.click();
  assert.equal(page.root.dataset.theme, 'light');
  assert.equal(page.button.attributes['aria-label'], 'Switch to dark theme');
});
test('system changes apply until the visitor chooses explicitly', () => {
  const page = boot();
  page.system(true);
  assert.equal(page.root.dataset.theme, 'dark');
  page.click();
  page.system(true);
  assert.equal(page.root.dataset.theme, 'light');
});
test('unavailable storage does not prevent initialization or toggling', () => {
  const page = boot({ blocked: true, dark: true });
  page.click();
  assert.equal(page.root.dataset.theme, 'light');
  page.system(true);
  assert.equal(page.root.dataset.theme, 'light');
});
test('another tab can update or clear the preference', () => {
  const page = boot();
  page.stored('dark');
  assert.equal(page.root.dataset.theme, 'dark');
  page.stored(null);
  assert.equal(page.root.dataset.theme, 'light');
  page.system(true);
  assert.equal(page.root.dataset.theme, 'dark');
});

function luminance(hex) {
  const channels = hex.match(/[a-f\d]{2}/gi).map((part) => {
    const value = parseInt(part, 16) / 255;
    return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return channels.reduce((sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index], 0);
}
function contrast(a, b) {
  const values = [luminance(a), luminance(b)].sort((x, y) => x - y);
  return (values[1] + 0.05) / (values[0] + 0.05);
}
test('both palettes meet text and interactive-boundary contrast targets', () => {
  const css = readFileSync('src/assets/css/site.css', 'utf8');
  for (const selector of [':root', ':root[data-theme="dark"]']) {
    const body = css.slice(css.indexOf(selector + ' {')).split('}')[0];
    const palette = Object.fromEntries([...body.matchAll(/--([\w-]+):\s*(#[a-f\d]{6})/gi)].map((m) => [m[1], m[2]]));
    for (const background of ['bg', 'surface', 'note-bg']) {
      for (const text of ['ink', 'muted', 'link', 'accent']) {
        assert.ok(contrast(palette[text], palette[background]) >= 4.5, `${selector}: ${text}/${background}`);
      }
      assert.ok(contrast(palette['control-line'], palette[background]) >= 3, `${selector}: control boundary`);
    }
    for (const background of ['button-bg', 'button-hover']) {
      assert.ok(contrast(palette['button-ink'], palette[background]) >= 4.5, `${selector}: button text`);
    }
    assert.ok(contrast(palette.ink, palette.selection) >= 4.5, `${selector}: selected text`);
  }
});
