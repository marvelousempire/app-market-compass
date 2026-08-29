from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from .models import Evidence, LayerResult, Route


def ema(s: pd.Series, period: int) -> pd.Series:
    return s.ewm(span=period, adjust=False, min_periods=period).mean()


def rsi(s: pd.Series, period: int = 14) -> pd.Series:
    d = s.diff()
    gain = d.clip(lower=0).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    loss = (-d.clip(upper=0)).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    rs = gain / loss.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.where(loss.ne(0), 100).fillna(50)


def macd(s: pd.Series) -> pd.DataFrame:
    fast, slow = ema(s, 12), ema(s, 26)
    line = fast - slow
    signal = line.ewm(span=9, adjust=False, min_periods=9).mean()
    return pd.DataFrame({"macd": line, "signal": signal, "hist": line - signal})


def stochastic(df: pd.DataFrame, period: int = 14) -> pd.Series:
    low = df.low.rolling(period).min()
    high = df.high.rolling(period).max()
    return (100 * (df.close - low) / (high - low).replace(0, np.nan)).fillna(50)


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    for p in (13, 27, 50, 81):
        x[f"ema{p}"] = ema(x.close, p)
    x["rsi14"] = rsi(x.close)
    x = x.join(macd(x.close))
    x["ret1"] = x.close.pct_change()
    x["ret5"] = x.close.pct_change(5)
    x["ret20"] = x.close.pct_change(20)
    x["vol20"] = x.ret1.rolling(20).std() * math.sqrt(252)
    x["vol_z"] = (x.volume - x.volume.rolling(30).mean()) / x.volume.rolling(30).std().replace(0, np.nan)
    return x


def trend_layer(x: pd.DataFrame) -> LayerResult:
    row, prev = x.iloc[-1], x.iloc[-6]
    aligned_up = row.ema13 > row.ema27 > row.ema81
    aligned_down = row.ema13 < row.ema27 < row.ema81
    slope = np.nanmean([(row[f"ema{p}"] / prev[f"ema{p}"] - 1) for p in (13, 27, 81)])
    score = float(np.clip((0.65 if aligned_up else -0.65 if aligned_down else 0) + np.tanh(slope * 80) * 0.35, -1, 1))
    state = "strong uptrend" if score > .55 else "uptrend" if score > .15 else "strong downtrend" if score < -.55 else "downtrend" if score < -.15 else "range or transition"
    ev, ce = [], []
    (ev if row.ema13 > row.ema27 else ce).append(Evidence(text=f"EMA 13 is {'above' if row.ema13 > row.ema27 else 'below'} EMA 27.", direction=1 if row.ema13 > row.ema27 else -1, strength=.7))
    (ev if row.close > row.ema81 else ce).append(Evidence(text=f"Price is {'above' if row.close > row.ema81 else 'below'} EMA 81.", direction=1 if row.close > row.ema81 else -1, strength=.8))
    return LayerResult(key="trend", label="Trend", state=state, score=score, confidence=.85 if aligned_up or aligned_down else .62, evidence=ev, counter_evidence=ce, metrics={"ema13": row.ema13, "ema27": row.ema27, "ema50": row.ema50, "ema81": row.ema81, "slope": slope})


def _rsi_divergence(x: pd.DataFrame, lookback: int = 20) -> tuple[str, float, float]:
    d = x[["close", "rsi14"]].tail(lookback).dropna()
    if len(d) < 10:
        return "none", 0.0, 0.0
    t = np.arange(len(d), dtype=float)
    price_slope = float(np.polyfit(t, d.close.to_numpy(dtype=float), 1)[0] / max(abs(d.close.mean()), 1e-9))
    rsi_slope = float(np.polyfit(t, d.rsi14.to_numpy(dtype=float), 1)[0] / 100)
    if price_slope < -0.0005 and rsi_slope > 0.0005:
        return "bullish", price_slope, rsi_slope
    if price_slope > 0.0005 and rsi_slope < -0.0005:
        return "bearish", price_slope, rsi_slope
    return "none", price_slope, rsi_slope


