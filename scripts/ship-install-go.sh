#!/usr/bin/env bash
set -euo pipefail

# Run from the commissioned checkout after the accepted Gitea PR reaches main.
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$root"
door="http://market-compass.localhost"
service="ai.market-compass"
plist="$HOME/Library/LaunchAgents/$service.plist"
python="$root/.venv/bin/python"
no_open=false
if [[ "${1:-}" == "--no-open" ]]; then no_open=true; shift; fi
if [[ $# -ne 0 ]]; then echo "Usage: make ship-install-go [SHIP_NO_OPEN=1]" >&2; exit 2; fi

[[ -x "$python" ]] || { echo "The commissioned Python environment is missing: $python" >&2; exit 1; }
[[ -f "$plist" ]] || { echo "The commissioned LaunchAgent is missing: $plist" >&2; exit 1; }
[[ "$(git branch --show-current)" == main ]] || { echo "Run this from the clean, commissioned main checkout." >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo "The commissioned checkout has edits; preserve them before shipping." >&2; exit 1; }
git fetch gitthat-canonical main
revision="$(git rev-parse FETCH_HEAD)"
git merge-base --is-ancestor HEAD "$revision" || { echo "Gitea main cannot fast-forward this checkout." >&2; exit 1; }

stage="$(mktemp -d "${TMPDIR:-/tmp}/market-compass-ship.XXXXXX")"
cleanup() { git worktree remove --force "$stage/source" 2>/dev/null || true; rm -rf "$stage"; }
trap cleanup EXIT
git worktree add --detach "$stage/source" "$revision" >/dev/null
(
  cd "$stage/source"
  "$python" -m pytest -q
  node --check src/market_compass/web/market-studio.js
  node --check src/market_compass/web/act-v1-shell.js
  cargo test --manifest-path rust/market-compass-core/Cargo.toml
  CARGO_TARGET_DIR="$stage/cargo" cargo build --release --target wasm32-unknown-unknown --manifest-path rust/market-compass-core/Cargo.toml
  cmp "$stage/cargo/wasm32-unknown-unknown/release/market_compass_core.wasm" src/market_compass/web/options_engine.wasm || {
    echo "The bundled options engine does not match this source build." >&2
    exit 1
  }
)

[[ "$(git ls-remote gitthat-canonical refs/heads/main | cut -f1)" == "$revision" ]] || {
  echo "Gitea main moved during qualification; rerun for the new revision." >&2
  exit 1
}
git merge --ff-only "$revision"
"$python" -m pip install --no-deps --no-build-isolation -e "$root"

old_receipt="$($python - "$door/api/operator/status" <<'PY'
import json,sys,urllib.request
try:
    with urllib.request.urlopen(sys.argv[1],timeout=4) as response:
        print(json.load(response).get('source_revision',''))
except Exception:
    print('')
PY
)"
if [[ "$old_receipt" != "$revision" ]]; then
  backup="$plist.before-ship-${revision:0:8}"
  [[ ! -e "$backup" ]] || { echo "LaunchAgent backup already exists: $backup" >&2; exit 1; }
  cp -p "$plist" "$backup"
  "$python" - "$plist" "$revision" <<'PY'
import os,plistlib,sys,tempfile
path,revision=sys.argv[1:]
with open(path,'rb') as source: data=plistlib.load(source)
assert data.get('Label')=='ai.market-compass'
assert data['EnvironmentVariables']['MARKET_COMPASS_AUTHORITY']=='gitea:averygoodman/app-market-compass@main'
assert data['ProgramArguments'][0].endswith('/market-compass-live/.venv/bin/python')
data['EnvironmentVariables']['MARKET_COMPASS_SOURCE_REVISION']=revision
mode=os.stat(path).st_mode & 0o777
fd,temporary=tempfile.mkstemp(dir=os.path.dirname(path),prefix='.market-compass.')
try:
    with os.fdopen(fd,'wb') as target: plistlib.dump(data,target,sort_keys=False)
    os.chmod(temporary,mode)
    os.replace(temporary,path)
except BaseException:
    os.unlink(temporary)
    raise
PY
  plutil -lint "$plist"
  launchctl bootout "gui/$(id -u)/$service"
  loaded=false
  for attempt in 1 2 3 4 5; do
    if launchctl bootstrap "gui/$(id -u)" "$plist"; then loaded=true; break; fi
    sleep 1
  done
  if [[ "$loaded" != true ]]; then
    echo "Market Compass did not reload. The previous LaunchAgent is backed up at $backup." >&2
    exit 1
  fi
fi

"$python" - "$door" "$revision" <<'PY'
import json,sys,time,urllib.request
door,revision=sys.argv[1:]
for attempt in range(20):
    try:
        with urllib.request.urlopen(door+'/api/operator/status',timeout=3) as response: status=json.load(response)
        with urllib.request.urlopen(door+'/health',timeout=3) as response: health=json.load(response)
        with urllib.request.urlopen(door+'/',timeout=3) as response: page=response.read().decode()
        assert status['source_revision']==revision, status
        assert status['commissioned'] and status['signal_generation'] and not status['trade_execution'] and not status['score_influence'], status
        assert health['status']=='ok', health
        assert all(label in page for label in ('Player Exchange','Player Record','Player Market Studio'))
        print(f"Installed {revision} at {door}/ — Player Exchange, Record, and Market Studio ready.")
        break
    except Exception:
        if attempt==19: raise
        time.sleep(1)
PY
if [[ "$no_open" != true ]]; then open "$door/#player-exchange"; fi
