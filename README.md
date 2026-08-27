# Market Compass

**Market Compass** is a node-based market decision-intelligence system for researching stocks, crypto, ETFs, and, later, options.

It is built around a simple idea: a market decision should never be based on one indicator, one headline, or one story. The system gathers evidence from several independent directions, measures the argument **for** and **against** a setup, explains both sides, and shows what would invalidate the current view.

> Market Compass is not a black-box buy/sell bot. It is an evidence engine.

## What it answers

For a selected asset and trading horizon, Market Compass is designed to answer:

- What is this asset, and is there enough real activity, utility, liquidity, or business substance to analyze it seriously?
- Is price trending up, down, sideways, or changing direction?
- Is momentum reversing, continuing, or merely bouncing?
- Where did price come from?
- What is the **last bus stop**, and what are the **next bus stops**?
- How strong is support below price?
- How strong is resistance above price?
- How many times has the market visited those areas, and over what span of time?
- What news directly affects the asset?
- What news may affect it indirectly through suppliers, customers, sectors, technologies, regulators, or related assets?
- What happened during similar setups in the past?
- What market narrative is currently attracting attention and money?
- What evidence supports the setup, what evidence contradicts it, and what would make the conclusion wrong?

## Product architecture

Market Compass has one foundation gate and eight primary evidence layers.

| Layer | Purpose |
| --- | --- |
| **Foundation Gate 0: Asset Reality & Quality** | Understand what the asset is, what gives it value, liquidity, supply or float, dilution, concentration, economic activity, and major operational risks. |
| **1. Trend** | Measure direction using EMA structure, slope, crossovers, regime, and multiple timeframes. |
| **2. Momentum & Reversal** | Use RSI, MACD, divergence, and optional stochastic signals to distinguish continuation, bounce, reversal, and overextension. |
| **3. Price Structure, Fibonacci & Bus Stops** | Find meaningful swings, Fibonacci levels, the last price stop, next destinations, confluence, and invalidation. |
| **4. Human Factor, News & Event Risk** | Measure headlines, event relevance, source quality, sentiment, novelty, scheduled risk, and actual market reaction. |
| **5. Historical Context & Analogs** | Find similar prior setups, measure what happened next, and deliberately surface counterexamples. |
| **6. Price Memory, Support & Resistance** | Measure how often price tested an area, over what period, how strongly it reacted, and whether repeated tests are strengthening or eroding the level. |
| **7. Relationship Intelligence** | Build the evidence-board graph: companies, protocols, suppliers, customers, sectors, technology, macro factors, regulators, and events connected by sourced relationships. |
| **8. Market Narrative** | Identify the story the market is trading and determine whether it is emerging, accelerating, crowded, fading, or reversing. |

## Founder-defined starting profile

The first swing-trading profile preserves the original product rules:

- **RSI:** 14 periods, with guides at 30, 50, and 70.
- **EMA:** 13, 27, and 81.
- **MACD:** a separate momentum and reversal signal.
- **Stochastic:** optional and disabled by default because duplicated momentum signals can add noise rather than insight.
- **Fibonacci:** supports automatic and manual anchors. For an upward swing, the default search is the meaningful low on the left to the meaningful high on the right; the direction reverses for a downward swing.
- **Trading horizon:** initial product focus is several days to several weeks.

## The Bus Stop model

Market Compass explains price structure like a route instead of pretending a chart is a collection of mystical colored lines.

- **Last bus stop:** the most recent meaningful price area that price left.
- **Current stop:** the present price area.
- **Next bus stop:** the nearest meaningful destination in the expected direction.
- **Later stops:** secondary targets.
- **Wrong road:** the invalidation condition or level.

Every stop must explain why it matters: historical tests, reaction size, volume, Fibonacci confluence, EMA confluence, prior highs/lows, break-and-retest behavior, and other evidence.

## Contrast is mandatory

Every analytic node must return both sides of the argument.

A bullish conclusion must include bearish evidence. A bearish conclusion must include bullish evidence. Missing data and invalidation conditions must also be explicit.

