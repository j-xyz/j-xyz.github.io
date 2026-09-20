# Jane Swift / swiftlabs.xyz overhaul

Accepted by the user on September 20, 2026, with an explicit instruction to implement. The user chose a Jane-led personal site over a mission-led studio. This document records that accepted direction; it creates no repository policy.

## Objective and audience

Connect Jane’s hospitality grounding to private, decentralized, open-source, agent-first computing for people and small businesses. Restaurant operators are the first concrete audience; potential collaborators are a secondary audience.

The homepage leads with “Computing should answer to the people who use it.” The mission begins “I’m Jane Swift” and identifies restaurant work as the starting point. Explain private as control over access/data, decentralized as distributed ownership and replaceable providers, open-source as inspectability/adaptability/continuity, and agent-first as permissioned, understandable assistance under human control. Retaining data and identity, changing providers, and recovery are intended outcomes, not established product guarantees.

## Structure and design

Preserve Home, About, Work, Contact and 404 routes. Home introduces Jane, the mission, four principles and the restaurant experiment. About grounds the mission in hospitality. Work separates the direction, workflow research questions and observations still needing evidence. Contact preserves direct email and location. The error page provides recovery links.

Use ivory, charcoal, deep green and restrained terracotta; system serif headlines and sans-serif body text; generous spacing, ruled sections and numbered principles. The asymmetric homepage has a restaurant field note. Mobile follows a single reading order with visible navigation. No decorative animation, stock imagery, invented product screenshots, external fonts or scripted menu.

Update shared metadata and manifest consistently. Preserve canonical domain, contact details and required notices; omit the error page from the sitemap. No public APIs, tracking, embeds, forms, new services or dependency upgrades.

## Boundaries and acceptance examples

- Visitors can identify Jane, the mission and restaurant application from Home.
- The FloCafe fork is experimental. No production, disconnected-client, peer-replication, payment-integration or autonomous-reliability claims.
- No new biography, customers, endorsements, metrics, prices or readiness claims.
- No public implementation-product inventory in copy, metadata or illustrations. Technical evidence belongs in development documentation.
- No source/download CTA without verifying the exact public destination and license.
- All existing routes work on desktop, mobile and keyboard; preserve canonical domain and email.

## Verification and handoff

Use Node 20 with existing Eleventy 3.1.2/Nunjucks 3.2.4. Run build and preview. Inspect all pages at desktop/mobile widths, 320px reflow, zoom, keyboard order, skip link, focus, contrast, reduced motion, links, metadata and external requests. Record actual outcomes and screenshots, distinguishing unavailable tests.

Maintain source only; never edit generated output. Preserve pre-existing work. No commits, pushes or publication. Report uncommitted scopes and limitations. Any Goal instruction or replacement must remain at most 4,000 characters including newlines; supporting specification/evidence stays separate.

## Rationale and revisions

Initial source review found generic professional messaging, an empty hero column, repeated dark cards, external font requests, and manifest branding/color drift. Existing routes, semantic landmarks, navigation state and skip-link structure were useful foundations. A light editorial system brings Jane and practical questions forward without suggesting a launched product.

Implementation kept the accepted scope. The Person metadata uses JSON serialization and central identity data; no external source CTA was added. Node 26 in the shell conflicted with repository Node 20 guidance; a checksum-verified temporary Node 20 runtime resolved build verification without changing system configuration.
