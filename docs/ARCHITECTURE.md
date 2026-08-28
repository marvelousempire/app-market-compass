# Market Compass Architecture

This document explains **how the current system is structured**, **why it is structured that way**, and **where future capabilities should plug in without turning the repository into a shrine to accidental complexity**.

---

# 1. Architecture goals

Market Compass is designed around six engineering goals.

## 1.1 Preserve every product idea as an addressable capability

The PRD defines 115 stable IP nodes. Each node should remain independently nameable, testable, callable, and versionable.

## 1.2 Minimize duplicate implementation

A node does not automatically deserve its own Python file. Related capabilities should share data preparation and algorithms when that reduces duplication without destroying testability.

## 1.3 Keep evidence inspectable

The system should make it possible to trace a final conclusion back through layer scores, metrics, input data, and eventually source provenance.

## 1.4 Treat disagreement as useful information

The system must not optimize merely for agreement. Trend can be bullish while news is bearish. Daily structure can improve while weekly structure remains weak. Those conflicts should reduce confidence rather than be averaged into oblivion.

## 1.5 Separate research confidence from predictive probability

Evidence direction, confidence, and calibrated probability are separate concepts and should remain separate in the contracts.

## 1.6 Keep provider and model replacement cheap

Data providers, forecast models, graph sources, and UI surfaces should be replaceable without rewriting core evidence contracts.

---

# 2. Current runtime flow

```text
AnalysisRequest
      |
      v
+-----------------------+
| data.py               |
| provider / CSV        |
| symbol resolution     |
| TLS trust             |
+-----------+-----------+
            |
            v
+-----------------------+
| technical.py          |
| normalized indicators |
| swing structure       |
| price memory          |
| Bus Stops             |
+-----------+-----------+
            |
            +-----------------------------+
            |                             |
            v                             v
+-----------------------+       +-----------------------+
| context.py            |       | forecast()            |
| foundation            |       | Ridge + baseline      |
| news                  |       | chronological CV      |
| historical analogs    |       +-----------+-----------+
| relationships         |                   |
| narratives            |                   |
+-----------+-----------+                   |
            |                               |
            +---------------+---------------+
                            |
                            v
                  +-----------------------+
                  | scoring.py            |
                  | dependence discounts  |
                  | confidence            |
                  | bull/bear evidence    |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | engine.py             |
                  | Report orchestration  |
                  +-----+------------+----+
                        |            |
                        v            v
                    registry.py    cli.py
                        |            |
                        v            v
                    node output   terminal
                        |
                        +------------------+
                                           |
                                           v
                                         api.py
                                           |
                                           v
                                      launcher.py
                                           |
                                           v
                                        browser
```

---

# 3. Current modules and responsibilities

## `data.py`

Responsibilities:

- retrieve live market/search data;
- load CSV input;
- normalize OHLCV columns;
- resolve requested symbol to provider symbol;
- preserve provider metadata;
- use an explicit trusted CA bundle for HTTPS.

What should not accumulate here:

- technical indicators;
- scoring rules;
- product decision logic;
- provider-specific business rules beyond acquisition/normalization.

Future direction:

Create a provider protocol/interface so Yahoo, licensed market feeds, news feeds, macro feeds, fundamentals, and crypto data can be swapped independently.

## `technical.py`

Responsibilities:

- enriched price frame;
- EMA calculations;
- RSI;
- MACD;
- stochastic;
- pivot/swing logic;
- Fibonacci structure;
- Price Memory;
- support/resistance;
- Bus Stop route construction.

Future direction:

As this module grows, split by **cohesive algorithm family**, not by one file per IP node. Likely future modules:

```text
technical/
  indicators.py
  swings.py
  fibonacci.py
  price_memory.py
  route.py
```

## `context.py`

Responsibilities today:

- asset/foundation context;
- news sentiment/event risk;
- historical analogs;
- Ridge forecast helper logic;
- relationship graph;
- narrative classification.

This is the module most likely to split as data depth increases.

Expected future structure:

```text
context/
  foundation.py
  news.py
  history.py
  relationships.py
  narrative.py
forecast/
  baseline.py
  statistical.py
  machine_learning.py
  calibration.py
```

## `scoring.py`

Responsibilities:

- consume layer outputs;
- apply confidence weighting;
- reduce correlated evidence weights;
- normalize the directional evidence split;
- derive action state.

This module is a high-trust boundary. It should remain transparent, testable, and resistant to hidden side effects.

## `engine.py`

Responsibilities:

- orchestrate a complete analysis;
- construct a report;
- keep layer execution consistent across CLI/API/UI;
- avoid embedding provider-specific or UI-specific logic.

