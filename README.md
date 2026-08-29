# Market Compass

**Market Compass is an explainable market-research and decision-intelligence application.** It is designed to answer a harder question than “is RSI oversold?” or “did the news sound bullish?”:

> **Given the evidence available right now, what supports the bullish case, what supports the bearish case, where could price go next, and what would prove the current thesis wrong?**

The project combines technical analysis, price memory, historical analogs, news context, relationship intelligence, market narratives, forecasting, and explicit counter-evidence into one report.

It is intentionally **not** a black-box trading bot. It does not turn a 56/44 evidence split into a fake 56% chance of profit. Humans have already invented enough precise-looking numbers with questionable ancestry.

---

## Product status at a glance

**Current release:** trading workbench with grounded multi-model analyst bridge, `v0.4`
**Primary use case:** swing-trade research over days to several weeks  
**Current interfaces:** browser app, CLI, FastAPI, CSV input  
**Current default market-data source:** Yahoo public search/chart endpoints  
**Runtime model:** 115 stable IP node IDs routed through compact shared Python implementations  
**AI interpretation:** Nephew/local/cloud provider mesh with explicit privacy consent and model receipts
**Trading execution:** not implemented  
**Production-grade institutional data:** not implemented

The most important distinction in this repository is:

- **Implemented** means code exists and is runnable today.
- **Partial** means a real implementation exists, but its data or modeling depth is intentionally limited.
- **Planned** means the PRD defines the feature, but production code does not yet exist.

See [`docs/STATUS.md`](docs/STATUS.md) for the complete capability matrix.

---

# What Market Compass is trying to build

Most trading tools give users disconnected pieces: a chart, an RSI value, a headline feed, a support line, perhaps an AI-generated paragraph, and then leave the human to decide whether those pieces actually agree.

Market Compass is building an **evidence system** instead.

For any asset, the long-term product should answer seven practical questions:

1. **What is this asset?** Is there enough real activity, liquidity, utility, business substance, or market participation to analyze it seriously?
2. **What is price doing?** Is the market trending, ranging, reversing, continuing, or becoming overextended?
3. **Where has price reacted before?** How strong are support and resistance when measured across repeated tests and time?
4. **Where could price go next?** What are the last and next “Bus Stops,” and where is the route invalidated?
5. **What is happening around the asset?** Which headlines, economic events, sectors, suppliers, customers, technologies, regulators, or narratives matter?
6. **Has something like this happened before?** What happened after similar historical setups, including examples where the setup failed?
7. **What argues against the conclusion?** What is the strongest opposing evidence, and what information is missing?

The product is successful only when the answer is understandable enough for a normal person and inspectable enough for an engineer or quantitative researcher.

---

# The evidence model

Every analysis layer returns the same basic contract:

- a state;
- a directional score from `-1` to `+1`;
- confidence from `0` to `1`;
- supporting evidence;
- opposing evidence;
- relevant metrics;
- missing data;
- an explanation.

The aggregate engine applies confidence and dependence discounts before producing a two-sided evidence balance.

Example:

```text
Bull evidence: 56
Bear evidence: 44
Confidence: 61%
Action state: watch
```

### Evidence balance is not probability

`56 / 44` means the **current weighted evidence leans bullish**. It does **not** mean there is a statistically calibrated 56% probability of profit.

A true probability is only appropriate when:

- the target event is precisely defined;
- the model was evaluated out of sample;
- validation respected time order;
- probability calibration was measured;
- the calibration remains acceptable in the current regime.

That distinction is a core product rule, not legal decoration.

---

# What works today

The current `v0.4` implementation includes the following real, runnable capabilities.

## 0. Asset reality / quality gate

**Status: Partial**

The engine uses available quote metadata, trading history, and liquidity evidence to determine whether the instrument is analyzable.

Today this is strongest for market activity and liquidity. It does **not yet** have dedicated institutional-quality feeds for company fundamentals, crypto protocol revenue, token unlocks, holder concentration, or governance risk.

## 1. Trend

