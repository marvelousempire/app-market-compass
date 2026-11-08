# Market Compass Product Status

**Purpose:** separate what is implemented from what is partial, planned, or intentionally out of scope.

This document is the repository's expectation contract. If another document sounds more ambitious than this one, this document wins for current implementation status.

## Status labels

- **Implemented** — runnable code exists now and is part of the supported flow.
- **Partial** — runnable code exists, but its data depth, modeling sophistication, or coverage is limited.
- **Research** — implementation exists for evaluation, but it is not mature enough for production claims.
- **Planned** — defined in the product architecture/PRD but not implemented as a complete runtime capability.
- **Not in current scope** — intentionally excluded from the current release.

---

## Core product surfaces

| Capability | Status | What exists now | What is still expected |
| --- | --- | --- | --- |
| Browser app | Implemented | v0.8.1 no-build FastAPI workbench launched by `make app`. ACT v1 provides real navigation, a contextual right rail, System/Light/Dark appearance, report-bound Actors, 15 Exchange modules, 58 reviewed private bankTHAT evidence contracts, and a dedicated intelTHAT application. Friendly company-name search and the BB/AAPL/QQQ/SPCX defaults remain available. | Persistent server-side workspaces, richer verified graph/data, manual Fibonacci controls, authentication, and cross-model comparison. |
| CLI | Implemented | Analyze, node, registry, and backtest commands. | Batch jobs, richer export controls, job persistence. |
| FastAPI | Implemented | Health, analysis, symbol search, analyst provider/health/interpretation, node listing/output, browser surface, and research backtest endpoints. | Auth, server-side cloud approval, versioned production contracts, quotas, async jobs, persistence. |
| Decision gates + calculateTHAT | Research | The read-only `/api/decision-readiness` endpoint and ACT v1 surface generate active Go, Watch, Do Not Go and Invalidated research signals from asset reality, confidence, evidence edge, timeframe agreement, route, reward/risk and missing evidence. calculateTHAT shows its arithmetic and reads without mutating scores. | Bind versioned Actor preferences and refine signal calibration. Broker connectivity and execution are permanently outside Market Compass. |
| Imported research lenses | Research | The provenance-bound Day Trader lens refines daily setup detection and RSI 35/50/65 crossings into Brown/Wuda MicroSlices. Its API and UI declare no score influence, trading, credentials, or money movement. | Admit further sources through the same license, provenance, placement, refusal, test, and live-readback gates. |
| Native intelTHAT application | Research | `/intelthat/` is a dedicated ACT-matched app with Cockpit, Market Pack, Macro Conditions, News Intelligence, SEC Monitor, and browser-local Run History. It resolves company names, runs the Market Compass-owned v1 readers, restores saved receipts, and exposes formulas, inputs, freshness, timestamps, provenance, confidence, and export. The Market Compass panel is only its bridge. Donor execution/credential paths are rejected and score influence remains false. | Add licensed provider redundancy, server-side cache/jobs, and a scheduled macro calendar; authenticate only if the Door leaves its trusted private boundary. |
| Measurement Studio | Research | One ACT room exposes seven source-owner-neutral Hybrid CCK draft schedules and a transparent hypothetical 0–100 method-relative calculation. Results show inputs, formula, observation timeframe, timestamp, method/source provenance, unrated confidence, refusal holds, authority flags, and exportable input/receipt hashes. Brown's Barometers owns the measuring seat; Marvin's Metrics and donor marketing identity remain absent. | Real CCK/SchemaTHAT registration and witnesses, independently verified evidence, owner-issued methods, and automatic schedules remain outside this source projection. |
| CSV mode | Implemented | Reproducible OHLCV input independent of live provider. | Browser upload workflow, broader schemas and dataset manifests. |
| Live market data | Partial | Yahoo public search/chart endpoints with TLS trust bundle and symbol resolution. | Licensed provider(s), retries, caching, provider failover, SLA monitoring, intraday/multi-timeframe provider contract. |

---

## Evidence layers

