# Source and claim check — September 20, 2026

## Authority

Read the supplied draft-specs and source-check skills at `/Users/jane/jxyz/maeve/skills/`, the website AGENTS.md, and the mission/FloCafe AGENTS.md files when inspecting those repositories. Source documents were evidence, not authorization to execute application handoffs. The website working tree was clean at implementation start.

## Mission and application evidence

Read `/Users/jane/jxyz/swiftOS/README.md`, `docs/vision.md`, `docs/specs/owner-controlled-node.md`, `docs/specs/restaurant-pos-evaluation.md`, `docs/research/flocafe-baseline-source-check-2026-09-19.md`, and `docs/planning/flocafe-remote-goal/continuation-spec.md`.

Those sources establish direction, the selected restaurant experiment, and a user-reported installation/build trial. They do not establish current fork behavior. The continuation packet identifies a separate Linux application checkout; it was not queried during this website task.

The accessible `/Users/jane/jxyz/FloCafe` checkout was clean at `4f9be2053ba6041836ac2870b9de2175813d6ffa`, with origin `https://github.com/FreeOpenSourcePOS/FloCafe.git`. LICENSE is MIT, copyright 2025–2026 FloCafe Contributors. Current local startup/database code still imports the desktop runtime; `docs/headless-baseline.md` is absent. This is the upstream baseline, not current remote fork execution evidence.

Public fork availability, current end-to-end fork behavior, physical device usability, recovery, peripherals and payment integration remain unverified. Public copy says experimental and provides no source/download CTA. No FloCafe code or assets were copied. The website’s existing MIT LICENSE is unchanged.

## Website implementation sources

- Manifest: `@11ty/eleventy` range `^3.1.2`; lockfile resolves 3.1.2 and Nunjucks 3.2.4. Existing installed Eleventy build reports 3.1.2.
- [Official Nunjucks integration](https://www.11ty.dev/docs/languages/nunjucks/): Eleventy 3 supports Nunjucks 3 and shared includes. Retain existing template configuration; no custom environment or disabled escaping.
- [Official passthrough-copy API](https://www.11ty.dev/docs/copy/): retain configured source asset/manifest/domain copies.
- Canonical URLs, navigation and contact identity remain centralized. JSON-LD strings use Nunjucks JSON serialization; generated JSON was parsed successfully.

## Temporary runtime safety

The shell was Node 26.8.2, incompatible with the repository’s `>=20 <21` rule. Downloaded official Node 20.20.2 to `/private/tmp`, retaining project dependencies and system runtime unchanged. Archive SHA-256 matched official checksums: `466e05f3477c20dfb723054dfebffe55bc74660ee77f612166fca121dacb65b6`.

[Official release notes](https://nodejs.org/en/blog/release/v20.20.2) identify a security release and list addressed advisories. This was a scoped provenance/release check, not a comprehensive current CVE audit. The runtime was used for local build/preview only. Network permission was obtained for the official download. No credentials or private application data were used.