The engine should eventually become dependency-aware and able to run independent layers concurrently, but v0.1 favors simplicity.

## `registry.py`

Responsibilities:

- preserve all 115 stable node IDs;
- route node requests to the relevant report/layer implementation;
- expose the product/IP surface independently of physical module structure.

Key rule:

> Stable node identity belongs in the registry and contracts, not in duplicated wrapper code.

## `models.py`

Responsibilities:

- typed result contracts;
- stable report structure;
- evidence-layer shape.

Future direction:

Add schema versions and explicit provenance models before external production API consumers depend on the contracts.

## `backtest.py`

Responsibilities:

- research validation using past-only information;
- basic outcome observation;
- simple fee assumption.

What it is not:

- a broker simulator;
- a limit-order-book simulator;
- proof of real-world profitability.

## `api.py`

Responsibilities:

- expose local analysis endpoints;
- serve the lightweight browser interface.

Future production API concerns not implemented yet:

- authentication;
- rate limiting;
- tenancy;
- async job execution;
- persistent runs;
- API version migration;
- observability.

## `launcher.py`

Responsibilities:

- start the local application server;
- wait for readiness;
- open the local browser automatically.

The launcher exists because `make app` should behave like an application, not hand the user a URL and wish them emotional strength.

---

# 4. Core data contracts

The architecture should continue converging around a small set of canonical contracts.

## 4.1 Analysis request

Conceptually:

```json
{
  "asset": "HYPE-USD",
  "as_of": "2026-08-28T14:00:00Z",
  "horizon": 20,
  "timeframes": ["1d"],
  "use_stochastic": false,
  "data_source": "live"
}
```

Future additions:

- asset class;
- portfolio context;
- multiple timeframes;
- manual Fibonacci anchors;
- requested data families;
- relationship depth;
- report detail level.

## 4.2 Layer result

Every evidence layer should expose:

```json
{
  "state": "bullish",
  "score": 0.25,
  "confidence": 0.68,
  "supporting_evidence": [],
  "opposing_evidence": [],
  "metrics": {},
  "missing_data": [],
  "explanation": "..."
}
```

The exact field names may evolve, but the conceptual requirements should not.

## 4.3 Final report

The report should keep distinct fields for:

- requested symbol;
- resolved/provider symbol;
- price/time metadata;
- layer outputs;
- bull evidence;
- bear evidence;
- confidence;
- action state;
- route/Bus Stops;
- explanations;
- missing data;
- eventual provenance.

---

# 5. Evidence aggregation philosophy

## 5.1 Scores are directional evidence, not probabilities

Layer scores are normalized evidence values.

The aggregate engine converts weighted net evidence into a two-sided split summing to 100.

## 5.2 Confidence modifies authority, not direction

A bullish layer with poor data quality should have less influence than a bullish layer with strong coverage and stable logic.

## 5.3 Correlated evidence is discounted

Examples:

- EMA direction, RSI, and MACD all derive from price history;
- narrative, relationship inference, and news sentiment may derive from the same headlines.

Without dependence discounts, one underlying fact could receive three or four votes.

## 5.4 Counter-evidence is mandatory

The final product should actively search for the strongest argument against the dominant view.

Future scoring work should make this even more explicit by storing paired contrast objects.

---

# 6. Trust boundaries

Some components produce more trustworthy claims than others. The UI and report should reflect that.

## Deterministic calculation

Examples:

- EMA;
- RSI;
- MACD;
- Fibonacci values;
- historical touch counts.

These are highly inspectable if the input data is correct.

## Statistical inference

Examples:

- Ridge forecast;
- historical analog similarity;
- estimated route outcomes.

These require validation and should expose sample/performance information.

## Text interpretation

Examples:

- news sentiment;
- narrative classification.

These depend heavily on source quality and model/rule limits.

## Relationship inference

Current co-mention graph edges are the lowest-trust relationship type and must remain labeled **inferred**.

Verified relationship data should be stored separately from inferred graph edges.

---

# 7. Provenance architecture target

A mature report should be able to answer:

- Which provider supplied this fact?
- When was it retrieved?
- What market timestamp does it describe?
- Which code/model version transformed it?
- Which node used it?
- Was the relationship verified or inferred?
- Was the source stale?
- Was the value later corrected?

Target conceptual structure:

```text
source data
  -> provider/version/timestamp
  -> normalized dataset hash
  -> feature calculation version
  -> node result
  -> evidence contribution
  -> final report
```

This lineage is not fully implemented in v0.1 and is a Phase 1 priority.

---

# 8. Data-provider architecture target

Instead of allowing direct provider calls throughout the codebase, future providers should satisfy common interfaces.

Conceptual example:

