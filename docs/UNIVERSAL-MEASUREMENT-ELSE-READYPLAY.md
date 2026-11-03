# Universal Market Compass: measurements, not money

**Founder intent, 2026-11-03:** Market Compass is the origin and reusable *view/measurement studio* for anything that can be observed over time, including phones, cameras, computers, batches of eggs, companies, and consented READYPLAY profiles. It is not solely a securities or brokerage product. A simulated point/index curve is not proof of economic worth, ownership of a person, a price, a tradable token, or a marketplace.

## Application authority

| Application | Owns | Does not own |
| --- | --- | --- |
| **ELSE**, independent repository `marvelousempire/else`; canonical Gitea `avery/else` | Owner-defined methodology, formula versions, qualitative interpretations, evidence/ratings and consent/permission contracts; existing READYPLAY-compatible formulas remain untouched. | Market Compass UI, imported user assets, or a person's identity. |
| **Market Compass**, `marvelousempire/app-market-compass` | Generic subject/observation/index simulation and chart visualizations, provenance display, reusable calculation/view contracts. | ELSE methodology authority, READYPLAY accepted player facts, brokerage execution, or users' uploaded data. |
| **READYPLAY**, `marvelousempire/red-e-play-app` | Player profiles, accepted game/training/witness records, source consent and the official scores/ratings already governed by READYPLAY and ELSE. | Ownership of the reusable Market Compass simulation/visualization engine. |
| **intelTHAT / Omo's Intel** | Independent research snapshots. | Universal score methodology, any other participant's content, trade execution. |

**Portable flow:** Author an interpretable, versioned method and evidence rules in ELSE -> obtain authorized measurements from the original source (READYPLAY, user device/inventory, an uploaded table, etc.) -> pass a bounded method+observations snapshot to Market Compass -> review chart, changes, uncertainty and missing data -> export local JSON. No consumer writes back a rating or changes source truth without a separate authority contract.

**Current reality:** The new `POST /api/simulate` endpoint accepts a *user-supplied* versioned methodology payload and a time series. It DOES NOT claim that a method came from, was verified by, or was authorized by the running ELSE service. A proposed ELSE publisher/adapter must add provenance/authentication and owner readback before that claim becomes true. The browser simulator keeps its input in the form only and the API is stateless; no server-side record storage or saving/export button is commissioned yet. Do not paste sensitive information or private profiles into a server you don't control. The current app preview should run on localhost only.

### Contract v1: example

```json
{
  "subject": {"id": "demo-old-laptop", "name": "Illustrative old laptop",
              "kind": "device", "source_owner": "local example", "authorized_use": true},
  "method": {"id": "example-condition", "version": "0.1-demo", "author": "Example operator",
             "provenance": "local illustrative fixture; not an ELSE-issued method",
             "metrics": [
               {"id": "battery", "label": "Battery health", "unit": "percent",
                "lower": 0, "upper": 100, "weight": 2, "favorable": "higher"},
               {"id": "wear", "label": "Visible wear", "unit": "score",
                "lower": 0, "upper": 10, "weight": 1, "favorable": "lower"}
             ]},
  "observations": [
    {"at": "2026-01-01T12:00:00Z", "values": {"battery": 100, "wear": 0}, "evidence_ref": "demo:1"},
    {"at": "2026-02-01T12:00:00Z", "values": {"battery": 80, "wear": 2}, "evidence_ref": "demo:2"},
    {"at": "2026-03-01T12:00:00Z", "values": {"battery": 60, "wear": 6}, "evidence_ref": "demo:3"}
  ],
  "purpose": "simulation"
}
```

Only measurements with every required metric are calculated; missing/extra metrics create held records. Normalization clamps each metric to its declared range and direction, then combines with weights as a **0–100 method-relative points index**. Consecutive changes are in *index points*, and displayed volatility is the population standard deviation of those changes when at least three complete index observations exist. This is not financial realized volatility, forecast performance, or a statistical claim of real value. The calculation is deterministic for fixed input. Its SHA-256 fingerprint establishes byte-level comparison of normalized request JSON, not independent evidence authenticity or permission.

`GET /api/participants` preserves **Omo's Intel (Clubs), Prince's Principles (Diamonds), Marvin's Metrics (Spades), Wuda's Watch (Hearts)** and separate uncarded Prince's Intel. Names do not assign roles or access privileges.

## READYPLAY backfill, stages and status

Source reference: `marvelousempire/red-e-play-app/docs/plans/Plan-Player-Market-Studio-Hub.md` and merged Player Market work, including PRs #1547, #1552, #1554. READYPLAY retains its sports formula/match-point facts until a tested owner-approved consumer adapter exists.

- **Done in Market Compass branch:** Existing financial candles/EMA/RSI/MACD/Fibonacci; existing intelTHAT receipt bridge; named participant directory; ten-room study index; new generic simulated-index kernel and a browser-input example.
- **Not done:** Full source-equivalent READYPLAY market chart/workbench extraction, multi-book generic chart math, complete scenario/option-chain UI, actual player-record adapter, ELSE method publisher and verifier, identity/consent mapping, versioned SDKs, export flow and network authentication.
- **Acceptance gate:** A consented READYPLAY player observation and a device observation are both consumed by a single Market Compass contract, with identical method-version rules, explicit missing evidence, correct separate source receipts, read-only output, and reproducible test vectors. READYPLAY then calls Market Compass as a consumer rather than owning a diverging copy. Until then, no statement that the entire READYPLAY market stack is migrated.

## Operational guards

Method authors choose criteria, not objective truth. Method inputs remain portable and changeable; compare incompatible methods only with their IDs and version/ranges visible. Persons and devices are **subjects of measurements**, never money, securities, commodities, or property-right claims. No broker orders, real trades, wagers, or token transfers. Do not conflate synthetic example observations with real player stats. Preserve the original apps, repository histories, permission scopes and owner-signed evidence gates.
