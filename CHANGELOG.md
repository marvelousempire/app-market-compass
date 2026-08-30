# Market Compass Change Log

This is the factual, chronological log of shipped repository changes. Product reasoning and
founder direction are recorded separately in [`docs/FEATURE-JOURNAL.md`](docs/FEATURE-JOURNAL.md).

## Unreleased

- No unmerged product changes are currently recorded.

## [0.5.0] — Sunday, August 30, 2026 at 2:33:48 PM Eastern · *Fold 8001 information sequence into the workbench*
**Signed:** Grok > grok-4.6

- Restyled the live desk so the first screen follows the 8001 information sequence: large header, identity strip, decision sentence, then Asset Reality / Market State / Evidence / Confidence, then Trend / Momentum / Fibonacci / Reversal.
- Kept the v0.4 tools: Nephew Analyst, 4H/1D/1W, Price Memory, charts, contributions, catalysts, and research surfaces.
- Replaced the six-card cockpit with one action line so Evidence and Confidence are not shown twice.
- Advanced the health surface to `application-v0.5` so the launcher will not reopen an older process as current.


## 2026-08-29 — Intelligence overview preservation

- Restored explicit Asset Reality, Market State, Evidence, Confidence, Trend, Momentum,
  Fibonacci, and Reversal cards in the latest workbench.
- Preserved Price Memory, News/Catalysts, Historical Analogs, multi-timeframe analysis, Evidence
  Board, research tools, and Nephew Analyst.
- Prevented the launcher from reopening an older Market Compass version on port 8000.
- Added regression coverage for the preserved projection and stale-version rejection.
- Merged through PR #6 at `fcd94e4002dc203406c7ad8266a0be866c490aae`.

## v0.4 — Nephew multi-model analyst bridge

- Added grounded analyst request/response contracts and report-bound model receipts.
- Added local M5/MLX, DGX/vLLM, and Ollama routes.
- Added configurable OpenAI, Anthropic, Perplexity, and xAI adapters.
- Added fail-closed cloud permission plus per-request consent.
- Added friendly ticker entry and provider symbol resolution.
- Added the Nephew analyst workbench panel and offline deterministic provider.
- Merged through PR #5 at `1710b6611043a645a9ba788828ce7fb49fc28480`.

## v0.3 — Trading workbench

- Shipped the interactive decision cockpit, charts, indicators, multi-timeframe analysis,
  watchlist, snapshots, catalysts, Price Memory, Evidence Board, historical context, node inspector,
  and research backtest.
- Shipped at `13d6bb793dcc303c83c21135f6e25faa16a777c5`.

## v0.1–v0.2 — Evidence engine and report surface

- Established the canonical evidence-layer contract, two-sided scoring, confidence separation,
  Bus Stop routes, Price Memory, news/human context, historical analogs and counterexamples,
  relationship intelligence, narrative, forecasting gate, API, CLI, and browser report.
