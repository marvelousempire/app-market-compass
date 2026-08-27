# Market Compass Product Requirements Document

**Product:** Market Compass  
**Subtitle:** Node-Based Market Decision Intelligence System  
**Version:** 1.0  
**Date:** August 27, 2026  
**Status:** Engineering Draft  
**Audience:** Product owner, junior engineers, senior engineers, quantitative developers, data engineers, machine-learning engineers, and research analysts  
**Confidentiality:** Founder intellectual property and working product specification

---

## Document purpose

This document turns the complete product discussion into a build-ready specification. It preserves every distinct product idea as an intellectual-property node. Each node is intended to become an independent Python microscript, package, API function, and potentially a standalone product.

The system must be understandable at two levels:

1. **Simple mode:** explain results at approximately a fourth- to fifth-grade reading level.
2. **Technical mode:** let engineers and advanced users inspect formulas, parameters, timestamps, data sources, model versions, assumptions, evidence, counter-evidence, and tests.

The product must never give only one side of a market argument. Every bullish result must show the bearish case. Every bearish result must show the bullish case. Every score must explain what supports it, what weakens it, what data is missing, and what would prove the current conclusion wrong.

---

# 1. Plain-English product definition

Market Compass is a research tool for stocks, crypto, exchange-traded funds, and later options.

A user picks an asset, such as HYPE or BlackBerry. The system checks the price, chart, news, market mood, asset history, and the people or companies connected to it.

The system then answers simple questions:

- Is this asset real, useful, and active, or mostly hype?
- Is price moving up, moving down, or stuck?
- Is price turning around, or is the old move still going?
- Where did price come from?
- What may be the next **bus stop** for price?
- How strong is the floor below price?
- How strong is the ceiling above price?
- What news matters to this asset?
- Can news affect the asset through another company or market?
- What happened during similar setups in the past?
- What facts support the trade?
- What facts argue against the trade?

A result may look like:

```text
Bull evidence: 56
Bear evidence: 44
Confidence: Medium
Current state: A possible reversal is starting, but it is not confirmed.
Last bus stop: The last strong price area that price left.
Next bus stop: The next strong price area price may test.
Main risk: A news event or resistance level may stop the move.
```

The 56/44 split is an **evidence balance**, not automatically a 56% probability of profit. A probability may only be shown when a clearly defined target has been tested out of sample and calibrated.

---

# 2. Executive summary

## 2.1 Product vision

Market Compass is a transparent market decision-intelligence platform. It combines technical analysis, market structure, price history, news, market psychology, historical analogs, relationship graphs, market narrative, and forecasting into one node-based system.

The core question is:

> Given all available evidence, what is the most likely explanation for the current market state, and what is the most likely path from here?

The system must not simply ask what the indicators say. It must ask:

- Do the indicators agree?
- Are they measuring the same thing and being counted twice?
- What evidence contradicts the main view?
- Is the asset fundamentally real enough to trade?
- Is the present chart setup different from similar setups in the past?
- Does the news directly affect the asset, or only affect it through connected entities?
- Is the market reacting to the news in the expected direction?
- Where are the likely next price destinations?
- What would invalidate the trade idea?

## 2.2 Product structure

The platform has one foundation gate and eight primary evidence layers.

### Foundation Gate 0: Asset Reality and Quality

Answers: **What is this asset, and is it real enough to analyze?**

For tokens it examines utility, supply, unlocks, emissions, liquidity, revenue or fee activity, concentration, governance, security, and major risks. For companies it examines the business, financial health, float, dilution, liquidity, dependencies, and material risks.

### Layer 1: Trend

Checks direction and structure using exponential moving averages, slopes, alignment, crossovers, and multiple timeframes.

### Layer 2: Momentum and Reversal

Checks RSI, MACD, divergence, and optional stochastic signals. It decides whether momentum is improving, weakening, reversing, continuing, or overextended.

### Layer 3: Price Structure, Fibonacci, and the Bus-Stop Route

Finds major swings, draws Fibonacci levels, identifies where price came from, finds likely next destinations, and defines invalidation.

### Layer 4: Human Factor, News, Sentiment, and Event Risk

Checks headlines, political and economic events, scheduled announcements, source quality, sentiment, relevance, novelty, and actual market reaction.

### Layer 5: Historical Context and Analogs

Finds similar past setups and shows what happened next, including examples that support and contradict the current case.

### Layer 6: Price Memory, Support, and Resistance

Measures how often price visited a level, over what period, how strongly it bounced or rejected, whether volume confirmed the level, and whether repeated testing weakened it.

### Layer 7: Relationship Intelligence and the Evidence Board

Builds a graph like a crime-scene wall with tacks and yarn. It connects an asset to suppliers, customers, competitors, technologies, sectors, regulators, macro factors, exchanges, protocols, people, and related assets. It traces how a headline may travel through those links.

### Layer 8: Market Narrative

Identifies the story the market is trading, such as artificial intelligence, interest rates, regulation, risk-on behavior, crypto adoption, institutional accumulation, or dilution fear. It measures whether the story is new, growing, crowded, fading, or reversing.

## 2.3 Shared engines

The eight layers feed shared engines for:

- pairwise contrast;
- disconfirming evidence;
- evidence scoring;
- confidence;
- correlation and duplicate-signal penalties;
- forecasting;
- volatility;
- risk and route analysis;
- plain-language explanation;
- technical explanation;
- provenance and audit;
- backtesting and calibration;
- Python orchestration.

## 2.4 Core promise

The product does not say only buy, sell, or hold. It shows:

- what the evidence supports;
- what the evidence opposes;
- how strong each side is;
- how fresh the data is;
- whether the conclusion is stable or fragile;
- the likely next price stops;
- what would invalidate the setup;
- which sources and calculations produced the result.

---

# 3. Problem statement

Most market tools have one or more of these problems:

1. They show many indicators but do not explain how those indicators relate.
2. They count correlated indicators as if each were independent proof.
3. They show support or resistance without explaining how often the market tested it or how long the level mattered.
4. They show headlines without explaining whether the news directly or indirectly affects the selected asset.
5. They show bullish evidence and hide bearish evidence, or the reverse.
6. They present model output as certainty.
7. They do not distinguish a temporary bounce from a real reversal.
8. They do not define the last price stop, the next price stop, or the condition that breaks the route.
9. They use historical patterns without showing sample size, regime, differences, or counterexamples.
10. They use technical language that many users cannot understand.
11. They combine too much logic in one script, making the system hard to test, audit, and improve.
12. They do not preserve each product idea as a modular intellectual-property component.

Market Compass solves these problems by making every idea a node, every node a focused Python process, and every process responsible for the main case and the counter-case.

---

# 4. Goals and non-goals

## 4.1 Goals

Market Compass shall:

