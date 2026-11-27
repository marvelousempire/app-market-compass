<!-- handbook-sync:generated -->

# daily workflow

> Composite page — sections are editable as separate leaf files. Regenerate with `node scripts/handbook-sync.mjs`.

---

<!-- section:01-daily-workflow -->

# Use Market Compass

## Analysis and navigation — LIVE

Search by symbol or company, select a result, and press **Analyze**. The completed report opens in Compass Desk. Use the left rail for major rooms and the right rail for the selected room's sections. On a phone, Menu provides the same sections. The current work stays mounted while you move between rooms; a long report may still scroll inside the center.

In Compass Desk, open Price Route to inspect the last and next Bus Stops, invalidation, and downside structure. Select an available timeframe and check the observation window. Use Appearance for System, Light, or Dark. Open an Actor from the current report and export its receipt from the comp card. The Overview runtime controls report status in plain language; they do not analyze a Player.

## Player Exchange, Record, and Market Studio — LIVE

In **Player Exchange**, BB, AAPL, QQQ, and other ticker symbols are Players. Search by ticker or company name, filter and sort the catalog, then select a card. That opens the individual **Player Record** in the same center canvas. Its right rail chooses Overview, Intelligence, Player News, Price history, Evidence and receipts, or My view. Price history uses dated market bars; saved studies and notes are browser-local and labeled separately. A missing current reading stays unknown until analysis returns.

From the Player Record, open **Player Market Studio** to inspect the three evidence books, Market pulse, Chart room, levels, splits, reports, evidence, and your local market desk. The Chart room uses dated ticker candles with study switches. Its Option chain entrance leads to the existing Options Lab; a futures contracts board remains unavailable without a verified feed. Ready Play's original player records remain in Ready Play; Market Compass uses its own market evidence for these ticker Players.

## Options Lab — THEORETICAL SIMULATION

Choose **Options Lab** in the left rail. Its right rail opens Option Chain, Trade Builder, Returns, Strategies, Alpaca Data, SEC Filings, Positions, and Journal as separate cassettes in the main canvas. Open a right-rail item to reveal its submenu for that cassette’s controls and results. Switching cassettes retains the selected Player, option choices, virtual cash, positions, and journal. The chain and premiums are theoretical. Select a call or put, strike, expiration, side, and quantity to see estimated premium, break-even, expiration profit and loss, and Rust model projections. A virtual order changes only the browser's simulated cash, positions, and journal. Reset clears that simulated state after confirmation.

Choose **Strategies** in the right rail or **Two-leg strategy** in Options Lab to compare a bull call spread, bear put spread, long straddle, or long strangle. Choose the strikes and contracts per leg, then move projected price, days remaining, and volatility to inspect the combined Rust-model return. Net debit and bounded expiration gain or loss are shown where applicable. This view makes no virtual order; it only projects a same-expiration two-leg scenario.

The Rust projection uses a European-style Black–Scholes approximation with an illustrative fixed rate and no dividends. It is not a live option quote, an American-style assignment model, a full multi-leg strategy engine, or a promise of return. The option scenario uses the desk's supported equity or ETF price evidence; unsupported or stale evidence leaves scenarios unavailable.

Alpaca Data is read-only stock bid/ask context, and SEC Filings shows EDGAR submissions evidence when the service has its required data-only configuration. A held or unconfigured state means the source was not fetched. Neither source changes the theoretical option premium or enables a real order.

## Research rooms — PARTIAL

Choose **intelTHAT App** in the left rail and use its right rail for Cockpit, Market Pack, Macro Conditions, News Intelligence, SEC Monitor, and Run History. The selected desk symbol flows into the embedded research app. Run a research pack, inspect source, freshness, formula, and missing evidence, then export its receipt. Run History is browser-local. The standalone [intelTHAT address](http://market-compass.localhost/intelthat/) remains available, but the main Door is the normal entrance.

In Market Exchange, inspect catalog contracts and API/auth states. Enable, save, install, SSO, and API mutations stay with the recorded owners. In Measurement Studio, choose a method and an authorized example, review held or calculated output, and export its inputs and receipt. Source Refinery creates local provenance receipts from a repository, URL, pasted text, or file. The file-picker witness is still open. Check the [operator status guide](../../../docs/STATUS.md) for current limits.