**Status: Implemented**

- EMA 13 / 27 / 81
- EMA 50 as an available reference
- EMA ordering and trend structure
- slope and direction signals
- trend state used in the evidence engine

The founder-defined default profile is preserved rather than replacing it with whichever moving average happens to be fashionable this quarter.

## 2. Momentum and reversal

**Status: Implemented**

- RSI 14
- RSI interpretation around 30 / 50 / 70
- standard MACD 12 / 26 / 9
- optional stochastic
- momentum confluence
- reversal-vs-continuation classification

A setup is allowed to improve without RSI first falling below 30. RSI is evidence, not a religious requirement.

## 3. Fibonacci and Bus Stop routing

**Status: Implemented**

The route layer finds meaningful swing structure and converts price levels into a route metaphor:

- **Last Bus Stop**: the meaningful area price recently left
- **Current Stop**: current price area
- **Next Bus Stop**: nearest meaningful destination
- **Later Stops**: secondary destinations
- **Wrong Road**: invalidation level

Bus Stops can combine historical price levels and Fibonacci structure.

## 4. Price Memory: support and resistance

**Status: Implemented**

Market Compass does not treat support as a single line somebody drew because the candle looked emotionally significant.

The current engine measures price levels using:

- independent test episodes;
- first seen / last seen;
- total historical span;
- reaction magnitude;
- volume near the level;
- recency;
- repeated-test erosion;
- overall level strength.

The same logic is applied symmetrically to **support and resistance**.

## 5. Human factor, headlines, and event risk

**Status: Partial**

The current implementation uses related news from the live provider and a transparent lexical model for:

- headline sentiment;
- event-risk keywords;
- freshness decay;
- comparison with observed price reaction.

This is real and useful, but it is intentionally modest. It is **not** yet a licensed institutional news pipeline with full entity/event extraction and verified causal exposure.

## 6. Historical context and analogs

**Status: Implemented research version**

The system creates comparable historical feature states and searches prior periods for similar setups.

It explicitly includes **counterexamples**. Historical analysis that only finds the five times a setup worked is just marketing wearing a lab coat.

Only historical rows with a known future outcome are eligible for evaluation.

## 7. Relationship Intelligence / Evidence Board

**Status: Partial**

The long-term product concept is an evidence board similar to an investigation wall: assets, companies, technologies, sectors, events, regulators, suppliers, and customers are nodes connected by sourced edges.

The current implementation builds a NetworkX graph from related-news co-mentions and can find multi-hop paths.

**Important:** current graph edges are marked as **inferred**. They are not proof of supplier, ownership, customer, regulatory, or causal relationships.

The architecture is ready for curated/verified relationship feeds later.

## 8. Market narrative

**Status: Partial**

The system currently recognizes transparent keyword-driven narrative families such as:

- AI / chips;
- rates / Federal Reserve;
- crypto adoption;
- regulation;
- geopolitics.

The eventual product should measure narrative emergence, acceleration, crowding, exhaustion, and counter-narratives using stronger text and attention data.

## Forecasting

**Status: Implemented research baseline**

The current forecast uses Ridge regression over lagged returns and market features with chronological `TimeSeriesSplit` validation.

A simple baseline is calculated too. If the model does not beat that baseline, its forecast is labeled `baseline_not_beaten` and **cannot influence the final evidence score**.

The long-term forecasting stack may include state-space, regime, volatility, boosting, Bayesian, and graph-informed models, but complexity must demonstrate out-of-sample value before it earns production weight.

---

# What is not built yet

The current repository should **not** be described as containing these capabilities yet:

- brokerage connectivity or automatic execution;
- position management for a real account;
- options-chain modeling;
- institutional real-time market data;
- a licensed premium news/event feed;
- verified supplier/customer/ownership knowledge graphs;
- comprehensive corporate fundamentals;
- comprehensive crypto tokenomics, unlock, treasury, protocol-revenue, governance, or holder-concentration feeds;
- calibrated profit probabilities;
- production model monitoring and drift management;
- persistent user accounts, saved portfolios, alerting, or cloud deployment;
- execution-quality simulation suitable for real-money claims.