```python
class MarketDataProvider(Protocol):
    def bars(self, symbol, timeframe, start, end): ...
    def quote(self, symbol): ...

class NewsProvider(Protocol):
    def events(self, symbol, start, end): ...

class FundamentalsProvider(Protocol):
    def asset_profile(self, symbol): ...

class RelationshipProvider(Protocol):
    def edges(self, entity): ...
```

Benefits:

- easier failover;
- reproducible mocks/tests;
- provider comparison;
- licensing boundaries;
- cleaner caching.

---

# 9. Forecast architecture target

Current:

```text
features -> Ridge -> chronological CV -> compare with baseline -> allow/reject score influence
```

Future champion/challenger flow:

```text
                 +-> naive baseline
                 +-> statistical model
feature snapshot +-> boosting model
                 +-> Bayesian model
                 +-> optional advanced model
                         |
                         v
               walk-forward evaluation
                         |
                         v
                 calibration checks
                         |
                         v
              champion selection/gating
```

Promotion rule:

A model should gain production influence only when it improves at least one meaningful dimension without unacceptable regression elsewhere:

- forecast error;
- probability calibration;
- interval coverage;
- regime stability;
- interpretability;
- useful uncertainty estimates.

---

# 10. Relationship graph architecture target

The graph should ultimately contain multiple edge trust levels.

## Verified edge

Example:

```json
{
  "source": "filing-or-authoritative-dataset",
  "relationship": "supplies",
  "from": "COMPANY_A",
  "to": "COMPANY_B",
  "valid_from": "2026-01-01",
  "valid_to": null,
  "confidence": 0.95,
  "inferred": false
}
```

## Inferred edge

Example:

```json
{
  "source": "news-co-mention",
  "relationship": "co_mentioned",
  "from": "COMPANY_A",
  "to": "COMPANY_B",
  "confidence": 0.30,
  "inferred": true
}
```

The two edge families must never be visually or numerically interchangeable.

---

# 11. Historical testing architecture

No historical analysis may use information that would not have been known at the simulated decision time.

Required safeguards:

- as-of timestamp filtering;
- train-before-test chronology;
- feature transformations fit only on training history;
- outcome labels generated strictly after the decision bar;
- no future relationship/news metadata leaking backward;
- survivorship awareness for future cross-asset datasets.

The current Ridge path uses chronological splitting. Broader leakage audits remain future work.

---

# 12. Failure behavior

A trustworthy research application should fail loudly and specifically.

Desired rules:

- missing critical OHLCV -> fail the analysis;
- missing optional news -> continue with lower confidence;
- live provider SSL/network error -> explain provider failure and suggest CSV/fallback;
- failed forecast validation -> remove forecast influence, do not fail entire report;
- relationship graph unavailable -> mark layer missing/low-confidence;
- stale data -> label stale and reduce confidence;
- partial provider results -> preserve explicit missing fields.

The system should never quietly substitute invented data.

---

# 13. Testing strategy

## Unit tests

Validate deterministic functions and contracts.

## Golden tests

Needed next for technical calculations and known market snapshots.

## Property tests

Useful invariants:

- bull + bear = 100;
- confidence stays in `[0,1]`;
- support zone low <= high;
- historical test never reads future timestamps;
- adding duplicated correlated evidence cannot increase confidence without bound.

## Integration tests

Needed for:

- live provider success/failure;
- CSV equivalence;
- browser launch;
- API response contracts;
- provider fallback.

## Walk-forward research tests

Needed for model and signal evaluation by asset/horizon/regime.

---

# 14. When to split a module

Split a shared module when at least one of these becomes true:

- the module has more than one independent data dependency;
- testing one family requires mocking unrelated families;
- one capability has its own version/release cadence;
- the file becomes difficult to reason about;
- the capability needs independent caching/persistence;
- the node is likely to become a separately deployed service.

Do **not** split a module merely because the PRD assigns separate node IDs.

---

# 15. Production architecture not yet present

The current repo does not yet include:

- persistent database;
- Redis/cache service;
- job queue;
- cloud deployment manifests;
- authentication;
- user/workspace model;
- secrets manager integration;
- distributed tracing;
- metrics dashboard;
- model registry service;
- feature store;
- graph database;
- event streaming;
- broker/exchange service.

Those may become appropriate later. Adding them before the research contracts stabilize would mostly produce a beautifully distributed collection of uncertainties.

---

# 16. Architectural north star

The mature system should remain understandable as:

```text
DATA
  -> independent evidence nodes
  -> paired support/counter-evidence
  -> confidence and dependence adjustment
  -> route/risk/forecast synthesis
  -> plain explanation + technical audit trail
```

Everything else is implementation detail.
