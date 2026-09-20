# swiftlabs.xyz

This repository contains the Eleventy source for `swiftlabs.xyz`, Jane Swift’s personal site connecting hospitality work with owner-controlled computing.

## Purpose

The site serves as:

- a Jane-led introduction to private, decentralized, open-source, agent-first computing
- a durable contact surface on a custom domain
- an evidence-bounded introduction to the experimental restaurant application

## Topology

The site is built with Eleventy and outputs static files to `_site/`.

```text
.
├── .eleventy.js
├── .node-version
├── package.json
├── src/
│   ├── _data/
│   ├── _includes/
│   ├── assets/
│   ├── index.njk
│   ├── about.njk
│   ├── work.njk
│   ├── contact.njk
│   ├── 404.njk
│   ├── robots.txt
│   ├── sitemap.njk
│   ├── site.webmanifest
│   └── CNAME
└── _site/
```

## Local Development

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Build the static site:

```bash
npm run build
```

## Deployment

The generated output lives in `_site/`. The site keeps the custom domain via `src/CNAME`.

## Notes

- `src/_includes/layout.njk` owns the shared page shell and metadata.
- `src/_data/site.json` is the central place for site-wide identity and navigation data.
- `src/assets/` is passed through to the build output unchanged.

## Design and verification

The accepted overhaul specification, source checks, verification results and screenshots are in [docs/planning/site-overhaul](docs/planning/site-overhaul/spec.md). Use Node 20 as specified in `.node-version`; the system default may differ. Public copy describes principles and benefits, while implementation details remain in development documentation.

## Theme checks

Run `npm test` on Node 20 for theme preference behavior and light/dark contrast checks. The small theme bootstrap is included before the stylesheet; it follows the system preference until a visitor chooses a theme, then saves that choice locally. With scripting disabled, CSS follows the system preference and hides the switcher.

Theme experiments and their screenshots are recorded in [docs/planning/theme-experiments](docs/planning/theme-experiments/dark-light.md). The original overhaul report remains historical baseline evidence.
