# Market Compass Roadmap

This roadmap describes the intended order of development. It is deliberately staged so the project earns complexity rather than collecting libraries as decorative trophies.

## Guiding rule

Each phase should make the system **more useful, more measurable, or more trustworthy**. A phase is not complete merely because code exists.

---

# Phase 0 — Runnable research core

**Status: substantially implemented in v0.1**

Goal: prove the core evidence architecture with a compact codebase.

Delivered or substantially delivered:

- local Python package and `.venv` setup;
- CLI;
- FastAPI;
- browser launcher;
- live OHLCV/news provider plus CSV fallback;
- EMA 13/27/81;
- RSI 14;
- MACD;
- optional stochastic;
- Fibonacci;
- Bus Stop routing;
- support/resistance Price Memory;
- basic news context;
- historical analogs and counterexamples;
- inferred relationship graph;
- basic narrative classification;
- Ridge forecast with chronological validation and baseline gating;
- evidence scoring, confidence, dependence discounts;
- 115-ID runtime registry;
- research backtest;
- unit tests and CI.

Exit criteria:

- full local analysis runs successfully on representative equity and crypto symbols;
- tests pass on supported Python versions;
- browser app opens reliably;
- outputs expose both supporting and opposing evidence;
- docs clearly identify the release as research software.

---

# Phase 1 — Data trust and reproducibility

**Status: next priority**

Goal: make every result reproducible and less dependent on one public provider.

Build:

- provider interface for market data;
- provider interface for news/events;
- local cache and retry policy;
- persisted analysis run manifest;
- source timestamp and provider version fields;
- normalized symbol/instrument identity layer;
- deterministic saved data snapshots for backtests;
- provider health checks;
- clearer error/fallback behavior;
- more integration tests around live-data failure.

Expected result:

A report can answer not only “what did the model say?” but also “exactly which data did it see, when, and from where?”

Exit criteria:

- a run can be reproduced from saved inputs;
- provider outage does not create ambiguous partial output;
- data freshness is visible in the report;
- CSV and live-provider runs share the same normalized contract.

---

# Phase 2 — Multi-timeframe technical intelligence

Goal: make technical evidence behave more like an experienced swing trader and less like a single daily chart.

Build:

- configurable 1h / 4h / 1d / 1w analysis;
- timeframe conflict detection;
- richer EMA slope/trend strength;
- formal divergence detection;
- improved pivot/swing ranking;
- multi-timeframe Fibonacci confluence;
- volume profile and/or volume-at-price;
- anchored VWAP;
- improved level clustering;
- gap and breakout/retest analysis;
- route probability research.

Expected result:

Market Compass can distinguish “daily chart is improving” from “weekly structure still says this is probably a bounce.”

Exit criteria:

- timeframe conflicts are visible and reduce confidence;
- route levels are stable across small changes in lookback;
- technical nodes have golden test datasets.

---

# Phase 3 — Asset reality and fundamental context

Goal: answer “is this asset real, healthy, liquid, and worth analyzing?” with data rather than generic metadata.

## Equities

Build:

- revenue and earnings trends;
- cash flow;
- balance-sheet health;
- share-count dilution;
- float and short interest;
- customer/supplier concentration where data permits;
- earnings/event calendar;
- sector and index exposures.

## Crypto

Build:

- circulating/total/max supply;
- unlock and emissions schedule;
- staking and token utility;
- protocol fee/revenue activity;
- treasury and major-holder concentration;
- exchange liquidity;
- chain activity;
- governance and security risk fields.

Expected result:

The engine can say “this is a functioning asset with real activity, but current dilution/unlock conditions make the trade setup less attractive.”

Exit criteria:

- asset-quality claims link to specific source fields;
- missing fundamental data lowers confidence;
- equity and crypto profiles use asset-specific contracts rather than one generic score.

---

# Phase 4 — Human factor and event intelligence

Goal: make news analysis about **impact**, not merely sentiment.

Build:

- licensed or more reliable news/event source;
- source reliability tiers;
- entity resolution;
- event taxonomy;
- scheduled macro/event calendar;
- novelty detection;
- directness and exposure scoring;
- expected-vs-observed market reaction;
- cross-asset event reaction;
- headline clustering/deduplication;
- explicit positive and negative impact paths.

Expected result:

A headline should be interpreted as:

> what happened → who is exposed → how direct the exposure is → whether the market confirmed the expected reaction.

Exit criteria:

- each event has provenance and timestamps;
- direct and indirect impact are separated;
- stale/duplicate headlines do not dominate scoring;
- scheduled risk is visible before an event.

---

# Phase 5 — Verified Evidence Board

Goal: evolve the relationship graph from inferred news co-mentions into a sourced market dependency graph.

Build verified edge families:

- supplier/customer;
- ownership/investment;
- competitor;
- partner/integration;
- technology dependency;
- index/ETF membership;
- regulator/jurisdiction;
- exchange/protocol relationship;
- commodity/macro exposure;
- institutional holder;
- derivative/underlying relationships.

