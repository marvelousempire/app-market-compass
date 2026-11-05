# Market Compass Change Log

This is the factual, chronological log of shipped repository changes. Product reasoning and
founder direction are recorded separately in [`docs/FEATURE-JOURNAL.md`](docs/FEATURE-JOURNAL.md).

## Unreleased

- Added the first provenance-bound imported research lens from `marvelousempire/day-trader-skill` at immutable revision `3d0f4ef6986f4984b7c6bd46f7ff4f87744c3abd`. Five daily setup detectors and RSI 35/50/65 crossings are isolated Brown/Wuda MicroSlices with a read-only API and ACT panel. Intraday claims are held without intraday bars; broker, order, credential, account, and money-movement paths are rejected.

- Added a contextual right-rail submenu for every primary room. Items navigate to real in-page sections or invoke existing Actor, Market Exchange, and calculateTHAT controls without creating new execution authority. The shell assets now carry a revision binding so commissioned browsers receive the matching submenu behavior and presentation together.

- Removed remaining dark-only color ownership from Market Exchange, Runtime Controls, Actor cassettes, intelTHAT and Nephew Analyst source styles. Dashboard metrics, filter buttons, product cards and inspectors now consume the ACT semantic palette directly instead of depending on lower-specificity repair overrides.

- Completed a full-app ACT appearance census after a second client-demo contrast report. Repaired Current Route, active timeframe, neutral badge, gate-state, calibration, timeline, provider-consent and System-dark conflicts through the shared semantic appearance layer rather than isolated paint patches.

- Repaired the client-demo Market Exchange contract tabs: Light mode now uses one readable segmented control with an unmistakable selected state, keyboard focus and ARIA selection. Also corrected the washed-out live price and replaced execution-suggestive shell language with Compass Desk and Signals active.

- Repaired ACT v1 appearance inheritance so Light mode no longer contains hard-coded dark workbench islands. Operator controls, Actors, Market Exchange, intelTHAT, analysis cards, Evidence Board and charts now follow the selected Light, Dark or System palette.

- Corrected the permanent product boundary: Market Compass generates active research signals but will never connect to a broker, place trades, manage real-money positions or move money.
- Replaced approval-blocked readiness states with active `GO_SIGNAL`, `WATCH_SIGNAL` and `DO_NOT_GO_SIGNAL` outputs. calculateTHAT reads the existing evidence score without mutating it.

- Added a design-first, micro-sliced readiness contract for triggers, hard stops, Actor psychology, approval and execution boundaries.
- Added calculateTHAT as a transparent research instrument and `/api/decision-readiness` as a read-only explanation endpoint.
- Added an ACT v1 Decision Gates surface. Trading and score influence remain off; approval remains externally owned.

- Completed the READYPLAY ACT v1 receiving shell after the founder identified the first implementation as partial: added grouped collapsible navigation, Appearance, Rail/Focus/Wide modes and recovery, supporting right rail, footer quick launch, mobile tabs, Menu search, compact rail persistence and real-section bindings.
- Removed the invented one-rail approximation as the completion boundary. Market Compass keeps its own identity, data and read-only authority while adopting the pinned READYPLAY shell anatomy.

- Replaced the label-only ACT v1 treatment with a genuine full-page administrative shell: persistent room navigation, calm light workspace materials, responsive compact/mobile rails, active-room readback and direct links to real Market Compass sections.
- Preserved Market Compass identity, analysis behavior, operator controls and the research-only/trading-off boundary; no READYPLAY data, identity or engine authority was imported.