def momentum_layer(x: pd.DataFrame, use_stochastic: bool = False) -> LayerResult:
    row, p1, p5 = x.iloc[-1], x.iloc[-2], x.iloc[-6]
    points = 0.0
    points += .25 if row.rsi14 > 50 else -.25
    points += .20 if row.rsi14 > p5.rsi14 else -.20
    points += .30 if row.macd > row.signal else -.30
    points += .15 if row["hist"] > p1["hist"] else -.15
    points += .10 if row.close > row.ema13 else -.10
    divergence, price_slope, rsi_slope = _rsi_divergence(x)
    if divergence == "bullish":
        points += .12
    elif divergence == "bearish":
        points -= .12
    zone = "oversold" if row.rsi14 < 30 else "overbought" if row.rsi14 > 70 else "bullish half" if row.rsi14 >= 50 else "bearish half"
    crossed_30_up = bool(p1.rsi14 < 30 <= row.rsi14)
    crossed_50_up = bool(p1.rsi14 < 50 <= row.rsi14)
    crossed_50_down = bool(p1.rsi14 > 50 >= row.rsi14)
    crossed_70_down = bool(p1.rsi14 > 70 >= row.rsi14)
    metrics: dict[str, Any] = {
        "rsi14": row.rsi14, "rsi_zone": zone, "rsi_change_5": row.rsi14 - p5.rsi14,
        "crossed_30_up": crossed_30_up, "crossed_50_up": crossed_50_up,
        "crossed_50_down": crossed_50_down, "crossed_70_down": crossed_70_down,
        "rsi_divergence": divergence, "price_slope_20": price_slope, "rsi_slope_20": rsi_slope,
        "macd": row.macd, "macd_signal": row.signal, "histogram": row["hist"],
    }
    if use_stochastic:
        k = stochastic(x).iloc[-1]
        metrics["stochastic"] = k
        points = .9 * points + (.1 if 20 < k < 80 and points > 0 else -.1 if k > 80 else 0)
    score = float(np.clip(points, -1, 1))
    improving = row.rsi14 > p5.rsi14 and row["hist"] > p1["hist"]
    long_bear = row.close < row.ema81
    if improving and long_bear:
        state = "possible bounce inside a downtrend"
    elif score > .45 and row.close > row.ema81:
        state = "bullish reversal or continuation"
    elif score < -.45 and row.close < row.ema81:
        state = "bearish continuation"
    elif abs(score) < .2:
        state = "mixed momentum"
    else:
        state = "early reversal watch" if improving else "momentum fading"
    observations = [
        Evidence(text=f"RSI 14 is {row.rsi14:.1f}, in the {zone}.", direction=1 if row.rsi14 >= 50 else -1, strength=.6),
        Evidence(text=f"MACD is {'above' if row.macd > row.signal else 'below'} its signal line.", direction=1 if row.macd > row.signal else -1, strength=.7),
    ]
    if divergence != "none":
        observations.append(Evidence(text=f"RSI shows {divergence} divergence over the recent window.", direction=1 if divergence == "bullish" else -1, strength=.55))
    return LayerResult(
        key="momentum", label="Momentum & Reversal", state=state, score=score, confidence=.78,
        evidence=[e for e in observations if e.direction > 0], counter_evidence=[e for e in observations if e.direction < 0], metrics=metrics,
    )


def _cluster_levels(values: list[tuple[pd.Timestamp, float]], tolerance: float) -> list[dict]:
    clusters: list[dict] = []
    for dt, value in sorted(values, key=lambda z: z[1]):
        hit = next((c for c in clusters if abs(value - c["price"]) <= tolerance), None)
        if hit:
            n = hit["touches"]
            hit["price"] = (hit["price"] * n + value) / (n + 1)
            hit["touches"] += 1
            hit["dates"].append(dt)
        else:
            clusters.append({"price": float(value), "touches": 1, "dates": [dt]})
    return clusters


