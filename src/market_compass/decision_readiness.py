from __future__ import annotations

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
    """Explain readiness without changing scores or authorizing execution."""
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
        _gate("approval", "External approval receipt", False, "not bound", "exact, current, independently owned approval", True),
    ]
    failed_hard = [gate for gate in gates if gate["key"] != "approval" and gate["hard_stop"] and not gate["passed"]]
    evidence_ready = all(gate["passed"] for gate in gates if gate["key"] != "approval")
    state = "DO_NOT_GO" if failed_hard else "APPROVAL_READY" if evidence_ready else "REVIEW_ONLY"
    return {
        "instrument": "calculateTHAT",
        "state": state,
        "symbol": report.symbol,
        "score_influence": False,
        "trade_execution": False,
        "approval_bound": False,
        "formula": {
            "evidence_edge": "abs(bull_evidence - bear_evidence)",
            "evidence_edge_value": evidence_edge,
            "readiness": "all non-authority gates pass",
        },
        "gates": gates,
        "next_action": "Repair hard stops." if failed_hard else "Request an external approval receipt." if evidence_ready else "Review incomplete readiness gates.",
        "boundary": "A trigger is an observation, not an order. Market Compass cannot execute trades.",
    }
