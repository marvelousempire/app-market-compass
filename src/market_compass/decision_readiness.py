from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import Report


def _gate(key: str, label: str, passed: bool, actual: Any, requirement: str, hard_stop: bool = False) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "passed": bool(passed),
        "actual": actual,
        "requirement": requirement,
        "hard_stop": hard_stop,
    }


def calculate_readiness(report: Report) -> dict[str, Any]:
    """Produce an active research signal without changing scores or placing orders."""
    foundation = report.layers.get("foundation")
    missing = [f"{layer.label}: {item}" for layer in report.layers.values() for item in layer.missing]
    consensus = report.timeframes.get("consensus", {})
    agreement = float(consensus.get("agreement") or 0)
    evidence_edge = abs(int(report.bull_evidence) - int(report.bear_evidence))
    reward_risk = report.route.reward_risk
    route_bound = report.route.direction in {"up", "down"} and report.route.invalidation is not None
    gates = [
        _gate("asset_reality", "Asset reality", bool(foundation and foundation.state == "acceptable"), foundation.state if foundation else "missing", "acceptable", True),
        _gate("confidence", "Confidence", report.confidence >= 0.65, report.confidence, ">= 0.65", True),
        _gate("evidence_edge", "Evidence edge", evidence_edge >= 10, evidence_edge, ">= 10 points"),
        _gate("timeframe_agreement", "Timeframe agreement", agreement >= 0.67, agreement, ">= 0.67"),
        _gate("route_bound", "Route and invalidation", route_bound, {"direction": report.route.direction, "invalidation": report.route.invalidation}, "known direction and explicit invalidation", True),
        _gate("reward_risk", "Reward / risk", reward_risk is not None and reward_risk >= 2.0, reward_risk, ">= 2.0"),
        _gate("evidence_gaps", "Evidence gaps", not missing, missing, "none", True),
    ]
    failed_hard = [gate for gate in gates if gate["hard_stop"] and not gate["passed"]]
    evidence_ready = all(gate["passed"] for gate in gates)
    direction = "BULLISH" if report.bull_evidence > report.bear_evidence else "BEARISH" if report.bear_evidence > report.bull_evidence else "NEUTRAL"
    state = "DO_NOT_GO_SIGNAL" if failed_hard else "GO_SIGNAL" if evidence_ready else "WATCH_SIGNAL"
    timestamp = report.as_of.isoformat()
    result = {
        "instrument": "calculateTHAT",
        "state": state,
        "symbol": report.symbol,
        "signal_generation": True,
        "signal": {
            "active": True,
            "direction": direction,
            "bull_evidence": report.bull_evidence,
            "bear_evidence": report.bear_evidence,
            "confidence": report.confidence,
            "action": state,
            "inputs": {"bull_evidence": report.bull_evidence, "bear_evidence": report.bear_evidence, "confidence": report.confidence, "timeframe_agreement": agreement, "reward_risk": reward_risk},
            "formula": "hard_stop ? DO_NOT_GO : all_gates_pass ? GO : WATCH",
            "timeframe": f"{report.horizon_days}D with 4H/1D/1W agreement",
            "timestamp": timestamp,
            "provenance": {"provider": report.data_meta.get("provider"), "requested_symbol": report.data_meta.get("requested_symbol", report.symbol), "resolved_symbol": report.data_meta.get("resolved_symbol", report.symbol)},
            "confidence_receipt": {"value": report.confidence, "meaning": "evidence confidence; not outcome probability"},
        },
        "score_influence": False,
        "trade_execution": False,
        "approval_required_for_signal": False,
        "formula": {
            "evidence_edge": "abs(bull_evidence - bear_evidence)",
            "evidence_edge_value": evidence_edge,
            "readiness": "all research gates pass",
        },
        "gates": gates,
        "next_action": "Do not go; repair hard stops." if failed_hard else "Go signal is active for research review." if evidence_ready else "Watch signal is active; review incomplete gates.",
        "boundary": "Signals are active research outputs, not orders. Market Compass does not execute trades.",
    }
    receipt_payload = {key: result[key] for key in ("instrument", "state", "symbol", "signal", "formula", "gates", "score_influence", "trade_execution")}
    result["receipt"] = {
        "schema": "market-compass.calculate-that-receipt.v1",
        "issued_at": timestamp,
        "sha256": hashlib.sha256(json.dumps(receipt_payload, sort_keys=True, default=str, separators=(",", ":")).encode()).hexdigest(),
        "exportable": True,
    }
    return result
