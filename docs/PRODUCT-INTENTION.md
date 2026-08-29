# Market Compass Product Intention

**Authority:** canonical founder-intention record  
**Applies to:** every release, interface, feature, provider, model, and agent working in this repository

This document answers **why Market Compass exists and what every feature is supposed to do**.
It is not a release-status claim. [`STATUS.md`](STATUS.md) records what is implemented today, while
[`FEATURE-JOURNAL.md`](FEATURE-JOURNAL.md) records how the product interpretation changes over time.

## Foundation: why the product exists

Market Compass exists to help a person understand a market decision as a body of inspectable,
two-sided evidence. It should gather the relevant facts, calculate repeatable signals, show what
supports and opposes a thesis, explain the route price may take, and state what would prove the
current interpretation wrong.

The purpose is the foundation at the bottom. Every feature grows upward from that foundation.
A feature that cannot trace its function back to this purpose does not belong in the product.

## Intended outcome

A user should be able to type the natural ticker they know, receive a complete market workbench,
understand the evidence without being a quantitative engineer, inspect the technical reasoning
when desired, and ask Nephew or another approved model for a grounded interpretation. The user
must always be able to distinguish:

- calculated evidence from model interpretation;
- bullish support from bearish opposition;
- evidence balance from calibrated probability;
- verified facts from inferred relationships;
- live capabilities from planned capabilities;
- local/private processing from information explicitly approved to leave the private network.

## Non-negotiable product rules

1. Market Compass calculations are authoritative; an LLM may interpret but may not silently alter them.
2. Every conclusion shows support, opposition, missing information, and invalidation.
3. Evidence and confidence remain separate. Neither is mislabeled as probability.
4. Each founder idea remains visible as its own named feature and IP node; later projections must not erase earlier capabilities.
5. Simple language and technical inspection are two views of the same truth, not separate products.
6. Friendly user input is translated to provider-specific syntax behind the interface.
7. Data, model, and source provenance remain inspectable.
8. Local models are preferred for private work. Cloud use is fail-closed and requires explicit authorization.
9. Historical patterns and forecasts are context, not promises.
10. Market Compass does not place trades or present itself as individualized investment advice.

## Feature intention registry

