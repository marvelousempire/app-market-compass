# Using proposeTHAT with Market Compass

**This is an extension of the existing Market Compass handbook, not another application or another skill.** Source instruction date: November 21, 2026. **Current stage:** GitHub source workflow; not a verified in-app proposeTHAT control, automatic intake, live FiveMac receiving or trade operation.

## What you can ask for

**Improve our existing app:** Say to the agent with the approved canonical skill:

> proposeTHAT Market Compass: inspect what we actually have, preserve our existing features, and propose the smallest useful improvement to my daily research workflow. Compare the latest source with the handbook and real accepted runtime evidence. Give each distinct improvement its FUNCTION, RESULT, owner, proof and next safe test.

**Compare a new trading product:** Say:

> proposeTHAT compare [exact trading app/repository/strategy and source version] with Market Compass. Show what each genuinely does better, which overlaps already exist, what is worth adopting, what must not be copied, and what evidence is still missing.

These are **different modes**: `owner-improvement` versus `outside-trading-source`. The research source is captured by proposeTHAT; **Market Compass owns market-specific conclusions**. A stock screen, chart screenshot, AI indicator, educational trading video or broker app must not be silently passed to another owner.

## What currently exists

- Market Compass contains its own [product intention](../docs/PRODUCT-INTENTION.md), [current source status](../docs/STATUS.md), [feature journal](../docs/FEATURE-JOURNAL.md), [115-node registry](../docs/IP-NODE-REGISTRY.md), [two-way source intake specification](../docs/TRADING-SOURCE-INTAKE-AND-TWO-WAY-COMPARISON.md), research-only calculation/Actor surfaces and this nine-chapter handbook.
- proposeTHAT has a **source-only routing helper** at `routing/trading_intake.py` with tests. It can distinguish an internal product-improvement request from outside-market research, but **does not automatically write an intake to Market Compass or conduct the requested source comparison**.
- The canonical reusable skill and complete study method live at [AI Skills Library](https://github.com/marvelousempire/ai-skills-library/blob/main/skills/research/proposethat-research-inventory/SKILL.md), with [owner-mode guidance](https://github.com/marvelousempire/ai-skills-library/blob/main/skills/research/proposethat-research-inventory/references/market-compass-owner-improvement-v1.md).
- The dated **November 14, 2026** FiveMac receipt records commissioned v0.8.1 at 16/20 gates. It is historical evidence, **not proof this November 21 source change runs at the Door**. Use the locally accepted Gitea revision and fresh runtime receipts before asserting current health.

## One safe, practical pass

1. **Attach to accepted checkouts.** Verify the actual Gitea `averygoodman/app-market-compass`, local proposeTHAT, AI Skills Library and current branches. `git status --short` must be clean before any write; use a disposable clone for speculative work. Don't overwrite `~/Developer/market-compass-live`.
2. **Verify mode, without an effect.** From a real proposeTHAT checkout, run:
   ```sh
   python3 routing/trading_intake.py "proposeTHAT Market Compass: improve our research workflow"
   python3 routing/trading_intake.py "Compare Invo trading to Market Compass"
   cd routing && python3 -m unittest -v test_trading_intake
   ```
   Expect `owner-improvement` then `outside-trading-source`. Both return `trade_execution=false`, `score_influence=false`, `automatic_owner_intake=false`. Running these **only proves classification**.
3. **Read current owner truth.** Inspect Market Compass's actual implementation, source tests, source revision, docs and handbook. Confirm which capabilities really exist: 115 nodes, EMA/RSI/MACD, Bus Stops, Price Memory, bull/bear evidence, missing-data explanations, Day Trader, intelTHAT, Market Exchange, research Actors and Measurement Studio. A proposed feature may already be in the app.
4. **Make one two-way table.** For internal improvement, compare requested outcome versus verified existing behavior. For outside sources, compare *both* apps with each other. Mark claims, observed tests, unknowns and deliberate exclusions separately. Do not infer that publisher screenshots prove function or that missing documentation means missing code.
5. **Produce a decision-ready owner proposal.** Include exact request and source pin; existing capability/reuse; numbered non-duplicate candidates; Nephew FUNCTION; independently testable Niece RESULT; owner; evidence; a baseline/target with unknowns explicit; priority; safety/privacy/license; the one smallest reversible pilot; acceptance and rollback. File the formal parent/children only through the real proposeTHAT source inventory and generator; do not create a competing Market Compass recommendation registry.
6. **Prove the pilot before declaring success.** Run proposeTHAT inventory and tests on the right clean checkout, Market Compass's `make test` on a disposable owner-approved copy, and independently read the proposed UI/result with a named source SHA. Only after Gitea authority and actual FiveMac browser receipt may the handbook label a behavior `LIVE NOW`.

## What to investigate first

| Candidate | Why it matters | Present evidence | Next proof |
| --- | --- | --- | --- |
| **P0: Source-to-owner intake** | Research should arrive where Market Compass can inspect and accept it | A stand-alone proposeTHAT classifier and Market Compass two-way specification exist; no verified end-to-end owner write | Deliver one source-pinned, private, read-only packet and obtain Market Compass readback |
| **P1: Product improvement proposals** | You should be able to ask what to improve in Market Compass itself | Canonical skill now has a two-mode procedure; current app is not verified to expose that as a UI control | One full owner-scoped audit with non-duplicate, testable children |
| **P2: My Market Mindset** | A personal view should preserve user preferences without replacing market evidence | Product intent establishes user views and Actor boundaries; verify actual implementation before claiming this feature missing | Map requested view, indicators and ELSE-defined preferences against existing code, then test a read-only display |
| **P3: Source freshness and release truth** | You need to know which research result is current and which source really runs | Versioned source docs and historical FiveMac receipt are present | A current Gitea SHA, staged-source comparison, and live readback for the selected pilot |

*P0–P3 are editorial candidates, not admitted `-rNN` inventory records, deployed features, validated demand or performance rankings.* The first recommended pilot is **P0: one read-only source-to-owner handoff**, followed by P1 once receiving is verified.

## Non-negotiable boundaries

Market Compass remains **research-only**. It never accepts broker credentials, orders, copied trades, wallet execution, money movement, third-party scoring changes or implied financial advice from proposeTHAT. `trade_execution=false` and `score_influence=false` remain true. The Market Compass scorer owns its calculations; external models may interpret, not rewrite them. ELSE owns authored perspectives, while Brown's Barometers retains the measurement seat. Market Intel's separate weekly jobs remain with Market Intel. Do not silently put all Market apps inside one repository.

The skill, classifier and handbook are **source deliverables**. A real Hermes-triggered report, owner intake, Gitea reconciliation and FiveMac acceptance must be individually tested and recorded before being called working integration.

## Actual local research intake page (additive source as of November 21)

The source branch includes a new /proposethat/ page and local-only /api/proposethat/ endpoints. Once installed and verified on FiveMac, open http://market-compass.localhost/proposethat/, choose Improve Market Compass or Compare outside market technology, enter the goal and optional source, then Save research intake. The page shows a saved receipt, documented existing capabilities to inspect, numbered candidate research tasks, a history list and Export receipt.

The API stores private JSON in ~/.market-compass/private/proposethat with create-only files and mode 0600 (private directory 0700). The environment variable MARKET_COMPASS_PROPOSAL_DIR can select an approved local folder. Duplicate identical requests reuse an ID. Unapproved remote clients, cross-origin requests, unsafe paths, account credentials placed in source URLs and unauthorized model/execution fields are rejected. No outside URLs are fetched.

From the accepted proposeTHAT checkout, the operator can also submit an explicitly authorized source request by running its tools/submit_market_compass.py helper. It uses the actual classifier, posts to the local owner and reads back the saved record.

This is a working SOURCE FEATURE until the accepted Gitea application is reconciled, tests pass and FiveMac/browser receiving is observed. A saved intake is not an executed research investigation or a validated technology comparison. The nine existing handbook chapters and historical v0.8.1 commissioning evidence remain untouched.
