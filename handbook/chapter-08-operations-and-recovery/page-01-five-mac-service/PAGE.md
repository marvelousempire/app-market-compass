<!-- handbook-sync:generated -->

# five mac service

> Composite page — sections are editable as separate leaf files. Regenerate with `node scripts/handbook-sync.mjs`.

---

<!-- section:01-five-mac-service -->

# Operations and Recovery

## Commissioned FiveMac service — LIVE NOW

The named [Door](http://market-compass.localhost/) exposes [health](http://market-compass.localhost/health) and [operator status](http://market-compass.localhost/api/operator/status). The `ai.market-compass` launch agent runs from `~/Developer/market-compass-live`, binds locally on FiveMac, and reports the installed source revision. Check that the revision matches the accepted owner release, that the runtime is commissioned, and that research and signal generation remain enabled while trade execution and score influence stay disabled.

## One-line build, install, and open

After the exact Gitea main revision has passed its required checks and merged, run this from the commissioned checkout:

```sh
cd ~/Developer/market-compass-live && make ship-install-go
```

The command refuses a dirty or diverged checkout. It fetches canonical main, tests the exact revision in a temporary worktree, builds the Rust options engine and compares it with the bundled WebAssembly file, then fast-forwards the live checkout. It refreshes the Python installation, pins the LaunchAgent to the installed revision, restarts that named service, and checks the health, operator receipt, and three Player screens at the named Door before opening Player Exchange. A failed source check stops before the live checkout moves. If a later service step fails, inspect the named Door and recover from the saved LaunchAgent backup before claiming installation. Use `SHIP_NO_OPEN=1` when the browser should stay put.

## Restart and recovery — PARTIAL

Use the [owner recovery runbook](../../../docs/TROUBLESHOOTING.md) for the launch agent, Door transport, logs, and exact-source readback. Read the [operator plan](http://market-compass.localhost/api/operator/plan) before a service action. Restore the last accepted source and prove health and status again through the named Door. The isolated Stop and restart witness remains open.

## Feed, event, and storage recovery — APPROVED TARGET

Future feed, Event Watch, and storage services require tested backups and restore, followed by replay with preserved workspaces, receipts, immutable history, and incident delivery deduplication. Admit Alpaca only with independently proved data-only credentials and negative order, account, and funding probes through the authorized verification path. Hold the lane if the data-only scope cannot be proved.