1. Analyze one asset over a selected trading horizon, initially focusing on days to several weeks.
2. Explain whether the asset appears fundamentally legitimate, active, liquid, and analyzable.
3. Detect trend, momentum, reversal, continuation, support, resistance, and price-route conditions.
4. Identify the last bus stop, next bus stops, and invalidation point.
5. Measure the historical strength of both support and resistance.
6. Connect news to the asset through direct and indirect relationships.
7. Identify the dominant market narrative and its stage.
8. Retrieve historical analogs without using future information.
9. Produce paired bullish and bearish evidence for every node and layer.
10. Use a normalized evidence split that totals 100.
11. Show confidence separately from the evidence split.
12. Produce simple and technical explanations.
13. Preserve data lineage, formulas, timestamps, model versions, and source provenance.
14. Run each node independently as a Python script.
15. Run the complete system through a Makefile and Python orchestrator.
16. Allow each node or layer to become a standalone API or commercial product.
17. Support backtesting, calibration, and continuous performance measurement.
18. Search actively for evidence that disproves the current view.

## 4.2 Initial non-goals

The first release shall not:

1. Guarantee profits or price direction.
2. Automatically place trades.
3. Treat an uncalibrated evidence score as a probability.
4. Hide conflicting evidence behind a single score.
5. Use random train/test splits for time-series forecasting.
6. Treat social-media claims as verified facts.
7. Infer causation only because two assets moved together.
8. Use deep learning merely because it sounds advanced.
9. Support every asset class on day one.
10. Replace legal, tax, investment, or fiduciary advice.

---

# 5. Users and use cases

## 5.1 Primary user: swing trader

The primary user holds or considers trades lasting several days to several weeks. Primary questions include:

- Is this a reasonable entry area?
- Am I chasing price after a large run?
- Is this a real reversal or only a bounce?
- Where is the next target?
- Where is the trade wrong?
- What news can change the setup?

## 5.2 Research-oriented trader

Wants deeper evidence, historical analogs, graph paths, and technical details.

## 5.3 Quantitative developer

Needs independent node execution, stable data contracts, backtests, model metrics, reproducible runs, and leakage protection.

## 5.4 Product or research analyst

Wants to compare assets, inspect narratives, and preserve decision snapshots.

## 5.5 Initial use cases

### HYPE over a multi-week horizon

Check whether the token has real utility and liquidity, whether supply or unlock conditions create risk, whether technical conditions support an entry, what news matters, and where the next route stops may be.

### BlackBerry and indirect technology news

Given a headline about a technology company or chip developer, map possible paths from that company to BlackBerry through customers, suppliers, products, industries, shared technology, or market narratives, then score how credible each path is.

### Possible reversal

RSI is not below 30, but MACD turns up, price holds a Fibonacci level, and shorter EMAs improve. Determine whether the evidence supports a reversal, continuation, or unconfirmed bounce.

### Historical support and resistance

Identify a price area and report how many times price tested it, the period covered, prior bounce or rejection sizes, volume near the level, and whether repeated testing may have weakened it.

---

# 6. Product principles

1. **Node first.** Every distinct idea is a node with one main job and a stable input/output contract.
2. **Contrast is mandatory.** Every node returns evidence for and against its current view.
3. **Explanation is mandatory.** A number without a reason is incomplete.
4. **Evidence is not certainty.** Scores express the present balance of evidence.
5. **Time awareness.** All calculations respect the selected `as_of` timestamp.
6. **Independence matters.** Correlated signals must not be counted as independent proof.
7. **Simple outside, technical inside.** Default explanations are plain; technical detail remains available.
8. **Provenance by default.** Every result identifies its data and calculation origins.
9. **Modular commercialization.** Each node, layer, and engine can become a standalone capability.
10. **Makefile as launch control.** Make invokes Python; business logic stays in Python.

---

# 7. Core terminology

**Asset:** the stock, token, fund, option, or other instrument being analyzed.  
**Horizon:** how far forward the user cares about.  
**Timeframe:** chart interval, such as 1h, 4h, 1d, or 1w.  
**Node:** one independent unit of IP and one focused analytic job.  
**Microscript:** a Python script that executes one node or tightly bounded action.  
**Layer:** a group of related nodes.  
**Evidence item:** one fact, calculation, event, or observation supporting or opposing a view.  
**Evidence split:** a normalized bullish/bearish or positive/negative balance totaling 100.  
**Confidence:** a separate measure of data quality, coverage, agreement, freshness, and calibration.  
**Last bus stop:** the most recent meaningful price area that price left before the current area.  
**Next bus stop:** the next meaningful support, resistance, Fibonacci, volume, or forecast target.  
**Route:** the ordered path from the last bus stop through possible next stops.  
**Invalidation:** a condition that makes the current explanation no longer valid.  
**Price memory:** the history of market reactions around a price area.  
**Historical analog:** a prior market setup resembling the current setup.  
**Relationship path:** a chain of entities and links that may transmit event impact to the selected asset.  
**Narrative:** the story or theme attracting market attention and capital.  
**Regime:** the broader market condition, such as trending, ranging, high-volatility, low-volatility, risk-on, or risk-off.

---

# 8. System architecture

## 8.1 High-level flow

```text
Analysis Request
      |
      v
Asset Resolver and Reality Gate
      |
      v
Data Acquisition -> Data Quality -> Canonical Feature Store
      |
      +-------------------------------------------------------------+
      |              |             |             |                  |
      v              v             v             v                  v
Trend Layer     Momentum Layer  Route Layer   News Layer       History Layer
      |              |             |             |                  |
      +--------------+-------------+-------------+------------------+
                                     |
                                     v
                          Price Memory Layer
                                     |
                                     v
                       Relationship Intelligence Layer
                                     |
                                     v
                          Market Narrative Layer
                                     |
                                     v
                    Pairwise Contrast and Conflict Engine
                                     |
                                     v
                  Forecast, Volatility, and Risk Engines
                                     |
                                     v
                     Evidence Scoring and Calibration
                                     |
                                     v
                  Plain Explanation + Technical Explanation
                                     |
                                     v
                       Decision Report, API, and UI
```

Nodes may execute in parallel once their required data is available. The orchestrator owns dependency resolution rather than forcing the entire system into one serial script.

## 8.2 Node execution contract

Each microscript shall:

1. accept an `AnalysisRequest` or node-specific request;
2. load only required inputs;
3. validate data contracts;
4. execute one bounded analytic action;
5. create one `NodeResult`;
6. save the result to a run-specific path;
7. return a non-zero exit code on failure;
8. never silently invent missing data.

## 8.3 Run directory

```text
runs/
  <timestamp>_<asset>_<horizon>_<run-id>/
    request.json
    manifest.json
    data_quality.json
    nodes/
    layers/
    forecasts/
    final/
      decision_report.json
      decision_report.md
      evidence_board.graphml
      evidence_board.json
    logs/
      run.log
      errors.jsonl
```

## 8.4 IP registry

Every node must have an IP registry entry containing:

- stable node ID;
- node name;
- product name;
- founder-origin note;
- functional description;
- script path;
- input contract;
- output contract;
- dependencies;
- formula or model version;
- test suite;
- commercial packaging option;
- version history;
- status: concept, prototype, tested, production, or deprecated.

