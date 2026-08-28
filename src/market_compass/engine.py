from __future__ import annotations

import pandas as pd

from .context import foundation_layer, forecast, historical_layer, news_layer, relationship_and_narrative
from .data import MarketData, get_market_data
from .models import Report
from .scoring import action_state, aggregate
from .technical import enrich, memory_and_route_layers, momentum_layer, trend_layer


def analyze_frame(symbol: str, data: MarketData, horizon: int = 20, use_stochastic: bool = False) -> Report:
    if len(data.bars) < 90:
        raise ValueError("At least 90 bars are required for the default EMA 81 profile")
    x = enrich(data.bars)
    trend = trend_layer(x)
    momentum = momentum_layer(x, use_stochastic)
    memory, route_layer, route = memory_and_route_layers(x, trend.score)
    foundation = foundation_layer(x, data.quote)
    news = news_layer(x, data.news, symbol)
    history = historical_layer(x, horizon)
    relationships, narrative, board = relationship_and_narrative(data.news, symbol)
    layers = {z.key: z for z in [foundation, trend, momentum, route_layer, news, history, memory, relationships, narrative]}
    fc = forecast(x, horizon)
    net, bull, bear, confidence = aggregate(layers, fc)
    action = action_state(net, confidence)

    biggest_for = max(layers.values(), key=lambda z: z.score * z.confidence)
    biggest_against = min(layers.values(), key=lambda z: z.score * z.confidence)
    if bull >= bear:
        summary = f"Buyers have the evidence edge ({bull} to {bear}), but this is evidence, not a promise. The strongest help is {biggest_for.label.lower()}. The biggest problem is {biggest_against.label.lower()}."
    else:
        summary = f"Sellers have the evidence edge ({bear} to {bull}), but this is evidence, not a promise. The strongest warning is {biggest_against.label.lower()}. The best thing on the other side is {biggest_for.label.lower()}."
    if route.next_bus_stops:
        summary += f" The next bus stop is near {route.next_bus_stops[0]:.4g}."
    if route.invalidation:
        summary += f" The current route is wrong near {route.invalidation:.4g}."

    technical = f"Net evidence={net:+.3f}; confidence={confidence:.3f}; trend={trend.state}; momentum={momentum.state}; historical={history.state}; forecast={fc.get('state')}. Correlated technical and news-derived layers are discounted before aggregation."
    chart_x = x.tail(180)
    chart = {
        "date": [d.isoformat() for d in chart_x.index],
        "close": [None if pd.isna(v) else round(float(v), 6) for v in chart_x.close],
        "ema13": [None if pd.isna(v) else round(float(v), 6) for v in chart_x.ema13],
        "ema27": [None if pd.isna(v) else round(float(v), 6) for v in chart_x.ema27],
        "ema81": [None if pd.isna(v) else round(float(v), 6) for v in chart_x.ema81],
    }
    return Report(symbol=symbol.upper(), horizon_days=horizon, price=float(x.close.iloc[-1]), action=action, bull_evidence=bull, bear_evidence=bear, confidence=round(confidence, 3), summary=summary, technical_summary=technical, route=route, layers=layers, forecast=fc, evidence_board=board, data_meta=data.meta | {"bars": len(data.bars), "quote": data.quote}, chart=chart)


def analyze(symbol: str, horizon: int = 20, csv_path: str | None = None, use_stochastic: bool = False) -> Report:
    return analyze_frame(symbol, get_market_data(symbol, csv_path), horizon, use_stochastic)