def price_memory(x: pd.DataFrame, lookback: int = 500) -> tuple[list[dict], list[dict]]:
    d = x.tail(lookback)
    if len(d) < 20:
        return [], []
    w = 3
    lows, highs = [], []
    for i in range(w, len(d) - w):
        row = d.iloc[i]
        if row.low <= d.low.iloc[i-w:i+w+1].min():
            lows.append((d.index[i], row.low))
        if row.high >= d.high.iloc[i-w:i+w+1].max():
            highs.append((d.index[i], row.high))
    atr = (d.high - d.low).rolling(14).mean().iloc[-1]
    tolerance = float(max(d.close.iloc[-1] * .006, atr * .35 if pd.notna(atr) else 0))

    def decorate(clusters: list[dict], side: str) -> list[dict]:
        out = []
        now = d.index[-1]
        current = float(d.close.iloc[-1])
        series = d.low if side == "support" else d.high
        for c in clusters:
            near = (series - c["price"]).abs() <= tolerance
            starts = near & ~near.shift(1, fill_value=False)
            dates = list(d.index[starts]) or c["dates"]
            touches = len(dates)
            reactions = []
            for dt in dates:
                pos = d.index.get_loc(dt)
                future = d.iloc[pos + 1:pos + 6]
                if future.empty:
                    continue
                if side == "support":
                    reactions.append(max(0.0, float(future.high.max() / c["price"] - 1)))
                else:
                    reactions.append(max(0.0, float(1 - future.low.min() / c["price"])))
            avg_reaction = float(np.mean(reactions)) if reactions else 0.0
            span = max((dates[-1] - dates[0]).days, 1)
            age = max((now - dates[-1]).days, 0)
            erosion = min(1.0, max(0.0, (touches - 3) / 7))
            volume_ratio = float(d.loc[near, "volume"].mean() / d.volume.median()) if near.any() and d.volume.median() else 1.0
            strength = min(1.0, .15 * touches + .10 * np.log1p(span) + 2.5 * avg_reaction + .08 * min(volume_ratio, 2) + .12 * np.exp(-age / 180) - .18 * erosion)
            out.append({
                "price": round(c["price"], 6), "touches": touches,
                "first_seen": dates[0].isoformat(), "last_seen": dates[-1].isoformat(),
                "span_days": span, "age_days": age, "avg_reaction": round(avg_reaction, 4),
                "volume_ratio": round(volume_ratio, 3), "erosion": round(float(erosion), 3),
                "strength": round(float(max(0, strength)), 3), "type": side,
                "distance_pct": round(float(c["price"] / current - 1), 4),
            })
        return sorted(out, key=lambda z: z["strength"], reverse=True)

    return decorate(_cluster_levels(lows, tolerance), "support"), decorate(_cluster_levels(highs, tolerance), "resistance")


def fibonacci(x: pd.DataFrame, lookback: int = 180) -> tuple[str, dict[str, float]]:
    d = x.tail(lookback)
    hi_i, lo_i = d.high.idxmax(), d.low.idxmin()
    hi, lo = float(d.loc[hi_i, "high"]), float(d.loc[lo_i, "low"])
    levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618]
    if lo_i < hi_i:
        direction = "up"
        vals = {str(k): hi - (hi - lo) * k for k in levels[:6]}
        vals.update({str(k): lo + (hi - lo) * k for k in levels[6:]})
    else:
        direction = "down"
        vals = {str(k): lo + (hi - lo) * k for k in levels[:6]}
        vals.update({str(k): hi - (hi - lo) * (k - 1) for k in levels[6:]})
    return direction, {k: round(float(v), 6) for k, v in vals.items()}


def fibonacci_anchors(x: pd.DataFrame, lookback: int = 180) -> dict[str, Any]:
    d = x.tail(lookback)
    hi_i, lo_i = d.high.idxmax(), d.low.idxmin()
    direction = "up" if lo_i < hi_i else "down"
    return {
        "direction": direction,
        "low_price": round(float(d.loc[lo_i, "low"]), 6), "low_date": lo_i.isoformat(),
        "high_price": round(float(d.loc[hi_i, "high"]), 6), "high_date": hi_i.isoformat(),
        "lookback_bars": len(d),
    }


