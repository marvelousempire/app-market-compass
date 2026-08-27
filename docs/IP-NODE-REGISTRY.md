# Market Compass IP Node Registry

**Version:** 1.0  
**Date:** August 27, 2026  
**Purpose:** Stable catalog of independently buildable Market Compass capabilities.

This registry preserves each product idea as a node. Every node is intended to have a stable ID, Python implementation path, input/output contract, tests, provenance, version history, and a clear relationship to the canonical PRD.

The node IDs below are the initial stable naming scheme. File paths are proposed implementation paths and may move before code is production, but node IDs should remain stable once implementation begins.

---

# 1. Foundation Nodes

- **F0-001 — Asset Resolver** — `src/market_compass/nodes/foundation/asset_resolver.py` — Resolves symbol, venue, chain, company, instrument, and asset class.
- **F0-002 — Instrument Identity** — `src/market_compass/nodes/foundation/instrument_identity.py` — Confirms what the user can actually buy or trade.
- **F0-003 — Utility or Business Model** — `src/market_compass/nodes/foundation/utility_business_model.py` — Explains what creates demand or value.
- **F0-004 — Supply, Float, and Capital Structure** — `src/market_compass/nodes/foundation/supply_float.py` — Measures circulating supply, float, share count, and capital structure.
- **F0-005 — Unlock and Dilution Risk** — `src/market_compass/nodes/foundation/unlock_dilution.py` — Identifies scheduled or likely new supply.
- **F0-006 — Revenue, Fees, or Cash-Flow Evidence** — `src/market_compass/nodes/foundation/economic_activity.py` — Measures productive economic activity.
- **F0-007 — Liquidity and Concentration** — `src/market_compass/nodes/foundation/liquidity_concentration.py` — Measures tradability, float/holder concentration, and liquidity quality.
- **F0-008 — Legitimacy and Operational Risk Gate** — `src/market_compass/nodes/foundation/legitimacy_gate.py` — Scores fraud, abandonment, security, governance, and verification risks.

---

# 2. Data Nodes

- **D-001 — Price-Bar Loader** — `src/market_compass/data/market_data.py`
- **D-002 — Volume and Order-Book Loader** — `src/market_compass/data/order_book_data.py`
- **D-003 — Options-Chain Loader** — `src/market_compass/data/options_data.py`
- **D-004 — News and Event Loader** — `src/market_compass/data/news_data.py`
- **D-005 — Macro Calendar Loader** — `src/market_compass/data/macro_data.py`
- **D-006 — Entity and Relationship Loader** — `src/market_compass/data/relationship_data.py`
- **D-007 — Narrative and Attention Loader** — `src/market_compass/data/narrative_data.py`
- **D-008 — Data Quality and Freshness** — `src/market_compass/data/quality.py`

---

# 3. Trend Nodes

- **L1-001 — EMA Calculator** — `src/market_compass/nodes/trend/ema_calculator.py`
- **L1-002 — EMA Alignment** — `src/market_compass/nodes/trend/ema_alignment.py`
- **L1-003 — EMA Slope** — `src/market_compass/nodes/trend/ema_slope.py`
- **L1-004 — Crossover State** — `src/market_compass/nodes/trend/crossover_state.py`
- **L1-005 — Multi-Timeframe Trend** — `src/market_compass/nodes/trend/multi_timeframe.py`
- **L1-006 — Trend Regime Classifier** — `src/market_compass/nodes/trend/trend_regime.py`

Founder starting profile: EMA 13, 27, and 81, with optional separately configured EMA 50 support.

---

# 4. Momentum and Reversal Nodes

- **L2-001 — RSI Calculator and State** — `src/market_compass/nodes/momentum/rsi_state.py`
- **L2-002 — RSI Midpoint and Zone Transitions** — `src/market_compass/nodes/momentum/rsi_transitions.py`
- **L2-003 — MACD Calculator and State** — `src/market_compass/nodes/momentum/macd_state.py`
- **L2-004 — Momentum Divergence** — `src/market_compass/nodes/momentum/divergence.py`
- **L2-005 — Optional Stochastic** — `src/market_compass/nodes/momentum/stochastic_optional.py`
- **L2-006 — Momentum Confluence** — `src/market_compass/nodes/momentum/momentum_confluence.py`
- **L2-007 — Reversal Versus Continuation** — `src/market_compass/nodes/momentum/reversal_continuation.py`

Founder starting profile: RSI 14 with 30, 50, and 70 guides; stochastic disabled by default.

---

# 5. Route and Fibonacci Nodes

