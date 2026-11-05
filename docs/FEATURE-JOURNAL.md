# Market Compass Feature Journal

This is the separate, chronological journal of founder direction, product interpretation, and the
reason important features changed. It complements the factual release log in
[`../CHANGELOG.md`](../CHANGELOG.md). It must not be replaced by short-lived chat history, a pull
request description, or an issue comment.

## Journal rules

Every material feature decision records:

- date and author/source;
- intention being protected or changed;
- affected feature names and IP nodes when known;
- what the user should see;
- what changed in code or documentation;
- validation evidence;
- unresolved work;
- GitTalk issue/PR/commit references.

Do not rewrite old entries to make the history look cleaner. Add a new entry that corrects or
supersedes the earlier interpretation.

---

## 2026-11-04 — Commission ACT v1 Market Exchange and its stable main door

**Founder direction:** Bring the Admin Market Exchange tools and bankTHAT contracts into Market Compass, present them through ACT v1, merge and commission the result, update the original and mirror, and keep the localhost main door on final main.

**Intention:** Make the actual read-only admin inventory usable from the research desk without copying owner engines, donor identity, credentials, trading authority or financial writes. Keep one canonical Gitea truth line and make the installed revision independently readable.

**User-visible requirement:** Market Compass starts on BB; includes Omo, Prince, Wuda and Brown’s Barometers; exposes ACT v1 Dashboard, Catalog, All Products, Installed, APIs & MCPs and API Observatory rooms; and keeps the 14 Exchange modules plus 58 bankTHAT candidates inspectable.

**Implementation:** Added working local search, filters, selection and General/UI/API/SSO/Install contract inspection; moved the surface to the ACT v1 Administrative Control Tower room pattern; installed `ai.market-compass` from `~/Developer/market-compass-live`; bound exact Gitea runtime receipts; routed Gitea Actions to the registered `macos-briefcase` runner; and kept GitHub as a downstream mirror.

**Evidence:** Gitea PRs #4, #5 and #6 merged through exact-head green checks. FiveMac passed 42 tests. The commissioned door returned HTTP health with 115 nodes and reported `commissioned:true`, `preview_only:false`, `research_only`, `trade_execution:false`, and `score_influence:false`. The localhost forward at `127.0.0.1:18003` read the same commissioned surface.

**Still open:** Owner-reviewed adapters and data contracts; real Actor psychology preferences; authenticated Exchange enable/save/install/API/SSO actions; bank persistence; broker integration; order execution and money movement. None is implied by this commissioning.

---

## 2026-11-03 — Commission the research desk around named Actors

**Founder direction:** Start on BB; provide Apple/AAPL, QQQ, and SPCX as starter choices; treat Omo, Prince, Wuda, and Brown as Actors with their own spaces and comp cards; put trading psychology in each Actor's space; consolidate market metrics and technical-analysis instruments under Brown's Barometers; put trends, hottest pointers, and notable RSI crossings under Wuda; remove Marvin; then merge and ship through the canonical forge.

**Intention:** Make the desk feel like an inspectable team of research Actors without inventing personal traits, market evidence, signal authority, or trading permission. Preserve the distinction between visible presentation categories and bound analytical sources.

**Features/IP nodes:** GitThat operator controls, intelTHAT Proof Health, Default Watch Choices, Actor Spaces, Actor Comp Card, Wuda Trends / Hottest Pointers / Notables, Brown's Barometers, Runtime Source Authority.

**User-visible requirement:** Market Compass opens on BB with BB/AAPL/QQQ/SPCX choices. Omo, Prince, Wuda, and Brown are selectable Actor spaces. Every Actor shows identity, role, individual trading-psychology configuration state, and authority. Wuda shows trend and RSI-threshold examples; Brown shows Breadth, Momentum, Volatility, Volume, RSI, MACD, moving averages, ATR, Bollinger Bands, and view-governance categories. Marvin is absent.

**Implementation:** Added the Actor rail and centered Stage, per-Actor comp cards, Wuda and Brown groupings, starter-list migration, read-only intelTHAT bridge, six safe runtime controls, canonical-source environment receipts, and a native Gitea Actions workflow. The November 4 entry records the later runner-label correction.

**Evidence:** Canonical Gitea PR #1 merged at `394ecdd0dd79e9c004448df5b567536ea898d281`; authority follow-up PR #2 merged at `29b2c263467bc7257e746872550f8b079486b2dd`; both exact-head checks passed; merged FiveMac suite passed 40 tests; live health returned HTTP 200 with 115 nodes; runtime reported canonical Gitea authority while trading and score influence remained disabled. Commissioning journal: `marvelousempire/nephew#540`.

**Still open:** Bind approved source data and owner receipts to Actor categories; define each Actor's psychology preferences and process rules; replace example threshold labels with versioned event calculations; retain broker connection and order execution as separately approved future work.

## 2026-08-30 — Dead desk after restyle (launcher opened the wrong door)

**Founder direction:** “not working - 2hrs and nothing”

**Intention:** The daily door is the running v0.5 desk. `make app` must open that desk, not spawn a second process on the next free port while the promised URL sits dead.

**Features protected:** Market Compass application launcher, live desk URL.

**User-visible requirement:** After a restyle is live, refreshing the desk URL still shows the current workbench. Running the app again reopens the same matching surface.

**Implementation:** `select_port` scans the whole port range for `application-v0.5` before binding a free port.

**Evidence:** Unit test `test_select_port_reuses_matching_surface_off_default_port`; live `GET /health` on 8006 returns `application-v0.5`.