def _confluence(fib: dict[str, float], x: pd.DataFrame, supports: list[dict], resistances: list[dict]) -> list[dict]:
    row = x.iloc[-1]
    references = [
        ("EMA 13", float(row.ema13)), ("EMA 27", float(row.ema27)),
        ("EMA 50", float(row.ema50)), ("EMA 81", float(row.ema81)),
    ]
    references += [(f"Support {i+1}", z["price"]) for i, z in enumerate(supports[:4])]
    references += [(f"Resistance {i+1}", z["price"]) for i, z in enumerate(resistances[:4])]
    tolerance = max(float(row.close) * .012, 1e-9)
    out: list[dict] = []
    for name, value in fib.items():
        hits = [label for label, ref in references if abs(value - ref) <= tolerance]
        if hits:
            out.append({"fib": name, "price": value, "matches": hits, "strength": round(min(1.0, .35 + .18 * len(hits)), 3)})
    return sorted(out, key=lambda z: z["strength"], reverse=True)


def memory_and_route_layers(x: pd.DataFrame, trend_score: float) -> tuple[LayerResult, LayerResult, Route]:
    price = float(x.close.iloc[-1])
    supports, resistances = price_memory(x)
    below = sorted([z for z in supports if z["price"] < price], key=lambda z: price - z["price"])
    above = sorted([z for z in resistances if z["price"] > price], key=lambda z: z["price"] - price)
    fib_dir, fib = fibonacci(x)
    anchors = fibonacci_anchors(x)
    confluence = _confluence(fib, x, below, above)
    fib_vals = sorted(set(fib.values()))
    ups = sorted(set([z["price"] for z in above[:3]] + [v for v in fib_vals if v > price]))[:3]
    downs = sorted(set([z["price"] for z in below[:3]] + [v for v in fib_vals if v < price]), reverse=True)[:3]
    direction = "up" if trend_score > .1 else "down" if trend_score < -.1 else fib_dir
    last = (downs[0] if downs else None) if direction == "up" else (ups[0] if ups else None)
    next_stops = ups if direction == "up" else downs
    invalid = (downs[0] if downs else None) if direction == "up" else (ups[0] if ups else None)
    rr = None
    if next_stops and invalid and abs(price - invalid) > 0:
        rr = abs(next_stops[0] - price) / abs(price - invalid)
    route = Route(
        direction=direction, last_bus_stop=last, next_bus_stops=next_stops, downside_stops=downs,
        invalidation=invalid, reward_risk=round(rr, 2) if rr else None, fibonacci=fib,
        fibonacci_anchors=anchors, confluence=confluence,
    )
    sup_strength = below[0]["strength"] if below else 0
    res_strength = above[0]["strength"] if above else 0
    mem_score = float(np.clip(sup_strength - res_strength, -1, 1))
    mem = LayerResult(
        key="memory", label="Price Memory", state="support stronger" if mem_score > .1 else "resistance stronger" if mem_score < -.1 else "balanced",
        score=mem_score, confidence=.72 if below and above else .48,
        evidence=[Evidence(text=f"Nearest support has strength {sup_strength:.2f}.", direction=1, strength=sup_strength)] if below else [],
        counter_evidence=[Evidence(text=f"Nearest resistance has strength {res_strength:.2f}.", direction=-1, strength=res_strength)] if above else [],
        metrics={"supports": supports[:10], "resistances": resistances[:10]},
        missing=[] if supports and resistances else ["one side has no well-tested level in the current history"],
    )
    route_score = .35 if direction == "up" else -.35 if direction == "down" else 0
    if rr is not None:
        route_score += .25 * np.tanh(rr - 1) * (1 if direction == "up" else -1)
    if confluence:
        route_score += .08 * confluence[0]["strength"] * (1 if direction == "up" else -1)
    route_layer = LayerResult(
        key="route", label="Fibonacci & Bus Stops", state=f"route {direction}", score=float(np.clip(route_score, -1, 1)), confidence=min(.88, (.68 if next_stops and invalid else .4) + .04 * len(confluence)),
        evidence=[Evidence(text=f"Next bus stop is {next_stops[0]:.4g}." if next_stops else "No clear next bus stop.", direction=1 if direction == "up" else -1, strength=.65)],
        counter_evidence=[Evidence(text=f"The route is invalidated near {invalid:.4g}." if invalid else "No reliable invalidation level found.", direction=-1 if direction == "up" else 1, strength=.7)],
        metrics={"fibonacci_direction": fib_dir, "fibonacci": fib, "fibonacci_anchors": anchors, "confluence": confluence, "reward_risk": rr},
    )
    return mem, route_layer, route