Those are product directions, not hidden features.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the staged build plan.

---

# The 115 IP nodes and the compact codebase

The PRD identifies **115 stable product/IP nodes**. That does **not** mean the repository should contain 115 tiny Python files.

A node is a stable **addressable capability and contract**, not a requirement to create another wrapper file.

For example, the momentum family contains several node IDs, but they share one enriched price frame and common momentum implementation. This lets us preserve:

- node identity;
- version lineage;
- independent testing;
- API addressability;
- future product packaging;

without duplicating calculations and maintenance burden.

The live mapping is in [`src/market_compass/registry.py`](src/market_compass/registry.py). The conceptual inventory is in [`docs/IP-NODE-REGISTRY.md`](docs/IP-NODE-REGISTRY.md).

---

# Architecture

```text
                     Analysis Request
                           |
                           v
                 +-------------------+
                 | Market Data / CSV |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Technical Frame   |
                 | EMA RSI MACD etc. |
                 +---------+---------+
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
   Price Memory       Context Layer     Forecasting
   Fib + Bus Stops    News / History    Baseline gate
                      Graph / Narrative
          |                |                |
          +----------------+----------------+
                           |
                           v
                 +-------------------+
                 | Evidence Scoring  |
                 | + counter-evidence|
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Report / Node API |
                 +----+---------+----+
                      |         |
                     CLI      Web/API
```

Current source layout:

```text
src/market_compass/
├── data.py        # Yahoo/CSV acquisition, TLS trust, symbol resolution
├── technical.py   # EMA, RSI, MACD, stochastic, Fib, price memory, Bus Stops
├── context.py     # quality, news, historical analogs, forecast, graph, narrative
├── scoring.py     # contrast, dependence discounts, confidence, action state
├── engine.py      # end-to-end orchestration
├── registry.py    # all 115 stable node IDs
├── backtest.py    # chronological research backtest
├── api.py         # FastAPI + browser UI
├── launcher.py    # local server + automatic browser launch
├── cli.py         # analyze/node/registry/backtest commands
└── models.py      # typed report contracts
```

For deeper engineering expectations, see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

# Quick start

Python **3.11+** is required.

## Fresh clone

```bash
git clone https://github.com/marvelousempire/app-market-compass.git
cd app-market-compass
make setup
make test
```

`make setup` creates a local `.venv`, so the project does not need to pollute system Python like an overconfident shell script from 2009.

## Analyze HYPE

```bash
make analyze ASSET=HYPE HORIZON=20
```

## Launch the browser application

```bash
make app
```

`make app` starts the local server and attempts to open the default browser automatically.

Default address:

```text
http://127.0.0.1:8000
```

## Headless API mode

```bash
make api
```

## Run a specific node

```bash
.venv/bin/market-compass node L2-001 HYPE --horizon 20
```

## List all node IDs

```bash
.venv/bin/market-compass registry
```

## JSON report

```bash
.venv/bin/market-compass analyze HYPE --horizon 20 --json
```

---

# CSV mode

The analytic engine can run without the live provider.

CSV requires:

```text
date,open,high,low,close,volume
```

Example:

```bash
.venv/bin/market-compass analyze TEST --csv ./prices.csv --horizon 20
```

CSV mode is important for reproducible research and provider-independent testing.

---

# API

Current local endpoints include:

```text
GET /health
GET /api/analyze?symbol=HYPE&horizon=20
GET /api/nodes
GET /api/nodes/L2-001?symbol=HYPE&horizon=20
```

The API currently serves a local research application. Authentication, quotas, persistence, tenancy, and production deployment controls are future work.

---

# Backtesting expectations

```bash
make backtest ASSET=HYPE HORIZON=20
```

The current backtest is a **research validation tool**. It respects historical time order and includes a fee assumption, but it is not yet a complete broker/exchange execution simulator.

Before Market Compass makes stronger predictive or trading-performance claims, the project needs broader validation across:

