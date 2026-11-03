#!/usr/bin/env bash
# Local Mac preview only. Additive, abort-on-dirty, no remote execution, no live trading.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v git >/dev/null 2>&1 || ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "STOP: this demo must run from a Git worktree." >&2
  exit 1
fi
if [[ -n "$(git status --porcelain --untracked-files=all)" ]]; then
  echo "STOP: the Market Compass worktree contains uncommitted files." >&2
  echo "Nothing was changed. Commit, stash, or use a fresh clone first." >&2
  exit 1
fi
if [[ "$(git branch --show-current)" != "feat/intelthat-proof-health-bridge" ]]; then
  echo "STOP: this preview requires branch feat/intelthat-proof-health-bridge." >&2
  exit 1
fi

PY=""
for candidate in python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>/dev/null; then
    PY="$candidate"
    break
  fi
done
if [[ -z "$PY" ]]; then
  echo "STOP: install Python 3.11 or newer before running this preview." >&2
  exit 1
fi

echo "Market Compass preview branch: $(git rev-parse --short HEAD)"
echo "Preserving existing auto-analysis, watchlist, charts and all market controls."
echo "Preparing isolated Python environment with $PY..."
make setup PYTHON="$PY"
echo "Running full repository regression tests..."
make test
echo "Running offline synthetic player, device, CCK, and preservation preflight..."
.venv/bin/python scripts/demo_preflight.py
echo "Launching a dedicated browser preview while retaining normal market startup..."
echo "Exit with Ctrl+C. No upstream source or broker data is modified."
exec .venv/bin/python scripts/preview_server.py