def compact_chart(x: pd.DataFrame, limit: int = 240) -> dict[str, list[Any]]:
    d = x.tail(limit)
    def vals(name: str, digits: int = 6) -> list[Any]:
        return [None if pd.isna(v) else round(float(v), digits) for v in d[name]]
    return {
        "date": [z.isoformat() for z in d.index],
        "open": vals("open"), "high": vals("high"), "low": vals("low"), "close": vals("close"), "volume": vals("volume", 2),
        "ema13": vals("ema13"), "ema27": vals("ema27"), "ema50": vals("ema50"), "ema81": vals("ema81"),
        "rsi14": vals("rsi14", 3), "macd": vals("macd"), "signal": vals("signal"), "hist": vals("hist"),
    }


def timeframe_matrix(frames: dict[str, pd.DataFrame], use_stochastic: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in ("4h", "1d", "1w"):
        frame = frames.get(key)
        if frame is None or len(frame) < 90:
            result[key] = {"available": False, "reason": "not enough bars"}
            continue
        x = enrich(frame)
        trend = trend_layer(x)
        momentum = momentum_layer(x, use_stochastic)
        result[key] = {
            "available": True, "price": round(float(x.close.iloc[-1]), 6),
            "trend_state": trend.state, "trend_score": round(float(trend.score), 4),
            "momentum_state": momentum.state, "momentum_score": round(float(momentum.score), 4),
            "rsi14": round(float(x.rsi14.iloc[-1]), 2), "ema13": round(float(x.ema13.iloc[-1]), 6),
            "ema27": round(float(x.ema27.iloc[-1]), 6), "ema50": round(float(x.ema50.iloc[-1]), 6), "ema81": round(float(x.ema81.iloc[-1]), 6),
            "chart": compact_chart(x, 220 if key != "1w" else 180),
        }
    available = [v for v in result.values() if v.get("available")]
    if available:
        signs = [np.sign(v["trend_score"]) for v in available if abs(v["trend_score"]) > .08]
        result["consensus"] = {
            "available_count": len(available),
            "direction": "up" if signs and sum(signs) > 0 else "down" if signs and sum(signs) < 0 else "mixed",
            "agreement": round(float(abs(sum(signs)) / len(signs)), 3) if signs else 0.0,
        }
    else:
        result["consensus"] = {"available_count": 0, "direction": "unknown", "agreement": 0.0}
    return result


def apply_timeframe_context(trend: LayerResult, timeframes: dict[str, Any]) -> None:
    consensus = timeframes.get("consensus", {})
    agreement = float(consensus.get("agreement", 0))
    direction = consensus.get("direction")
    if consensus.get("available_count", 0) < 2:
        trend.metrics["timeframe_consensus"] = consensus
        return
    sign = 1 if direction == "up" else -1 if direction == "down" else 0
    if sign:
        trend.score = float(np.clip(.82 * trend.score + .18 * sign * agreement, -1, 1))
    trend.confidence = float(np.clip(trend.confidence * (.82 + .24 * agreement), .25, .95))
    trend.metrics["timeframe_consensus"] = consensus
