# proposeTHAT ↔ Market Compass source receiving record — November 21, 2026

**Delivery stage:** Additive GitHub source branch, not accepted Gitea or commissioned FiveMac.

## Scope completed in GitHub branch
- `/proposethat/` dedicated local research intake page and link from Market Compass rail
- `/api/proposethat/status`, `POST/GET /api/proposethat/intakes`, `GET /api/proposethat/intakes/{id}`
- Two request modes (existing product improvement and outside technology comparison)
- Local private create-only saved JSON receipts, re-open/history, export and stable deduplication
- Source-documented capability checklist, three numbered candidate research actions, explicit NOT RESEARCHED status
- API validates bounded fields, loopback host, request origin, source URI; blocks unauthorized trade/score fields
- proposeTHAT router and explicit CLI readback helper in separate repo; canonical teaching in AI Skills Library
- `make accept-proposethat` runs source suite and local running-service synthetic receipt test

## Actual independent local checks performed from ChatGPT environment
- Isolated Pydantic/storage module unit tests: **5 passed**.
- Local simulated FastAPI HTTP acceptance: **passed** for POST, GET, listing, repeated identical request, Origin/Host refusal and unsupported trade field refusal.
- JS syntax validated on an isolated working-file copy using Node.js `node --check` (GitHub page bundle still needs accepted checkout test).
- Headless Chromium attempt to load a loopback page: **blocked by environment policy (ERR_BLOCKED_BY_ADMINISTRATOR)** before an application assertion could be made.
- GitHub branch files and diffs were read back. Exact new GitHub source was not installed on FiveMac.
- GitHub Actions: some checks reported failure before any job steps were available; other checks queued. Do not infer actual pytest failures or passing full repository CI.

## Accept the real application (mandatory)
1. Inspect clean Gitea canonical and current FiveMac installed revision. Abort on dirty or diverged source; do not overwrite the running installation.
2. Reconcile paired GitHub source PRs: `proposeTHAT#17`, `ai-skills-library#199`, `app-market-compass#13`, retaining the real Gitea authority.
3. In an accepted clean Market Compass checkout: `make test`, `make lint`, and `make accept-proposethat MARKET_COMPASS_BASE_URL=http://127.0.0.1:8000` against a separately launched approved preview.
4. In an accepted proposeTHAT checkout: `make test` and `python3 tools/submit_market_compass.py --description "proposeTHAT Market Compass improve our daily research" --subject "Market Compass" --goal "Find a measurable, non-duplicate research workflow improvement" --base-url http://127.0.0.1:8000`.
5. Independently witness the browser room, saved history, JSON export, and owner receipt on FiveMac; compare exact source SHA.
6. Only then promote to the commissioned Gitea-authoritative Market Compass service, observe the named Door and retain rollback. Running Hermes source research remains a **separate** acceptance step.

**Never claim:** that a source-bound intake is a completed proposeTHAT study, an installed Hermes skill, independent outside-source comparison, predictive signal improvement or financial trade authority.

**Source safety:** `research_only=true`, `trade_execution=false`, `score_influence=false`, `broker_credentials=false` and `money_movement=false`.