| Feature | Why it exists | What the user must receive | What it must never become |
| --- | --- | --- | --- |
| Friendly asset entry | Let the user speak in normal ticker language. | Type `HYPE`, `BTC`, `ETH`, `NVDA`, or `AAPL`; resolve provider identifiers invisibly and preserve both names in provenance. | A requirement to memorize `-USD`, exchange suffixes, or provider syntax. |
| Asset identity and freshness | Establish exactly what was analyzed and when. | Requested and resolved symbols, asset type, price, bar count, retrieval time, and analysis time. | An unlabeled price detached from its instrument or data age. |
| Asset Reality | Decide whether the instrument is real, active, liquid, and sufficiently known to analyze. | State, confidence, activity/liquidity evidence, missing fundamentals, and quality warnings. | A popularity score or unsupported claim of business/token quality. |
| Market State | Summarize the present condition before suggesting action. | Trend/reversal/continuation state and a plain-language description. | A concealed buy/sell command. |
| Bull/bear evidence | Make both sides visible. | A normalized two-sided balance totaling 100, plus the evidence behind each side. | A fake probability of profit. |
| Confidence | Show how much authority the evidence deserves. | A separate measure reduced by weak, missing, correlated, stale, or unvalidated inputs. | Direction disguised as certainty. |
| Trend | Show structural direction. | EMA 13/27/81, EMA 50 reference, ordering, slope, state, support, and opposition. | A single moving-average crossover presented as sufficient truth. |
| Momentum | Show the force and change behind price movement. | RSI 14, MACD, histogram, crossings, divergence, state, and counter-signals. | A rule that RSI must reach 30 before any valid setup exists. |
| Reversal versus continuation | Distinguish a turn from an extension of the existing move. | Explicit state tied to momentum, trend, and the asset-quality gate. | A buried derivative that disappears from the interface. |
| Fibonacci and Bus Stop route | Translate market structure into understandable destinations. | Last stop, current stop, upside/downside stops, anchors, confluence, reward/risk, and Wrong Road/invalidation. | Exact-price prophecy. |
| Price Memory | Measure where price repeatedly reacted. | Symmetric support and resistance with tests, span, age, reaction, volume context, erosion, and distance. | Decorative horizontal lines without history. |
| Multi-timeframe analysis | Prevent one timeframe from impersonating the whole market. | 4H, 1D, and 1W availability, state, momentum, and agreement/conflict. | Hidden substitution when a timeframe is unavailable. |
| Trading chart | Let the user inspect the calculations visually. | Candles, EMA overlays, route levels, Fibonacci, Price Memory, timeframe selection, RSI, and MACD. | A chart disconnected from the report values. |
| News and event risk | Represent the human and event environment around the asset. | Headlines, timestamps, sources, relevance, risk tags, sentiment, and observed reaction when available. | Unsourced rumor treated as causal fact. |
| Historical Analogs | Compare the current setup with completed past states. | Sample count, similarity, forward outcomes, dates, and explicit counterexamples. | Cherry-picked winners or guarantees about the future. |
| Forecast | Test whether a predictive model adds information beyond a simple baseline. | Validation method, baseline comparison, error measures, state, and withholding when the baseline is not beaten. | An unvalidated forecast influencing the score. |
| Evidence Board | Trace direct and indirect relationships like an investigation wall. | Entities, paths, sources, dates, confidence, strength, and clear verified/inferred labels. | Co-mention or correlation presented as causation. |
| Market narrative | Show the story currently organizing attention. | Dominant narrative, stage, sentiment, crowding/counter-narrative when supported. | Storytelling detached from evidence and price reaction. |
| Main case and counter-case | Make disagreement useful. | Strongest bullish evidence beside strongest bearish evidence. | A one-sided promotional summary. |
| Invalidation and missing data | Tell the user what changes the conclusion. | Wrong Road price/condition, evidence gaps, and next research actions. | Fine print hidden below the recommendation. |
| Simple / Technical / Sources views | Serve normal users and expert inspection from one report. | Plain explanation, technical values, source provenance, and consistent conclusions across views. | Different truths for different audiences. |
| 115-node inspector | Preserve each original idea as addressable product IP. | Stable node IDs, meanings, outputs, and a route from concept to runtime implementation. | A generic feature bucket that erases founder-defined concepts. |
| Watchlist and snapshots | Let the user maintain research continuity. | Friendly symbols, saved observations, timestamps, and later comparison. | Silent broker execution or permanent storage claims when data is browser-local. |
| Research backtest | Challenge a rule against completed history. | Past-only evaluation, fees/assumptions, results, limitations, and time-respecting validation. | Proof of profitability or leakage from future data. |
| Nephew Analyst | Interpret the complete Market Compass evidence packet in useful language. | Bull/bear cases, main conflict, invalidation, missing information, research actions, citations, and model receipt. | A second hidden scoring engine. |
| Local model lanes | Use private hardware for normal and heavy reasoning. | M5/MLX primary route, DGX/vLLM heavy route, Ollama recovery, health/configuration visibility, and explicit lane receipt. | Raw model servers unnecessarily exposed outside the private gateway. |
| Approved cloud models | Allow deliberate access to specialized external reasoning. | Selectable GPT, Claude, Perplexity, and Grok adapters with model IDs, consent, approval, and receipts. | Automatic report exfiltration because an API key happens to exist. |
| Model routing and receipts | Make dynamic AI use inspectable. | Selected provider/model/lane, report hash, prompt version, time, latency, and future cost/evaluation data. | Invisible routing or an untraceable answer. |
| Cross-model comparison | Reveal agreement and disagreement between competent analysts. | Separate responses/receipts, consensus, conflicts, citations, cost, and latency. | Majority vote treated as truth. |
| Approval Engine boundary | Put authority before external action. | Server-side permission in addition to user-interface consent. | A checkbox acting as the only security boundary. |

## Preservation rule

A newer release may reorganize or improve a feature, but it may not silently remove the feature's
named user-facing projection. If a replacement is proposed, the pull request must map the old
feature to the new surface and update this registry, `STATUS.md`, `CHANGELOG.md`, and the feature
journal. Screenshots and prior release surfaces are product evidence, not disposable mockups.

## Documentation ownership

- **Intention:** this file.
- **Current implementation truth:** [`STATUS.md`](STATUS.md).
- **Chronological shipped changes:** [`../CHANGELOG.md`](../CHANGELOG.md).
- **Founder decisions and feature interpretation:** [`FEATURE-JOURNAL.md`](FEATURE-JOURNAL.md).
- **Long-form requirements:** [`PRODUCT-REQUIREMENTS.md`](PRODUCT-REQUIREMENTS.md).
- **Concept/IP identities:** [`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md).
- **Engineering design:** [`ARCHITECTURE.md`](ARCHITECTURE.md).

When documents conflict, intention controls **why**, status controls **what exists**, and code plus
tests provide the implementation evidence.
