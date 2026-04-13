# j-xyz.github.io

## Scope And Authority

- This repo is the Eleventy source for `swiftlabs.xyz`, a public-facing site
  for Jane Swift.
- Keep edits inside the repo and treat `src/` as the source of truth for
  content, layout, metadata, and assets.
- Treat this repository as locally authoritative for site code, content, and
  project docs.
- Use root Maeve guidance only for cross-project coordination or when local
  guidance is absent.

## Defaults

- Prefer concise, polished updates that fit a professional homepage and
  contact surface.
- Keep copy, navigation, and metadata aligned with the current site
  positioning in `src/_data/site.json`.
- Use the existing Eleventy structure and `npm run dev` / `npm run build`
  scripts for iteration and verification.

## Safety

- Do not edit `_site/` directly; it is generated output.
- Treat canonical URLs, social metadata, and contact details as user-facing
  publication content.
- If you change templates, styles, or shared data, verify the build so the
  public site stays consistent.

## Publication Boundary

- This is a public website project, so changes should be publication-ready
  and free of accidental draft-only content.
- Keep any future work in step with the site structure already established by
  the homepage, about, work, and contact pages.
