# Market Compass v0.1 Implementation

This document describes the code that exists now. The PRD describes the larger product direction.

## Design decision: stable nodes, shared code

The product preserves 115 stable IP node IDs. The implementation does **not** create 115 Python wrapper files. Related nodes route to shared modules through `registry.py`. This preserves addressability and product lineage while minimizing duplicated code.

The rule is:

> Node identity is a contract. File count is not intellectual property.

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
```

## Data

The default provider uses Yahoo's public search and chart endpoints through the Python standard library. The search step resolves symbols before requesting chart data because some Yahoo crypto symbols include internal numeric suffixes.

CSV is a fully supported input path and requires `date`, `open`, `high`, `low`, `close`, and `volume`.

## Technical layer

The initial deterministic profile uses EMA 13, 27, 81; RSI 14; standard MACD 12/26/9; and optional stochastic.

Price memory clusters local pivot candidates, then measures independent nearby test episodes. Each level records test count, first/last seen, time span, average reaction, volume ratio, recency, repeated-test erosion, and overall strength.

Fibonacci automatically decides whether the dominant lookback swing is low-to-high or high-to-low based on timestamp order. Bus Stops combine historical levels and Fibonacci levels around current price.

## Context layer

News uses a small transparent lexical model rather than hiding the output behind an opaque language model. It adds freshness decay, event-risk detection, and comparison with actual latest price reaction.

Historical analogs use standardized current features and nearest neighbors. Only historical rows with a complete future outcome are eligible. Counterexamples are returned explicitly.

The forecast uses Ridge regression with chronological `TimeSeriesSplit`. A simple historical-mean target forecast is the baseline. A forecast that fails to beat the baseline receives `baseline_not_beaten` and cannot change the final evidence score.

Relationship intelligence uses NetworkX. Current edges are derived from co-mentions in related news, are marked inferred, and can form multi-hop paths. They are not causal or verified business relationships.

Narrative classification uses transparent keyword families. It is deliberately modest until a licensed or stronger text-data source exists.

## Scoring

Layer scores run from -1 to +1. Confidence is separate.

The aggregator reduces momentum weight when momentum agrees with trend because both come from price. It also discounts relationship/narrative outputs because they are currently derived from the same news source.

The normalized two-sided split always sums to 100.

## Surfaces

`market-compass analyze` returns the full report.

`market-compass node <ID>` exposes an IP node through the registry.

`market-compass registry` lists all 115 IDs.

`market-compass backtest` runs the research backtest.

`make app` starts FastAPI and the browser UI from one process.

## Extension seams

The compact architecture is designed so later work can replace or extend one surface without rewriting the product:

- swap Yahoo for licensed market/news providers in `data.py`;
- add verified company/protocol edges to the NetworkX graph;
- add statsmodels/GARCH/boosting challengers behind `forecast()`;
- add calibrated event probabilities only after proper out-of-sample testing;
- add persistence/cache around `engine.analyze()`;
- add options and execution as separate modules;
- promote individual IP nodes to their own modules only when their logic becomes large enough to justify it.

## Current engineering status

The core package compiles and the local test suite passes. CI is configured to install the package and run pytest on pushes and pull requests.

The repository should describe this as a runnable v0.1 research app, not as a production-ready automated trading system.