The canonical catalog lives in [`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md).

---

# 9. Foundation Gate 0: Asset Reality and Quality

## Purpose

The first question is not only whether the chart looks good. The system must also ask what the asset is and whether enough verifiable substance exists to analyze it seriously.

## Questions

- What exactly is the asset?
- What gives it value or utility?
- Is there real usage, revenue, fees, cash flow, or productive demand?
- How much supply or float is available?
- Are unlocks, emissions, dilution, or insider holdings material?
- Is trading liquid enough for the selected horizon?
- Is ownership or token concentration high?
- Are legal, security, governance, or operational risks material?
- Is the asset active, abandoned, fraudulent, or unverifiable?

## Crypto profile

- protocol or application purpose;
- token utility;
- network activity;
- fee or revenue activity;
- circulating, total, and maximum supply;
- unlock and emission schedule;
- treasury or insider concentration;
- exchange liquidity;
- smart-contract, bridge, validator, governance, and regulatory risk.

## Equity profile

- business model;
- revenue and earnings quality;
- balance-sheet condition;
- cash generation;
- share count and dilution;
- short interest and float;
- trading liquidity;
- customer, supplier, and sector concentration;
- regulatory and litigation risk.

## Outputs

`asset_identity`, `quality_state`, `utility_score`, `liquidity_score`, `dilution_or_supply_risk`, `concentration_risk`, `operational_risk`, `bull_case`, `bear_case`, and `gate_status`.

The gate must allow conclusions such as: **the asset is real, but the current entry may still be poor**.

---

# 10. Layer 1: Trend

## Purpose

Determine whether price is moving up, down, or sideways and how stable that direction is.

## Default configuration

- EMA 13
- EMA 27
- EMA 81
- Multi-timeframe review

An optional reference EMA, including EMA 50, may be configured. The system must not confuse EMA 50 with the RSI midpoint at 50.

## Actions

1. Calculate EMA values.
2. Calculate slopes.
3. Calculate price distance from each EMA.
4. Determine EMA alignment.
5. Detect crossovers and crossover age.
6. Compare timeframes.
7. Classify regime.

## States

Strong uptrend, weak uptrend, early bullish transition, range/compression, early bearish transition, weak downtrend, strong downtrend, or indeterminate.

## Contrast pairs

- short EMA above long EMA versus below;
- rising versus falling slope;
- price above structure versus below;
- daily trend versus weekly trend;
- new crossover versus mature crossover;
- trend strength versus overextension.

---

# 11. Layer 2: Momentum and Reversal

## Purpose

Determine whether buying or selling pressure is strengthening or weakening and whether price is more likely to reverse, continue, or remain uncertain.

## Default configuration

- RSI period: 14
- RSI lower guide: 30
- RSI midpoint: 50
- RSI upper guide: 70
- MACD starting profile: 12, 26, 9
- Stochastic: optional and disabled by default

## Critical product rule

A buy setup may exist even when RSI is not below 30. For example, RSI may recover through the middle area while MACD improves and price holds a key structural or Fibonacci level. The system evaluates confluence rather than enforcing one rigid threshold.

## Actions

1. Calculate RSI.
2. Classify RSI zone and direction.
3. Calculate MACD line, signal line, and histogram.
4. Detect MACD crosses and histogram acceleration.
5. Detect price/indicator divergence.
6. Calculate optional stochastic signals.
7. Measure momentum agreement.
8. Classify reversal versus continuation.

## Reversal states

No reversal evidence, early reversal watch, reversal developing, reversal confirmed by configured rules, temporary bounce inside a downtrend, continuation after consolidation, failed reversal, or mixed.

## Correlation control

RSI, MACD, stochastic, and some moving-average signals derive from the same price history. The final aggregator must reduce duplicated evidence rather than treating several similar indicators as independent witnesses.

---

# 12. Layer 3: Price Structure, Fibonacci, and Bus Stops

## Purpose

Identify the meaningful price swing, calculate Fibonacci levels, explain where price came from, identify likely destinations, and show invalidation.

## Bus-stop model

- **Last bus stop:** most meaningful price area price recently left.
- **Current stop:** present price area.
- **Next bus stop:** nearest meaningful destination in the expected direction.
- **Later bus stops:** secondary targets.
- **Wrong road:** invalidation condition or level.

The product must show both the expected route and the route that disproves the setup.

## Fibonacci anchor logic

For an upward swing:

- lowest meaningful swing low on the left;
- highest meaningful swing high on the right.

For a downward swing, reverse the direction.

Manual anchors, automatic anchors, and manual-versus-automatic comparisons are required.

## Initial configurable Fibonacci levels

23.6%, 38.2%, 50.0%, 61.8%, 78.6%, 100.0%, 127.2%, and 161.8%.

A Fibonacci level is never proof by itself. It grows stronger when it overlaps price memory, volume, prior highs/lows, trend structure, or other independently useful evidence.

## Actions

1. Detect swing highs and lows.
2. Rank candidate anchors.
3. Select or request anchors.
4. Calculate retracement and extension levels.
5. Detect confluence.
6. Identify the last bus stop.
7. Identify ordered next stops up and down.
8. Calculate distance and route reward-to-risk.
9. Define invalidation.
10. Classify route state.

---

# 13. Layer 4: Human Factor, News, Sentiment, and Event Risk

## Purpose

Measure how headlines, political events, economic events, company events, protocol events, and human emotion may affect the asset.

## Core questions

- Does this news affect the asset?
- Is the effect direct or indirect?
- How strong is the connection?
- Is the source reliable?
- Is the event new or already known?
- Is the market reacting in the expected direction?
- Is a major scheduled event close enough to make the trade riskier?

## Event categories

Company-specific, protocol-specific, earnings, product or technology, customer or supplier, sector, regulation, litigation, monetary policy, rates, inflation, employment, government funding/shutdown risk, geopolitics, sanctions, cybersecurity, exchange listing/delisting, token unlock/issuance, M&A, partnerships, institutional action, and social-media-driven events.

## Actions

1. Fetch headlines and event-calendar items.
2. Remove duplicates and near-duplicates.
3. Resolve named entities.
4. Link each event to the selected asset.
5. Classify event type.
6. Score source reliability.
7. Score directness and relevance.
8. Measure sentiment and emotional intensity.
9. Detect novelty.
10. Measure actual price, volume, volatility, and options reaction when available.
11. Apply time decay.
12. Identify scheduled event risk.
13. Produce positive and negative impact paths.

## First-generation event impact model

```text
impact =
    source_reliability
  x entity_link_strength
  x directness
  x exposure
  x novelty
  x sentiment_intensity
  x market_reaction_confirmation
  x time_decay
```

Each factor must remain visible for explanation and audit.

## Market reaction versus headline meaning

The system must compare expected event direction with observed price, volume, volatility, and related-asset reaction. Apparently good news followed by selling should be flagged as a negative reaction divergence.

---

# 14. Layer 5: Historical Context and Analogs

## Purpose

Compare the current setup with similar prior setups that occurred before the current `as_of` time. History provides context, not a promise.

## Questions

- Has this combination of signals happened before?
- What happened next over the selected horizon?
- Was the market regime similar?
- Was volatility similar?
- Was the asset at a similar life-cycle stage?
- How many examples exist?
- Which examples failed?
- Are results stable across time?

## Candidate historical feature vector

Trend state, EMA alignment and slopes, RSI, MACD, divergence, support/resistance distance, Fibonacci location, volatility regime, volume regime, broad market regime, sector regime, news sentiment, narrative state, liquidity, and supply/dilution events.

## Analog retrieval modes

- exact-rule matching;
- nearest-neighbor similarity;
- regime-filtered similarity;
- shape similarity where justified;
- event-conditioned analogs;
- same-asset analogs;
- cross-asset analogs with lower default weight.

## Outcome measurements

- returns after configured periods;
- upside stop reached before invalidation;
- downside stop reached first;
- maximum favorable excursion;
- maximum adverse excursion;
- time to target;
- time to failure.

The strongest historical counterexamples must be returned, not merely successful matches.

---

# 15. Layer 6: Price Memory, Support, and Resistance

## Purpose

Explain how strongly the market remembers a price area and analyze support and resistance symmetrically.

## Required questions for every level

- When did price first see this area?
- When did price last see it?
- How many independent tests occurred?
- Over what span of time?
- How often did price bounce or reject?
- How large were the reactions?
- Did volume increase near the level?
- Did the level matter on several timeframes?
- Was the level broken and retested?
- Has repeated testing made the level weaker?

The same questions apply to lows and highs.

## Candidate level detection methods

Pivot highs/lows, swing clustering, prior closes and gaps, volume profile, anchored VWAP, density/clustering methods, Fibonacci confluence, moving-average confluence, options open interest when available, and round-number behavior.

## Touch definition

A touch must use a configurable tolerance based on percentage, ATR, volatility, or tick size. Candles within one continuous visit are grouped into one test episode rather than counted as many separate touches.

## Strength factors

- independent test episodes;
- span between first and last test;
- recency;
- bounce/rejection magnitude;
- reaction speed;
- volume;
- multi-timeframe agreement;
- break-and-retest behavior;
- false-break frequency;
- time spent at the level;
- regime;
- repeated-test erosion.

More touches do not always mean stronger support or resistance. Repeated pressure may erode a level.

## Symmetric output

The system compares strongest support below price and strongest resistance above price, including distance, strength, age, tests, reaction size, erosion, and historical break behavior.

---

# 16. Layer 7: Relationship Intelligence and the Evidence Board

## Purpose

Trace how an event may affect the selected asset through direct and indirect relationships.

## Evidence-board metaphor

The interface resembles a crime-scene investigation wall:

- each company, token, person, technology, regulator, sector, event, or macro factor is a tack;
- each relationship is a piece of yarn;
- the user can follow the yarn from headline to selected asset;
- the system shows the source, validity period, confidence, and strength of each link.

## Entity types

Public company, private company, token, protocol, exchange, fund, supplier, customer, competitor, partner, product, technology, chip/component, commodity, sector, industry, country, regulator, government body, executive/person, institutional holder, index, derivative, macro factor, event, and narrative.

## Edge types

Supplies, purchases from, customer of, competes with, partners with, integrates with, owns, invests in, regulates, lists, issues, secures, depends on, uses technology from, exposed to, correlated with, included in index, shares narrative with, shares customers with, shares suppliers with, and derivative of.

## Edge requirements

Each edge must include:

- source;
- source type;
- valid-from date;
- valid-to date if known;
- confidence;
- direct or inferred status;
- exposure magnitude if known;
- last verification date.

## Path search

- default maximum depth: 3;
- user-expandable maximum depth: 6;
- longer paths receive decay;
- weak or unverified edges receive strong penalties;
- cycles and repeated entities are controlled.

## Propagation model

```text
path_impact =
    event_impact
  x product(edge_confidence)
  x product(exposure_weight)
  x path_length_decay
  x timing_relevance
  x observed_market_confirmation
```

The graph must show positive paths, negative paths, offsetting paths, competing explanations, and missing or unverifiable links.

---

# 17. Layer 8: Market Narrative

## Purpose

Identify the story the market is trading. News is an event. A narrative is a continuing story built from repeated events, ideas, price behavior, attention, and expectations.

## Examples

Artificial intelligence growth, lower-rate expectations, higher-for-longer rates, crypto adoption, regulation relief, regulation fear, energy shortages, cybersecurity demand, meme behavior, risk-on, risk-off, short squeeze, institutional accumulation, and dilution fear.

## Narrative stages

Emerging, confirming, accelerating, mainstream, crowded, exhausting, fading, reversing, or unclear.

## Actions

1. Cluster related headlines and discussions.
2. Label narrative topics.
3. Measure mention volume and velocity.
4. Measure sentiment.
5. Measure asset relevance.
6. Measure price and volume confirmation.
7. Identify narrative stage.
8. Search for counter-narratives.
9. Distinguish narrative claims from verified facts.

---

# 18. Pairwise Contrast and Disconfirming-Evidence Engine

## Purpose

Every notion must be checked against its contrast. The engine pairs opposing claims rather than producing one undifferentiated bull list and one undifferentiated bear list.

## Example pairs

- support strength versus resistance strength;
- reversal versus continuation;
- trend improvement versus long-term downtrend;
- positive news versus negative market reaction;
- historical matches versus historical failures;
- direct relationship versus weak indirect relationship;
- growing narrative versus crowding risk;
- real utility versus dilution risk;
- upside bus stop versus downside invalidation.

## Pair object

Each pair contains:

`pair_id`, `question`, side labels, side scores, evidence for both sides, shared uncertainty, missing data, dominant side, margin, invalidation conditions, and plain-language explanation.

## Disconfirming-evidence search

Before finalizing a result, the system asks:

1. What evidence would make the opposite view stronger?
2. Is that evidence present?
3. Is relevant data missing?
4. Are the strongest signals all derived from the same source?
5. Is the result dependent on one fragile assumption?
6. Has the market behaved differently under similar conditions?

## Normalization

A two-sided evidence split always totals 100. If one side is 56, the opposite side is 44.

---

# 19. Evidence Scoring and Confidence

## Evidence item dimensions

Each evidence item includes:

- direction;
- strength 0..1;
- relevance 0..1;
- source reliability 0..1;
- freshness 0..1;
- model/rule reliability 0..1;
- independence adjustment 0..1;
- data-quality adjustment 0..1;
- explanation;
- provenance.

## Contribution formula

```text
contribution =
    direction_sign
  x strength
  x relevance
  x source_reliability
  x freshness
  x model_reliability
  x independence_adjustment
  x data_quality_adjustment
```

`direction_sign` is +1 for bullish/positive, -1 for bearish/negative, and 0 for neutral/unknown.

## Node net score

```text
node_net =
  sum(contribution)
  / sum(absolute_possible_weight)
```

Constrain to `[-1, +1]`.

## Evidence split

```text
bull_evidence = round(50 * (node_net + 1))
bear_evidence = 100 - bull_evidence
```

A net score of 0.12 becomes approximately 56/44.

## Confidence

Confidence remains separate from evidence direction. It combines data coverage, data quality, source reliability, feature agreement, model calibration, historical sample size, freshness, and regime stability.

A conservative combination such as a geometric mean is preferred so one very weak factor can materially lower confidence.

## Probability rule

The system may show forecast probability only when the event is clearly defined, the model is tested out of sample using chronological validation, the probability is calibrated, and the model version plus test window are stored.

Example:

> Probability that the first upside bus stop is reached before invalidation within 20 trading days.

---

# 20. Forecasting and Prediction Engine

## Forecast targets

- next upside stop before invalidation;
- next downside stop before recovery target;
- reversal;
- continuation;
- expected return distribution;
- expected price range;
- expected time to next stop;
- volatility;
- maximum adverse excursion;
- maximum favorable excursion.

## Model ladder

### Baselines

No-change/last-value, historical mean or drift, moving-average baseline, exponential smoothing, and linear/regularized lag-feature models.

### Statistical models

ARIMA/SARIMAX, state-space models, vector autoregression when justified, Markov/regime-switching models, and GARCH-family volatility models.

### Machine-learning models

Gradient boosting, random forest/extra trees, XGBoost, LightGBM, CatBoost, calibrated classification, and quantile regression.

### Advanced optional models

Bayesian models, hidden-state models, neural forecasting, transformer-based time-series models, and graph-informed models.

Advanced models do not enter production merely because they are more complex. They must improve out-of-sample performance, calibration, stability, or useful uncertainty estimates.

## Champion/challenger

One production champion per prediction target and asset profile, plus challenger models tested on the same walk-forward schedule. Promotion requires documented improvement.

## Time-series validation

- train only on past data;
- test on later data;
- use rolling or expanding windows;
- support a gap between train and test;
- fit preprocessing only on training data;
- separate tuning, validation, and final testing;
- detect and block future leakage.

## Metrics

Classification: precision, recall, F1, balanced accuracy, ROC-AUC where appropriate, PR-AUC, and confusion matrix.  
Probability: Brier score, log loss, reliability diagrams, expected calibration error.  
Forecast: MAE, RMSE, MASE, quantile loss, interval coverage.  
Trading path: target before invalidation, time to target, MFE, MAE, transaction-cost-adjusted return, drawdown, profit factor, and exposure-adjusted return.

---

# 21. Risk and Trade-Route Engine

## Required outputs

Entry watch zone, entry confirmation condition, last bus stop, next upside stops, next downside stops, invalidation, volatility state, liquidity state, event-risk warning, route reward-to-risk, gap/slippage risk, and optional position-size support only when the user provides explicit risk rules.

## Action states

Avoid, wait, watch, early setup, confirming setup, enter only on a defined condition, hold and monitor, reduce risk, exit condition reached, or insufficient data.

Automated execution is outside the initial release.

---

# 22. Explanation Engine

Every node and final report must create both:

1. `plain_language_explanation`
2. `technical_explanation`

## Plain-language rules

The default explanation uses short sentences, familiar words, defined terms, no unexplained abbreviations, main point first, strongest opposing point, and a clear statement of what would change the conclusion. Target reading level: approximately fourth to fifth grade.

Example:

> Price is trying to turn up. The short trend lines are getting better. Buyers are also getting stronger. But price is still under a strong ceiling. This is a watch setup, not a clear buy yet.

## Technical explanation

Must include input range, timeframe, parameters, formulas or library versions, signal timestamps, evidence contributions, counter-evidence, confidence components, model version, backtest metrics, freshness, and provenance.

## Explain Why object

No node is valid without a main conclusion, reason, strongest support, strongest opposition, missing information, and invalidation condition.

---

# 23. Canonical Data Contracts

## AnalysisRequest

```json
{
  "asset": "HYPE-USD",
  "asset_class": "crypto",
  "as_of": "2026-08-27T18:00:00Z",
  "horizon": "2-6w",
  "timeframes": ["4h", "1d", "1w"],
  "profile": "swing_weeks_v1",
  "manual_fibonacci": null,
  "include_options": false,
  "include_social": true,
  "max_relationship_depth": 3,
  "language_mode": "simple_and_technical"
}
```

## EvidenceItem

```json
{
  "evidence_id": "ev_01J...",
  "node_id": "L2-002",
  "direction": "bullish",
  "claim": "RSI rose through the midpoint while price held support.",
  "strength": 0.72,
  "relevance": 0.90,
  "source_reliability": 1.00,
  "freshness": 0.98,
  "model_reliability": 0.74,
  "independence_adjustment": 0.65,
  "data_quality_adjustment": 0.95,
  "effective_contribution": 0.294,
  "source_refs": ["market_bar_set_123"],
  "observed_at": "2026-08-27T16:00:00Z"
}
```

## NodeResult

```json
{
  "node_id": "L2-006",
  "node_version": "1.0.0",
  "run_id": "run_01J...",
  "asset": "HYPE-USD",
  "as_of": "2026-08-27T18:00:00Z",
  "status": "success",
  "state": "early_reversal_watch",
  "bull_evidence": 56,
  "bear_evidence": 44,
  "confidence": 0.63,
  "confidence_label": "medium",
  "evidence": [],
  "counter_evidence": [],
  "missing_data": [],
  "invalidation_conditions": [],
  "plain_language_explanation": "Price may be trying to turn up, but the turn is not proven yet.",
  "technical_explanation": "RSI and MACD improved, but the weekly trend remains negative.",
  "data_freshness": {},
  "provenance": []
}
```

## PriceStop

Each price stop stores a type, price zone, rank, strength, distance, first/last seen, independent test episodes, average reaction, erosion, confluence, and plain-language explanation.

## Final DecisionReport

The final report stores overall action state, bull/bear evidence, confidence, asset quality, reversal state, last and next bus stops, invalidation, supporting factors, opposing factors, event risks, historical context, relationship paths, narrative state, forecast, both explanations, and provenance.

---

# 24. Python Repository and Microscript Design

## Proposed repository structure

```text
app-market-compass/
  Makefile
  pyproject.toml
  uv.lock
  README.md
  .env.example
  config/
    default.yaml
    logging.yaml
    profiles/
      swing_weeks_v1.yaml
      crypto_v1.yaml
      equity_v1.yaml
  schemas/
    analysis_request.schema.json
    evidence_item.schema.json
    node_result.schema.json
    decision_report.schema.json
  src/
    market_compass/
      contracts/
      core/
      data/
      nodes/
        foundation/
        trend/
        momentum/
        route/
        news/
        history/
        price_memory/
        relationships/
        narrative/
        forecast/
        risk/
        explain/
      contrast/
      orchestrator/
      backtest/
      api/
      reports/
      cli/
  tests/
    unit/
    integration/
    contracts/
    golden/
    leakage/
    backtest/
    performance/
  notebooks/
    research_only/
  data/
    raw/
    normalized/
    features/
  models/
    registry/
  runs/
```

## Node command contract

```bash
python -m market_compass.orchestrator.run_node \
  --node L2-001 \
  --request runs/<run-id>/request.json \
  --output runs/<run-id>/nodes/L2-001_rsi.json
```

## Makefile launch surface

```makefile
setup:
	uv sync

analyze:
	python -m market_compass.orchestrator.run_pipeline \
		--asset "$(ASSET)" \
		--horizon "$(HORIZON)" \
		--profile "$(PROFILE)"

node:
	python -m market_compass.orchestrator.run_node \
		--node "$(NODE)" \
		--request "$(REQUEST)"

layer:
	python -m market_compass.orchestrator.run_layer \
		--layer "$(LAYER)" \
		--request "$(REQUEST)"

backtest:
	python -m market_compass.backtest.walk_forward \
		--strategy "$(STRATEGY)" \
		--asset "$(ASSET)"

test:
	pytest

lint:
	ruff check .
	mypy src

format:
	ruff format .
```

The production Makefile must validate required variables and provide useful usage output.

## Orchestrator responsibilities

Dependency resolution, safe parallelism, timeouts, retry of idempotent actions, immutable-input caching, version recording, visible partial failures, run manifests, confidence penalties for noncritical missing nodes, and blocking final conclusions when critical data is missing.

---

# 25. IP Node Registry

The complete stable node catalog is maintained separately in [`IP-NODE-REGISTRY.md`](IP-NODE-REGISTRY.md). It preserves the foundation, data, trend, momentum, route, news, history, price-memory, relationship, narrative, contrast, forecast, risk, explanation, orchestration, backtest, monitoring, and IP-lineage nodes as independently buildable products.

---

# 26. Functional Requirements

## Request and configuration

- **FR-001:** select an asset.
- **FR-002:** select a horizon.
- **FR-003:** select one or more timeframes.
- **FR-004:** preserve exact `as_of` time.
- **FR-005:** configure indicator periods and thresholds.
- **FR-006:** default swing profile uses RSI 14 with 30/50/70 guides and EMA 13/27/81.
- **FR-007:** stochastic is optional and off by default.
- **FR-008:** Fibonacci supports automatic and manual anchors.

## Node execution

- **FR-009:** every node is independently executable.
- **FR-010:** every node returns a validated `NodeResult`.
- **FR-011:** every node returns supporting and opposing evidence.
- **FR-012:** every node returns missing-data and invalidation fields.
- **FR-013:** every node records version and provenance.
- **FR-014:** noncritical node failure permits labeled partial results.
- **FR-015:** critical missing data prevents an unsupported final action state.

## Scoring

- **FR-016:** bull and bear evidence total 100.
- **FR-017:** confidence is separate from the evidence split.
- **FR-018:** correlated indicators receive an independence penalty.
- **FR-019:** uncalibrated evidence is never labeled probability.
- **FR-020:** final report shows strongest evidence on both sides.

## Price route

- **FR-021:** identify last bus stop.
- **FR-022:** identify ordered upside and downside stops.
- **FR-023:** define invalidation.
- **FR-024:** explain why each stop matters.
- **FR-025:** analyze support and resistance symmetrically.

## News and relationships

- **FR-026:** classify direct and indirect news relevance.
- **FR-027:** show source reliability.
- **FR-028:** compare headline meaning with market reaction.
- **FR-029:** show scheduled event risk.
- **FR-030:** return relationship paths with source provenance.
- **FR-031:** allow graph-depth expansion up to configured maximum.
- **FR-032:** visibly penalize weak long paths.

## History and forecasting

- **FR-033:** historical analogs only use information available at each simulated decision time.
- **FR-034:** analog results show sample size and counterexamples.
- **FR-035:** forecasts are compared with simple baselines.
- **FR-036:** time-series models use rolling or expanding validation.
- **FR-037:** backtests support transaction costs and slippage.
- **FR-038:** probability output includes calibration status.

## Explanations and reports

- **FR-039:** every result has simple and technical explanations.
- **FR-040:** simple explanation targets fourth- to fifth-grade reading level.
- **FR-041:** report shows data freshness.
- **FR-042:** report shows unresolved conflicts.
- **FR-043:** report includes main case, counter-case, and invalidation.
- **FR-044:** evidence board is exportable as JSON and graph format.
- **FR-045:** final report is reproducible from its run manifest.

## Productization

- **FR-046:** each node is discoverable through a registry.
- **FR-047:** each node declares dependencies and contracts.
- **FR-048:** each layer is packageable as a separate API product.
- **FR-049:** node versions are backward compatible or explicitly migrated.
- **FR-050:** founder origin and version lineage are retained.

---

# 27. User Interface Requirements

The main analysis screen shall include asset, horizon, timeframe, freshness, overall evidence, confidence, asset reality, reversal-vs-continuation, bus-stop route, support-vs-resistance, news/event risk, historical analogs, evidence board, narrative, main counter-case, invalidation, simple/technical toggle, and provenance drawer.

## Overall evidence card

Must show current action state, bull evidence, bear evidence, confidence, main reason, strongest opposing reason, and next decision condition.

## Bus-stop route

```text
Downside Stop 2 <- Downside Stop 1 <- Current Price -> Upside Stop 1 -> Upside Stop 2
                                  |
                             Invalidation
```

Each stop opens its price zone, level type, test history, reaction size, confluence, strength, erosion, and explanation.

## Evidence board

The graph view supports relationship filters, direct-first paths, indirect expansion, verified-versus-inferred markings, source/date inspection, positive/negative/neutral/uncertain paths, and hiding weak paths.

## Accessibility

Color is never the only way to encode positive/negative states. Graph nodes and edges have labels. Simple-mode reading level is tested automatically.

---

# 28. API Requirements

Initial endpoints:

```text
POST   /v1/analyses
GET    /v1/analyses/{run_id}
GET    /v1/analyses/{run_id}/report
GET    /v1/analyses/{run_id}/nodes
GET    /v1/analyses/{run_id}/nodes/{node_id}
POST   /v1/nodes/{node_id}/run
GET    /v1/nodes
GET    /v1/assets/{asset}/evidence-board
POST   /v1/backtests
GET    /v1/backtests/{backtest_id}
GET    /v1/models
GET    /v1/health
```

All responses include schema versions. Long-running analysis returns a run ID. Partial results are queryable. Errors identify the failing node. Secrets never appear in errors or logs. Idempotency keys are supported where appropriate.

---

# 29. Data and Storage Requirements

## Initial local/research stack

- Parquet for immutable market and feature data;
- Apache Arrow for in-memory interchange;
- DuckDB for local analytical queries;
- JSON for node results and manifests;
- GraphML or JSON for relationship exports.

## Production options

PostgreSQL or a time-series extension for operational data, object storage for raw/feature data, and a graph database such as Neo4j if graph scale exceeds local NetworkX needs.

## Data lineage

Every dataset records provider, retrieval time, market time, timezone, symbol mapping, corporate-action adjustment status, missing intervals, corrections, license/permitted use, and version/hash.

## Quality gates

Detect stale data, missing bars, duplicate bars, timestamp ordering problems, impossible values, symbol changes, split/dividend adjustment errors, timezone errors, future news in historical runs, and expired graph edges.

---

# 30. Recommended Python Technology Stack

## Core numerical/data

NumPy, SciPy, Polars, pandas, PyArrow, DuckDB, and Numba when profiling justifies acceleration.

## Technical analysis

TA-Lib for established indicators plus audited custom implementations for founder-specific price-memory, bus-stop, contrast, and scoring logic.

## Statistics and forecasting

statsmodels, `arch`, scikit-learn, and a scikit-learn-compatible forecasting wrapper when useful.

## Machine learning

XGBoost, LightGBM, CatBoost, PyTorch only when justified, PyMC for Bayesian uncertainty, Optuna for controlled hyperparameter optimization, and MLflow for experiment/model tracking.

## Graph and language intelligence

NetworkX initially, optional Neo4j at larger scale, spaCy for entity extraction/rules, transformers and sentence-transformers for classification and semantic matching.

## Explainability

SHAP for compatible predictive models, deterministic rule explanations for rule nodes, and custom evidence-contribution explanations for final scoring. Predictive explanation must never be described as causal proof.

## Backtesting

vectorbt for fast vectorized research plus custom event-driven simulation for route-first targets, event handling, and complex execution assumptions.

## Contracts, API, and quality

Pydantic, FastAPI, pytest, Hypothesis, Pandera, Ruff, mypy, and pre-commit.

## UI

Streamlit/Plotly for fast research UI; React or Next.js against FastAPI for a production interface.

---

# 31. Backtesting, Calibration, and Audit

- No node may read data after the simulated `as_of` time.
- Signals and models use chronological rolling or expanding validation.
- Transaction fees, bid-ask spread, slippage, perpetual funding, borrow costs, and options spread/volatility effects are supported where relevant.
- Bias audits cover look-ahead, leakage, survivorship, selection, overfitting, multiple testing, regime concentration, and revised data.
- Every backtest stores code version, config, dataset version, model version, seed, windows, costs, results, exceptions, and excluded periods.

---

# 32. Testing Requirements

## Unit tests

Every node gets formula, edge-case, missing-data, and invalid-input tests.

## Contract tests

Every script is checked against Pydantic and JSON schemas.

## Golden tests

Known datasets produce stable expected outputs within tolerance.

## Property-based tests

Examples:

- bull plus bear evidence always equals 100;
- confidence remains in `[0,1]`;
- stop low cannot exceed stop high;
- future data is never used in historical runs;
- longer unverified graph paths cannot gain weight merely for being longer;
- duplicate correlated indicators cannot increase confidence without limit.

## Founder-idea tests

1. RSI 14 uses 30, 50, and 70 guides by default.
2. EMA 13, 27, and 81 are calculated and compared.
3. Stochastic stays disabled unless requested.
4. An early buy watch can exist when RSI is above 30.
5. Fibonacci supports the meaningful low-left to high-right upward swing.
6. Support and resistance use the same strength framework.
7. A bull score of 56 yields a bear score of 44.
8. Every node includes the opposing case.
9. Bus-stop route contains last stop, next stop, and invalidation.
10. Historical analogs include counterexamples.
11. News relevance can travel through a relationship path.
12. Evidence-board edges preserve sources.
13. Simple explanations meet configured reading-level targets.

## Integration tests

Crypto analysis, equity analysis, no-news scenario, stale-data scenario, conflicting-timeframe scenario, high-volatility event scenario, and missing-relationship-data scenario.

---

# 33. Non-Functional Requirements

Reliability, reproducibility, observability, security, data licensing, explainability, and extensibility are required from the beginning.

- Node failures are isolated.
- Critical failures block unsupported conclusions.
- Deterministic nodes reproduce from identical inputs.
- Logs include run ID, node ID, timestamps, input hashes, outputs, freshness, errors, retries, and model version.
- Secrets use environment variables or a secret manager and never enter source control.
- External content is treated as untrusted input.
- Data licensing tracks whether information may be stored, displayed, redistributed, and used commercially.
- New nodes are registered rather than hard-coded into one giant decision script.

---

# 34. Product Metrics

## Trust/explanation

Complete provenance rate, two-sided-evidence rate, explanation completeness, reading-level pass rate, counter-evidence inspection, and source-path inspection.

## Model metrics

Precision/recall by signal, Brier score, calibration error, interval coverage, target-before-invalidation accuracy, regime performance, and asset-class performance.

## System metrics

Node success rate, full-run success rate, data freshness, latency, cache hit rate, API error rate, and stale graph-edge rate.

## Product metrics

Analyses completed, reports saved, user overrides, most-used standalone nodes, and repeat usage by asset and horizon.

---

# 35. Risks and Mitigations

## False precision

Users may treat 56/44 as exact odds. Mitigation: label it evidence balance; show probability only after calibration.

## Indicator double counting

RSI, MACD, stochastic, and trend signals can overlap. Mitigation: correlation/independence penalties.

## Overfitting

Complex models may fit history and fail live. Mitigation: baselines, walk-forward testing, held-out periods, regime reporting, and simple champion models when competitive.

## Data leakage

Future information can contaminate testing. Mitigation: strict `as_of` filtering, pipelines, immutable snapshots, and leakage tests.

## Weak news sources

Rumors may resemble facts. Mitigation: source tiers, corroboration, uncertainty, and provenance.

## Graph explosion

Six degrees of separation can create mountains of weak links. Mitigation: default depth 3, path decay, source requirements, exposure weighting, and controlled expansion.

## Correlation mistaken for causation

Co-movement does not establish a business link. Mitigation: mark inferred edges, separate association from verified relationships, and show competing explanations.

## Regime change

Historical analogs can fail under changed market structure. Mitigation: regime matching, recency weighting, counterexamples, and lower confidence.

## Level overconfidence

Support/resistance are not exact walls. Mitigation: zones, volatility-based tolerances, erosion, and invalidation.

## Narrative crowding

A popular story may already be priced. Mitigation: narrative-stage, crowding, and price-reaction confirmation.

## Legal/regulatory boundary

Decision support may be mistaken for individualized investment advice or execution. Mitigation: transparent assumptions, no automatic trading in V1, user-controlled risk, and legal review before commercialization.

---

# 36. Delivery Roadmap

## Phase A: Foundation and technical core

Repository/contracts, Makefile, orchestrator, asset resolver, data quality, asset reality gate, trend, momentum, Fibonacci/bus-stop route, contrast scoring, and explanations.

## Phase B: Price memory and historical context

Support/resistance history, test episodes, erosion, break/retest, historical feature snapshots, analog retrieval, and counterexamples.

## Phase C: News and relationship intelligence

News ingestion, event classification, relevance, market reaction, entity graph, path search, and evidence-board interface.

## Phase D: Narrative and forecasting

Narrative clustering/stages, baseline forecasts, statistical and ML challengers, volatility forecasts, and calibration.

## Phase E: Product interface and API

FastAPI, research interface, simple/technical views, saved reports, and graph exploration.

## Phase F: Options and advanced execution research

Options chain and implied volatility, open-interest price memory, multi-leg strategy analysis, event-driven simulation, and broker integration only after separate security, regulatory, and safety review.

---

# 37. Definition of Done for Version 1

Version 1 is complete when:

1. `make analyze ASSET=<asset> HORIZON=2-6w PROFILE=swing_weeks_v1` produces a complete run.
2. Every required node emits a valid `NodeResult`.
3. Every node includes support, opposition, missing data, and invalidation.
4. Final evidence split totals 100.
5. Confidence is calculated separately.
6. Report identifies last bus stop, next stops, and invalidation.
7. Support and resistance include historical test counts and time spans.
8. News is linked directly or indirectly with provenance.
9. Historical analogs include counterexamples.
10. Evidence board can be exported.
11. User can switch between simple and technical explanations.
12. Backtests use time-respecting validation.
13. Leakage tests pass.
14. A crypto example and an equity example complete end to end.
15. IP registry lists every production node and version.
16. No automatic trade is placed.

---

# 38. Conversation-to-IP Audit

This audit ensures the original product concepts remain explicitly represented.

1. **“What is HYPE, and is it real or bull junk?”** -> Foundation Gate 0.
2. **Trading horizon measured in weeks.** -> `swing_weeks_v1` and multi-week horizon.
3. **RSI 30 bottom, 50 middle, 70 top.** -> Layer 2 defaults.
4. **RSI 14-period signal.** -> RSI node configuration.
5. **MACD with RSI.** -> separate momentum node and confluence input.
6. **Fibonacci with momentum.** -> route layer and confluence.
7. **Buy signal may exist even if RSI is not under 30.** -> reversal logic.
8. **Stochastic may overcomplicate things.** -> optional, disabled by default.
9. **EMA 13, 27, 81.** -> trend profile.
10. **The 50 reference point.** -> RSI midpoint by default; optional EMA 50 remains separately configurable.
11. **Reversal versus continuation.** -> dedicated node and contrast pair.
12. **Next bus stop and last place price left.** -> route model.
13. **Human behavior and headlines.** -> Layer 4.
14. **Political, geopolitical, Fed, shutdown, and broad events.** -> event taxonomy.
15. **Market mood and emotion.** -> sentiment, emotional intensity, market reaction, narrative.
16. **Historical context measured against what happened before.** -> Layer 5.
17. **History is an indicator, not a guarantee.** -> confidence and product principle.
18. **Fibonacci high right / low left for upward swing.** -> anchor logic.
19. **How long ago and how often price saw an area.** -> price memory.
20. **True support over time.** -> support-strength scoring.
21. **Equal analysis of highs and resistance.** -> symmetric price memory.
22. **Count high hits and rejections.** -> rejection statistics.
23. **News may affect BlackBerry through a chip developer or connected company.** -> relationship paths.
24. **Six degrees of separation can move assets unexpectedly.** -> graph depth up to six, with default depth three.
25. **Crime-scene board with thumbtacks and yarn.** -> Evidence Board UI.
26. **Trace where impact came from.** -> edge provenance and path tracing.
27. **Market narrative as a separate factor.** -> Layer 8.
28. **Each layer must be an action.** -> node action definitions.
29. **Each action must be a Python microscript.** -> repository architecture.
30. **Each notion must be checked against its contrast.** -> pairwise contrast engine.
31. **Show the opposite side of every score.** -> normalized two-sided evidence.
32. **Explain derivatives of each contrast.** -> evidence dimensions and explanations.
33. **Each idea is IP and remains a node.** -> stable IP registry.
34. **Each feature is also a product.** -> modular packaging requirement.
35. **Serve junior and senior engineers.** -> plain definitions plus technical contracts.
36. **Use multiple Python scripts, not one large script.** -> microscript architecture.
37. **Use a Makefile to call scripts.** -> launch surface.
38. **Use sophisticated mathematics, prediction, and forecasting libraries.** -> technology stack and model ladder.
39. **Every result must explain why.** -> Explain Why object.
40. **Actively search for disconfirming evidence.** -> dedicated disconfirming engine.
41. **Score and test agents independently.** -> node contracts, independent tests, calibration, precision, recall, and reproducible execution.

No core product idea in the originating discussion should be collapsed into an unnamed generic feature.

---

# 39. Engineering Decision Notes

## Makefile and Python orchestrator

The Makefile remains the clean developer launch surface. Python owns dependencies, concurrency, caching, retries, manifests, and execution because those responsibilities become brittle when hidden inside Make recipes.

## Sophistication without decorative complexity

Preferred progression:

1. correct deterministic rules;
2. strong statistical baselines;
3. interpretable machine-learning models;
4. calibrated ensembles;
5. advanced Bayesian, neural, or graph models only after measurable improvement.

## Founder configuration versus learned weights

The first system uses explicit founder-defined rules and configurable weights. Later versions may learn weights from walk-forward tests, but learned weights must remain inspectable and must not erase the founder-defined node structure.

## Decision support, not a black box

The differentiation is the evidence architecture:

- one node per idea;
- one script per action;
- one paired contrast per conclusion;
- one provenance trail per fact;
- one simple explanation per result;
- one technical explanation per result.

---

# 40. Research Basis for Technical Choices

The planned stack is grounded in current official documentation for the selected tools:

- TA-Lib provides established technical-analysis functions including RSI, MACD, stochastic indicators, and candlestick functions.
- NetworkX supports graph creation, manipulation, path search, and network analysis.
- statsmodels provides classical time-series, state-space, autoregressive, vector-autoregressive, and regime-related methods.
- scikit-learn provides pipelines, calibration, model evaluation, and time-aware splitting; its guidance also warns against leakage from future information.
- vectorbt provides high-performance vectorized backtesting and portfolio research.
- SHAP supports feature attribution for compatible predictive models but must not be misrepresented as causal proof.
- Polars, Apache Arrow, and DuckDB support efficient columnar analytical workflows.
- Optuna supports hyperparameter optimization and MLflow supports experiment/model tracking.
- Pydantic provides typed Python data validation.

The tools are implementation components. The founder-specific intellectual property is in the node definitions, paired contrast architecture, bus-stop route, price-memory model, relationship evidence board, and evidence/confidence system.

---

# 41. Reference Sources

- TA-Lib: https://ta-lib.org/
- TA-Lib function catalog: https://ta-lib.org/functions/
- NetworkX: https://networkx.org/
- statsmodels time series: https://www.statsmodels.org/stable/tsa.html
- statsmodels state space: https://www.statsmodels.org/stable/statespace.html
- scikit-learn TimeSeriesSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- scikit-learn common pitfalls: https://scikit-learn.org/stable/common_pitfalls.html
- vectorbt: https://vectorbt.dev/
- SHAP: https://shap.readthedocs.io/
- DuckDB Python: https://duckdb.org/docs/stable/clients/python/overview
- Apache Arrow datasets: https://arrow.apache.org/docs/python/dataset.html
- Polars: https://docs.pola.rs/
- Optuna: https://optuna.org/
- MLflow: https://mlflow.org/docs/latest/
- Pydantic: https://docs.pydantic.dev/
- arch volatility forecasting: https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_forecasting.html

---

# 42. Canonical Product Statement

Market Compass is not another chart covered in indicators. It is a transparent market evidence engine.

It asks what the asset is, what price is doing, where price has been, where price may go, what people are reacting to, what happened in similar cases, what companies and events are connected, and what story the market is trading.

Then it shows both sides.

It explains the route.

It explains the risk.

It explains why.

Every idea remains its own node, script, feature, and product.
