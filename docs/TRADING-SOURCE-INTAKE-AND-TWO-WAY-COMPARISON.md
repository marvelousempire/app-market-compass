# Trading-source intake and two-way capability comparison

**Founder direction: November 19, 2026. Owner: Market Compass.**
Status: specification + first source comparison. Not a deployed classifier, data connector, live Invo integration or trading executor.

## Mandatory routing rule
Every user-supplied **trading-related** app, GitHub repository, skill, bot, strategy, indicator, chart, brokerage venue, copy-trading service, community, transcript, video, screenshot, news source or training material is routed to **Market Compass for evaluation**. General proposeTHAT still preserves the original source and experiment structure, but Market Compass is the authoritative owner of trading-specific interpretation, comparisons, decisions and historical reviews. Do not create an alternate trading evaluator inside proposeTHAT, ACT V5, Hello or a new app.

Classification must handle ambiguous text: 'training bots' may mean machine-learning training or trading bots; ask or retain unknown where intent is unclear rather than silently route. Preserve all original text, date, source URL, version and previous review IDs. Deduplicate by normalized source identity and exact version without destroying earlier evaluations.

## Two-way comparison — every intake must answer
1. What does the outside product *actually implement and prove* that Market Compass lacks or only plans?
2. What does Market Compass *actually implement and prove* that the outside product lacks or has not demonstrated?
3. Which capabilities overlap, and which owner should retain them?
4. What can be adopted as data, technique, scoring method, interface or reusable micro-slice without copying unrelated code, users, secrets, identity or execution authority?
5. Which differences reflect product purpose rather than shortcomings (e.g. Market Compass does not execute trades)?
6. What are the sources, licenses, costs, privacy implications, financial/regulatory considerations, data freshness, security risks, hardware/model dependencies and exact unknowns?
7. Which bounded experiment, repeatable tests, and human decision would be required to add value?
8. Where does the dated review live and what changed since prior evaluations?

## Intake output record
Use a dated, source-pinned dossier with: source identifier and raw reference; verified source revision; product category; intended job; source claims versus observed runtime evidence; two-way capability matrix; uniqueness; overlaps; adoption opportunities; explicit exclusions; source/provider requirements; proposed experiment; accuracy/bias/fraud/follower-selection checks; status (research/qualified/tested/rejected); result and receiving proof. Publisher-provided screenshots and testimonials are claims, not verification.

Market Compass calculations, evidence weighting and counter-cases retain their existing authority. External trading bots may be inspected or simulated but **must never gain order placement, brokerage credentials, wallet management, exchange permissions, automatic copied trades, real-money position management, or score influence by intake**. Market Compass's permanent no-trade-execution boundary is unchanged. An external execution feature cannot be counted as a 'missing Market Compass feature'.

## Integration boundaries
- proposeTHAT: generic original-source capture, classification handoff, isolated experiment folders, provenance/history
- Market Compass: trading-specific decision, bidirectional comparison, research-only evidence and simulation
- ClassifyTHAT / ResearchTHAT: classification and research assistance
- stackTHAT: actual qualifying software/data/model/hardware inventory, deduplicated with registered owners
- SkillTHAT / AI Skills Library: reusable teaching and validation skill; do not copy live scorer
- ACT V5 Grand Canvas: only verified research cassette or Bone Fast Look receiver, preserves the retained Stage; does not execute
- Approval/credentials remain with existing original owners, outside Market Compass

## Required test cases before routing can be called automatic
Trade bot, crypto copy-trading app, stock screener, technical analysis repo, strategy video, chart screenshot, indicator skill, broker integration, financial news and general non-trading technology. Positive examples must produce Market Compass referral and two-way comparison; unrelated material stays with proposeTHAT. Ambiguous 'training' must not become trading without evidence.

## First intake
[Invo two-way comparison](../reviews/2026-11-19-invo-two-way-comparison.md).

**Delivery boundary:** This document records the canonical routing requirement. A tested classifier, owner API, automatic event/handoff, live provider connection, UI, and FiveMac receiving are separate uncompleted implementation steps.

## Owner-improvement mode — proposeTHAT Market Compass (November 21, 2026)

This extends, not replaces, the outside-source comparison above. A request like **"proposeTHAT Market Compass: improve the research workbench"** means research the **existing Market Compass app itself**. It must not be misclassified as a request to compare another bot or as permission to create a separate scoring product. The source-only classifier at `proposeTHAT/routing/trading_intake.py` now identifies `mode=owner-improvement` separately from `mode=outside-trading-source`. **This is not automatic owner intake.**

For owner improvements, verify the latest app source/branch and accepted Gitea authority, product intention, STATUS, existing 115-node registry, Actors, Market Intel and ELSE boundaries, nine-chapter handbook, source tests, earlier proposals and the last *dated* FiveMac commissioning receipt. Produce only non-duplicate proposed FUNCTION/RESULT children, measurable acceptance tests, missing evidence and a reversible owner-approved pilot. Any suggestion to change trading evidence calculations needs independent Market Compass code/tests and owner acceptance; proposeTHAT is never a second scorer.

**Delivery and current proof:** the documented source-only classifier can distinguish two request modes and its unit tests can verify that decision. There is not yet a wired owner intake endpoint, guaranteed SkillTHAT/Hermes receiving, read-only in-app action or independent FiveMac runtime proof. Classifying a request, changing an instruction, and running an owner's actual end-to-end research workflow are different outcomes. See [the handbook's practical guide](../handbook/PROPOSETHAT.md) for the first bounded source-to-owner pilot. Never claim real client delivery from this document alone.
