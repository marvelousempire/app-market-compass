# Live and Delayed Market Data

## Yahoo on-demand observations — PARTIAL

The existing Yahoo public search and chart paths resolve symbols and fetch data on demand. Treat provider coverage, depth, and freshness as limited. Inspect the actual observation time and provider before using a report.

## Options context and SEC filings — PARTIAL

Options Lab can display read-only Alpaca stock bid/ask context and SEC EDGAR submissions evidence beside its theoretical simulation. These are context panels, not a live option chain. The service holds Alpaca when its data credentials are absent or unavailable and holds EDGAR when the required fair-access contact is missing or the source fails. Read the source state and timestamp on each panel. Neither source changes the simulator's theoretical premium, virtual records, or the no-trading boundary.

## Free Alpaca hybrid — APPROVED TARGET

Use consolidated SIP observations for the whole supported U.S. equity and ETF universe at least 15 minutes delayed. Use real-time IEX for a focus list capped at 30 symbols. Reserve BB, AAPL, QQQ, and SPCX and permit up to 26 governed dynamic slots. Record admissions, evictions, and effective subscription counts. Keep consolidated SIP and single-venue IEX separate in storage, display, and receipts. Label every relevant surface `LIVE · IEX PARTIAL MARKET` or `CONSOLIDATED · 15M DELAYED` according to the lane. The gateway credential must deny trading, account, funding, position, and order access. Market Compass never carries an Alpaca brokerage credential.

Support `1m`, `5m`, `15m`, `1h`, `4h`, `1D`, and `1W`. Retain timestamps, market session, provider lane, delay, and aggregation provenance. Real-time IEX is partial-market evidence and cannot independently issue final Go. The Basic plan documents a 30-symbol WebSocket ceiling and 200 historical requests per minute. See [Alpaca’s market-data plans](https://docs.alpaca.markets/us/docs/about-market-data-api).
