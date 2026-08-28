# Market Compass

Market Compass is a runnable market decision-intelligence app for stocks, crypto, and other OHLCV-traded assets. It combines technical signals, price memory, news, historical analogs, relationship intelligence, market narratives, and a time-series forecast into one explainable bull-vs-bear evidence report.

It does **not** turn a 56/44 evidence split into a fake 56% chance of profit. Humans have produced enough confident numbers already.

## What works now

The current v0.1 engine implements:

- Asset reality/quality gate using available instrument metadata, trading history, and liquidity.
- EMA 13 / 27 / 81 trend structure, plus EMA 50 as an available reference.
- RSI 14 with 30 / 50 / 70 interpretation.
- MACD and optional stochastic momentum.
- Reversal-vs-continuation classification.
- Fibonacci swing analysis using left-to-right swing ordering.
- **Bus Stop Route**: last stop, next stops, downside stops, invalidation, and reward/risk.
- **Price Memory**: support and resistance using repeated test episodes, time span, reaction size, volume, recency, and erosion from repeated testing.
- News sentiment, event-risk keywords, freshness decay, and observed price-reaction comparison.
- Historical analog retrieval with nearest-neighbor matching and explicit counterexamples.
- Relationship/Evidence Board graph built from news co-mentions, including multi-hop paths. Inferred links are labeled as inferred, not causal facts.
- Narrative detection for major themes such as AI/chips, rates/Fed, crypto adoption, regulation, and geopolitics.
- Ridge time-series forecast with chronological cross-validation. The forecast is excluded from the final score when it does not beat a simple baseline.
- Correlation discounts so RSI/MACD/trend and news/narrative/relationship evidence are not counted as fully independent proof.
- Bull/bear evidence that always totals 100, with confidence shown separately.
- Plain-language and technical explanations.
- A 115-ID node registry that keeps every PRD IP node addressable while routing related nodes to shared implementations.
- CLI, FastAPI endpoints, a no-build browser UI, CSV input, unit tests, and a compact research backtest.

## Architecture

The code stays intentionally small. A node is a stable addressable action, **not necessarily a physical Python file**.

```text
src/market_compass/
├── data.py        # Yahoo/CSV data and symbol resolution
├── technical.py   # EMA, RSI, MACD, stochastic, Fib, price memory, Bus Stops
├── context.py     # quality, news, history, forecast, graph, narrative
├── scoring.py     # contrast, correlation discounts, confidence, action state
├── engine.py      # end-to-end orchestration
├── registry.py    # all 115 stable IP node IDs
├── backtest.py    # past-only research backtest
├── api.py         # FastAPI + browser UI
├── cli.py         # analyze/node/registry/backtest commands
└── models.py      # typed report contracts
```

The complete product requirements remain in [`docs/PRODUCT-REQUIREMENTS.md`](docs/PRODUCT-REQUIREMENTS.md). The original conceptual IP inventory remains in [`docs/IP-NODE-REGISTRY.md`](docs/IP-NODE-REGISTRY.md); the live 115-ID runtime map is `src/market_compass/registry.py`.

## Install

Python 3.11+ is required. On macOS the Makefile uses `python3` by default.

For a fresh clone:

```bash
git clone https://github.com/marvelousempire/app-market-compass.git
cd app-market-compass
make doctor
make setup
```

If you already cloned the repository, update before installing:

```bash
git pull
make doctor
make setup
```

`make doctor` prints the Python interpreter and validates that it is Python 3.11 or newer. To use a specific interpreter:

```bash
make setup PYTHON=/path/to/python3
```

Or install directly:

```bash
python3 -m pip install -e '.[dev]'
```

## Run the full analysis

```bash
make analyze ASSET=HYPE-USD HORIZON=20
```

Equivalent CLI command:

```bash
market-compass analyze HYPE-USD --horizon 20
```

For JSON:

```bash
market-compass analyze HYPE-USD --horizon 20 --json
```

