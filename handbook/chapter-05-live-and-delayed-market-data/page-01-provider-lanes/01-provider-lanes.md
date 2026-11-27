# Live and Delayed Market Data

## Yahoo on-demand observations — PARTIAL

The existing Yahoo public search and chart paths resolve symbols and fetch data on demand. Treat provider coverage, depth, and freshness as limited. Inspect the actual observation time and provider before using a report.

## Options context and SEC filings — PARTIAL

Options Lab can display read-only Alpaca stock bid/ask context and SEC EDGAR submissions evidence beside its theoretical simulation. These are context panels, not a live option chain. The service holds Alpaca when its data credentials are absent or unavailable and holds EDGAR when the required fair-access contact is missing or the source fails. Read the source state and timestamp on each panel. Neither source changes the simulator's theoretical premium, virtual records, or the no-trading boundary.

## Connected Alpaca observations — verified November 27, 2026

Alpaca's ordinary Paper Trading API keys also permit paper orders. Do not enter them in Market Compass. The former Terminal setup command has been closed. Settings → Market prices accepts the separate Alpaca Connect app Client ID and Client Secret locally, stores them in Mac Keychain, and starts paper-account sign-in with only the `data` scope. When Alpaca is not connected, the bottom of the right rail shows Set up Alpaca or Finish connection, based on the actual connection status; it disappears when connected and stays hidden when status cannot be checked. Both actions open Market prices. Register `http://market-compass.localhost/api/alpaca-connect/callback` as the exact Redirect URI in Alpaca Connect. The callback rejects returned tokens with trading or account-write scope. After saving app details, use Finish Alpaca app setup in Market prices to complete the app registration and exact Redirect URI before selecting Connect with Alpaca. Alpaca's application form currently estimates around 30 business days for approval. A saved app credential is not proof of active market data.

The Market prices cassette keeps the observed price, source time, credential fields, and next action in one readable view. Its return-address instructions expand when needed. Settings hides the unrelated research control bar while retaining its values; left and right rail labels remain readable in both light and dark modes.
After saving Connect app details, Market Compass verifies both entries can be read back from Keychain before it reports success or clears the form. On return, the fields remain blank so the secret is never exposed; the status says plainly whether the app details are saved and whether Alpaca sign-in remains. If confirmation fails, the typed entries remain and the app shows a readable error.
Only a confirmed save plays a brief checkmark and highlight. The saved message remains visible afterward and on return; Reduced Motion keeps the same confirmation without animation.
The local Market Compass Door forwards Settings saves to its loopback service. The service accepts the exact Market Compass Door origin for that local route while refusing other browser origins. This prevents the visible Settings page from rejecting its own Save action.
The left rail also offers **Connect Alpaca** as a direct entrance to that cassette. Opening the repository's `index.html` as a local file redirects to the running Market Compass Door, because local files cannot serve the app's `/static/` styles or `/api/` data.

### Set up Alpaca Connect

1. In Alpaca Connect → My Developed Apps, create or edit Market Compass. Save its Client ID and Client Secret privately.
2. Add the exact Redirect URI `http://market-compass.localhost/api/alpaca-connect/callback`.
3. Enable **Publish app**, accept Alpaca’s OAuth agreement, and submit. On November 27, the saved Publish switch enabled paper OAuth even while the detail page still said Not Published; this is not proof of community listing or Compliance approval.
4. In Market Compass → Settings → Market prices, save the Connect Client ID and Client Secret. Verified saved fields say **Saved in Keychain**, appear lightly greyed out, and remain disabled until **Change app details** is selected. Values never return to the browser. Failed saves retain typed entries.
5. Select **Connect with Alpaca**, choose the intended paper account, and approve the consent. The request asks for `data`, without `trading` or `account:write`. Alpaca’s generic consent copy also mentions account access and trades; it does not change the requested scopes. OAuth read access is assumed by Alpaca, so this token is not evidence of an account-read-denying gateway.
6. Confirm the displayed source is **Alpaca IEX**, with a price and observation timestamp. A saved Client ID alone is not a connected feed.

