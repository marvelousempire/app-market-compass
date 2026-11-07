"""Market Compass-owned contract for provenance-bound intelTHAT research evidence."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any

CONTRACT = "market-compass.intelthat-evidence/v1"
SOURCE_REPOSITORY = "marvelousempire/intelTHAT"
SOURCE_REVISION = "483f86e5aec2d800811c52863dd0765c20c9d441"
KINDS = ("pack", "macro", "rss", "edgar")
STATES = ("observed", "held", "excluded", "missing")
_SYMBOL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._^=-]{0,29}$")


def symbol(value: str) -> str:
    result = value.strip().upper()
    if not _SYMBOL.fullmatch(result):
        raise ValueError("Invalid symbol.")
    return result


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def evidence(
    kind: str,
    *,
    state: str,
    reason: str,
    as_of: str | None,
    timeframe: str,
    inputs: dict[str, Any],
    formula: str,
    metrics: dict[str, Any],
    confidence: float,
    source_urls: list[str],
    retrieved_at: str,
    freshness: str,
) -> dict[str, Any]:
    if kind not in KINDS or state not in STATES:
        raise ValueError("Unknown intelTHAT evidence kind or state.")
    bounded_confidence = round(max(0.0, min(1.0, float(confidence))), 3)
    input_sha = digest(inputs)
    return {
        "kind": kind,
        "state": state,
        "reason": reason,
        "as_of": as_of,
        "timeframe": timeframe,
        "freshness": freshness,
        "inputs": inputs,
        "formula": formula,
        "metrics": metrics,
        "confidence": bounded_confidence,
        "provenance": {
            "publisher": "Market Compass native intelTHAT refinery",
            "source_urls": source_urls,
            "retrieved_at": retrieved_at,
            "input_sha256": input_sha,
            "outside_source_repository": SOURCE_REPOSITORY,
            "outside_source_revision": SOURCE_REVISION,
            "adoption": "independent safe adaptation; donor runtime not executed",
            "license_observation": "no license file observed at pinned revision",
        },
    }


def workspace(symbol_value: str, items: dict[str, dict[str, Any]], *, as_of: str) -> dict[str, Any]:
    selected = symbol(symbol_value)
    if tuple(items) != KINDS:
        raise ValueError("intelTHAT workspace must contain each governed evidence kind in order.")
    counts = {state: sum(item["state"] == state for item in items.values()) for state in STATES}
    result: dict[str, Any] = {
        "contract": CONTRACT,
        "symbol": selected,
        "as_of": as_of,
        "mode": "research_only",
        "trade_execution": False,
        "broker_credentials": False,
        "money_movement": False,
        "signal_generation": True,
        "score_influence": False,
        "proof_health": counts,
        "sources": items,
        "source_refinery": {
            "source_repository": SOURCE_REPOSITORY,
            "source_revision": SOURCE_REVISION,
            "reused": ["research categories", "proof-health vocabulary"],
            "adapted": ["options/market context", "macro context", "headline evidence", "EDGAR evidence"],
            "rejected": [
                "E*TRADE OAuth and credentials",
                "execution-ready flags as authority",
                "orders and trade execution",
                "position and spread management",
                "trade recording and money movement",
                "unsupported performance claims",
            ],
        },
    }
    result["receipt_sha256"] = digest(result)
    return result