Yahoo sometimes uses internal symbols for crypto. Market Compass first searches the requested symbol and records both `requested_symbol` and `resolved_symbol` in the report metadata.

## Run the app

```bash
make app
```

Then open `http://127.0.0.1:8000`.

The same process serves both the UI and API, which avoids maintaining a separate frontend build for a young product that has more important things to prove first.

### API

```text
GET /health
GET /api/analyze?symbol=HYPE-USD&horizon=20
GET /api/nodes
GET /api/nodes/L2-001?symbol=HYPE-USD&horizon=20
```

## Run any IP node

List all 115 node IDs:

```bash
market-compass registry
```

Run one:

```bash
market-compass node L2-001 HYPE-USD --horizon 20
```

Related node IDs share implementations on purpose. For example, the L2 momentum family uses the same enriched price frame and momentum layer instead of seven wrapper files containing approximately four useful lines each.

## CSV mode

If the live provider is unavailable, use a CSV containing:

```text
date,open,high,low,close,volume
```

Example:

```bash
market-compass analyze TEST --csv ./prices.csv --horizon 20
```

This makes the analytic engine independent of the live data provider and makes testing reproducible.

## Backtest

```bash
make backtest ASSET=HYPE-USD HORIZON=20
```

The current backtest uses only information available at each historical bar. It includes a fee assumption and reports signal-observation outcomes. It is a research test, not a brokerage cash-account simulator.

## Tests

```bash
make test
```

CI runs the test suite on pushes and pull requests.

Current tests cover:

- all 115 stable node IDs;
- RSI bounds;
- EMA 13/27/81 and MACD feature creation;
- 100-point bull/bear contrast math;
- complete layer output;
- symmetric support/resistance price-memory fields;
- Bus Stop/Fibonacci routing;
- research backtest output.

## Evidence model

Every layer returns:

- a state;
- score from -1 to +1;
- confidence from 0 to 1;
- supporting evidence;
- opposing evidence;
- metrics;
- missing data.

The aggregate engine applies confidence and independence discounts, then converts the final net evidence to a two-sided split:

```text
Bull evidence: 56
Bear evidence: 44
Confidence: 61%
```

The split is **evidence balance**, not a calibrated probability.

## Forecast rule

The forecasting layer currently uses Ridge regression over lagged returns, RSI, volatility, and volume features. It uses `TimeSeriesSplit`, not random train/test splitting.

If its cross-validated error is not better than the baseline error, the model is marked `baseline_not_beaten` and its forecast is **not allowed to influence the final score**.

More complicated models can be added later, but complexity has to earn rent.

## Relationship intelligence boundary

The current Evidence Board creates graph links from related-news co-mentions. Those edges are explicitly marked `inferred=true` and are not treated as proof that one company supplies, owns, controls, or causes another.

Curated supplier/customer/ownership/regulatory edges can be added as a future data source without changing the graph/report contract.

## Important limits

This is a complete runnable **v0.1 research application**, not a production trading platform.

It does not currently:

- place trades;
- guarantee price direction;
- provide calibrated profit probabilities;
- maintain a licensed institutional news feed;
- verify crypto token utility, unlock schedules, holder concentration, or protocol revenue unless that data is supplied by a future provider;
- infer causation from news co-mentions;
- model options chains or broker execution.

Missing data lowers confidence rather than being invented.

## Product documents

- [`docs/PRODUCT-REQUIREMENTS.md`](docs/PRODUCT-REQUIREMENTS.md) — full PRD and long-term product specification.
- [`docs/IP-NODE-REGISTRY.md`](docs/IP-NODE-REGISTRY.md) — original 115-node product inventory and conceptual module plan.
- [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md) — what v0.1 implements, how data flows, and where later extensions plug in.

## Disclaimer

Market Compass is research and decision-support software. It is not investment advice and does not guarantee outcomes. Historical patterns can fail, news can be wrong or incomplete, and models can break when market regimes change.