| Layer | Status | Current implementation | Expected mature version |
| --- | --- | --- | --- |
| Foundation / asset reality | Partial | Quote metadata, trading history, liquidity evidence; now visible in the browser surface. | Company fundamentals, tokenomics, unlocks, protocol revenue, holder concentration, governance, security and operational risk. |
| Trend | Implemented | EMA 13/27/81, EMA 50 reference, directional structure and chart projection. | Multi-timeframe regime model and richer trend-strength diagnostics. |
| Momentum | Implemented | RSI 14, MACD, optional stochastic, reversal/continuation classification. | More formal divergence detection and calibration by asset/regime. |
| Fibonacci / Bus Stops | Implemented | Swing selection, Fib structure, last/next stops, downside stops, invalidation and reward/risk; route is visible in the browser. | Manual anchors, stronger multi-timeframe confluence and probabilistic route outcomes. |
| Price Memory | Implemented | Support/resistance test episodes, age, reactions, volume, recency, erosion; strongest levels are visible in the browser. | Volume profile, anchored VWAP, options/open-interest confluence, more robust clustering. |
| News / Human factor | Partial | Related headlines, lexical sentiment, event-risk keywords, freshness decay, price-reaction comparison; dedicated browser panel. | Licensed event feed, entity/event extraction, novelty, source tiers, scheduled macro calendar, better sentiment models. |
| Historical analogs | Research | Nearest historical states, future outcome filtering, counterexamples; analog metrics and dates are visible in the browser. | Regime-aware same/cross-asset analogs, richer similarity metrics, confidence/sample-quality calibration. |
| Relationship Intelligence | Partial | NetworkX graph from news co-mentions, inferred edges and multi-hop paths; interactive browser Evidence Board. | Verified supplier/customer/ownership/regulatory/technology edges with dated provenance and exposure weights. |
| Market narrative | Partial | Transparent keyword families, dominant narrative and basic stage; dedicated browser panel. | Topic clustering, attention velocity, richer narrative stages, crowding, counter-narratives, stronger text sources. |

---

## Forecasting and scoring

| Capability | Status | Current implementation | Expected mature version |
| --- | --- | --- | --- |
| Bull/bear evidence split | Implemented | Always normalized to 100 and now displayed with paired bull/bear evidence surfaces. | Continued calibration against realized outcomes without relabeling evidence as probability. |
| Confidence | Implemented | Separate from direction score and visible independently in the UI. | Richer decomposition by data quality, source coverage, calibration, regime stability. |
| Dependence discounts | Implemented | Discounts correlated price-derived and news-derived evidence families. | Data-driven dependence/correlation estimation by regime. |
| Ridge forecast | Research | Chronological TimeSeriesSplit; baseline gating; browser shows when model influence is withheld. | Champion/challenger model registry. |
| Statistical forecasting | Planned | Architecture only. | ARIMA/SARIMAX, state space, regime switching, GARCH-family volatility. |
| Gradient boosting | Planned | Architecture only. | XGBoost/LightGBM/CatBoost challengers after walk-forward validation. |
| Bayesian forecasting | Planned | Architecture only. | Explicit uncertainty and hierarchical models where justified. |
| Calibrated probabilities | Planned | Not shown today. | Brier/log-loss/reliability-tested probabilities for precisely defined events. |

---

## Research validation

| Capability | Status | Notes |
| --- | --- | --- |
| Unit tests | Implemented | Covers core calculations/contracts, browser application/static surface, and the six runtime controls with explicit no-trading and no-promotion boundaries. |
| Actor spaces | Implemented research projection | Omo, Prince, Wuda and Brown’s Barometers bind to the current report with individual psychology, comp cards, evidence rows, and exportable receipts. Wuda owns formula-bound RSI 35/50/65 notables; Brown owns consolidated metrics and instruments. | Persist user-edited psychology profiles; score, broker, approval, and execution authority remain absent by design. |
| ACT v1 shell and Market Exchange | Read-only working projection | The responsive ACT v1 shell provides grouped navigation, Appearance, Rail/Focus/Wide layouts and recovery, contextual right rail, footer quick launch, mobile tabs, and Menu. Market Exchange has six internal surfaces, 15 tools, an executable local intake-receipt workflow, and 58 reviewed private bankTHAT contracts. | Enable/save/install/SSO/API mutations remain with their owners; bank evidence stays private and read-only. |
| Runtime source authority | Commissioned on FiveMac | `ai.market-compass` binds Gitea authority, commissioned state and exact source revision at launch from `~/Developer/market-compass-live`. Development launch remains available; trading and score influence stay disabled in both states. |
| Canonical Gitea Actions CI | Implemented | Native authenticated checkout on the registered `macos-briefcase` runner; required tests run on pushes and pull requests. GitHub is a downstream mirror, not merge authority. |
| Chronological validation | Implemented for Ridge forecast | No random train/test split for the current forecast. |
| Research backtest | Research | Past-only signal observation with fee assumption; runnable from CLI and browser. |
| Full execution simulator | Planned | Needs spread, slippage, liquidity, funding/borrow, partial fills, gaps, venue behavior. |
| Regime performance reporting | Planned | Needed before stronger predictive claims. |
| Calibration monitoring | Planned | Needed before probabilities are exposed as probabilities. |
| Model drift monitoring | Planned | Needed for production. |

---

## Data and knowledge expectations

