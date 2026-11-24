# Source Code Pro experiment

User-requested typography change on September 20, 2026, after baseline `c2592f5`.

All typography now uses `"Source Code Pro", Menlo, monospace`. Copy, routes, colors and layout rules remain unchanged. Regular (400) and Semibold (600) are served locally with `font-display: swap`; no external font request or new service is introduced.

Font binaries are unmodified files from [Adobe’s official repository](https://github.com/adobe-fonts/source-code-pro/tree/803b7e23ec97ae58b6232ea76519a76d428ba268), using its WOFF2/TTF Regular and Semibold files. The accompanying SIL Open Font License is preserved at `src/assets/fonts/source-code-pro/LICENSE.txt`. The text extension prevents the static-site generator from treating the license as a content page.

Verification: Node 20 build passed; `git diff --check` passed. Desktop homepage and 320px homepage inspected visually; all five routes at 320px had clientWidth and scrollWidth of 320, with no horizontal page overflow. Screenshots are saved beside this record. Earlier baseline evidence remains unchanged. No commit or push performed for this experiment.
