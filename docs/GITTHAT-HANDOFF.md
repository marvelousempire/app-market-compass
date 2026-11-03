# gitThat handoff: Market Compass, additive demo (2026-11-03)

## Founder order (unmodified intent)
**Bring the full Market Compass development work into the computer using gitThat, while preserving EVERY pre-existing capability.** Market analysis on launch, stock charts, live market source lookups, EMA/RSI/MACD, Fibonacci, watchlists, evidence/history, and all analysis panels remain intact. New universal subject simulations, Hybrid CCK schedules, Omo's Intel and named King-card participant sections ADD to the application. Never remove or suppress an existing feature because another feature uses it.

## Exact handoff pointers
- GitHub proposal repository: `marvelousempire/app-market-compass`
- Pull request: https://github.com/marvelousempire/app-market-compass/pull/11
- Proposed source branch: `feat/intelthat-proof-health-bridge`
- Target branch: `main`, **not merged**; source authority/Gitea readback remains unverified
- Mac preview runbook: `docs/FIVEMAC-PREVIEW.md`
- Local preview entry: `scripts/commission-demo.sh`
- Synthetic receipt script: `scripts/demo_preflight.py`
- Dedicated browser preview: `scripts/preview_server.py`
- Source/API additions: `src/market_compass/simulation.py`, `hcck_profiles.py`, `intelthat_bridge.py`, `participants.py`, `studio_rooms.py`
- CI: `.github/workflows/test.yml` and `.github/workflows/universal-demo.yml`

## Existing gitThat contract: do not fake installation

The existing gitThat owner is **Nephew**, with documented implementation and command names in:
- `marvelousempire/nephew/docs/runbooks/gitthat-that-app-studio.md`
- `marvelousempire/nephew/docs/runbooks/gitthat-pinned-proposals.md`
- `marvelousempire/ai-skills-library/docs/standards/gitthat-fleet-freshness.md`

GitThat is **read-only fetch into registered existing checkouts**. It does NOT clone missing repos, switch current branches, merge PRs, launch code, install packages or rewrite Gitea authority. A fetch receipt is NOT a deployment or local application test.

**Observed prerequisite:** The inspected Nephew GitHub mirror `data/fleet-repos.json` did **not** contain the literal `app-market-compass` at inspection time. Do not claim the scheduled fleet job already covers the target. Ask the agent to reconcile the canonical Gitea identity and registry, and inspect whether a matching local checkout exists. Do not invent a Gitea URL, checkout location or access token.

## Give this to the Mac agent (Bootstrap English order)

1. **RECEIVE:** Read this PR, this handoff, `docs/FIVEMAC-PREVIEW.md`, and the actual canonical Nephew gitThat runbook. Preserve all original Market Compass UI and server behavior, no exceptions.
2. **LOCATE:** Inspect `git status`, exact remotes, full repo identities and current branches for a matching Market Compass checkout in approved folders. Check the registered Gitea source before treating GitHub as authority. If there is no matching registered checkout, mark `no-local-checkout` rather than claiming gitThat fetched it.
3. **FETCH ONLY:** From an existing canonical Nephew checkout, the supported one-shot workflow is `make gitthat-fleet-plan HOURS=12`, then `make gitthat-fleet-fetch HOURS=12`, subject to actual status/configuration and existing authorization. Inspect `~/.nephew/run/claim-receipts/gitthat-fleet.rolling-12h.latest.json` and verify `fetch.ran`, `fetch.ok`, repository coverage, matching identities and changed ref hashes. This refresh might NOT include a GitHub-only PR branch or an unregistered repo.
4. **ACQUIRE PROPOSAL SEPARATELY IF NEEDED:** If the local target doesn't exist, the owner has authorized an **isolated preview**, not a change to canonical main. Clone the exact reviewed GitHub branch to `$HOME/MarketCompass-preview` ONLY if that directory does not exist, using the command below. If already present, inspect status, remotes and branch; do not overwrite local changes. Do not auto-apply GitHub onto Gitea. A proposed upstream import requires the documented pinned-proposal review and explicit authorization.
5. **VERIFY:** Require Python 3.11+, clean preview branch, full `make test`, Node and shell syntax checks from GitHub CI, and `scripts/demo_preflight.py`. Confirm initial `runAnalysis()` still runs, market controls remain reachable, seven schedules and five participant seats are visible, synthetic READYPLAY and computer profiles compute, incomplete evidence gets held, and exports remain hypothetical.
6. **SEE:** Launch the dedicated localhost preview and open the actual app. Do not expose the unauthenticated API on the public network. Retain the original `make app` launcher and all functionality. Collect a real Mac browser/UI observation and receipt, marking it unverified until the operator sees it.
7. **RECONCILE:** Gitea authoritative source, CCK That issued profile, Schema That signed/indexed schema, ELSE methods and READYPLAY consented measurements are distinct gates; don't equate a passing demo or GitHub CI with completing them. Publish an actual receipt/blocked state back to appropriate owner records after authorization; don't invent GitTalk ACK, Raven broadcast or merge.