### What we repaired and verified

The registered client initially failed before consent. Saving the callback and enabling Publish app resolved that stage. Token exchange then failed because the commissioned Python service had no default certificate bundle. Its LaunchAgent now sets `SSL_CERT_FILE` to the installed certifi CA bundle; TLS verification stays enabled. Preserve that environment binding when reinstalling. Never bypass certificate verification. After restarting the service and repeating consent, the token was saved in Mac Keychain. Actual `/api/market-price/BB` and `/api/market-price/AAPL` responses returned Alpaca IEX trades. This proves the local paper connection and stock data, not live trading or a public app listing.

### Compass Desk and Options Lab

Analyze the desired equity or ETF. Compass Desk requests the dated market observation, shows its provider, feed and time, and offers **Refresh market price**. The existing endpoint prefers Alpaca and explicitly labels its Yahoo fallback when Alpaca is unavailable. The historical **Study close** and chart bars retain their original research provenance; they are not overwritten with a newer trade.

Options Lab receives that same observed underlying price for its Rust theoretical chain, return projections and two-leg scenarios. No hardcoded illustrative stock price substitutes for missing market evidence. Wrong-symbol, malformed, future or older-than-five-day observations refuse; changing symbols clears the previous underlying while the new request resolves. The source line identifies Alpaca IEX or the actual fallback provider. A last observed trade is not automatically live: inspect its timestamp. Use the desk refresh action to request a new observation; this is on-demand data, not a streaming subscription.

Option premiums, generated strikes and expirations, assumed volatility, virtual fills and positions remain theoretical. An observed stock trade does not turn the simulator into an exchange option chain. Saved virtual records remain intact, with their original entry evidence. Market Compass cannot place broker orders.

### Research Health, filings, earnings and developments

The top-right Research Health LEDs show independently checked Alpaca connection, price provider/feed, SEC/EDGAR, earnings evidence and development candidates. Connected credentials do not imply a fresh price or a healthy SEC source. Unavailable checks remain visible.

Compass Desk → Company research provides filing links, earnings-related headlines and financial reports, and recent significant-development candidates. **Refresh research** retries those sources. SEC requests use the operator-approved fair-access contact configured in `MARKET_COMPASS_SEC_CONTACT` on the service; this installation uses the approved boss contact. No secret is needed for EDGAR. SEC forms include foreign-issuer 6-K, 20-F and 40-F alongside domestic forms. Earnings evidence includes 8-K Item 2.02 and periodic financial reports, not a fabricated next earnings date. No verified future earnings calendar is connected yet.

Development candidates are ticker-related headlines from the last 30 days mentioning acquisitions, mergers, investigations, lawsuits, guidance, buybacks, contracts, patents, restructuring, bankruptcy or approvals. They retain their publisher, source link and date. This bounded screen does not establish materiality, completeness, surprise, or that nobody noticed an event. Review the linked evidence before interpreting it.

## Broader hybrid feed — target, not installed coverage

Use consolidated SIP observations for the whole supported U.S. equity and ETF universe at least 15 minutes delayed. Use real-time IEX for a focus list capped at 30 symbols. Reserve BB, AAPL, QQQ, and SPCX and permit up to 26 governed dynamic slots. Record admissions, evictions, and effective subscription counts. Keep consolidated SIP and single-venue IEX separate in storage, display, and receipts. Label every relevant surface `LIVE · IEX PARTIAL MARKET` or `CONSOLIDATED · 15M DELAYED` according to the lane. The gateway credential must deny trading, account, funding, position, and order access. Market Compass never carries an Alpaca brokerage credential.

Support `1m`, `5m`, `15m`, `1h`, `4h`, `1D`, and `1W`. Retain timestamps, market session, provider lane, delay, and aggregation provenance. Real-time IEX is partial-market evidence and cannot independently issue final Go. The Basic plan documents a 30-symbol WebSocket ceiling and 200 historical requests per minute. See [Alpaca’s market-data plans](https://docs.alpaca.markets/us/docs/about-market-data-api).
