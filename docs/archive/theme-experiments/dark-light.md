# Coordinated dark and light themes

September 20, 2026. User requested a dark theme inspired by Carbonfox, Vercel and Ayu, a light/dark switch, and complementary light colors. Follow-up requested a subtler position with sun/moon icons and no visible label. Earlier Source Code Pro work remains intact and uncommitted.

## Final design and behavior

Carbon-gray backgrounds, soft white text, amber accents and muted blue links in dark mode; pale neutral backgrounds with deeper amber/blue in light mode. Shared semantic color tokens cover panels, text, links, buttons, focus, selection and browser theme metadata. Typography and page copy are unchanged.

The 18px sun/moon control sits beside Jane’s identity, separate from navigation. It has no visible label or persistent button border, but retains a 44px target, visible keyboard focus, hover treatment, descriptive accessible name and tooltip. Sun offers light mode; moon offers dark mode. Icons are inline decorative SVG, not additional network requests.

On first visit, use the system preference. Explicit choices persist in localStorage under `swiftlabs-theme`. System changes apply while no explicit preference exists. Cross-tab changes synchronize; unavailable storage does not disable switching. An inline shared bootstrap applies the preference before the stylesheet. Without scripting, the switch is hidden and CSS follows the system theme. No analytics, cookies, new services, libraries or dependency upgrades.

## Sources and implementation rules

- [Carbonfox palette](https://github.com/EdenEast/nightfox.nvim/blob/main/lua/nightfox/palette/carbonfox.lua): charcoal/neutral inspiration.
- [Geist colors](https://vercel.com/geist/colors): distinct surface, border and text roles.
- [Ayu palette](https://github.com/ayu-theme/ayu-colors/blob/master/themes/dark.yaml): warm-accent inspiration. This is a custom combination, not an exact theme port.
- [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme) and [matchMedia](https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia): system fallback and preference-change events.
- [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage): persistent origin-local preference; reads/writes guarded because storage can be unavailable.

Existing Eleventy 3.1.2 and Nunjucks 3.2.4 conventions are retained. No framework changes.

## Verification

- Added six behavior tests first; all failed because the theme bootstrap was absent. Implemented behavior, then all passed. Added contrast coverage: `npm test` now passes seven tests on Node 20.20.2.
- Cases: light/dark system defaults before DOM ready, saved overrides, invalid values, toggle persistence/accessible action/browser metadata, system changes, blocked storage, cross-tab update/removal.
- Both palettes meet 4.5:1 for checked text/background pairs and 3:1 for checked control-boundary pairs. Final icon uses muted text color, already covered at 4.5:1. Focus uses the checked accent.
- `npm run build` and `git diff --check` pass. Generated theme bootstrap precedes CSS on all five routes; theme metadata and local links were checked. Sitemap still has four content routes.
- Browser: desktop homepage in both themes, dark About/Contact/404, Work content panels in both themes, mobile homepage in both themes, and tablet header. All five routes checked at 320px in both modes without horizontal page overflow; preference retained across navigation/reload.
- Enter and Space activate switching. After repositioning, Tab reaches the switch immediately after the brand link. Accessible label changes with the target theme and both SVG icons survive switching. Final mobile homepage rechecked at 320px.
- Browser error/warning log query returned no entries. Screenshots saved alongside this document; current homepage/focus images reflect the icon-only revision.

System changes, storage failures and cross-tab events were tested with a small DOM/storage harness, not OS/browser emulation. No-JavaScript fallback was source-inspected, not tested with scripting disabled. No physical-device, cross-browser, or network-tracing coverage is claimed. The original baseline reports and screenshot files remain historical evidence.

## Handoff

All theme and preceding font changes remain uncommitted. Proposed commit: `feat(theme): add coordinated light and dark palettes`. Include shared layout/bootstrap, stylesheet, manifest, test command/tests, README and this experiment’s evidence. Keep font assets/license and their earlier experiment record in a separate `feat(type): use locally served Source Code Pro` commit, using partial staging for the shared stylesheet. No commit or push is authorized by the theme requests.

### Hearth and masthead revision

At Jane’s request, moved the icon switch onto the domain line beneath her name. Its accessible action label and 44px target remain. Replaced the Field notes label and table drawing with an original inline SVG of a wood fire in an arched stone hearth, with a node network behind it. The drawing uses theme colors, contains no animation or external assets, and has an accessible image title. This is a conceptual illustration, not a capability diagram. Restaurant copy and experimental status remain.

Verification: Node 20 build and all seven tests passed. Inspected desktop dark and mobile light rendering; checked keyboard Space toggling and 320px reflow (client and scroll widths both 320). Screenshots: hearth-dark-desktop.png, hearth-light-desktop.png, hearth-mobile-header.png, hearth-light-mobile.png. These supersede earlier masthead screenshots. Changes remain uncommitted.
