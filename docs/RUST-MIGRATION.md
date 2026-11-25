# Market Compass Rust migration

**Decision (November 25, 2026):** Rust is the destination for Market Compass's engine and service. The current Python app remains the commissioned research service until each route and capability has an independently compared Rust replacement. The browser may retain HTML/CSS and small interaction glue; calculations and data authority move to Rust. The first receiving slice is the Options scenario model compiled from one Rust crate to native code and WebAssembly.

## Owner boundaries

- Market Compass owns research calculations, report schemas, options scenarios, its web surface and research-only runtime. It never acquires brokerage execution or money-movement authority.
- Pineal owns retrieval and awareness. The current `pineal-rs` kernel provides search/fusion and `pineal-live/rust` is a replacement candidate while its Python service still occupies the live port. Market Compass must call a versioned Pineal read contract only after the Pineal owner commissions it; a Cargo path dependency into a private checkout is not a deployable integration.
- ClusterTHAT owns its control-room view inside NetworkThat. YouSirJuan supplies live machine facts; Nephew owns commissioned dispatch. Market Compass may offer bounded, read-only research jobs and receipts to those owners. It must not send machine commands, infer cluster capacity from saved links, or add a second dispatcher.
- The user-visible Market Compass Door remains `http://market-compass.localhost/`. Source merge, package, service source revision, Door identity and real interactions are separate proof.

## Current migration inventory

| Capability family | Current owner modules | Rust destination | Gate |
| --- | --- | --- | --- |
| Options scenario prices and sensitivities | `web/options.html`, `web/options-projection.js` | `rust/market-compass-core`; native and WebAssembly builds | **First slice:** native tests, WASM browser readback, missing/ABI-mismatched engine refusal |
| Market data and symbol resolution | `data.py`, `intelthat_native.py`, `intelthat_contract.py` | `market-compass-data` crate with provider adapters and typed provenance | Compare symbols, bars, timestamps, freshness, missing data and provider failures |
| Technical calculations, route and memory | `technical.py`, `pack002.py`, `research_lenses/` | `market-compass-signals` crate | Golden fixtures for EMA/RSI/MACD, levels, timeframe alignment, routes and refusal |
| Evidence, scoring, forecast, decision gates | `context.py`, `scoring.py`, `engine.py`, `decision_readiness.py` | `market-compass-engine` crate | Report JSON parity, counter-evidence, time-ordered validation, no false probability |
| Simulations and backtests | `simulation.py`, `hcck_profiles.py`, `backtest.py` | `market-compass-sim` crate | Time isolation, receipt hashes, profile holds, no trades or writeback |
| Analyst and external data bridges | `ai/`, `intelthat_bridge.py` | `market-compass-adapters` crate | Consent, provider receipts, privacy and error behavior preserved |
| Registry and 115 node IDs | `registry.py`, `models.py` | Versioned Rust schema/registry | Exact IDs, meanings and typed JSON contract |
| HTTP and operations | `api.py`, `launcher.py`, `cli.py` | Rust service and CLI, one commissioned process | Every existing route and status field; service restart, Door and rollback proof |
| Browser controls and rooms | `web/*.js`, HTML/CSS | Keep authored views during service cutover; migrate calculations to Rust/WASM and replace remaining behavior without losing saved browser work | Full interaction inventory, accessibility, return/reopen, mobile layout |

## Sequence

1. Freeze API and representative fixture outputs from the accepted Python revision. Record every route and field; preserve user state and current service.
2. Land Rust core crates behind exact, versioned contracts. Compare results and refusal cases against independent fixtures, with explicit differences where formulas improve.
3. Bind Pineal retrieval through its commissioned read interface and ClusterTHAT job/receipt intake through its accepted owner contract. Refuse unavailable or mismatched owners without substituting saved facts.
4. Bring up the Rust HTTP service on an isolated loopback port. Compare all routes, browser actions, source provenance, privacy decisions and research-only status with the Python service.
5. Promote one accepted Rust package to the existing `ai.market-compass` service and named Door. Verify exact source revision and live interactions. Retain a tested rollback package and original Python source.
6. Remove Python from the runtime only after complete route and behavior coverage. Keep historical source and receipts for recovery.

The Rust options model uses a European-style Black-Scholes approximation, a fixed illustrative 4% rate and no dividends. It is not a live option quote or the American-option model used by Robinhood for stocks/ETFs. Market data, actual option chains, multi-leg strategies, assignment and open-position valuation remain separate work.
