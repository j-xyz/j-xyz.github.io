# swiftwork.xyz

This repository contains the Eleventy source for `swiftwork.xyz`, a small professional website for Jane Swift.

## Purpose

The site serves as:

- a professional homepage
- a durable contact surface on a custom domain
- a foundation for future work, writing, and case-study pages

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
