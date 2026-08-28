from __future__ import annotations

import numpy as np

from .models import LayerResult

WEIGHTS = {
    "foundation": .45, "trend": 1.15, "momentum": 1.05, "route": .9,
    "news": .6, "history": .85, "memory": .9, "relationships": .3, "narrative": .4,
}


def aggregate(layers: dict[str, LayerResult], forecast: dict) -> tuple[float, int, int, float]:
    weighted, denom = 0.0, 0.0
    for key, layer in layers.items():
        w = WEIGHTS.get(key, .5)
        # Price-derived trend and momentum are correlated. Do not count them twice at full weight.
        if key == "momentum" and np.sign(layer.score) == np.sign(layers.get("trend", layer).score):
            w *= .72
        # News-derived relationships and narratives are also dependent on the news layer.
        if key in {"relationships", "narrative"}:
            w *= .65
        weighted += layer.score * layer.confidence * w
        denom += layer.confidence * w
    net = weighted / denom if denom else 0.0
    if forecast.get("beats_baseline") and forecast.get("expected_return") is not None:
        fscore = float(np.clip(np.tanh(forecast["expected_return"] * 6), -1, 1))
        net = (net * denom + fscore * forecast.get("confidence", .4) * .7) / (denom + forecast.get("confidence", .4) * .7)
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
