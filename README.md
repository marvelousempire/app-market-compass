# app-market-compass

The complete engineering PRD is finished. It is 56 pages and includes the full product architecture, 115 proposed IP nodes, Python microscripts, Makefile commands, scoring formulas, data contracts, repository structure, APIs, model-validation rules, test requirements, delivery phases, and a 41-point audit mapping the original conversation into the product.

Download the complete Market Compass PRD⁠￼

The technical stack was checked against current official documentation. The design uses TA-Lib for standard technical indicators, NetworkX for relationship graphs, statsmodels and scikit-learn for time-series and predictive modeling, vectorbt for backtesting, SHAP for model explanations, Polars/Arrow/DuckDB for analytical data processing, and Optuna with MLflow for tuning and experiment tracking. 

Market Compass PRD — Engineering Handoff

Status: Complete engineering draft
Version: 1.0
Date: August 27, 2026
Primary horizon: Swing trades lasting several days to several weeks
Architecture: One foundation gate, eight evidence layers, and shared decision engines
Proposed IP registry: 115 independently buildable nodes

Product Definition

Market Compass is a node-based market decision-intelligence system.

It answers two separate questions:

1. Is the asset real, active, useful, liquid, and worth analyzing?
2. Does the present evidence support buying, waiting, avoiding, holding, reducing risk, or exiting?

The product does not return only one conclusion. It presents the case supporting a trade, the case opposing the trade, the strength of each side, the confidence level, the next likely price destinations, and the conditions that would prove the setup wrong.

Core Architecture

The foundation gate evaluates asset reality and quality.

The eight evidence layers are:

1. Trend
2. Momentum and reversal
3. Fibonacci, price structure, and the bus-stop route
4. Human behavior, news, sentiment, and event risk
5. Historical context and analogs
6. Price memory, support, and resistance
7. Relationship intelligence and the crime-scene evidence board
8. Market narrative

Shared engines handle:

* Pairwise contrast
* Disconfirming evidence
* Evidence normalization
* Confidence calculation
* Correlation and duplicate-signal penalties
* Forecasting
* Volatility
* Risk and route analysis
* Plain-language explanations
* Technical explanations
* Backtesting
* Calibration
* Monitoring
* Provenance
* IP lineage

Founder Concepts Preserved

The PRD preserves the founder-defined RSI configuration of 14 periods with guides at 30, 50, and 70.

It preserves EMA periods of 13, 27, and 81.

MACD is included as a separate momentum signal.

Stochastic is optional and disabled by default because it may add noise or duplicate other momentum evidence.

Fibonacci analysis supports the founder’s upward-move method of selecting the meaningful low on the left and the meaningful high on the right. Downward-move anchoring reverses the direction.

The bus-stop route is a named product feature:

* The last bus stop is the meaningful price area price recently left.
* The current stop is the present price area.
* The next bus stop is the nearest meaningful price destination.
* Later stops are secondary targets.
* The wrong road is the invalidation level.

The price-memory engine records:

* When price first saw a level
* When price last saw it
* The number of independent test episodes
* The period covered
* Bounce or rejection size
* Reaction speed
* Volume near the level
* Multi-timeframe agreement
* Break-and-retest behavior
* False breaks
* Repeated-test erosion

Support and resistance are analyzed using the same framework.

The crime-scene evidence board maps companies, tokens, protocols, suppliers, customers, technologies, regulators, sectors, macro factors, events, and narratives. Each relationship is represented as an evidence-backed edge. The system traces how a headline may move through several connected entities before affecting the selected asset.

Mandatory Contrast Rule

Every node must produce both sides of its conclusion.

A node returning bullish evidence must also return bearish evidence.

A node returning bearish evidence must also return bullish evidence.

Each result must contain:

* Supporting evidence
* Opposing evidence
* Missing information
* Assumptions
* Data freshness
* Confidence
* Invalidation conditions
* Plain-language explanation
* Technical explanation
* Source provenance

A two-sided evidence score must total 100.

A score of 56 on one side therefore produces 44 on the other side.

The score is called an evidence split unless the underlying predictive model has been tested and calibrated as a probability model.

Python Microscript Requirement

Every intellectual-property node is designed as an independently executable Python microscript.

Each script must:

1. Accept a validated request.
2. Load only the data it needs.
3. Perform one bounded analytic action.
4. Return a standard NodeResult.
5. Show both the main case and the counter-case.
6. Record its version and provenance.
7. Save its output inside a run directory.
8. Fail visibly rather than invent missing data.

The Makefile acts as launch control. Python retains all decision logic, orchestration, dependency management, retries, concurrency, caching, and manifest creation.

The primary launch command is specified as:

make analyze ASSET=HYPE-USD HORIZON=2-6w PROFILE=swing_weeks_v1

Individual nodes and layers can also be executed separately.

Evidence Scoring

Each evidence item is weighted using:

* Direction
* Strength
* Relevance
* Source reliability
* Freshness
* Rule or model reliability
* Data quality
* Independence from other signals

The scoring engine reduces the weight of correlated signals. RSI, MACD, stochastic, and moving averages cannot be counted as fully independent proof merely because all point in the same direction.

Confidence remains separate from the evidence split. Confidence reflects:

* Data coverage
* Data quality
* Source reliability
* Feature agreement
* Historical sample size
* Model calibration
* Freshness
* Regime stability

Forecasting Standard

The model ladder begins with simple baselines. More sophisticated models must beat those baselines during time-respecting out-of-sample tests.

The PRD specifies:

* Naive and drift baselines
* Exponential smoothing
* Regularized lagged-feature models
* ARIMA and SARIMAX
* State-space models
* Regime-switching models
* GARCH-family volatility models
* Gradient boosting
* XGBoost
* LightGBM
* CatBoost
* Bayesian models
* Optional neural and graph-informed models

Forecast targets include:

* Reversal probability
* Continuation probability
* Probability of reaching the next upside stop before invalidation
* Probability of reaching the next downside stop first
* Expected price range
* Expected time to the next stop
* Volatility
* Maximum favorable excursion
* Maximum adverse excursion

A model may display probability only after out-of-sample testing and probability calibration.

Engineering Deliverables Included

The full PRD includes:

* Product vision
* Problem statement
* Goals and non-goals
* User profiles and use cases
* One foundation gate
* Eight complete evidence-layer specifications
* Pairwise contrast engine
* Disconfirming-evidence engine
* Evidence and confidence formulas
* Forecasting architecture
* Risk and route engine
* Explanation requirements
* JSON data contracts
* Python repository tree
* Makefile specification
* 115-node IP registry
* 50 functional requirements
* User-interface requirements
* API endpoints
* Data and storage architecture
* Recommended Python stack
* Backtesting and calibration requirements
* Unit, contract, golden, property-based, leakage, integration, and performance tests
* Non-functional requirements
* Product and model metrics
* Risks and mitigations
* Delivery roadmap
* Version 1 definition of done
* A complete conversation-to-IP audit

Final Product Standard

Market Compass is not designed as another chart covered in indicators.

It is designed as a transparent market evidence engine.

It asks what the asset is, what price is doing, where price has been, where price may go, what people are reacting to, what occurred in similar cases, what companies and events are connected, and what story the market is trading.

It then shows both sides.

It explains the route.

It explains the risk.

It explains why.

Every idea remains its own node, script, feature, and product.