- Reconciled the handoff, status, implementation, troubleshooting, feature journal and README with the commissioned ACT v1 FiveMac runtime, registered `macos-briefcase` CI lane, canonical Gitea authority and downstream GitHub mirror.
- Presented the Market Exchange through the ACT v1 Administrative Control Tower room pattern while preserving its working read-only search, filters, product inspector, 14 exchange modules and 58 Bank Reader candidate roles across seven bankTHAT consoles.
- Kept every imported module read-only and owner-bound. No exchange or Bank Reader engine, credential, account payload, persistence, score influence, trading or money-movement authority is copied into Market Compass. The legacy Ledger empty-state auto-generate POST is explicitly held outside the projection.
- Advanced the application contract to 0.6.0.
- Runtime receipts now read the configured bind address instead of falsely reporting port 8000 for separately bound review previews.
- The Exchange projection now carries working read-only admin tools: dashboard totals, catalog search and filters, product state/metadata/auth cards, and General/UI/API/SSO/Install contract panels. Mutating enable, save, install and SSO/API actions remain owner-gated stubs.
- Pack #2 — Relative Strength Desk + Market Tape. Seven stdlib micro-slices under `slices/pack-002/`. Scoring weights and the 8001 evidence sequence stay untouched. Offline fixture only. Live Yahoo feed is a later engine load.
- Canonical Gitea release — merged PRs #1 and #2 at `394ecdd` and `29b2c26`; repaired the repository's Gitea Actions lane and commissioned the FiveMac research runtime from exact canonical source.
- Added read-only intelTHAT proof health with explicit missing/held/excluded evidence and no score or trading influence.
- Added safe GitThat runtime controls for plan, status, launch, open, receipts, and stop.
- Changed the untouched starter watch choices to BB, AAPL, QQQ, and SPCX while preserving operator-edited lists.
- Added FlowThat-shaped Actor spaces and comp cards for Omo, Prince, Wuda, and Brown's Barometers. Wuda owns trends and notable RSI thresholds; Brown owns metrics, technical-analysis instruments, and view governance. Removed Marvin's Metrics and consolidated its metrics under Brown.
- Bound commissioned runtime authority and exact source revision through environment receipts while keeping `research_only`, `trade_execution=false`, and `score_influence=false` invariant.

## [0.5.1] — Sunday, August 30, 2026 at 5:34:50 PM Eastern · *Reuse the live desk instead of starting a second one*
**Signed:** Grok > grok-4.6

- Launcher now reuses any matching `application-v0.5` process in the port scan, not only port 8000.
- This stops `make app` from opening a new empty door (8001) while the working desk on 8006 is already running — which left the promised URL dead.

## [0.5.0] — Sunday, August 30, 2026 at 2:33:48 PM Eastern · *Fold 8001 information sequence into the workbench*
**Signed:** Grok > grok-4.6

- Restyled the live desk so the first screen follows the 8001 information sequence: large header, identity strip, decision sentence, then Asset Reality / Market State / Evidence / Confidence, then Trend / Momentum / Fibonacci / Reversal.
- Kept the v0.4 tools: Nephew Analyst, 4H/1D/1W, Price Memory, charts, contributions, catalysts, and research surfaces.
- Replaced the six-card cockpit with one action line so Evidence and Confidence are not shown twice.
- Advanced the health surface to `application-v0.5` so the launcher will not reopen an older process as current.


## 2026-08-29 — Intelligence overview preservation

- Restored explicit Asset Reality, Market State, Evidence, Confidence, Trend, Momentum,
  Fibonacci, and Reversal cards in the latest workbench.
- Preserved Price Memory, News/Catalysts, Historical Analogs, multi-timeframe analysis, Evidence
  Board, research tools, and Nephew Analyst.
- Prevented the launcher from reopening an older Market Compass version on port 8000.
- Added regression coverage for the preserved projection and stale-version rejection.
- Merged through PR #6 at `fcd94e4002dc203406c83c21135f6e25faa16a777c5`.

## v0.4 — Nephew multi-model analyst bridge

- Added grounded analyst request/response contracts and report-bound model receipts.
- Added local M5/MLX, DGX/vLLM, and Ollama routes.
- Added configurable OpenAI, Anthropic, Perplexity, and xAI adapters.
- Added fail-closed cloud permission plus per-request consent.
- Added friendly ticker entry and provider symbol resolution.
- Added the Nephew analyst workbench panel and offline deterministic provider.
- Merged through PR #5 at `1710b6611043a645a9ba788828ce7fb49fc28480`.

## v0.3 — Trading workbench

- Shipped the interactive decision cockpit, charts, indicators, multi-timeframe analysis,
  watchlist, snapshots, catalysts, Price Memory, Evidence Board, historical context, node inspector,
  and research backtest.
- Shipped at `13d6bb793dcc303c83c21135f6e25faa16a777c5`.

## v0.1–v0.2 — Evidence engine and report surface

- Established the canonical evidence-layer contract, two-sided scoring, confidence separation,
  Bus Stop routes, Price Memory, news/human context, historical analogs and counterexamples,
  relationship intelligence, narrative, forecasting gate, API, CLI, and browser report.