- **L3-001 — Pivot Detector** — `src/market_compass/nodes/route/pivot_detector.py`
- **L3-002 — Swing Ranker** — `src/market_compass/nodes/route/swing_ranker.py`
- **L3-003 — Fibonacci Anchor Selector** — `src/market_compass/nodes/route/fibonacci_anchors.py`
- **L3-004 — Fibonacci Level Calculator** — `src/market_compass/nodes/route/fibonacci_levels.py`
- **L3-005 — Confluence Detector** — `src/market_compass/nodes/route/level_confluence.py`
- **L3-006 — Last Bus Stop** — `src/market_compass/nodes/route/last_bus_stop.py`
- **L3-007 — Next Bus Stops** — `src/market_compass/nodes/route/next_bus_stops.py`
- **L3-008 — Route and Invalidation** — `src/market_compass/nodes/route/route_invalidation.py`

The route family is a named product capability. It must show where price came from, likely next destinations in both directions, and what invalidates the present route.

---

# 6. Human Factor, News, and Event Nodes

- **L4-001 — Headline Deduplicator** — `src/market_compass/nodes/news/headline_deduplicator.py`
- **L4-002 — Entity Linker** — `src/market_compass/nodes/news/entity_linker.py`
- **L4-003 — Event Classifier** — `src/market_compass/nodes/news/event_classifier.py`
- **L4-004 — Source Reliability** — `src/market_compass/nodes/news/source_reliability.py`
- **L4-005 — Sentiment and Emotional Intensity** — `src/market_compass/nodes/news/sentiment_intensity.py`
- **L4-006 — News Relevance and Directness** — `src/market_compass/nodes/news/relevance_directness.py`
- **L4-007 — Market Reaction Analyzer** — `src/market_compass/nodes/news/market_reaction.py`
- **L4-008 — Scheduled Event Risk** — `src/market_compass/nodes/news/event_calendar_risk.py`
- **L4-009 — Event Impact Pair** — `src/market_compass/nodes/news/event_impact_pair.py`

This family must distinguish the meaning of a headline from the market's actual response to it.

---

# 7. Historical Context Nodes

- **L5-001 — Historical Feature Snapshot** — `src/market_compass/nodes/history/feature_snapshot.py`
- **L5-002 — Same-Asset Analog Search** — `src/market_compass/nodes/history/same_asset_analogs.py`
- **L5-003 — Cross-Asset Analog Search** — `src/market_compass/nodes/history/cross_asset_analogs.py`
- **L5-004 — Regime Similarity** — `src/market_compass/nodes/history/regime_similarity.py`
- **L5-005 — Outcome Calculator** — `src/market_compass/nodes/history/analog_outcomes.py`
- **L5-006 — Counterexample Finder** — `src/market_compass/nodes/history/counterexamples.py`
- **L5-007 — Historical Context Summary** — `src/market_compass/nodes/history/history_summary.py`

The counterexample node is mandatory. Historical matching that only searches for successful analogs is not acceptable.

---

# 8. Price Memory Nodes

- **L6-001 — Price-Level Candidate Generator** — `src/market_compass/nodes/price_memory/level_candidates.py`
- **L6-002 — Level Clusterer** — `src/market_compass/nodes/price_memory/level_clusterer.py`
- **L6-003 — Touch-Episode Counter** — `src/market_compass/nodes/price_memory/touch_episodes.py`
- **L6-004 — Bounce and Rejection Statistics** — `src/market_compass/nodes/price_memory/reaction_stats.py`
- **L6-005 — Volume-at-Level Confirmation** — `src/market_compass/nodes/price_memory/volume_confirmation.py`
- **L6-006 — Multi-Timeframe Level Confluence** — `src/market_compass/nodes/price_memory/timeframe_confluence.py`
- **L6-007 — Break and Retest Analyzer** — `src/market_compass/nodes/price_memory/break_retest.py`
- **L6-008 — Level Erosion** — `src/market_compass/nodes/price_memory/level_erosion.py`
- **L6-009 — Support Versus Resistance Pair** — `src/market_compass/nodes/price_memory/support_resistance_pair.py`

This family applies the same evidence model to support and resistance. Repeated tests may validate a level while simultaneously eroding it, so both forces must be represented.

---

# 9. Relationship Intelligence Nodes

- **L7-001 — Entity Graph Builder** — `src/market_compass/nodes/relationships/entity_graph.py`
- **L7-002 — Edge Resolver** — `src/market_compass/nodes/relationships/edge_resolver.py`
- **L7-003 — Edge Provenance and Validity** — `src/market_compass/nodes/relationships/edge_provenance.py`
- **L7-004 — Direct Path Search** — `src/market_compass/nodes/relationships/direct_paths.py`
- **L7-005 — Indirect Path Search** — `src/market_compass/nodes/relationships/indirect_paths.py`
- **L7-006 — Path Decay and Exposure** — `src/market_compass/nodes/relationships/path_impact.py`
- **L7-007 — Counter-Path Search** — `src/market_compass/nodes/relationships/counter_paths.py`
- **L7-008 — Market Confirmation of Path** — `src/market_compass/nodes/relationships/path_confirmation.py`
- **L7-009 — Evidence Board Export** — `src/market_compass/nodes/relationships/evidence_board.py`

