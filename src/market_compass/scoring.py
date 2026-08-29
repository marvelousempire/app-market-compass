from __future__ import annotations

import numpy as np

from .models import LayerResult

WEIGHTS = {
    "foundation": .45, "trend": 1.15, "momentum": 1.05, "route": .9,
    "news": .6, "history": .85, "memory": .9, "relationships": .3, "narrative": .4,
}


def _effective_weight(key: str, layer: LayerResult, layers: dict[str, LayerResult]) -> tuple[float, float]:
    base = WEIGHTS.get(key, .5)
    independence = 1.0
    if key == "momentum" and np.sign(layer.score) == np.sign(layers.get("trend", layer).score):
        independence *= .72
    if key in {"relationships", "narrative"}:
        independence *= .65
    return base * independence, independence


def contribution_breakdown(layers: dict[str, LayerResult], forecast: dict) -> list[dict]:
    rows: list[dict] = []
    denom = 0.0
    raw: list[tuple[str, LayerResult, float, float, float]] = []
    for key, layer in layers.items():
        w, independence = _effective_weight(key, layer, layers)
        effective = layer.confidence * w
        denom += effective
        raw.append((key, layer, w, independence, layer.score * effective))

    forecast_effective = 0.0
    forecast_score = 0.0
    if forecast.get("beats_baseline") and forecast.get("expected_return") is not None:
        forecast_score = float(np.clip(np.tanh(forecast["expected_return"] * 6), -1, 1))
        forecast_effective = forecast.get("confidence", .4) * .7
        denom += forecast_effective

    for key, layer, w, independence, signed in raw:
        normalized = signed / denom if denom else 0.0
        rows.append({
            "key": key,
            "label": layer.label,
            "score": round(float(layer.score), 4),
            "confidence": round(float(layer.confidence), 4),
            "weight": round(float(w), 4),
            "independence": round(float(independence), 4),
            "net_contribution": round(float(normalized), 4),
            "evidence_points": round(float(normalized * 50), 2),
        })
    if forecast_effective:
        normalized = forecast_score * forecast_effective / denom
        rows.append({
            "key": "forecast",
            "label": "Validated Forecast",
            "score": round(forecast_score, 4),
            "confidence": round(float(forecast.get("confidence", .4)), 4),
            "weight": .7,
            "independence": 1.0,
            "net_contribution": round(float(normalized), 4),
            "evidence_points": round(float(normalized * 50), 2),
        })
    return sorted(rows, key=lambda x: abs(x["evidence_points"]), reverse=True)


def aggregate(layers: dict[str, LayerResult], forecast: dict) -> tuple[float, int, int, float]:
    weighted, denom = 0.0, 0.0
    for key, layer in layers.items():
        w, _ = _effective_weight(key, layer, layers)
        weighted += layer.score * layer.confidence * w
        denom += layer.confidence * w
    net = weighted / denom if denom else 0.0
    if forecast.get("beats_baseline") and forecast.get("expected_return") is not None:
        fscore = float(np.clip(np.tanh(forecast["expected_return"] * 6), -1, 1))
        fw = forecast.get("confidence", .4) * .7
        net = (net * denom + fscore * fw) / (denom + fw)
    net = float(np.clip(net, -1, 1))
    bull = int(round(50 * (net + 1)))
    bull = min(100, max(0, bull))
    bear = 100 - bull
    confs = [max(.05, l.confidence) for l in layers.values()]
    confidence = float(np.exp(np.mean(np.log(confs)))) if confs else .1
    if forecast:
        confidence = float(np.clip(.85 * confidence + .15 * forecast.get("confidence", .2), 0, 1))
    return net, bull, bear, confidence


def action_state(net: float, confidence: float) -> str:
    if confidence < .35:
        return "insufficient data"
    if net >= .42 and confidence >= .58:
        return "confirming setup"
    if net >= .18:
        return "early setup / watch"
    if net <= -.42 and confidence >= .58:
        return "avoid / reduce risk"
    if net <= -.18:
        return "caution / wait"
    return "wait / mixed evidence"
