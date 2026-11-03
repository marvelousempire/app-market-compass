# intelTHAT → Market Compass (research-only bridge)

Market Compass remains the independent financial UI and evidence engine. intelTHAT remains the independent producer of options, macro, RSS and EDGAR intelligence. READYPLAY's Player Market Desk/Studio provides the proof-health pattern, not finance data or player-ranking logic.

## Working surface

Read-only GET /api/intelthat/{symbol} returns a compact allowlisted research snapshot with four states: observed, held, excluded, missing. An observed snapshot is readable and time-bounded, NOT proof that its market information is true. Read receipts contain the SHA-256 of the exact source bytes. An unbound EDGAR brief is held rather than attached to an arbitrary symbol.

Set MARKET_COMPASS_INTELTHAT_DIR to an existing intelTHAT runs/ directory. The bridge reads the latest archived options pack from runs/packs/SYMBOL_*.json, or the override runs/SYMBOL/pack.json. Optional manually published runs/SYMBOL/macro.json, rss.json and edgar.json are also supported.

This bridge does not run intelTHAT or touch its files. Macro/RSS/EDGAR publishing is not yet automated. No market data are retrieved in these API calls. Missing evidence stays missing. The response filters known scalar fields, not raw source content. Snapshot files are limited to 8 MiB, path traversal and symlinks are rejected, and timestamps plus matching symbol are required for observed status.

No broker execution, trade authorization, changes to Market Compass's bull/bear score, or copying READYPLAY's sports logic. Source repos remain unchanged. Because Market Compass has no API authentication, run this read-only endpoint only on localhost or a trusted private network.

## Test

Run: python -m pytest tests/test_intelthat_bridge.py -q

Follow-up: add a browser proof-health surface, a fully versioned intelTHAT publisher contract, and tests of complete market data provenance before promoting anything into scored evidence. Gitea authority reconciliation must precede an authoritative release.