Every edge should include:

- source;
- source date;
- valid-from / valid-to where known;
- confidence;
- direct vs inferred status;
- exposure magnitude where known.

Add:

- path-length decay;
- counter-paths;
- competing explanations;
- graph UI with source inspection;
- edge expiry/reverification.

Expected result:

The “crime-scene yarn board” becomes evidence-backed rather than merely suggestive.

Exit criteria:

- inferred and verified edges are visually and programmatically distinct;
- path scores can be decomposed;
- stale/expired relationships are suppressed.

---

# Phase 6 — Historical analog engine 2.0

Goal: turn historical context into a disciplined research system.

Build:

- same-asset and cross-asset analog pools;
- regime matching;
- volatility matching;
- shape similarity where useful;
- event-conditioned analogs;
- richer target outcomes;
- maximum favorable/adverse excursion;
- time-to-target / time-to-invalidation;
- sample-quality scoring;
- strongest counterexample retrieval;
- out-of-sample analog validation.

Expected result:

The system can say:

> “There are 27 comparable historical states; 17 reached the first upside stop before invalidation, but 6 strong counterexamples occurred during high-volatility risk-off regimes.”

Exit criteria:

- analog output always reports sample size;
- counterexamples are mandatory;
- future information cannot enter feature construction.

---

# Phase 7 — Forecast champion/challenger system

Goal: improve forecasting only where measurement proves value.

Candidate models:

- naive/drift baselines;
- exponential smoothing;
- ARIMA/SARIMAX;
- state-space models;
- Markov/regime switching;
- GARCH-family volatility;
- gradient boosting;
- XGBoost / LightGBM / CatBoost;
- Bayesian models;
- neural/transformer models only when justified;
- graph-informed models after the relationship graph is trustworthy.

Build infrastructure:

- walk-forward evaluation;
- tuning without leakage;
- champion/challenger registry;
- model versioning;
- calibration metrics;
- interval coverage;
- regime performance;
- promotion rules.

Expected result:

Advanced models are allowed to lose. If Ridge or a naive baseline wins, the system uses the simpler model.

Exit criteria:

- all production-weight models beat or materially complement baselines;
- probabilistic outputs are calibrated;
- performance is reported by regime and asset class.

---

# Phase 8 — Narrative and attention intelligence

Goal: measure what story the market is actually trading.

Build:

- semantic topic clustering;
- attention velocity;
- narrative stage detection;
- asset-to-narrative alignment;
- crowding/exhaustion signals;
- counter-narratives;
- price/volume confirmation;
- institutional vs retail attention where sourced reliably;
- narrative history.

Expected result:

The system distinguishes an emerging AI narrative from a crowded AI trade whose price stops reacting to positive news.

Exit criteria:

- narrative claims are supported by measurable attention inputs;
- narrative and news evidence are dependence-adjusted;
- speculative text is not silently promoted to fact.

---

# Phase 9 — Options intelligence

Goal: add derivatives as evidence and, later, strategy analysis.

Build:

- options chain normalization;
- implied volatility;
- Greeks;
- skew;
- term structure;
- open interest;
- unusual activity with robust baselines;
- expected move;
- event pricing;
- options-based support/resistance confluence.

Later:

- strategy payoff analysis;
- scenario analysis;
- liquidity/spread checks;
- assignment/exercise assumptions.

Exit criteria:

- options data quality is measured;
- spread/liquidity risk is visible;
- strategy outputs do not ignore execution reality.

---

# Phase 10 — Product platform

Goal: turn the local research app into a persistent product.

Build:

- accounts/authentication;
- saved watchlists;
- saved reports;
- analysis history;
- alerts;
- scheduled reports;
- portfolio context;
- persistent cache/database;
- cloud deployment;
- observability;
- usage controls;
- export/share workflows.

Exit criteria:

- users can reproduce prior reports;
- alerts preserve the exact evidence state that triggered them;
- production operations have monitoring and incident paths.

---

# Phase 11 — Execution, only after separate review

Goal: consider broker/exchange execution only after the research system is demonstrably reliable and the legal/security requirements are understood.

Before any execution feature:

- legal/regulatory review;
- broker/exchange integration review;
- secrets and credential architecture;
- order safety controls;
- position/risk limits;
- duplicate-order prevention;
- idempotency;
- audit logs;
- kill switch;
- reconciliation;
- paper trading;
- execution-quality validation.

Automated execution is deliberately last. A research engine should not get a brokerage account merely because somebody discovered an API endpoint.

---

# Priority order right now

The recommended near-term sequence is:

1. data trust and reproducibility;
2. multi-timeframe technical analysis;
3. stronger asset/fundamental data;
4. event/news intelligence;
5. verified relationship graph;
6. broader historical validation;
7. champion/challenger forecasting;
8. persistent product workflows;
9. options;
10. execution only after separate review.

That sequence preserves the central product idea: **better evidence before more automation**.
