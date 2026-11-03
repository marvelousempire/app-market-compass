"""Inspect the *running* local Market Compass HTTP surface, without touching market sources.

An HTTP receipt is not proof of browser rendering, Mac identity, data authority,
CCK certification, or commissioning. Do not quietly promote it to any of those.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

SCHEMA = "market-compass.runtime-inspection/v1"
EXPECTED_PROFILES = {
    "readyplay-player-v1", "equity-v1", "option-v1", "device-v1",
    "batch-v1", "participant-v1", "general-v1",
}
EXPECTED_SEATS = {
    "Omo's Intel", "Prince's Principles", "Prince's Intel",
    "Marvin's Metrics", "Wuda's Watch",
}
MARKET_CONTROLS = (
    "symbol", "analyze", "watchlist", "price-chart", "rsi-chart",
    "macd-chart", "forecast-panel", "evidence-board", "analyst-lane",
)
ADDED_CONTROLS = (
    "hcck-profile-select", "hcck-seat-select", "universal-run",
    "universal-export", "universal-simulator",
)
PATHS = (
    "/health", "/api/hcck/profiles", "/api/participants", "/",
    "/static/app.js", "/static/hcck.js", "/static/simulator.js",
)


def _require_loopback(base_url: str) -> str:
    parsed = urlsplit(base_url)
    if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1"
            or not parsed.port or parsed.username or parsed.password
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
        raise ValueError("Runtime inspection accepts only http://127.0.0.1:<port>")
    return f"http://127.0.0.1:{parsed.port}"


def _http_get(base: str, path: str) -> bytes:
    request = Request(base + path, headers={"Cache-Control": "no-store"})
    with urlopen(request, timeout=3) as response:
        if response.status != 200:
            raise RuntimeError(f"{path}: HTTP {response.status}")
        content = response.read(2_000_001)
        if len(content) > 2_000_000:
            raise RuntimeError(f"{path}: oversized response")
        return content


def _source_commit() -> str | None:
    root = Path(__file__).resolve().parents[2]
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root,
            capture_output=True, text=True, timeout=3, check=True
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def inspect_runtime(
    base_url: str,
    fetch: Callable[[str], bytes] | None = None,
    source_commit: str | None = None,
) -> dict:
    """Read only localhost endpoints; report held instead of assuming success.

    A supplied fetch function is for deterministic unit tests. A real preview
    uses actual HTTP requests and records SHA256 digests of responses.
    """
    base = _require_loopback(base_url)
    checks: dict[str, bool] = {}
    errors: list[str] = []
    digests: dict[str, str] = {}
    bodies: dict[str, bytes] = {}
    for path in PATHS:
        try:
            raw = fetch(path) if fetch is not None else _http_get(base, path)
            bodies[path] = raw
            digests[path] = hashlib.sha256(raw).hexdigest()
        except Exception as exc:
            errors.append(f"{path}: {type(exc).__name__}: {exc}")
            bodies[path] = b""

    def object_for(path: str) -> dict:
        try:
            obj = json.loads(bodies[path])
            return obj if isinstance(obj, dict) else {}
        except (ValueError, UnicodeDecodeError):
            return {}

    health = object_for("/health")
    profiles = object_for("/api/hcck/profiles")
    participants = object_for("/api/participants")
    profile_ids = {
        item.get("id") for item in profiles.get("profiles", [])
        if isinstance(item, dict)
    }
    seat_names = {
        item.get("name") for item in participants.get("participants", [])
        if isinstance(item, dict)
    }
    page = bodies["/"].decode("utf-8", errors="replace")
    app_js = bodies["/static/app.js"].decode("utf-8", errors="replace")
    hcck_js = bodies["/static/hcck.js"].decode("utf-8", errors="replace")
    simulator_js = bodies["/static/simulator.js"].decode("utf-8", errors="replace")

    checks["health_ok"] = health.get("status") == "ok"
    checks["seven_profiles_served"] = EXPECTED_PROFILES <= profile_ids
    checks["draft_schedules_not_running"] = profiles.get("schedules_running") is False
    checks["five_participant_sections_served"] = EXPECTED_SEATS <= seat_names
    checks["original_market_controls_served"] = all(
        f'id="{control}"' in page for control in MARKET_CONTROLS
    )
    checks["hybrid_cck_and_simulator_controls_served"] = all(
        f'id="{control}"' in page for control in ADDED_CONTROLS
    )
    checks["market_auto_analysis_source_served"] = (
        "async function runAnalysis()" in app_js
        and "runAnalysis();});" in app_js
        and "/api/analyze?symbol=" in app_js
    )
    checks["watchlist_startup_source_served"] = "renderWatchlist();" in app_js
    checks["hybrid_cck_script_served"] = (
        "/api/hcck/profiles" in hcck_js
        and "selector.addEventListener" in hcck_js
    )
    checks["simulator_script_served"] = (
        "/api/hcck/simulate" in simulator_js
        and "/api/simulate" in simulator_js
    )
    passed = not errors and all(checks.values())
    return {
        "schema": SCHEMA,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": source_commit if source_commit is not None else _source_commit(),
        "runtime_url": base,
        "host_os_reported": platform.system(),
        "python_version": platform.python_version(),
        "status": "http-contract-passed" if passed else "held",
        "http_contract_verified": passed,
        "checks": checks,
        "failed_checks": [name for name, ok in checks.items() if not ok],
        "errors": errors,
        "response_sha256": digests,
        "browser_render_verified": False,
        "live_market_feed_verified": False,
        "cck_certified": False,
        "readyplay_connected": False,
        "else_connected": False,
        "gitea_authority_verified": False,
        "five_mac_commissioned": False,
        "note": (
            "Live localhost HTTP surface checked; browser behavior and Mac "
            "operator acceptance must be witnessed independently."
        ),
    }


def save_receipt(receipt: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=".runtime-inspection-", suffix=".json", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(receipt, file, sort_keys=True, indent=2)
            file.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect the localhost Market Compass preview")
    parser.add_argument("--url", required=True, help="http://127.0.0.1:<port>")
    parser.add_argument(
        "--receipt", type=Path,
        default=Path("runs/runtime-inspection.json"),
    )
    args = parser.parse_args()
    evidence = inspect_runtime(args.url)
    save_receipt(evidence, args.receipt)
    print(f"Runtime inspection: {evidence['status']}; receipt: {args.receipt}")
    if evidence["failed_checks"] or evidence["errors"]:
        print("Failed checks:", ", ".join(evidence["failed_checks"]))
        for error in evidence["errors"]:
            print("  " + error)
    print("NOT VERIFIED: browser rendering, market feeds, Gitea, CCK, ELSE, READYPLAY, FiveMac signoff")
    return 0 if evidence["http_contract_verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
