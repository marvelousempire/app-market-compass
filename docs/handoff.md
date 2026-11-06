# Market Compass handoff — commissioned ACT v1 research runtime

This handoff reflects the commissioned v0.7 application, not the old developer-demo surface. The first
screen follows the 8001 information sequence (header, identity, four summary cards, then the
desk). The research workbench, indicators, multi-timeframe analysis, watchlist, catalysts,
Evidence Board, node inspector, research backtest, Nephew analyst panel, Actor spaces and ACT v1
Market Exchange remain visible.

## Installed target

| Target | Current state |
| --- | --- |
| Canonical forge | Gitea `averygoodman/app-market-compass`; accepted `main` owns releases |
| Downstream mirror | GitHub `marvelousempire/app-market-compass` follows accepted Gitea main |
| Stable FiveMac checkout | `~/Developer/market-compass-live` |
| Service and door | `ai.market-compass` at FiveMac `127.0.0.1:8000`; Make Doors operator URL `http://market-compass.localhost/` |
| Door ownership | Nephew owns the canonical registry and named, restartable FiveMac transport; Make Doors projects it. The raw `127.0.0.1:18003` forward is not the user-facing Door. |
| Authority boundary | Commissioned research only; no trading, score influence, bank writes or money movement |

Read the exact live revision rather than copying a dated SHA from this handoff:

```bash
curl -fsS http://127.0.0.1:8000/api/operator/status
curl -fsS http://127.0.0.1:8000/health
launchctl print gui/$(id -u)/ai.market-compass
```

## What is now visible

| Surface | Current behavior |
| --- | --- |
| Asset input | Accepts friendly symbols such as `HYPE`, `BTC`, `ETH`, `NVDA`, and `AAPL`; provider identifiers are resolved behind the UI. |
| Workbench | Asset reality, reversal/continuation, evidence/confidence, full route, Price Memory, charts, 4H/1D/1W alignment, catalysts, analogs, narrative, opposing cases, and invalidation. |
| Evidence Board | Interactive inferred relationship graph with relationship/source inspection and explicit inferred-versus-verified labeling. |
| Research tools | Simple/technical/source views, 115-node inspector, snapshots/watchlist, and research backtest. |
| AI interpretation | Nephew panel with automatic or explicit local/cloud provider selection, depth, per-request cloud consent, grounded response schema, and model receipt. |
| Actor spaces | Omo, Prince, Wuda and Brown’s Barometers bind current report evidence to explicit psychology, comp cards, and exportable research-only receipts. |
| ACT v1 Market Exchange | Six admin rooms inspect 15 modules and 58 reviewed private bankTHAT contracts. All six pipeline stages act, and Market Source Refinery exports intake receipts for repositories, URLs, files, and pasted text without donor execution. |

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
