# Unified Market Studio and Market Compass, without subtraction

**Owner:** Market Compass remains its existing `averygoodman/app-market-compass` Gitea product and FiveMac service. This GitHub branch is a proposed additive mirror change; do **not** install it over `~/Developer/market-compass-live` or claim its code is commissioned.

## What was already there

Current main (v0.7) already has the ACT v1 administrative shell, live-market analysis, Omo/Prince/Wuda/Brown's Barometers research Actors, Market Exchange, decision-readiness signals, intelTHAT read-only research, Day Trader lens, charts, risk/context, and a named FiveMac operator Door. No separate `market-that-studio` GitHub repository was confirmed. The ACT `market-studio` name occurs as a portfolio/studio identity, not evidence that it has the same installed behavior.

That App Studio's **Market Intel** is an independent owner application (`averygoodman/market-intel`), currently a separate six-job weekly-market measurement contract (`all`, `pack`, `macro`, `rss`, `events`, `prob`) and a CalculateThat consumer. Market Compass is **not** allowed to steal or reissue that app's data, method, approval or records.

## The additive weaving proposed here

1. **Existing Market Compass** is the only visual study application. Its entire ACT shell, original market analysis, Market Exchange, Actor Studio, signal gates and online provider paths stay intact.
2. **Universal Measurement Studio** is a new room in that same shell. The generic `POST /api/simulate` accepts explicitly authorized subject observations, a versioned user-supplied method, and returns a hypothetical 0–100 method-relative index, changes, holds, and exportable JSON. It is **not** securities trading or person pricing.
3. **Hybrid CCK** draft templates are in `GET /api/hcck/profiles`, and `POST /api/hcck/simulate` checks source fields, subject type and evidence references. Templates: READYPLAY player, equity, option, device, physical batch, participant and general. Existing CCK That and Schema That remain authoritative. No CCK witness, schema index, authentication or automatic schedules are claimed.
4. **Actor crosswalk:** Omo's Intel (King of Clubs) links to the existing Omo research actor; Prince's Principles (King of Diamonds) links to Prince; Wuda's Watch (King of Hearts) links to Wuda. Marvin's Metrics (King of Spades) and Prince's Intel remain distinct owner-content placeholders. **Brown's Barometers remains unchanged**: it owns current instrument/metrics research and must not be silently renamed into Marvin's Metrics.
5. **ELSE** authors actual method/perspective contracts; user-supplied example methods in this slice are *not* ELSE-issued. **READYPLAY** owns genuine player facts and consent; the synthetic player demo is *not* a live READYPLAY record.
6. **Market Intel** supplies weekly jobs to CalculateThat; its six-job manifest and independent authority stay untouched. The current Omo/intelTHAT receipt panel remains a read-only consumer, not a replacement for Market Intel.
7. **Existing market algorithms remain** EMA, RSI, MACD, Fibonacci, support/resistance, 115 nodes, forecasting, decision gates, and current Day Trader lens. No reduction to a non-financial-only simulator, and no real-money execution.

## How to verify before the owner receives anything

Review `tests/test_unified_measurement_integration.py` along with `tests/test_hcck_profiles.py` and `tests/test_universal_simulation.py`. Run the entire existing repository tests and the browser/JavaScript checks on a **separate clone** of this proposal. Check the ACT sidebar's **Measurement Studio** link, choose a synthetic profile, simulate, export, then confirm the original stock analysis and Actor rooms still work.

**Not completed:** Full feature-by-feature extraction of READYPLAY Player Market Studio's original chart/scenario books, real accepted CCK birth records, actual ELSE/READYPLAY/Market Intel adapters, Gitea authority reconciliation, successful hosted Mac CI, and installed FiveMac readback of this revision. They are not solved by adding an HTML panel.

## Integration release rule

Compare against accepted Gitea `main` at an exact revision and stop if it has moved. Bring the change through the existing Gitea receipt/approval path. Do not merge the conflicting older PR #11 wholesale: it predates v0.7 and is not a safe replacement. Preserve GitHub PR #11 as historical evidence of original intent while this branch ports selected missing behavior. Promotion to the installed FiveMac service requires tests, Gitea owner acceptance, real browser review, and reversible rollout. No force push or silent cutover.
