# Repository Guidelines

## Scope & Authority

This repo is the Eleventy source for `swiftlabs.xyz`, a public-facing site for Jane Swift. Treat `src/` as the source of truth for content, layout, metadata, and assets. Use this local guidance for site work; use root Maeve guidance only for cross-project coordination or when local guidance is absent.

## Project Structure & Module Organization

Source files live in `src/`; generated output lives in `_site/` and should not be edited directly. Page templates are top-level Nunjucks files such as `src/index.njk`, `src/about.njk`, `src/work.njk`, and `src/contact.njk`. Shared layout markup is in `src/_includes/layout.njk`, site-wide data and navigation are in `src/_data/site.json`, and static assets are under `src/assets/`. Files such as `src/CNAME`, `src/robots.txt`, and `src/site.webmanifest` are copied through during builds.

## Build, Test, and Development Commands

- `npm install`: install Eleventy and project dependencies.
- `npm run dev`: start the Eleventy development server with live rebuilds.
- `npm run build`: generate the static site into `_site/`.

Use Node 20, matching `.node-version` and the `package.json` engine range (`>=20 <21`).

## Coding Style & Naming Conventions

Use two-space indentation in Nunjucks, JSON, CSS, and JavaScript config files. Keep page filenames lowercase and route-oriented, for example `work.njk` for `/work/`. Prefer shared site metadata in `src/_data/site.json` over duplicating names, URLs, email addresses, or navigation labels in templates. Keep CSS classes descriptive and component-oriented, following patterns such as `site-header`, `hero-layout`, and `contact-panel`.

## Testing Guidelines

There is no formal automated test suite yet. Before submitting changes, run `npm run build` and inspect the generated site for template errors. For visual or content changes, also run `npm run dev` and check affected pages in a browser, including mobile-width layouts.

## Commit & Pull Request Guidelines

Recent history mostly uses Conventional Commit-style messages, such as `feat(theme): ...`, `refactor(site): ...`, `chore(node): ...`, and `docs(build): ...`. Pull requests should describe the user-visible change, list verification performed, and include screenshots for layout or theme changes. Link related issues or planning notes when available.

## Publication Safety

Keep canonical URLs, social metadata, and contact details aligned with `src/_data/site.json`. This is a public website, so changes should be publication-ready and free of accidental draft-only content.
