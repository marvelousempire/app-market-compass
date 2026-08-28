# Market Compass v0.1 Implementation

This document describes **the code that exists now**.

For the other views of the product:

- [`STATUS.md`](STATUS.md) is the truth table for what is implemented, partial, research, planned, or out of current scope.
- [`ROADMAP.md`](ROADMAP.md) defines the intended build sequence.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) explains engineering boundaries, contracts, trust levels, and future extension seams.
- [`PRODUCT-REQUIREMENTS.md`](PRODUCT-REQUIREMENTS.md) describes the larger long-term product.
- [`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md) preserves the 115-node conceptual/IP inventory.

If the PRD sounds broader than this document, that is expected. The PRD is the destination; this document is the currently running vehicle, including the mildly concerning noises from under the hood that we actually know about.

## Design decision: stable nodes, shared code

The product preserves 115 stable IP node IDs. The implementation does **not** create 115 Python wrapper files. Related nodes route to shared modules through `registry.py`. This preserves addressability and product lineage while minimizing duplicated code.

The rule is:

> Node identity is a contract. File count is not intellectual property.

A node can later become its own module or service if its data dependencies, testing needs, release cadence, caching, or operational complexity justify the split.

## Runtime flow

```text
request
  |
  v
data.py -> normalized OHLCV + quote metadata + news
  |
  v
technical.py -> EMA / RSI / MACD / stochastic / Fib / price memory / route
  |
  +--> context.py -> quality / news / historical analogs / forecast / graph / narrative
  |
  v
scoring.py -> confidence + dependence discounts + bull/bear split
  |
  v
engine.py -> Report
  |
  +--> cli.py
  +--> api.py -> FastAPI + browser UI
  +--> registry.py -> node-addressable outputs
  +--> launcher.py -> local server + automatic browser open
```

## Local environment

Python 3.11+ is required.

`make setup` creates `.venv` and installs the project in editable mode. Make targets automatically prefer `.venv/bin/python` when the environment exists.

```bash
make setup
make test
```

The local setup intentionally avoids depending on a global `python` executable because modern macOS installations commonly expose `python3` instead.

## Data

The default provider uses Yahoo's public search and chart endpoints through the Python standard library. The search step resolves symbols before requesting chart data because some Yahoo crypto symbols include internal numeric suffixes.

HTTPS requests use a `certifi` CA bundle rather than depending solely on the Python.org macOS certificate store. This addresses a common `CERTIFICATE_VERIFY_FAILED` failure mode on local Python installations.

CSV is a fully supported input path and requires:

```text
date,open,high,low,close,volume
```

### Current data limits

The public provider is sufficient for a runnable research application. It is **not** an institutional production data architecture.

The current implementation does not yet provide dedicated feeds for:

- corporate fundamentals;
- crypto supply/unlocks/protocol revenue;
- options chains;
- verified supplier/customer relationships;
- scheduled macro events;
- institutional news/event metadata.

Those omissions are represented as missing/limited evidence, not silently invented values.

## Technical layer

The initial deterministic profile uses:

- EMA 13, 27, 81;
- EMA 50 as a reference;
- RSI 14 with 30 / 50 / 70 interpretation;
- standard MACD 12 / 26 / 9;
- optional stochastic.

Price memory clusters local pivot candidates, then measures independent nearby test episodes. Each level records test count, first/last seen, time span, average reaction, volume ratio, recency, repeated-test erosion, and overall strength.

Fibonacci automatically decides whether the dominant lookback swing is low-to-high or high-to-low based on timestamp order. Bus Stops combine historical levels and Fibonacci levels around current price.

### What technical analysis does not claim

A deterministic indicator calculation can be correct while the trading conclusion is wrong. Technical nodes are evidence inputs, not guarantees.

## Context layer

### News

News uses a small transparent lexical model rather than hiding the output behind an opaque language model. It adds freshness decay, event-risk detection, and comparison with actual latest price reaction.

This is a **partial human-factor implementation**. It is not yet full entity/event intelligence.

### Historical analogs

Historical analogs use standardized current features and nearest neighbors. Only historical rows with a complete future outcome are eligible. Counterexamples are returned explicitly.

This is a research mechanism. Similarity is context, not proof that history will repeat.

### Forecast

The forecast uses Ridge regression with chronological `TimeSeriesSplit`. A simple historical-mean target forecast is the baseline. A forecast that fails to beat the baseline receives `baseline_not_beaten` and cannot change the final evidence score.

This is intentionally a baseline-gated research forecast, not a claim that Ridge is the final Market Compass prediction engine.

### Relationship intelligence

Relationship intelligence uses NetworkX. Current edges are derived from co-mentions in related news, are marked inferred, and can form multi-hop paths.

They are **not causal or verified business relationships**.

The future graph is expected to add sourced, dated, verified edge families such as supplier, customer, ownership, regulation, partnership, technology dependency, index membership, and macro exposure.

### Narrative

Narrative classification uses transparent keyword families. It is deliberately modest until a stronger text/attention data source exists.

## Scoring

Layer scores run from `-1` to `+1`. Confidence is separate.

The aggregator reduces momentum weight when momentum agrees with trend because both come from price. It also discounts relationship/narrative outputs because they are currently derived from the same news source.

The normalized two-sided split always sums to 100.

Example:

```text
Bull evidence: 56
Bear evidence: 44
Confidence: 61%
```

The 56/44 result is an **evidence balance**, not a 56% probability of profit.

## Surfaces

### Full report

```bash
.venv/bin/market-compass analyze HYPE-USD --horizon 20
```

### Node output

```bash
.venv/bin/market-compass node L2-001 HYPE-USD --horizon 20
```

### Registry

```bash
.venv/bin/market-compass registry
```

### Research backtest

```bash
.venv/bin/market-compass backtest HYPE-USD --horizon 20
```

### Browser app

```bash
make app
```

`make app` runs `launcher.py`, waits for the local server, and attempts to open the default browser automatically at `http://127.0.0.1:8000`.

### Headless API

```bash
make api
```

`make api` starts Uvicorn without the browser-launch behavior.

## Tests

The test suite currently covers core contracts such as:

- all 115 stable node IDs;
- RSI bounds;
- EMA/MACD feature creation;
- bull/bear normalization;
- complete report layers;
- Price Memory support/resistance shape;
- Bus Stop/Fibonacci output;
- research backtest output;
- SSL trust context;
- browser auto-open behavior.

GitHub Actions runs tests on pushes and pull requests.

Passing tests establish that the implemented code satisfies its current software contracts. Passing tests do **not** establish trading profitability or predictive calibration.

## Extension seams

The compact architecture is designed so later work can replace or extend one surface without rewriting the product:

- replace Yahoo with licensed market/news providers behind a provider interface;
- persist normalized input snapshots and run manifests;
- add verified company/protocol edges to the graph;
- add multi-timeframe technical analysis;
- add corporate and crypto fundamental providers;
- add statsmodels/GARCH/boosting challengers behind the forecast contract;
- add calibrated event probabilities only after proper out-of-sample testing;
- add persistence/cache around `engine.analyze()`;
- add options as a separate data/analysis family;
- add user workspaces and alerts after report provenance is stable;
- promote individual IP nodes to their own modules only when their logic becomes large enough to justify it.

## Current engineering status

The repository is a runnable v0.1 research application with:

- installation flow;
- live/CSV market input;
- full evidence pipeline;
- CLI;
- API;
- browser interface;
- node registry;
- research backtest;
- automated tests and CI.

It is **not** a production-ready automated trading platform.

The next engineering priority is data trust and reproducibility: provider abstraction, persisted run manifests, source provenance, caching/failover, and broader integration testing. See [`ROADMAP.md`](ROADMAP.md).