A two-sided evidence split always totals 100. For example:

```text
Bull evidence: 56
Bear evidence: 44
Confidence: Medium
```

The **56/44 split is evidence balance, not automatically a 56% probability of profit**. Probability may only be shown when a specific prediction target has been tested out of sample and calibrated.

## Explain Why

No score is valid without an explanation.

Every node returns:

- main conclusion;
- supporting evidence;
- opposing evidence;
- missing information;
- confidence;
- invalidation conditions;
- simple explanation;
- technical explanation;
- source and calculation provenance.

The default user-facing explanation targets roughly a fourth- to fifth-grade reading level. Engineers and advanced users can open the technical explanation to inspect parameters, formulas, timestamps, data sources, versions, calibration, and tests.

## Node-first engineering

Every distinct product idea is treated as an independent **IP node**. Each node is intended to become:

1. an independently testable Python module;
2. an independently executable Python microscript;
3. a stable input/output contract;
4. an API-capable component;
5. a separately versioned product capability.

A Python orchestrator owns dependency resolution, concurrency, retries, caching, partial results, manifests, and final aggregation. The `Makefile` is the developer-facing launch control, not the place where product logic goes to die.

Example intended launch surface:

```bash
make analyze ASSET=HYPE-USD HORIZON=2-6w PROFILE=swing_weeks_v1
make node NODE=L2-001 REQUEST=runs/<run-id>/request.json
make test
make backtest ASSET=HYPE-USD STRATEGY=swing_weeks_v1
```

## Technical direction

The planned Python stack includes:

- NumPy, SciPy, Polars, pandas, PyArrow, DuckDB, and Numba for numerical and analytical work;
- TA-Lib plus audited custom implementations for technical indicators and founder-specific logic;
- statsmodels, `arch`, and scikit-learn for statistical forecasting, volatility, pipelines, calibration, and validation;
- XGBoost, LightGBM, CatBoost, PyMC, and optional PyTorch models when advanced methods demonstrate measurable value;
- NetworkX for the initial evidence-board graph;
- spaCy, transformers, and sentence-transformers for entity linking, event classification, semantic similarity, and narrative analysis;
- SHAP for compatible model explanations, while keeping predictive explanations distinct from causal claims;
- vectorbt plus custom event-driven simulation for backtesting;
- Optuna and MLflow for controlled model tuning and experiment tracking;
- Pydantic, FastAPI, pytest, Hypothesis, Pandera, Ruff, and mypy for contracts, APIs, testing, and engineering quality.

Sophisticated tools are permitted. Unnecessary complexity is not. Every advanced model must beat a simpler baseline or provide materially better calibration, stability, or uncertainty estimates before it becomes the production champion.

## Repository documents

The canonical engineering specification is separate from this README:

- [`docs/PRODUCT-REQUIREMENTS.md`](docs/PRODUCT-REQUIREMENTS.md) — complete product requirements document and engineering specification.
- [`docs/IP-NODE-REGISTRY.md`](docs/IP-NODE-REGISTRY.md) — stable intellectual-property node catalog and proposed Python script mapping.

The README is the front door. The PRD is the law. The node registry is the construction inventory. Humanity has survived enough repositories where all three are one 4,000-line README.

## Current status

**Stage:** Product architecture and engineering specification.

The repository is being established from the product requirements outward. The initial implementation target is the Python microscript architecture, canonical data contracts, Makefile launch surface, deterministic technical-analysis nodes, contrast scoring, and an auditable end-to-end report.

## Important product boundary

Market Compass is decision-support software. It does not guarantee market outcomes, and the initial release does not place trades automatically. Evidence scores, historical analogs, forecasts, and narratives must remain transparent, testable, and explicitly uncertain.

## Canonical product statement

Market Compass asks what the asset is, what price is doing, where price has been, where it may go, what people are reacting to, what happened in similar cases, what companies and events are connected, and what story the market is trading.

Then it shows both sides.

It explains the route. It explains the risk. It explains why.

Every idea remains its own node, script, feature, and product.