| Data family | Current state | Needed later |
| --- | --- | --- |
| OHLCV | Live public provider + CSV | Licensed provider, redundancy, intraday/multi-timeframe support. |
| News | Related public-provider news | Licensed source, source tiers, full text/event metadata where permitted. |
| Macro context | Research public-proxy lens | VIX, 10-year yield, UUP and TLT five-session changes with a disclosed context formula. | Scheduled Fed, inflation, employment, government and geopolitical event calendar. |
| Corporate fundamentals | Not implemented | Revenue, earnings, balance sheet, cash flow, share count, dilution, customers/suppliers. |
| Crypto fundamentals | Not implemented | Supply, unlocks, emissions, fees/revenue, staking, treasury, holder concentration, chain activity. |
| Verified relationship graph | Not implemented | Sourced dated edges: supplier, customer, owner, regulator, partner, technology dependency. |
| Options | Research aggregate context | Bounded public chain contract counts and put/call open-interest and volume ratios; no candidate, order, broker or execution authority. | Licensed chain, IV, Greeks, skew, term structure and event pricing with provider redundancy. |
| Social attention | Not implemented | Source-controlled attention/velocity signals with spam/bot handling. |

---

## Product workflow maturity

### Works now

A user can:

1. install the project in `.venv`;
2. run tests;
3. analyze a symbol through live market data or CSV;
4. receive trend, momentum, route, price memory, contextual, historical, graph, narrative, forecast, evidence, and explanation output;
5. run any of the 115 stable node IDs through the registry;
6. launch a rich local browser dashboard with `make app` and inspect the current analysis instead of a four-card demo;
7. inspect the full Bus Stop route, chart, support/resistance history, news risk, analogs, inferred relationship graph, narrative, opposing evidence, invalidation and data sources;
8. inspect all 115 node IDs from the browser and run a selected node against the current asset;
9. run the current research backtest from the browser or CLI;
10. type friendly symbols without provider suffixes and receive provider-aware suggestions;
11. ask the grounded offline analyst, or a configured Nephew/local/cloud model, for a schema-validated interpretation with a model receipt.
12. start on BB and choose BB, AAPL, QQQ, or SPCX without replacing an operator-edited watchlist;
13. open Omo, Prince, Wuda, or Brown's Barometers as an Actor space and inspect its comp card;
14. inspect Wuda trend/notable categories and Brown metrics, technical-analysis instruments, and view-governance categories;
15. refresh the native intelTHAT research workspace, inspect formula/input/provenance details, filter proof states, export its receipt, and separately read canonical owner-published receipts without enabling score influence or trading.
16. choose a Measurement Studio profile, load a fictional authorized example, run a held-or-calculated hypothetical study, inspect its complete calculation receipt, and export the result without persistence or owner writeback;
17. inspect the ACT v1 Market Exchange dashboard, catalog filters, product contracts and API/auth state without invoking owner mutations;
18. use the commissioned FiveMac door as a restartable loopback service and read its exact source receipt.

### Does not work yet

A user cannot yet:

- compare multiple model interpretations in a single consensus view;
- use the M5, DGX, or cloud lanes until their private endpoints/credentials are commissioned;
- set manual Fibonacci anchors from the browser;
- save a persistent portfolio, workspace, or report;
- reproduce a run from an immutable data/run manifest;
- receive scheduled alerts;
- connect a broker or place a trade, because both are permanently outside Market Compass;
- analyze an options strategy;
- rely on institutional-grade company/crypto fundamentals;
- rely on verified multi-company relationship paths;
- receive calibrated profit probabilities;
- treat the application as production investment infrastructure.

---

## Definition of v1

A credible **v1 research platform** should include:

- provider abstraction and caching;
- stronger asset identity and fundamental data;
- multi-timeframe analysis;
- persistent run manifests and source provenance;
- improved evidence-board relationships;
- richer news/event parsing;
- broader historical validation;
- saved analysis snapshots;
- documented model performance by asset class and regime;
- robust integration tests.

## Definition of production-ready research platform

Production readiness requires more than feature completion. It requires evidence that the software remains trustworthy under failure and change:

- licensed and versioned data sources;
- provider failover;
- reproducible data snapshots;
- monitoring and incident behavior;
- model/calibration drift monitoring;
- authentication and secrets management;
- deployment automation;
- secure API controls;
- data licensing review;
- stronger backtest/execution assumptions;
- operational logging and observability;
- explicit legal/regulatory review before any execution or personalized-advice features.

---

## Rule for documentation

When describing Market Compass publicly:

- call v0.5 a **runnable research workbench with a grounded, configurable AI interpretation bridge**;
- call current relationship edges **inferred** unless verified data is added;
- call the 56/44 output an **evidence split**, not a probability;
- call the current backtest a **research backtest**, not proof of profitability;
- distinguish PRD/planned nodes from runtime implementations;
- never describe a future data source as if it is already connected.
