#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname)" != Darwin ]]; then
  echo 'This setup uses the macOS login Keychain.' >&2
  exit 1
fi

echo 'Market Compass · Alpaca market data'
echo 'Enter your Alpaca market-data key ID and secret below. Input stays on this Mac.'
echo 'The secret is not written to the app, LaunchAgent, shell history, or this script.'
echo 'Press Control-C to cancel.'
echo
echo 'Alpaca key ID (typing is hidden):'
security add-generic-password -U -s ai.market-compass.alpaca -a key-id -l 'Market Compass Alpaca key ID' -w
echo 'Alpaca secret key (typing is hidden):'
security add-generic-password -U -s ai.market-compass.alpaca -a secret-key -l 'Market Compass Alpaca secret key' -w

python3 - <<'PY'
import json
import urllib.request

with urllib.request.urlopen('http://market-compass.localhost/api/options-context/BB', timeout=12) as response:
    state = json.load(response)['alpaca']['state']
if state != 'observed':
    raise SystemExit('Keys saved, but the Alpaca quote is not available yet. Check account data access and try again.')
print('Alpaca data connected. Market Compass will label each trade with its feed and source time.')
PY