- different assets;
- different market regimes;
- multiple horizons;
- transaction-cost assumptions;
- liquidity conditions;
- out-of-sample periods;
- probability calibration where applicable.

---

# Testing and quality

```bash
make test
```

CI runs pytest on pushes and pull requests.

Current test coverage includes:

- all 115 stable node IDs;
- RSI bounds;
- EMA 13 / 27 / 81 and MACD creation;
- 100-point bull/bear normalization;
- complete report-layer output;
- symmetric support/resistance fields;
- Fibonacci / Bus Stop routing;
- research backtest output;
- trusted TLS certificate context;
- browser auto-open behavior.

Passing tests mean the implemented contracts behave as expected. They do not establish profitable trading performance.

---

# Product principles

## 1. Show both sides

Every conclusion must expose supporting and opposing evidence.

## 2. Confidence is separate from direction

A 60/40 evidence split with low-quality data is not a strong signal.

## 3. Missing data stays missing

The engine should lower confidence rather than invent an answer.

## 4. History is context, not destiny

Historical analogs must show failures and sample quality.

## 5. Correlated indicators do not get multiple votes for free

EMA, RSI, MACD, stochastic, narrative, and news features may overlap. The scoring architecture includes dependence discounts.

## 6. Complexity has to earn rent

A complicated model must beat a simpler baseline or materially improve calibration, uncertainty, or stability before it gets production weight.

## 7. Inference is labeled as inference

A graph co-mention is not automatically a business relationship. Predictive association is not automatically causation.

## 8. Explain Why is part of the output contract

A score without an explanation is an incomplete product result.

---

# Definition of the product we are building toward

The mature Market Compass product should eventually behave like an **evidence operating system for market decisions**:

1. ingest high-quality market, company, protocol, news, event, macro, options, and relationship data;
2. evaluate each source through independent evidence nodes;
3. compare bullish and bearish explanations;
4. identify route targets, invalidation, volatility, and event risk;
5. retrieve historical analogs and counterexamples;
6. trace indirect news impact through verified relationship graphs;
7. measure active market narratives and crowding;
8. run validated forecast ensembles;
9. explain the result in plain language and technical detail;
10. monitor whether the system remains calibrated after deployment.

The product should become more sophisticated without becoming less inspectable.

---

# Documentation map

| Document | Purpose |
| --- | --- |
| [`README.md`](README.md) | Product front door: what Market Compass is, what works, and how to run it. |
| [`docs/STATUS.md`](docs/STATUS.md) | Truth table of implemented, partial, planned, and out-of-scope capabilities. |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Staged path from research v0.1 to a production research platform. |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Engineering architecture, contracts, trust boundaries, and extension seams. |
| [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md) | Details of the current compact v0.1 implementation. |
| [`docs/PRODUCT-REQUIREMENTS.md`](docs/PRODUCT-REQUIREMENTS.md) | Full long-term PRD. |
| [`docs/IP-NODE-REGISTRY.md`](docs/IP-NODE-REGISTRY.md) | Original 115-node conceptual/IP inventory. |

---

# What “production-ready” will mean

Market Compass should not call itself production-ready merely because a browser opens and pytest is cheerful.

Production readiness will require, at minimum:

- versioned and licensed production data providers;
- persistent source provenance and timestamps;
- resilient caching and provider failover;
- broader regression and integration testing;
- model evaluation by asset class and regime;
- probability calibration for probabilistic claims;
- drift and degradation monitoring;
- authentication and secure configuration;
- deployment and observability;
- data licensing review;
- documented incident/failure behavior;
- stronger backtesting and execution-cost modeling;
- explicit regulatory/legal review before automated execution or personalized recommendations.

Until then, this repository is best understood as a **working research platform with a larger product architecture behind it**.

---

# Disclaimer

Market Compass is research and decision-support software. It is not investment advice, does not guarantee outcomes, and does not place trades in the current release. Historical behavior may not repeat, market data may be incomplete, news can be wrong, and models can fail when regimes change.
