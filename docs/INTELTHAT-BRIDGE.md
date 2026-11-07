# intelTHAT → Market Compass (native research refinery + owner-receipt bridge)

Market Compass owns this integration, its calculations, contract, UI, and runtime. The outside source is pinned at `marvelousempire/intelTHAT@483f86e5aec2d800811c52863dd0765c20c9d441`. It contributed research categories and proof-health vocabulary. No license file was observed at the pinned revision, so Market Compass independently implemented the admitted behavior and never imports or executes donor code.

## Native working surface

`GET /api/intelthat-workspace/{symbol}` returns `market-compass.intelthat-evidence/v1` with four independently degradable evidence classes:

| Kind | Native input | Calculation | Honest limitation |
| --- | --- | --- | --- |
| `pack` | Daily bars, weekly resample, bounded aggregate public options chain | Wilder RSI(14), EMA 13/27/81, MACD(12,26,9), put/call OI and volume ratios | Does not emit candidates, execution readiness, orders, or broker state. |
| `macro` | VIX, 10-year yield, UUP and TLT five-session changes | Disclosed bounded tanh context formula | A context lens, not a macro forecast or scheduled calendar. |
| `rss` | Latest provider headlines returned for the selected symbol | Disclosed bullish/bearish lexical hit ratio with publisher-volume confidence | Headlines and truth are not independently verified. |
| `edgar` | SEC ticker map and company submissions | Counts recent 8-K, 10-K, 10-Q, Form 4, Schedule 13D and 13G records | Held unless `MARKET_COMPASS_SEC_CONTACT` supplies the SEC-required fair-access contact. |

Every class includes inputs, formula, timeframe, evidence timestamp, retrieval timestamp, provenance, freshness, confidence, source URLs, and input fingerprint. The response includes a whole-receipt SHA-256 and these hard boundaries: `trade_execution=false`, `broker_credentials=false`, `money_movement=false`, `signal_generation=true`, and `score_influence=false`.

Network, parse, coverage, staleness and policy failures return `held` or `missing` evidence. They do not break the workspace or turn unknowns into zeros.

## Owner-published receipt bridge

Read-only GET /api/intelthat/{symbol} returns a compact allowlisted research snapshot with four states: observed, held, excluded, missing. An observed snapshot is readable and time-bounded, NOT proof that its market information is true. Read receipts contain the SHA-256 of the exact source bytes. An unbound EDGAR brief is held rather than attached to an arbitrary symbol.

Set MARKET_COMPASS_INTELTHAT_DIR to an existing intelTHAT runs/ directory. The bridge reads the latest archived options pack from runs/packs/SYMBOL_*.json, or the override runs/SYMBOL/pack.json. Optional manually published runs/SYMBOL/macro.json, rss.json and edgar.json are also supported.

This compatibility bridge does not run intelTHAT or touch its files. No market data are retrieved in this API call. Missing evidence stays missing. The response filters known scalar fields, not raw source content. Snapshot files are limited to 8 MiB, path traversal and symlinks are rejected, and timestamps plus matching symbol are required for observed status.

The donor inventory explicitly rejects E*TRADE OAuth, broker credentials, execution-ready authority, orders, trade execution, position/spread management, trade recording, money movement, and unsupported performance claims. Source repos remain unchanged. Because Market Compass has no API authentication, run these read-only endpoints only on localhost or a trusted private network.

## Test

Run: `python -m pytest tests/test_intelthat_native.py tests/test_intelthat_bridge.py tests/test_intelthat_surface.py -q`

The Research view includes a native ACT workspace with Refresh Live Evidence, Read Owner Receipts, state filters, expandable formula/input/provenance sections, and Export Receipt. No brokerage actions exist. None of this promotes a result into scored evidence. Protected Gitea acceptance, installed-source readback, real-Door behavior, and downstream mirror equality remain separate release proofs.
