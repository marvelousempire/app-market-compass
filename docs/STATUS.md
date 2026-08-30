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
| Browser app | Implemented | v0.5 no-build FastAPI workbench launched by `make app`. First screen follows the 8001 information sequence (header, identity, four summary cards) then the full trading desk: 4H/1D/1W analysis, watchlist/snapshots, catalysts, inferred Evidence Board, node inspector, backtest, friendly ticker search, and Nephew analyst panel. | Persistent workspaces, richer verified graph/data, manual Fibonacci controls, authentication, and cross-model comparison. |
| CLI | Implemented | Analyze, node, registry, and backtest commands. | Batch jobs, richer export controls, job persistence. |
| FastAPI | Implemented | Health, analysis, symbol search, analyst provider/health/interpretation, node listing/output, browser surface, and research backtest endpoints. | Auth, server-side cloud approval, versioned production contracts, quotas, async jobs, persistence. |
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
| Unit tests | Implemented | Covers core calculations/contracts plus browser application/static surface. |
| GitHub Actions CI | Implemented | Runs tests on pushes and pull requests. |
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
| Macro calendar | Not implemented | Fed, inflation, employment, government, geopolitical scheduled risk. |
| Corporate fundamentals | Not implemented | Revenue, earnings, balance sheet, cash flow, share count, dilution, customers/suppliers. |
| Crypto fundamentals | Not implemented | Supply, unlocks, emissions, fees/revenue, staking, treasury, holder concentration, chain activity. |
| Verified relationship graph | Not implemented | Sourced dated edges: supplier, customer, owner, regulator, partner, technology dependency. |
| Options | Not implemented | Chain, IV, Greeks, OI, skew, term structure, event pricing. |
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

### Does not work yet

A user cannot yet:

- compare multiple model interpretations in a single consensus view;
- use the M5, DGX, or cloud lanes until their private endpoints/credentials are commissioned;
- set manual Fibonacci anchors from the browser;
- save a persistent portfolio, workspace, or report;
- reproduce a run from an immutable data/run manifest;
- receive scheduled alerts;
- connect a broker;
- place a trade;
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
