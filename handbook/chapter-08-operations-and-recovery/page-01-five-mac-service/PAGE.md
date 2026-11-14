<!-- handbook-sync:generated -->

# five mac service

> Composite page — sections are editable as separate leaf files. Regenerate with `node scripts/handbook-sync.mjs`.

---

<!-- section:01-five-mac-service -->

# Operations and Recovery

## Commissioned FiveMac service — LIVE NOW

The named [Door](http://market-compass.localhost/) exposes [health](http://market-compass.localhost/health) and [operator status](http://market-compass.localhost/api/operator/status). The `ai.market-compass` launch agent runs from `~/Developer/market-compass-live`, binds locally on FiveMac, and reports the installed source revision. Check that the revision matches the accepted owner release, that the runtime is commissioned, and that research and signal generation remain enabled while trade execution and score influence stay disabled.

## Restart and recovery — PARTIAL

Use the [owner recovery runbook](../../../docs/TROUBLESHOOTING.md) for the launch agent, Door transport, logs, and exact-source readback. Read the [operator plan](http://market-compass.localhost/api/operator/plan) before a service action. Restore the last accepted source and prove health and status again through the named Door. The isolated Stop and restart witness remains open.

## Feed, event, and storage recovery — APPROVED TARGET

Future feed, Event Watch, and storage services require tested backups and restore, followed by replay with preserved workspaces, receipts, immutable history, and incident delivery deduplication. Admit Alpaca only with independently proved data-only credentials and negative order, account, and funding probes through the authorized verification path. Hold the lane if the data-only scope cannot be proved.