The Evidence Board is the crime-scene-wall product metaphor: entities are tacks, relationships are yarn, and every edge must show its source, confidence, validity period, and direct/inferred status.

Default path depth is 3; user-expandable maximum depth is 6 with path-length decay.

---

# 10. Market Narrative Nodes

- **L8-001 — Topic Clusterer** — `src/market_compass/nodes/narrative/topic_clusterer.py`
- **L8-002 — Narrative Labeler** — `src/market_compass/nodes/narrative/narrative_labeler.py`
- **L8-003 — Attention and Velocity** — `src/market_compass/nodes/narrative/attention_velocity.py`
- **L8-004 — Narrative Stage** — `src/market_compass/nodes/narrative/narrative_stage.py`
- **L8-005 — Asset Alignment** — `src/market_compass/nodes/narrative/asset_alignment.py`
- **L8-006 — Price Confirmation and Crowding** — `src/market_compass/nodes/narrative/price_crowding.py`
- **L8-007 — Counter-Narrative Search** — `src/market_compass/nodes/narrative/counter_narrative.py`

Narrative stages: emerging, confirming, accelerating, mainstream, crowded, exhausting, fading, reversing, and unclear.

---

# 11. Shared Contrast and Scoring Nodes

- **C-001 — Evidence Item Validator** — `src/market_compass/core/evidence_validator.py`
- **C-002 — Pairwise Contrast Engine** — `src/market_compass/contrast/pair_engine.py`
- **C-003 — Disconfirming-Evidence Search** — `src/market_compass/contrast/disconfirming_search.py`
- **C-004 — Signal Conflict Detector** — `src/market_compass/contrast/conflict_detector.py`
- **C-005 — Correlation and Double-Count Penalty** — `src/market_compass/core/correlation_penalty.py`
- **C-006 — Evidence Normalizer** — `src/market_compass/core/scoring.py`
- **C-007 — Confidence Calculator** — `src/market_compass/core/confidence.py`

A two-sided evidence split must total 100. Confidence remains a separate quantity.

---

# 12. Forecast Nodes

- **F-001 — Baseline Forecasts** — `src/market_compass/nodes/forecast/baselines.py`
- **F-002 — Statistical Forecasts** — `src/market_compass/nodes/forecast/statistical.py`
- **F-003 — Machine-Learning Forecasts** — `src/market_compass/nodes/forecast/machine_learning.py`
- **F-004 — Volatility Forecast** — `src/market_compass/nodes/forecast/volatility.py`
- **F-005 — Forecast Ensemble** — `src/market_compass/nodes/forecast/ensemble.py`
- **F-006 — Probability Calibration** — `src/market_compass/nodes/forecast/calibration.py`

No advanced forecast becomes the production champion unless it demonstrates measurable out-of-sample value over simpler baselines.

---

# 13. Risk Nodes

- **R-001 — Liquidity Risk** — `src/market_compass/nodes/risk/liquidity_risk.py`
- **R-002 — Volatility Risk** — `src/market_compass/nodes/risk/volatility_risk.py`
- **R-003 — Event Risk** — `src/market_compass/nodes/risk/event_risk.py`
- **R-004 — Route Reward-to-Risk** — `src/market_compass/nodes/risk/route_risk_reward.py`
- **R-005 — Action-State Generator** — `src/market_compass/nodes/risk/action_state.py`

Initial action states: avoid, wait, watch, early setup, confirming setup, enter only on a defined condition, hold and monitor, reduce risk, exit condition reached, and insufficient data.

---

# 14. Explanation Nodes

- **E-001 — Plain-Language Explanation** — `src/market_compass/nodes/explain/plain_language.py`
- **E-002 — Technical Explanation** — `src/market_compass/nodes/explain/technical.py`
- **E-003 — Explanation Completeness Validator** — `src/market_compass/nodes/explain/completeness.py`
- **E-004 — Reading-Level Validator** — `src/market_compass/nodes/explain/reading_level.py`
- **E-005 — Provenance Formatter** — `src/market_compass/nodes/explain/provenance_formatter.py`

Every final explanation must expose the main conclusion, strongest support, strongest opposition, missing data, and invalidation condition.

---

# 15. Orchestration Nodes

- **O-001 — Dependency Graph** — `src/market_compass/orchestrator/dependency_graph.py`
- **O-002 — Node Runner** — `src/market_compass/orchestrator/run_node.py`
- **O-003 — Layer Runner** — `src/market_compass/orchestrator/run_layer.py`
- **O-004 — Pipeline Runner** — `src/market_compass/orchestrator/run_pipeline.py`
- **O-005 — Run Manifest** — `src/market_compass/orchestrator/manifest.py`

