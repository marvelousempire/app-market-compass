# Market Compass Feature Journal

This is the separate, chronological journal of founder direction, product interpretation, and the
reason important features changed. It complements the factual release log in
[`../CHANGELOG.md`](../CHANGELOG.md). It must not be replaced by short-lived chat history, a pull
request description, or an issue comment.

## Journal rules

Every material feature decision records:

- date and author/source;
- intention being protected or changed;
- affected feature names and IP nodes when known;
- what the user should see;
- what changed in code or documentation;
- validation evidence;
- unresolved work;
- GitTalk issue/PR/commit references.

Do not rewrite old entries to make the history look cleaner. Add a new entry that corrects or
supersedes the earlier interpretation.

---

## 2026-08-30 — Fold 8001 information logic into the current desk

**Founder direction:** “fold 8001's look into 8006. I love the way 8001 provides that logic of info.”

**Intention:** Keep the fuller product (Analyst, charts, watchlist, multi-timeframe) and recover the older page's first-screen sequence. Do not roll the daily app back to `application-v0.2`. After this restyle is live, stop the leftover 8001 process so the old page cannot reopen.

**Features protected:** Asset Reality, Market State, Evidence, Confidence, Trend, Momentum, Fibonacci, Reversal, Price Memory, Nephew Analyst, Trading Workbench, Historical Analogs, Evidence Board.

**User-visible requirement:** Opening the current application shows a large Market Compass header, identity, a single decision sentence, then the four summary cards, then the rest of the desk. The six-card cockpit must not sit above those cards.

**Implementation:** HTML/CSS/JS restyle on the v0.4 workbench; health surface `application-v0.5`.

**Evidence:** Regression tests pin the 8001 sequence IDs (`summary-grid`, `signal-grid`, `identity-strip`) and refuse leftover cockpit/overview IDs.

**Still open:** Real data-provider depth, persistent workspaces, private M5/DGX commissioning, server-side Approval Engine authorization, and cross-model comparison.

---

## 2026-08-29 — Preserve original intelligence features in every later projection

**Founder direction:** “We had v1 things I need in the latest app.”

**Intention:** A later workbench or AI release must grow upward from the existing product. It must
not erase the clear, named presentation of earlier intelligence features.

**Features protected:** Asset Reality, Market State, Evidence, Confidence, Trend, Momentum,
Fibonacci, Reversal, Price Memory, News/Event Risk, and Historical Analogs.

**User-visible requirement:** The latest application shows an Intelligence Overview containing
the original top-level cards, followed by the newer Nephew analyst, multi-timeframe analysis,
interactive workbench, and research surfaces.

**Implementation:** PR #6 restored the explicit overview cards and added a launcher version check.
An older Market Compass process can no longer be mistaken for the current application merely
because it occupies port 8000.

**Evidence:** 21 tests passed; GitHub Actions passed; merged head
`fcd94e4002dc203406c7ad8266a0be866c490aae`.

**Still open:** Real data-provider depth, persistent workspaces, private M5/DGX commissioning,
server-side Approval Engine authorization, and cross-model comparison.

---

## 2026-08-29 — Add AI as a grounded interpretation layer

**Founder direction:** Nephew and appropriate local models must provide real analysis, while the
user can deliberately ask capable cloud models such as GPT, Claude, Perplexity, and Grok.

**Intention:** Market Compass calculates the evidence; Nephew and other approved models interpret
the same immutable report. Models may explain, challenge, and identify gaps, but do not silently
rewrite scores.

**Implementation:** v0.4 introduced validated analyst contracts, model receipts, M5/MLX,
DGX/vLLM, Ollama, OpenAI, Anthropic, Perplexity, and xAI adapters, depth-aware routing, a
deterministic offline provider, and fail-closed cloud controls.

**Evidence:** PR #5; merged commit `1710b6611043a645a9ba788828ce7fb49fc28480`;
GitTalk commissioning issue #4.

**Still open:** Commission real endpoints and credentials, enforce App Approval Engine authority,
evaluate champion models, and add transparent cross-model comparison.

---

## 2026-08-29 — Remove provider syntax from ticker entry

**Founder direction:** A user should type the ticker they know and should not have to append
`-USD`.

**Intention:** Provider conventions belong in adapters, not in the user's mental workload.

**Implementation:** Friendly symbol input and suggestions preserve `HYPE` in the interface while
recording provider-resolved identifiers such as `HYPE-USD` in provenance.

**Evidence:** Symbol-resolution regression coverage shipped with PR #5.

---

## v0.3 — Promote the dashboard into a trading workbench

**Intention:** The browser is a primary product projection rather than an afterthought attached to
the engine.

**Features:** Decision Cockpit, charts and indicators, 4H/1D/1W alignment, watchlist, snapshots,
catalysts, Evidence Board, contribution analysis, Price Memory, Bus Stops, and research backtest.

**Evidence:** [`V0.3-WORKBENCH.md`](V0.3-WORKBENCH.md); base commit
`13d6bb793dcc303c83c21135f6e25faa16a777c5`.

---

## v0.1–v0.2 — Establish the evidence system and its visible report

**Intention:** Answer more than “is a technical indicator bullish?” by building a two-sided,
explainable evidence system around asset reality, structure, momentum, routes, memory, news,
history, relationships, narrative, forecasting, and invalidation.

**Product principle:** Each feature remains a named product/IP node. The evidence balance is not a
calibrated probability, history is not a guarantee, inferred links are not verified causation, and
the system actively searches for counter-evidence.

**Evidence:** [`PRODUCT-REQUIREMENTS.md`](PRODUCT-REQUIREMENTS.md),
[`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md), and the v0.1/v0.2 implementation history.

---

## Entry template

```markdown
## YYYY-MM-DD — Decision title

**Founder direction:** Exact statement or faithful summary.

**Intention:** Why this exists and which foundation rule it serves.

**Features/IP nodes:** Named features and stable IDs.

**User-visible requirement:** What a person must be able to see or do.

**Implementation:** What changed.

**Evidence:** Tests, PR, commit, screenshots, or run receipt.

**Still open:** Remaining work and named next owner.
```
