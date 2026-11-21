#!/usr/bin/env python3
"""Offline integrity gate for the verified-slice inventory. No market network calls."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "src" / "market_compass" / "web"
EXPECTED = {
    "registry-node": 115,
    "exchange-admin-surface": 6,
    "exchange-catalog-entry": 15,
    "bankthat-contract": 58,
    "draft-cck-schedule": 7,
    "technical-instrument": 11,
    "intelthat-workspace-section": 6,
    "navigation-destination": 12,
    "verified-slice": 1,
}


def verify() -> dict:
    manifest = json.loads((WEB / "slice-manifest.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    seen = set()
    counts: dict[str, int] = {}
    for entry in entries:
        identifier = entry["id"]
        if identifier in seen:
            raise AssertionError(f"Duplicate manifest ID: {identifier}")
        seen.add(identifier)
        counts[entry["category"]] = counts.get(entry["category"], 0) + 1
        if entry["visible"] and not (ROOT / entry["source"]).is_file():
            raise AssertionError(f"Visible source is missing: {identifier}")
        if entry["visible"] and entry["evidence_status"] != "source-unit-tested-not-live-accepted":
            raise AssertionError(f"Unproven entry visible: {identifier}")
    if counts != EXPECTED or manifest["counts"] != EXPECTED:
        raise AssertionError(f"Inventory drift: {counts!r}")
    current_ids = set(re.findall(r"^- \*\*([A-Z0-9]+-\d{3}) — ", 
                         (ROOT / "docs" / "IP-NODE-REGISTRY.md").read_text(encoding="utf-8"), re.M))
    inventoried_ids = {e["node_id"] for e in entries if e["category"] == "registry-node"}
    if current_ids != inventoried_ids or len(current_ids) != 115:
        raise AssertionError("One or more stable node IDs are missing or changed")
    home = (WEB / "index.html").read_text(encoding="utf-8")
    archived = (WEB / "legacy-dashboard.html").read_text(encoding="utf-8")
    if "long-position-widget.mjs" not in home or "marketcompassreport" not in archived:
        raise AssertionError("Clean shell or archived dashboard is missing")
    if "Research Cockpit" in home or "Decision Intelligence" in home:
        raise AssertionError("Legacy feature surfaces reintroduced to clean home")
    return {"status": "source-manifest-pass", "entries": len(entries),
            "hidden": sum(not e["visible"] for e in entries),
            "source_testable": sum(e["visible"] for e in entries),
            "live_verified": 0, "counts": counts}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
