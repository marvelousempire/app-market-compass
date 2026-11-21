#!/usr/bin/env python3
"""Verify actual local Market Compass proposeTHAT API using a synthetic no-secret request.

This deliberately tests the *running* local service. It never deploys software,
changes market scores, contacts a third party, or authorizes broker operations.
"""
from __future__ import annotations

import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def verify(base_url: str) -> dict:
    url = urlsplit(base_url)
    if (url.scheme != "http" or url.hostname not in
            {"localhost", "127.0.0.1", "::1", "market-compass.localhost"}
            or url.username or url.password or url.query or url.fragment
            or url.path not in {"", "/"}):
        raise ValueError("Only a plain HTTP loopback Market Compass address is permitted.")
    base = base_url.rstrip("/")
    with urlopen(base + "/api/proposethat/status", timeout=5) as response:
        status = json.load(response)
    if (status.get("trade_execution") is not False
            or status.get("score_influence") is not False
            or status.get("local_only") is not True):
        raise ValueError("The installed owner did not show the required research-only state.")
    payload = {
        "mode": "owner-improvement",
        "subject": "Market Compass synthetic receiving test",
        "goal": "Verify that local research intake is saved and read back without executing any trades.",
        "source_url": None, "source_revision": "local-acceptance-synthetic",
    }
    request = Request(base + "/api/proposethat/intakes",
                      data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=5) as response:
        saved = json.load(response)
    identifier = saved.get("id", "")
    if not isinstance(identifier, str) or not identifier.startswith("mcpt-"):
        raise ValueError("Owner did not return a valid receipt ID.")
    with urlopen(base + "/api/proposethat/intakes/" + identifier, timeout=5) as response:
        readback = json.load(response)
    if (readback.get("request") != payload
            or readback.get("id") != identifier
            or readback.get("research_completed") is not False
            or readback.get("authority", {}).get("trade_execution") is not False
            or readback.get("authority", {}).get("score_influence") is not False):
        raise ValueError("Stored receipt or authority readback failed.")
    return {
        "acceptance": "local-api-intake-and-readback-pass",
        "id": identifier, "source_revision": status.get("source_revision"),
        "research_completed": False, "trade_execution": False, "score_influence": False,
        "still_required": ["real-research-result", "Hermes-skill-loader", "Gitea-reconciliation", "independent-FiveMac-receiver"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.base_url), indent=2))
        return 0
    except (ValueError, URLError, HTTPError, OSError) as exc:
        print(json.dumps({"acceptance": "HOLD", "reason": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
