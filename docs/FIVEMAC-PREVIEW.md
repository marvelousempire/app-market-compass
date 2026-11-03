# FiveMac Market Compass demonstration: full application preserved

**Status:** Development preview, not a commissioned deployment or an authorized upstream data integration.

## One Terminal line: fresh clone, test, demonstrate

Run on a Mac with Git and Python 3.11+ available:

```bash
git clone --single-branch --branch feat/intelthat-proof-health-bridge https://github.com/marvelousempire/app-market-compass.git "$HOME/MarketCompass-preview" && bash "$HOME/MarketCompass-preview/scripts/commission-demo.sh"
```

For an existing **clean** preview clone, the next run is:

```bash
cd "$HOME/MarketCompass-preview" && git pull --ff-only && bash scripts/commission-demo.sh
```

The bootstrap **does not edit any other repository**. It refuses a dirty worktree, unexpected branch, or unavailable Python 3.11+. A fresh clone to an existing folder fails without overwriting it. Python dependencies install only in this app's `.venv` environment.

The launcher then runs the complete repository test suite and the offline synthetic preflight, and opens a **dedicated localhost** preview on an available port in 18340–18359. It does not occupy a different app's port or claim to be that application.

## What stays in place

Nothing in the original market front end is removed: automatic initial market analysis, stock-symbol input, watchlist, research/quick views, EMA, RSI, MACD, Fibonacci, candles, support/resistance, history, related-news context, the evidence board, snapshots and the Nephew analyst panel.

The original `app.js` startup call `runAnalysis()` is still active. The preview **does not suppress or replace it**. If public data sources are unavailable, their native error/availability states appear; the simulation demonstration still works locally.

## Added beside the original application

- Seven draft Hybrid CCK profile schedules: READYPLAY player, equity, option, device, physical batch, named participant and general subject.
- Named sections: Omo's Intel (King of Clubs), Prince's Principles (King of Diamonds), Prince's Intel (no card), Marvin's Metrics (King of Spades), and Wuda's Watch (King of Hearts).
- Versioned hypothetical methods, 0–100 method-relative charts, changes and volatility in index points, held evidence and portable JSON export.
- No brokerage activity, transfer, market sale, source-right escalation, or official player rating writeback.

## Local evidence and what it proves

`scripts/demo_preflight.py` exercises a synthetic READYPLAY profile and a synthetic computer against the same generic calculation contract. It also checks that the five participant sections are named correctly, the existing chart controls remain visible, and automatic startup analysis still exists. A missing player evidence reference must cause a held result with no calculation.

The `runs/demo-preflight.json` record contains the actual checked commit, timestamp, synthetic index series, input fingerprints and explicit unverified flags. The `runs/` folder is ignored by Git. There is no need to send personal READYPLAY data to the demo.

**New localhost runtime inspection:** Once the preview server answers, it performs read-only HTTP requests to `/health`, the seven-profile catalog, five participant sections, the original HTML controls and served JavaScript. It writes `runs/runtime-inspection.json` with the observed commit, endpoint content SHA-256 digests, pass/held checks and errors. It never requests a live market analysis or modifies the existing stock startup. If the inspection is held, the browser is still opened and the failure is printed; nothing is silently removed or represented as commissioned. This proves a live local HTTP response, **not** browser visual execution, live data-provider success, FiveMac identity, or owner signoff. The same HTTP check runs in GitHub CI, but a CI receipt is not a FiveMac receipt.

After running the launcher on FiveMac, inspect both local receipts:

```bash
cat "$HOME/MarketCompass-preview/runs/demo-preflight.json"
cat "$HOME/MarketCompass-preview/runs/runtime-inspection.json"
```

The operator must still visually inspect the browser, test the original automatic market views and simulator, and record an explicit signoff before describing the FiveMac as commissioned.

GitHub CI also checks the full tests, browser JavaScript syntax, shell syntax and this synthetic preflight. CI evidence validates the code in GitHub's test environment, **not** the Mac's hardware, display, local permissions or attached Gitea.

## What still needs owner verification

- Reconcile primary Gitea authority and read back every accepted change.
- Have CCK That issue actual 77-field profiles and witnesses; register the versioned schema and SHA in Schema That Studio.
- Connect real, authorized READYPLAY observations and independently issued ELSE methodologies.
- Perform a real FiveMac browser walkthrough and record its screenshot/response/receipt. Until done, the preview is not signed off or merged as a commissioned release.

**Stopping the local preview:** Press Ctrl+C in the Terminal window. It does not terminate or replace an existing Market Compass server.

## Status

The preview works from an independent feature branch. PR #11 remains draft until source-authority and integration requirements are resolved. Never label synthetic fixtures as verified real-world results.
