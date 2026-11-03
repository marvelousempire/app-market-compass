#!/usr/bin/env python3
"""Offline synthetic commissioning rehearsal. Never claims upstream certification."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient
from market_compass.api import app

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def demo(profile_id: str, kind: str, fields: dict[str, str]) -> dict:
    return {
        "profile_id": profile_id,
        "cck_profile_ref": "draft:synthetic-only",
        "source_fields": fields,
        "simulation": {
            "subject": {
                "id": "fixture-" + profile_id,
                "name": "Fictional " + profile_id,
                "kind": kind,
                "source_owner": "local-synthetic-fixture",
                "authorized_use": True,
            },
            "method": {
                "id": "demonstration-method",
                "version": "v1-synthetic",
                "author": "test-fixture",
                "provenance": "local demo only; not issued by ELSE",
                "metrics": [
                    {"id": "quality", "label": "Quality", "unit": "points", "lower": 0,
                     "upper": 100, "weight": 3, "favorable": "higher"},
                    {"id": "wear", "label": "Wear", "unit": "points", "lower": 0,
                     "upper": 10, "weight": 1, "favorable": "lower"},
                ],
            },
            "observations": [
                {"at": "2026-01-01T12:00:00Z", "values": {"quality": 80, "wear": 2},
                 "evidence_ref": "synthetic:1"},
                {"at": "2026-02-01T12:00:00Z", "values": {"quality": 70, "wear": 4},
                 "evidence_ref": "synthetic:2"},
                {"at": "2026-03-01T12:00:00Z", "values": {"quality": 65, "wear": 5},
                 "evidence_ref": "synthetic:3"},
            ],
            "purpose": "simulation",
        },
    }


def get_json(path: str) -> dict:
    response = client.get(path)
    require(response.status_code == 200, f"{path} returned {response.status_code}")
    return response.json()


def main() -> None:
    health = get_json("/health")
    require(health["status"] == "ok", "app health not OK")
    profiles = get_json("/api/hcck/profiles")
    names = {x["id"] for x in profiles["profiles"]}
    require({"device-v1", "readyplay-player-v1", "equity-v1", "option-v1",
             "batch-v1", "participant-v1", "general-v1"} <= names,
            "seven profile templates not present")
    require(profiles["schedules_running"] is False, "unexpected scheduled jobs")
    require(profiles["authority"]["cck_witness_verified"] is False,
            "draft must not claim upstream CCK certification")
    participants = get_json("/api/participants")["participants"]
    cards = {p["name"]: p["card"]["title"] if p["card"] else None for p in participants}
    require(cards["Marvin's Metrics"] == "King of Spades", "Spades assignment changed")
    require(cards["Prince's Principles"] == "King of Diamonds", "Diamonds assignment changed")
    require(cards["Omo's Intel"] == "King of Clubs", "Clubs assignment changed")
    require(cards["Wuda's Watch"] == "King of Hearts", "Hearts assignment changed")
    require(cards["Prince's Intel"] is None, "Unassigned card was fabricated")

    html = client.get("/").text
    for selector in ['id="analyze"', 'id="price-chart"', 'id="rsi-chart"',
                     'id="macd-chart"', 'id="hcck-profile-select"',
                     'id="universal-run"', '/static/app.js', '/static/hcck.js']:
        require(selector in html, "Existing/new browser control missing: " + selector)
    app_js = client.get("/static/app.js").text
    require("runAnalysis();});" in app_js, "original startup market analysis removed")
    require("renderWatchlist();" in app_js, "existing watchlist initialization removed")

    cases = {
        "readyplay-player-v1": demo("readyplay-player-v1", "player_profile", {
            "player_ref": "fictional-profile", "sport": "basketball",
            "season": "synthetic", "source_scope": "demo-only",
            "consent_ref": "synthetic-not-validated",
        }),
        "device-v1": demo("device-v1", "device", {
            "device_category": "computer", "model": "fictional laptop",
            "inventory_ref": "synthetic-001",
        }),
    }

    checks: list[dict] = []
    for profile_id, payload in cases.items():
        response = client.post("/api/hcck/simulate", json=payload)
        require(response.status_code == 200, f"{profile_id}: HTTP {response.status_code}")
        result = response.json()
        require(result["state"] == "draft-shape-matched", f"{profile_id}: held unexpectedly")
        require(result["source_verified"] is False, "source truth fabricated")
        require(result["cck_witness_verified"] is False, "CCK witness fabricated")
        simulation = result["simulation"]
        require(simulation["trading_enabled"] is False, "trading unexpectedly enabled")
        require(simulation["money_involved"] is False, "money unexpectedly involved")
        require(simulation["data_stored"] is False, "server persistence unexpectedly enabled")
        require(simulation["observed_points"] == 3, "not all three points calculated")
        checks.append({
            "profile": profile_id, "state": result["state"],
            "index_points": [point["index_points"] for point in simulation["records"]],
            "input_sha256": simulation["input_sha256"],
            "source_verified": result["source_verified"],
            "cck_witness_verified": result["cck_witness_verified"],
        })

    withheld = json.loads(json.dumps(cases["readyplay-player-v1"]))
    withheld["simulation"]["observations"][1]["evidence_ref"] = None
    held = client.post("/api/hcck/simulate", json=withheld).json()
    require(held["state"] == "held" and held["simulation"] is None,
            "missing player evidence did not fail closed")
    require("observation-evidence-reference-missing" in held["reasons"],
            "missing-evidence reason lost")

    git_revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                  capture_output=True, text=True, check=True).stdout.strip()
    evidence = {
        "schema": "market-compass.demo-preflight/v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "commit": git_revision,
        "kind": "local-synthetic-rehearsal",
        "health": health["status"],
        "profiles_available": len(profiles["profiles"]),
        "participant_seats": len(cards),
        "existing_market_startup_preserved": True,
        "cases": checks,
        "missing_evidence": {"state": held["state"], "reasons": held["reasons"]},
        "cck_certified": False,
        "readyplay_connected": False,
        "else_connected": False,
        "gitea_authority_verified": False,
        "five_mac_commissioned": False,
    }
    receipt_dir = ROOT / "runs"
    receipt_dir.mkdir(exist_ok=True)
    receipt_path = receipt_dir / "demo-preflight.json"
    receipt_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print("PASS: 7 schedules, 5 seats, original market startup + all browser controls.")
    print("PASS: synthetic READYPLAY and device indices; missing evidence held closed.")
    print(f"Local synthetic receipt: {receipt_path}")
    print("NOT VERIFIED: Gitea, CCK certification, live READYPLAY/ELSE, FiveMac commissioning.")
    print("Safe to launch local development preview; no trade, money or real player export.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: local simulation demo preflight:", str(exc), file=sys.stderr)
        sys.exit(1)
