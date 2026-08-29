# Market Compass handoff — remaining user-visible gaps

This handoff reflects the v0.4 application, not the old developer-demo surface. The trading
workbench, indicators, multi-timeframe analysis, watchlist, catalysts, Evidence Board, node
inspector, research backtest, and Nephew analyst panel are visible in the running app.

## What is now visible

| Surface | Current behavior |
| --- | --- |
| Asset input | Accepts friendly symbols such as `HYPE`, `BTC`, `ETH`, `NVDA`, and `AAPL`; provider identifiers are resolved behind the UI. |
| Workbench | Asset reality, reversal/continuation, evidence/confidence, full route, Price Memory, charts, 4H/1D/1W alignment, catalysts, analogs, narrative, opposing cases, and invalidation. |
| Evidence Board | Interactive inferred relationship graph with relationship/source inspection and explicit inferred-versus-verified labeling. |
| Research tools | Simple/technical/source views, 115-node inspector, snapshots/watchlist, and research backtest. |
| AI interpretation | Nephew panel with automatic or explicit local/cloud provider selection, depth, per-request cloud consent, grounded response schema, and model receipt. |

## Remaining gaps only

| Gap | What the user sees today | Completion condition |
| --- | --- | --- |
| M5 Max lane commissioning | `Nephew · Five Mac MLX` is disabled until its endpoint/model environment is supplied. | Private Nephew gateway reaches the M5 MLX service and passes a real receipt/evaluation run. |
| DGX Spark lane commissioning | `Nephew · DGX Spark vLLM` is disabled until its endpoint/model environment is supplied. | Private gateway reaches DGX vLLM and passes a super-heavy receipt/evaluation run. |
| Cloud model commissioning | GPT Pro, Claude, Perplexity, and Grok appear but stay disabled without runtime keys. | Keychain/service-managed credentials are injected and each selected provider passes its contract test. |
| Approval authority | The UI requires explicit cloud consent, but the production App Approval Engine is not yet connected. | Both UI consent and server-side approval are required before report data can leave the private network. |
| Cross-model comparison | A user can choose one provider or let Nephew route; no side-by-side consensus view exists. | Parallel provider responses expose agreement, disagreement, citations, cost/latency, and separate receipts. |
| Persistent workspaces | Watchlist and snapshots are browser-local. | Authenticated, durable workspaces/reports with export and restore. |
| Manual chart control | Automatic Fibonacci/route anchors are visible; manual anchor editing is absent. | User can set/reset anchors and immediately see route recalculation and provenance. |
| Evidence depth | Relationship edges and news intelligence are useful but primarily inferred/public-provider based. | Licensed feeds add dated, sourced, verified relationships, fundamentals, events, and stronger entity resolution. |
| Reproducibility | Receipts bind AI output to the report hash, but the underlying market-data run is not an immutable manifest. | Data snapshot, code/model versions, parameters, and sources can reproduce a run. |
| Operational productization | No authentication, quotas, provider health probes, retry/circuit breaking, or production observability. | Secure deployment and failure behavior are tested and monitored. |

The deterministic `grounded-offline` analyst remains available with no endpoint or credential. It
validates the UI/API contract and produces evidence-bound interpretation, but it is not presented
as a language model. Market Compass calculations remain authoritative; every model is an
interpretation layer only.
