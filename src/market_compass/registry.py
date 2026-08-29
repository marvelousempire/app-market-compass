from __future__ import annotations

# All 115 stable PRD node IDs remain independently addressable. To keep the code small,
# related nodes share one implementation layer rather than living in 115 wrapper files.
GROUPS = {
    "foundation": [f"F0-{i:03d}" for i in range(1, 9)],
    "data": [f"D-{i:03d}" for i in range(1, 9)],
    "trend": [f"L1-{i:03d}" for i in range(1, 7)],
    "momentum": [f"L2-{i:03d}" for i in range(1, 8)],
    "route": [f"L3-{i:03d}" for i in range(1, 9)],
    "news": [f"L4-{i:03d}" for i in range(1, 10)],
    "history": [f"L5-{i:03d}" for i in range(1, 8)],
    "memory": [f"L6-{i:03d}" for i in range(1, 10)],
    "relationships": [f"L7-{i:03d}" for i in range(1, 10)],
    "narrative": [f"L8-{i:03d}" for i in range(1, 8)],
    "scoring": [f"C-{i:03d}" for i in range(1, 8)],
    "forecast": [f"F-{i:03d}" for i in range(1, 7)],
    "risk": [f"R-{i:03d}" for i in range(1, 6)],
    "explain": [f"E-{i:03d}" for i in range(1, 6)],
    "orchestrator": [f"O-{i:03d}" for i in range(1, 6)],
    "backtest": [f"B-{i:03d}" for i in range(1, 5)],
    "monitoring": [f"M-{i:03d}" for i in range(1, 4)],
    "ip": [f"IP-{i:03d}" for i in range(1, 3)],
}
NODE_REGISTRY = {node: group for group, nodes in GROUPS.items() for node in nodes}
assert len(NODE_REGISTRY) == 115


def node_output(report, node_id: str):
    node = node_id.upper()
    if node not in NODE_REGISTRY:
        raise KeyError(f"Unknown node {node_id}. Use the registry command to list valid IDs.")
    group = NODE_REGISTRY[node]
    if group in report.layers:
        return report.layers[group].model_dump(mode="json")
    if group == "forecast":
        return report.forecast
    if group == "data":
        return {"data_meta": report.data_meta, "timeframes": report.timeframes}
    if group == "risk":
        return {"action": report.action, "route": report.route.model_dump(mode="json"), "confidence": report.confidence}
    if group == "explain":
        return {"plain": report.summary, "technical": report.technical_summary}
    if group == "scoring":
        return {"bull_evidence": report.bull_evidence, "bear_evidence": report.bear_evidence, "confidence": report.confidence, "contributions": report.contributions}
    if group == "orchestrator":
        return {"status": "success", "layers": list(report.layers), "as_of": report.as_of.isoformat()}
    if group == "ip":
        return {"node_count": len(NODE_REGISTRY), "node": node, "implementation_group": group}
    if group == "monitoring":
        return {"data_meta": report.data_meta, "confidence": report.confidence, "forecast_state": report.forecast.get("state")}
    if group == "backtest":
        return {"note": "Run the backtest command for walk-forward strategy metrics."}
    return {"group": group}
