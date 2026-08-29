from __future__ import annotations

from typing import Any

import pandas as pd

from .context import (
    forecast,
    foundation_layer,
    historical_layer,
    news_layer,
    relationship_and_narrative,
)
from .data import MarketData, get_market_data, get_timeframe_bars
from .models import Report
from .scoring import action_state, aggregate, contribution_breakdown
from .technical import (
    apply_timeframe_context,
    compact_chart,
    enrich,
    memory_and_route_layers,
    momentum_layer,
    timeframe_matrix,
    trend_layer,
)


def _calibration(history) -> dict[str, Any]:
    metrics = history.metrics or {}
    if not metrics.get("analog_count"):
        return {"state": "insufficient_history", "warning": "No historical outcome rate is available."}
    return {
        "state": "analog_context",
        "sample_size": metrics.get("analog_count"),
        "positive_rate": metrics.get("positive_rate"),
        "mean_forward_return": metrics.get("mean_forward_return"),
        "q25": metrics.get("q25"), "q75": metrics.get("q75"),
        "warning": "This is the outcome rate of nearby historical analogs, not a calibrated probability of profit.",
    }


def analyze_frame(
    symbol: str,
    data: MarketData,
    horizon: int = 20,
    use_stochastic: bool = False,
    timeframe_frames: dict[str, pd.DataFrame] | None = None,
) -> Report:
    if len(data.bars) < 90:
        raise ValueError("At least 90 bars are required for the default EMA 81 profile")
    x = enrich(data.bars)
    trend = trend_layer(x)
    momentum = momentum_layer(x, use_stochastic)
    memory, route_layer, route = memory_and_route_layers(x, trend.score)
    foundation = foundation_layer(x, data.quote)
    news = news_layer(x, data.news, symbol)
    history = historical_layer(x, horizon)
    relationships, narrative, board = relationship_and_narrative(data.news, symbol, data.quote)

    frames = timeframe_frames or {"1d": data.bars}
    if "1w" not in frames and len(data.bars) >= 90:
        frames = dict(frames)
        frames["1w"] = data.bars.resample("W-FRI").agg({
            "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
        }).dropna(subset=["close"])
    timeframes = timeframe_matrix(frames, use_stochastic)
    apply_timeframe_context(trend, timeframes)

    layers = {z.key: z for z in [foundation, trend, momentum, route_layer, news, history, memory, relationships, narrative]}
    fc = forecast(x, horizon)
    net, bull, bear, confidence = aggregate(layers, fc)
    contributions = contribution_breakdown(layers, fc)
    action = action_state(net, confidence)

    biggest_for = max(layers.values(), key=lambda z: z.score * z.confidence)
    biggest_against = min(layers.values(), key=lambda z: z.score * z.confidence)
    if bull >= bear:
        summary = f"Buyers have the evidence edge ({bull} to {bear}), but this is evidence, not a promise. The strongest help is {biggest_for.label.lower()}. The biggest problem is {biggest_against.label.lower()}."
    else:
        summary = f"Sellers have the evidence edge ({bear} to {bull}), but this is evidence, not a promise. The strongest warning is {biggest_against.label.lower()}. The best thing on the other side is {biggest_for.label.lower()}."
    consensus = timeframes.get("consensus", {})
    if consensus.get("available_count", 0) >= 2:
        summary += f" The multi-timeframe read is {consensus.get('direction')} with {float(consensus.get('agreement', 0)):.0%} agreement."
    if route.next_bus_stops:
        summary += f" The next bus stop is near {route.next_bus_stops[0]:.4g}."
    if route.invalidation:
        summary += f" The current route is wrong near {route.invalidation:.4g}."

    technical = (
        f"Net evidence={net:+.3f}; confidence={confidence:.3f}; trend={trend.state}; momentum={momentum.state}; "
        f"historical={history.state}; forecast={fc.get('state')}; timeframe_consensus={consensus.get('direction', 'unknown')} "
        f"({consensus.get('agreement', 0)}). Correlated technical and news-derived layers are discounted before aggregation."
    )
    catalysts = (news.metrics or {}).get("timeline", [])
    return Report(
        symbol=symbol.upper(), horizon_days=horizon, price=float(x.close.iloc[-1]), action=action,
        bull_evidence=bull, bear_evidence=bear, confidence=round(confidence, 3), summary=summary,
        technical_summary=technical, route=route, layers=layers, forecast=fc, evidence_board=board,
        data_meta=data.meta | {"bars": len(data.bars), "quote": data.quote}, chart=compact_chart(x, 360),
        timeframes=timeframes, contributions=contributions, catalysts=catalysts,
        calibration=_calibration(history),
    )


def analyze(symbol: str, horizon: int = 20, csv_path: str | None = None, use_stochastic: bool = False) -> Report:
    data = get_market_data(symbol, csv_path)
    frames = get_timeframe_bars(symbol, data)
    return analyze_frame(symbol, data, horizon, use_stochastic, frames)
