# Dependency maintenance — 2026-09-20

Implemented locally, uncommitted. No source, theme, template, configuration, test, workflow, deployment, or system-runtime changes.

## Scope and preservation

Read repository AGENTS.md and the explicitly requested security-audit and source-check skills under `/Users/jane/jxyz/maeve/skills/`, including the dependency safety policy. The explicit user dispatch authorized local installs; network/listener escalation controls were respected.

Initial staged and unstaged status were clean at `1767f7537a57eb2b30a3a2b8e196f4d8160ceb6a`. The existing theme work and test script were already present. Captured source, tests, manifests, runtime instructions and installed dependencies at `/private/tmp/swiftlabs-dependency-20260920/baseline` before installation; checked shared files against that snapshot immediately before edits. Final source/test hashes still match. No overlapping writes were observed. Nothing was staged.

## Decision and versions

| Component | Before | After |
| --- | --- | --- |
| Runtime selector | 20 | 24.21.0 |
| Engines | >=20 <21 | >=24 <25 |
| Actual verification runtime | 20.20.2 | 24.21.0 (npm 11.19.0) |
| Eleventy | 3.1.2 | 3.1.6; manifest ^3.1.6 |
| LiquidJS | 10.25.0 | 10.29.0 |
| markdown-it | 14.1.1 | 14.3.2 |
| Nunjucks | 3.2.4 | 3.2.4 |
| js-yaml (Eleventy / gray-matter) | 4.1.1 / 3.14.2 | 4.3.2 / 3.15.2 |
| picomatch (root / watcher) | 4.0.3 / 2.3.1 | 4.0.7 / 2.3.2 |
| ws | 8.19.0 | 8.21.3 |

