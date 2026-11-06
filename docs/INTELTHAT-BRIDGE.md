# intelTHAT → Market Compass (research-only bridge)

Market Compass remains the independent financial UI and evidence engine. intelTHAT remains the independent producer of options, macro, RSS and EDGAR intelligence. The imported proof-health pattern contributes state semantics only—not finance data, donor identity, or ranking logic.

## Working surface

Read-only GET /api/intelthat/{symbol} returns a compact allowlisted research snapshot with four states: observed, held, excluded, missing. An observed snapshot is readable and time-bounded, NOT proof that its market information is true. Read receipts contain the SHA-256 of the exact source bytes. An unbound EDGAR brief is held rather than attached to an arbitrary symbol.

Set MARKET_COMPASS_INTELTHAT_DIR to an existing intelTHAT runs/ directory. The bridge reads the latest archived options pack from runs/packs/SYMBOL_*.json, or the override runs/SYMBOL/pack.json. Optional manually published runs/SYMBOL/macro.json, rss.json and edgar.json are also supported.

This bridge does not run intelTHAT or touch its files. Macro/RSS/EDGAR publishing is not yet automated. No market data are retrieved in these API calls. Missing evidence stays missing. The response filters known scalar fields, not raw source content. Snapshot files are limited to 8 MiB, path traversal and symlinks are rejected, and timestamps plus matching symbol are required for observed status.

No broker execution, trade authorization, changes to Market Compass's bull/bear score, or copying donor-domain logic. Source repos remain unchanged. Because Market Compass has no API authentication, run this read-only endpoint only on localhost or a trusted private network.

## Test

Run: python -m pytest tests/test_intelthat_bridge.py -q

The Research view includes a **read-on-click** intelTHAT Proof Health panel displaying four source states, allowlisted metrics, timestamps, and file fingerprints. No write or brokerage actions exist. Follow-up: add a versioned intelTHAT publisher contract, verify source provenance and Gitea owner authority, and consider authenticated deployment before exposing this outside localhost. None of this promotes a result into scored evidence. Gitea authority reconciliation must precede an authoritative release.
