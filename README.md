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
├── docs/
│   ├── archive/
│   │   ├── README.md
│   │   ├── dependency-update/
│   │   ├── site-overhaul/
│   │   └── theme-experiments/
│   └── planning/
│       └── project-brief.md
├── src/
│   ├── _data/
│   │   ├── built.json
│   │   ├── numbers.json
│   │   ├── roadmap.json
│   │   ├── site.json
│   │   └── updates.json
│   ├── _includes/
│   │   ├── field-note-background.njk
│   │   ├── hearth.svg
│   │   ├── layout.njk
│   │   └── theme.js
│   ├── assets/
│   ├── index.njk
│   ├── about.njk
│   ├── build.njk
│   ├── work.njk
│   ├── whats-new.njk
│   ├── whats-next.njk
│   ├── contact.njk
│   ├── 404.njk
│   ├── robots.txt
│   ├── sitemap.njk
│   ├── site.webmanifest
│   └── CNAME
└── tests/
    └── theme.test.cjs
```

### What feeds each page

| Data file in `src/_data/` | Pages that use it | Purpose |
| --- | --- | --- |
| `built.json` | Build (`src/build.njk`) | Built capabilities and screenshots. |
| `updates.json` | Build (`src/build.njk`), What's new (`src/whats-new.njk`) | Latest and earlier updates. |
| `roadmap.json` | Build (`src/build.njk`), What's next (`src/whats-next.njk`) | the one source for the plan lists on Build and What's next |
| `numbers.json` | Build (`src/build.njk`), What's new (`src/whats-new.njk`) | set from a release-count script kept outside this repo; never typed by hand |

## Local Development

Select Node 24.21.0 from `.node-version` using your local runtime manager (engines: `>=24 <25`). Then install the locked dependencies:

```bash
npm ci
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

The accepted overhaul specification, source checks, verification results and screenshots are in [docs/archive/site-overhaul](docs/archive/site-overhaul/spec.md). Use Node 24.21.0 as specified in `.node-version`; the system default may differ. Public copy describes principles and benefits, while implementation details remain in development documentation.

## Theme checks

Run `npm test` on Node 24.21.0 for theme preference behavior and light/dark contrast checks. The small theme bootstrap is included before the stylesheet; it follows the system preference until a visitor chooses a theme, then saves that choice locally. With scripting disabled, CSS follows the system preference and hides the switcher.

Theme experiments and their screenshots are recorded in [docs/archive/theme-experiments](docs/archive/theme-experiments/dark-light.md). The original overhaul report remains historical baseline evidence.
