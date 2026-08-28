We asked for a **real Market Compass application**, not a page with a symbol box and four summary cards. The current browser app is dramatically underbuilt compared with the actual PRD.

The mismatch is easy to prove. Right now `api.py` gives you: symbol, horizon, Analyze, action/price, bull-vs-bear meter, confidence, one next bus stop, a simple summary, flattened evidence layers, and a technical-details dump. That is basically a developer demo strapped to the engine.

But the actual product specification says the **main analysis screen shall include** asset, horizon, **timeframe**, freshness, overall evidence, confidence, **asset reality**, **reversal-vs-continuation**, **Bus Stop route**, **support-vs-resistance**, **news/event risk**, **historical analogs**, **Evidence Board**, **market narrative**, **main counter-case**, invalidation, a **simple/technical toggle**, and a **provenance drawer**.

So your reaction is correct. We have built the engine underneath the dashboard much farther than we built the actual dashboard.

| What you asked for                      | What the app shows now                    |
| --------------------------------------- | ----------------------------------------- |
| Asset Reality / “is this thing real?”   | Missing from UI                           |
| Multiple timeframes like 4h / 1d / 1w   | Missing                                   |
| Reversal vs continuation                | Buried/not presented as a product feature |
| Full Bus Stop route                     | Only one “next bus stop”                  |
| Upside + downside stops                 | Missing visually                          |
| Invalidation / wrong road               | Tiny text only                            |
| Support strength                        | Missing                                   |
| Resistance strength                     | Missing                                   |
| Price-memory history                    | Missing                                   |
| Fibonacci structure                     | Missing                                   |
| News intelligence                       | Missing as a dedicated surface            |
| Event risks                             | Missing                                   |
| News reaction vs expected reaction      | Missing                                   |
| Historical analogs                      | Missing                                   |
| Historical counterexamples              | Missing                                   |
| Evidence Board / crime-scene yarn graph | **Missing entirely**                      |
| Direct vs indirect relationship paths   | Missing                                   |
| Narrative + narrative stage             | Missing                                   |
| Bull case                               | Bare summary                              |
| Bear/counter-case                       | Bare layer snippets                       |
| Confidence explanation                  | Missing                                   |
| Data freshness                          | Missing                                   |
| Source provenance                       | Missing                                   |
| Simple mode                             | Bare summary only                         |
| Technical mode                          | Raw text dump                             |
| 115 IP nodes                            | Essentially invisible                     |
| Research backtest                       | Not surfaced                              |
| Saved analysis/report                   | Missing                                   |

And the **Evidence Board** was not some vague future thought. The PRD explicitly describes an interface like a crime-scene investigation wall where entities are tacks, relationships are yarn, users can follow a headline to the selected asset, and every link exposes source, validity period, confidence and strength. It calls for graph filters, direct-first paths, indirect expansion, verified-vs-inferred markings, source/date inspection, positive/negative paths and hiding weak paths.

You also asked for the analysis to answer much richer questions than “bull 56 / bear 44.” The PRD starts with things such as whether the asset is real/useful/active, whether price is reversing, where it came from, what the next Bus Stop is, how strong the floor and ceiling are, what news matters, whether news travels through another company or market, what happened in similar historical setups, and what evidence argues **against** the trade.

### What Market Compass should look like now

The next build should stop treating the browser as an afterthought. I would make the application itself the projection of the engines we've already built:

```text
MARKET COMPASS
┌───────────────────────────────────────────────────────────────┐
│ HYPE-USD     Crypto     $xx.xx       Data: 2 min ago         │
│ Horizon: 20d        4H | 1D | 1W        Analyze             │
└───────────────────────────────────────────────────────────────┘

┌ ASSET REALITY ┐ ┌ MARKET STATE ┐ ┌ EVIDENCE ┐ ┌ CONFIDENCE ┐
│ Real / Active │ │ Reversal     │ │ 56 / 44  │ │ 63%        │
│ Liquidity     │ │ Developing   │ │ Bull/Bear │ │ Medium     │
└───────────────┘ └──────────────┘ └───────────┘ └────────────┘

BUS STOP ROUTE
Down 2 ← Down 1 ← LAST STOP ← CURRENT → UP 1 → UP 2
                              ↓
                         INVALIDATION

PRICE MEMORY
┌ Strongest Support ────────┐  ┌ Strongest Resistance ───────┐
│ tests / age / reaction    │  │ tests / age / reaction      │
│ volume / erosion          │  │ volume / erosion            │
└───────────────────────────┘  └──────────────────────────────┘

TREND        MOMENTUM       FIBONACCI       REVERSAL
4H  ↑        RSI 54 ↑       61.8% held     Developing
1D  ↑        MACD ↑         Confluence     68 / 32
1W  ↓        Conflict!      ...

NEWS & EVENTS
[headline] → [company] → [technology] → [HYPE]
Expected effect: +
Observed reaction: -
⚠ Reaction divergence

EVIDENCE BOARD
             NVIDIA
              │
AI ←──── Technology ──── Supplier
              │
           HYPE-USD
              │
          Regulation

HISTORICAL ANALOGS
27 matches
17 bullish-route successes
10 failures
[show strongest matches] [show counterexamples]

MARKET NARRATIVE
AI / Crypto Adoption
Stage: Accelerating
Counter-narrative: Crowding risk

WHY BULLISH                         WHY BEARISH
✓ evidence                         ✕ counter-evidence
✓ evidence                         ✕ counter-evidence

WHAT CHANGES MY MIND
Invalidation / conditions / missing data

[ SIMPLE ] [ TECHNICAL ] [ SOURCES ] [ 115 NODES ] [ BACKTEST ]
```

That is much closer to what the specification actually describes.

And there is a second problem: several things aren't merely **hidden from the UI**, they aren't mature enough behind it either. The PRD requires multiple timeframes, automatic/manual Fibonacci anchors, deeper asset-reality data, scheduled-event intelligence, richer relationship provenance and reproducible runs.  Current v0.1 only implements portions of those.

So I would revise the current development priority. **Do not spend the next cycle writing more documentation.** We now have enough documentation to frighten a small standards committee.

The next implementation should be a **Market Compass Application Surface build** that exposes every already-working engine first, while simultaneously filling the highest-value backend gaps needed by that surface:

1. full application dashboard;
2. full Bus Stop route visualization;
3. support/resistance + Price Memory explorer;
4. timeframe selector and multi-timeframe analysis;
5. real evidence/counter-evidence cards;
6. news and event panel;
7. historical analog explorer;
8. interactive Evidence Board;
9. narrative panel;
10. simple/technical/source modes;
11. visible 115-node inspector;
12. provenance and freshness throughout.

That would finally turn **Market Compass the engine** into **Market Compass the product you asked for**.