[Node release policy](https://nodejs.org/en/about/previous-releases) confirms Node 20 EOL and Node 24 LTS. [24.21.0 release](https://nodejs.org/en/blog/release/v24.21.0) confirms the selected version. Downloaded official Darwin ARM64 archive into the task's temporary directory; SHA256 matched official SHASUMS256.txt: `bed7eea5325e1108f32ce5228ddd6a5f0f08a499ee42aa7442aea583702f6057`. System Node 26.8.2 was not replaced or used for project verification.

[Eleventy 3.1.6 release](https://github.com/11ty/eleventy/releases/tag/v3.1.6) and [tagged manifest](https://raw.githubusercontent.com/11ty/eleventy/v3.1.6/package.json), corroborated by `npm view @11ty/eleventy@3.1.6 version engines dependencies scripts --json`, establish Node >=18 compatibility and LiquidJS ^10.27.0, markdown-it ^14.2.0, Nunjucks ^3.2.4. The release redirects to the renamed repository; the installed package remains @11ty/eleventy v3. No v4 alpha adopted.

Resolved newer compatible transitives through npm. No overrides, forced fixes, direct transitive dependencies, or transitive major upgrades. Full changes are in `2026-09-20-package-changes.json`. The moo downgrade to 0.5.2 follows Eleventy's exact pin. Recursive-copy drops maximatch and its four array helper dependencies. npm also corrected stale root lockfile license ISC to match the existing MIT manifest and added its engines metadata; the manifest license itself was not changed.

## Security findings and mitigation

[LiquidJS advisory](https://github.com/harttle/liquidjs/security/advisories/GHSA-gf2q-c269-pqgc): crafted template execution threatens build-host code/data if an attacker controls templates. [markdown-it advisory](https://github.com/markdown-it/markdown-it/security/advisories/GHSA-6v5v-wf23-fmfq): smartquotes processing can consume excessive CPU when typographer is enabled. This site's inputs are repository-owned Nunjucks templates; configuration has no custom typographer enablement or public template/Markdown ingestion endpoint. Neither dependency finding proves a remotely exploitable public static site.

The first live audit after the Eleventy update reported three high-severity package groups: js-yaml, picomatch, ws. Saved verbatim in `2026-09-20-audit-initial.json` (this is an intermediate audit, not an original-tree audit). Compatible `npm update js-yaml picomatch ws --package-lock-only --ignore-scripts` resolved them:

- YAML parsing of front matter/data: [merge-source CPU advisory](https://github.com/advisories/GHSA-2883-xcg3-v3hh), patched in 3.15.2/4.3.2; earlier merge/omap findings are listed in audit JSON. Risk requires hostile build input.
- Glob matching in chokidar's anymatch/readdirp paths: [extglob ReDoS](https://github.com/advisories/GHSA-c2c7-rcm5-vvqj) and POSIX class injection finding; watcher copies now 2.3.2. No visitor-controlled glob path identified.
- Eleventy dev server WebSocket: [memory exhaustion advisory](https://github.com/advisories/GHSA-96hv-2xvq-fx4p) and memory disclosure finding; now 8.21.3. Relevant to preview clients, not deployed static output.

Final live `npm audit --include=dev --json` exited 0, reporting zero vulnerabilities across 130 dependencies (131 including root); saved in `2026-09-20-audit-final.json`. This is point-in-time known-advisory evidence, not comprehensive security clearance. Initial sandbox DNS failures were retried with approved network access; no offline result was accepted as clearance.

Install hooks: root has only dev/build/test scripts. Inspected published package manifests after an initial `npm ci --ignore-scripts`. Several packages have publisher/developer prepare scripts, not install hooks run from registry tarballs. The only lockfile install-script flag is unchanged optional Darwin fsevents 2.3.3; its installed manifest contains no preinstall/install/postinstall command or install.js. Ordinary npm ci succeeded but npm 11.19.0 warned that fsevents scripts were not approved by allowScripts. No approval bypass or persistent npm policy change was introduced. Preview starts successfully; native watcher rebuild behavior was not separately triggered.

## Commands and verification

Commands ran from the repository unless stated; prepend `PATH=/private/tmp/swiftlabs-dependency-20260920/node-v24.21.0-darwin-arm64/bin:$PATH` for the updated runtime. npm used `--cache /private/tmp/swiftlabs-dependency-20260920/npm-cache`; network resolution used `--fetch-retries=0 --fetch-timeout=15000`.

1. Baseline Node 20.20.2 `npm test` and `npm run build`: seven tests passed, six rendered files plus seven copied assets.
2. `npm install --package-lock-only --ignore-scripts`, then targeted update above: successful after controlled network retries.
3. `npm ci --ignore-scripts`: successful, 130 dependencies. Reviewed package hooks; then ordinary `npm ci`: successful clean install, optional-hook warning described above.
4. Live `npm audit --include=dev --json`: exit 0, zero findings. `npm ls @11ty/eleventy liquidjs markdown-it nunjucks js-yaml picomatch ws`: expected installed versions, no invalid dependency warning.
5. `npm test`: 7/7, including system preference, persistence, cross-tab updates, blocked storage and palette contrast. `npm run build`: successful Eleventy 3.1.6 build.
6. Fresh outputs: old isolated Eleventy cmd.cjs under Node 20 and new cmd.cjs under Node 24, each run against the unchanged original source path using separate `--output` directories. `diff -rq` empty; SHA256 matches for all 13 files, covering routes, text, metadata, sitemap, CSS, fonts, manifest, robots and CNAME. Hashes saved in `2026-09-20-output-hashes.json`.
7. Investigated first comparison discrepancy: copying source changes filesystem birth times used in collection ordering, swapping about/contact sitemap order. Same-path baseline removes that artifact. Existing `_site/` also contained .DS_Store and stale font LICENSE/LICENSE.md files absent from current source. Compared fresh directories instead; did not manually edit generated output or delete those pre-existing files.
8. `npm run dev -- --port=8098` with temporary NODE_OPTIONS preload that forces every TCP listen call to 127.0.0.1. `lsof -nP -iTCP:8098 -sTCP:LISTEN` verified `127.0.0.1:8098` before browser use. Sandbox bind failed on 8097; controlled retry on 8098 succeeded.
9. In-app browser: visually inspected homepage in both themes at desktop 1440 and mobile 390 widths; clicked all four primary navigation links at both widths. Correct titles/routes, no horizontal overflow, theme persisted across navigation and reload, no console errors. Screenshots were inspected inline in task history. Browser viewport override reset afterward. Standalone Playwright could not launch because its Chromium bundle was absent; used existing in-app browser without installing browser software. Temporary failed harness was not added to repository.
10. Final `git diff --check`: pass. Reviewed entire lockfile and runtime/documentation diffs. Source, tests, config and workflow unchanged.

Not performed: hosted Linux CI, deployment, exhaustive cross-browser/accessibility testing, new adversarial exploit tests, or native watcher edit/rebuild test. Existing unit tests cover more theme edge cases than the browser smoke check. No unresolved npm advisories at final audit.

## Separate control findings (unchanged)

- CI runtime: `.github/workflows/pages.yml` setup-node already reads `.node-version`, so the project runtime selection moves to 24.21.0 automatically.
- Action versions: checkout@v4, setup-node@v4, configure-pages@v5, upload-pages-artifact@v3, deploy-pages@v4. Tags are not immutable SHA pins; internal Action runtime versions are independent of the site's Node selection. Action upgrades were not evaluated or made.
- Credential scope: workflow-level contents:read, pages:write and id-token:write apply to build as well as deploy; checkout does not explicitly disable persisted credentials. No credentials inspected or used for GitHub writes. Job-level narrowing remains separate work.
- Preview listener: dev-server 2.0.8 `_serverListen` passes only port to listen, leaving default wildcard scope. Displaying localhost is not proof of private binding. The temporary preload constrained this verification only; normal npm run dev remains unchanged and requires a separate listener-hardening decision.

## Handoff and rollback

Uncommitted modifications: `.node-version`, `package.json`, `package-lock.json`, README.md, AGENTS.md, plus new dated records in this directory. Existing scripts preserved. node_modules and generated output are ignored. Temporary runtime and baseline remain under `/private/tmp/swiftlabs-dependency-20260920` and may be reclaimed later; select your own Node 24.21.0 installation for continued development.

To roll back only this update, first inspect for later edits. Reverse only the dependency/runtime hunks in those five files using the pre-update contents at commit `1767f7537a57eb2b30a3a2b8e196f4d8160ceb6a` or the temporary baseline; do not reset the worktree or overwrite subsequent design changes. Reinstall the restored lock with npm ci under the restored runtime and rebuild. Node 20 is EOL, so rollback is a temporary recovery path. Retain these records as history or remove only these dated records if desired.

Suggested commit scopes (not created): `chore(deps): move to Node 24 LTS and refresh Eleventy v3` for the five implementation/instruction files; `docs(deps): record maintenance audit and behavior verification` for this directory.