The Makefile invokes these interfaces. It does not replace the orchestrator.

---

# 16. Backtest and Validation Nodes

- **B-001 — Walk-Forward Backtest** — `src/market_compass/backtest/walk_forward.py`
- **B-002 — Transaction-Cost Model** — `src/market_compass/backtest/cost_model.py`
- **B-003 — Performance Metrics** — `src/market_compass/backtest/metrics.py`
- **B-004 — Leakage Audit** — `src/market_compass/backtest/leakage_audit.py`

Time-series validation must remain chronological. Random splitting is not a valid default for market forecasting.

---

# 17. Monitoring Nodes

- **M-001 — Data Drift Monitor** — `src/market_compass/monitoring/data_drift.py`
- **M-002 — Model Drift Monitor** — `src/market_compass/monitoring/model_drift.py`
- **M-003 — Calibration Monitor** — `src/market_compass/monitoring/calibration.py`

---

# 18. IP and Lineage Nodes

- **IP-001 — IP Node Registry** — `src/market_compass/core/ip_registry.py`
- **IP-002 — Version and Lineage Recorder** — `src/market_compass/core/version_lineage.py`

Each implemented node should eventually expose registry metadata similar to:

```json
{
  "node_id": "L3-006",
  "name": "Last Bus Stop",
  "version": "0.1.0",
  "status": "prototype",
  "script_path": "src/market_compass/nodes/route/last_bus_stop.py",
  "input_contract": "AnalysisRequest + PriceMemoryContext",
  "output_contract": "NodeResult + PriceStop",
  "dependencies": ["L3-001", "L6-001"],
  "tests": ["tests/unit/test_last_bus_stop.py"],
  "product_capability": "Bus Stop Route"
}
```

---

# 19. Node Contract Law

Every production node must satisfy all of these rules:

1. **One bounded purpose.** The node has one main analytic responsibility.
2. **Stable ID.** The ID does not casually change when code moves.
3. **Explicit inputs.** Required data and dependencies are declared.
4. **Validated outputs.** Results conform to a canonical schema.
5. **Two-sided evidence.** Supporting and opposing evidence are both returned.
6. **Missing data is visible.** Absence is never silently filled with invented information.
7. **Explain Why is mandatory.** A score without a reason is invalid.
8. **Provenance is mandatory.** Source data and calculation versions are recorded.
9. **Time is explicit.** Every market-sensitive result respects `as_of`.
10. **Tests are local.** Each node is independently testable.
11. **Backtest compatibility.** Historical execution cannot see future information.
12. **Commercial independence.** The node should be capable of becoming a standalone API/product without rewriting its core logic.

---

# 20. Contrast Contract

Every node capable of directional or qualitative judgment must emit an opposing case.

Minimum contrast object:

```json
{
  "question": "Is momentum reversing or continuing lower?",
  "side_a_label": "reversal",
  "side_a_score": 56,
  "side_a_evidence": [],
  "side_b_label": "continuation",
  "side_b_score": 44,
  "side_b_evidence": [],
  "missing_data": [],
  "invalidation_conditions": [],
  "plain_language_explanation": "Momentum is improving, but the larger trend is still weak."
}
```

Correlated evidence must be discounted before aggregation so that several versions of the same underlying signal do not impersonate independent witnesses.

---

# 21. Registry Governance

When a new feature is proposed:

1. Determine whether it is genuinely a new node or an extension of an existing node.
2. Assign a stable ID only after the responsibility is clear.
3. Add the node here before production implementation.
4. Define its input/output contracts.
5. Define its contrast requirement.
6. Define its provenance requirement.
7. Define its unit and historical tests.
8. Add it to the dependency graph.
9. Record version history.
10. Update the PRD if the new node changes product behavior.

Do not create dozens of microscopic nodes merely to inflate the catalog. A node exists because it represents a meaningful independent action, test, or piece of product IP. Humans have already invented enough meaningless abstraction layers.

---

# 22. Canonical Product Families

The node registry resolves upward into these product families:

1. **Asset Reality**
2. **Trend**
3. **Momentum & Reversal**
4. **Bus Stop Route & Fibonacci**
5. **Human Factor & Event Risk**
6. **Historical Mirror**
7. **Price Memory**
8. **Evidence Board / Relationship Intelligence**
9. **Narrative Intelligence**
10. **Contrast & Disconfirming Evidence**
11. **Forecasting & Calibration**
12. **Risk & Action State**
13. **Explain Why**
14. **Orchestration & Reproducibility**

Each family can become a module, API, UI surface, or separately licensed capability while retaining the same underlying node contracts.