## Two runnable paths

### Known registered local Nephew checkout: gitThat refresh (not app launch)

```bash
make gitthat-fleet-plan HOURS=12
make gitthat-fleet-fetch HOURS=12
```

Run these **inside the existing authorized Nephew checkout**. They may report no local Market Compass checkout or no registered target. Do not infer that a successful global fleet result pulled this branch. The receipt is the deciding evidence.

### Direct isolated development preview of this exact PR branch

```bash
git clone --single-branch --branch feat/intelthat-proof-health-bridge https://github.com/marvelousempire/app-market-compass.git "$HOME/MarketCompass-preview" && bash "$HOME/MarketCompass-preview/scripts/commission-demo.sh"
```

This one line creates a *separate* checkout, runs the complete tests and synthetic preflight, then opens the localhost browser preview. It DOES NOT represent the gitThat fleet refresh and DOES NOT merge the PR. A pre-existing destination stops rather than overwriting it.

For a clean **existing** preview checkout on the exact feature branch:
```bash
cd "$HOME/MarketCompass-preview" && git pull --ff-only && bash scripts/commission-demo.sh
```

## Receipt gates (must be independently verifiable)

- **GitThat freshness:** check exact `gitthat-fleet.rolling-12h.latest.json` data: owner identity, `fetch.ran`, `fetch.ok`, checkout and ref identity, missing copies. Don't infer success from a timer wake.
- **Source revision:** `git rev-parse HEAD` on the preview must match the pinned/reviewed PR branch tip recorded by the operator; do not hardcode an obsolete SHA in the command.
- **GitHub CI:** `test` and both Linux and hosted macOS jobs in `universal-measurement-preservation` must succeed on the actual current PR head SHA. The hosted macOS job uploads `market-compass-macos-hosted-rehearsal` with synthetic and HTTP receipts; do not mistake that runner for FiveMac. A prior successful run isn't a new revision's proof.
- **Synthetic output:** `runs/demo-preflight.json` generated on the receiving Mac with real digest/commit and `gitea_authority_verified=false`, `cck_certified=false`, `readyplay_connected=false`, `else_connected=false`. These flags are deliberate, not bugs to paper over.
- **Live HTTP receipt:** inspect the receiving Mac's `runs/runtime-inspection.json` after preview launch. Require `http_contract_verified=true`, the observed `source_commit` and server response fingerprints; a CI-produced receipt is not a receiving-Mac receipt. A `held` runtime gate does not disable the original app, and it is not commissioning.
- **User-visible app:** actual running browser; original auto-analysis and every existing control preserved; new selector, simulator, export available side by side. A localhost HTTP receipt does **not** establish visual rendering, live market-source availability, Mac identity or operator signoff. Record evidence, don't label a CI server screenshot as a FiveMac test.

## Explicitly forbidden silent changes

No deletion of any Market Compass capability; no restriction to financial or nonfinancial subjects; no disabling live market inputs, automatic market startup, RSI/MACD/moving averages, support/resistance, simulations, Nephew panel, or other existing features. No repo rename, unreviewed merge, forced push, reset, rebase, stash-pop, blind cherry-pick, Gitea overwrite or public API exposure. No permission widening, invented owner consent, automatic financial order, synthetic player promotion, or fabricated source evidence.

**Definition of ready:** The Mac can view the new additive experience through a clean isolated preview; the automatic market desk remains operational; CI and the synthetic preflight pass on the observed revision. **Definition of authoritative commission:** Additional owner-controlled Gitea/CCK/ELSE/READYPLAY gates and Mac runtime receipts actually complete.