**Still open:** Stale v0.3/v0.4 processes on 8000–8005 remain as leftovers from earlier days; they are skipped, not auto-killed.

## 2026-08-30 — Fold 8001 information logic into the current desk

**Founder direction:** “fold 8001's look into 8006. I love the way 8001 provides that logic of info.”

**Intention:** Keep the fuller product (Analyst, charts, watchlist, multi-timeframe) and recover the older page's first-screen sequence. Do not roll the daily app back to `application-v0.2`. After this restyle is live, stop the leftover 8001 process so the old page cannot reopen.

**Features protected:** Asset Reality, Market State, Evidence, Confidence, Trend, Momentum, Fibonacci, Reversal, Price Memory, Nephew Analyst, Trading Workbench, Historical Analogs, Evidence Board.

**User-visible requirement:** Opening the current application shows a large Market Compass header, identity, a single decision sentence, then the four summary cards, then the rest of the desk. The six-card cockpit must not sit above those cards.

**Implementation:** HTML/CSS/JS restyle on the v0.4 workbench; health surface `application-v0.5`.

**Evidence:** Regression tests pin the 8001 sequence IDs (`summary-grid`, `signal-grid`, `identity-strip`) and refuse leftover cockpit/overview IDs.

**Still open:** Real data-provider depth, persistent workspaces, private M5/DGX commissioning, server-side Approval Engine authorization, and cross-model comparison.

---

## 2026-08-29 — Preserve original intelligence features in every later projection

**Founder direction:** “We had v1 things I need in the latest app.”

**Intention:** A later workbench or AI release must grow upward from the existing product. It must
not erase the clear, named presentation of earlier intelligence features.

**Features protected:** Asset Reality, Market State, Evidence, Confidence, Trend, Momentum,
Fibonacci, Reversal, Price Memory, News/Event Risk, and Historical Analogs.

**User-visible requirement:** The latest application shows an Intelligence Overview containing
the original top-level cards, followed by the newer Nephew analyst, multi-timeframe analysis,
interactive workbench, and research surfaces.

**Implementation:** PR #6 restored the explicit overview cards and added a launcher version check.
An older Market Compass process can no longer be mistaken for the current application merely
because it occupies port 8000.

**Evidence:** 21 tests passed; GitHub Actions passed; merged head
`fcd94e4002dc203406c7ad8266a0be866c490aae`.

**Still open:** Real data-provider depth, persistent workspaces, private M5/DGX commissioning,
server-side Approval Engine authorization, and cross-model comparison.

---

## 2026-08-29 — Add AI as a grounded interpretation layer

**Founder direction:** Nephew and appropriate local models must provide real analysis, while the
user can deliberately ask capable cloud models such as GPT, Claude, Perplexity, and Grok.

**Intention:** Market Compass calculates the evidence; Nephew and other approved models interpret
the same immutable report. Models may explain, challenge, and identify gaps, but do not silently
rewrite scores.

**Implementation:** v0.4 introduced validated analyst contracts, model receipts, M5/MLX,
DGX/vLLM, Ollama, OpenAI, Anthropic, Perplexity, and xAI adapters, depth-aware routing, a
deterministic offline provider, and fail-closed cloud controls.

**Evidence:** PR #5; merged commit `1710b6611043a645a9ba788828ce7fb49fc28480`;
GitTalk commissioning issue #4.

**Still open:** Commission real endpoints and credentials, enforce App Approval Engine authority,
evaluate champion models, and add transparent cross-model comparison.

---

## 2026-08-29 — Remove provider syntax from ticker entry

**Founder direction:** A user should type the ticker they know and should not have to append
`-USD`.

**Intention:** Provider conventions belong in adapters, not in the user's mental workload.

**Implementation:** Friendly symbol input and suggestions preserve `HYPE` in the interface while
recording provider-resolved identifiers such as `HYPE-USD` in provenance.

**Evidence:** Symbol-resolution regression coverage shipped with PR #5.

---

## v0.3 — Promote the dashboard into a trading workbench

**Intention:** The browser is a primary product projection rather than an afterthought attached to
the engine.

**Features:** Decision Cockpit, charts and indicators, 4H/1D/1W alignment, watchlist, snapshots,
catalysts, Evidence Board, contribution analysis, Price Memory, Bus Stops, and research backtest.

**Evidence:** [`V0.3-WORKBENCH.md`](V0.3-WORKBENCH.md); base commit
`13d6bb793dcc303c83c21135f6e25faa16a777c5`.

---

## v0.1–v0.2 — Establish the evidence system and its visible report

**Intention:** Answer more than “is a technical indicator bullish?” by building a two-sided,
explainable evidence system around asset reality, structure, momentum, routes, memory, news,
history, relationships, narrative, forecasting, and invalidation.

**Product principle:** Each feature remains a named product/IP node. The evidence balance is not a
calibrated probability, history is not a guarantee, inferred links are not verified causation, and
the system actively searches for counter-evidence.

**Evidence:** [`PRODUCT-REQUIREMENTS.md`](PRODUCT-REQUIREMENTS.md),
[`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md), and the v0.1/v0.2 implementation history.

---

## Entry template

```markdown
## YYYY-MM-DD — Decision title

**Founder direction:** Exact statement or faithful summary.

**Intention:** Why this exists and which foundation rule it serves.

**Features/IP nodes:** Named features and stable IDs.

**User-visible requirement:** What a person must be able to see or do.

**Implementation:** What changed.

**Evidence:** Tests, PR, commit, screenshots, or run receipt.

**Still open:** Remaining work and named next owner.
```
