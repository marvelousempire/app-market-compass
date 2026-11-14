# Market Compass Handbook

## Commissioned FiveMac service — LIVE NOW

- [Market Compass Door](http://market-compass.localhost/)
- Version `0.8.1`
- FiveMac commissioned, observed November 14, 2026
- Observed live revision `1a93344317b8facd22e58c79268f594a315b7c15`
- `research_only=true` (operator mode `research_only`)
- `signal_generation=true`
- `trade_execution=false`
- `score_influence=false`

Commissioning remains **16/20**. The [November 12 historical closeout](../docs/CLOSEOUT-REPORT-2026-11-12.md) preserves the four remaining outcomes and the revision witnessed that day. Consult [product status](../docs/STATUS.md) and the [real operator readback](http://market-compass.localhost/api/operator/status) for current evidence.

Research v1 is an approved build contract. Runtime proof is required before any approved target can be promoted to LIVE NOW.

## Chapters

1. [Start](chapter-01-start/page-01-research-workbench/PAGE.md)
2. [Use Market Compass](chapter-02-use-market-compass/page-01-daily-workflow/PAGE.md)
3. [Evidence and Signals](chapter-03-evidence-and-signals/page-01-read-a-research-signal/PAGE.md)
4. [Actors and Instruments](chapter-04-actors-and-instruments/page-01-actor-owned-evidence/PAGE.md)
5. [Live and Delayed Market Data](chapter-05-live-and-delayed-market-data/page-01-provider-lanes/PAGE.md)
6. [Event Watch](chapter-06-event-watch/page-01-one-evolving-incident/PAGE.md)
7. [Alerts and Receipts](chapter-07-alerts-and-receipts/page-01-governed-delivery/PAGE.md)
8. [Operations and Recovery](chapter-08-operations-and-recovery/page-01-five-mac-service/PAGE.md)
9. [Research v1 Delivery](chapter-09-research-v1-delivery/page-01-acceptance-and-release/PAGE.md)

## Maintain the handbook

Edit the numbered leaf Markdown files. Nephew owns the generator; the `node scripts/handbook-sync.mjs` banner in generated `PAGE.md` files refers to that owner's checkout, not this Market Compass repository. Market Compass does not contain a local copy of that program.

Set these variables to your actual accepted checkouts, then run the existing [Nephew generator](https://gitmore.app/averygoodman/nephew/src/branch/main/scripts/handbook-sync.mjs):

```sh
NEPHEW_ROOT=/absolute/path/to/nephew
MARKET_COMPASS_ROOT=/absolute/path/to/app-market-compass
node "$NEPHEW_ROOT/scripts/handbook-sync.mjs" --root "$MARKET_COMPASS_ROOT"
node "$NEPHEW_ROOT/scripts/handbook-sync.mjs" --root "$MARKET_COMPASS_ROOT" --check
```

The first command updates the composite pages and lead sheets; the second verifies there is no generated drift. Review those changes and refresh the generated digests in `truth-manifest.json` before shipment. If the accepted Nephew checkout or generator is unavailable, stop and restore that dependency. Keep the editable leaves and last accepted generated files; do not copy the engine or hand-edit generated pages to mask the missing owner.
