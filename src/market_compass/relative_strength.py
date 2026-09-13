from __future__ import annotations

from typing import Any

import pandas as pd

from .technical import enrich, rsi

ZONE_ORDER = (
    "oversold",
    "support_zone",
    "neutral",
    "resistance_zone",
    "overbought",
)

ZONE_LABEL = {
    "oversold": "Oversold",
    "support_zone": "Support Zone",
    "neutral": "Neutral",
    "resistance_zone": "Resistance Zone",
    "overbought": "Overbought",
}

HORIZON_BARS = {
    "1d": 1,
    "7d": 7,
    "14d": 14,
    "30d": 30,
}

TAPE_UNIVERSE = (
    ("BTC", "BTC-USD"),
    ("ETH", "ETH-USD"),
    ("SOL", "SOL-USD"),
)


def rsi_zone(value: float | None) -> str | None:
    if value is None or pd.isna(value):
        return None
    if value < 30:
        return "oversold"
    if value < 40:
        return "support_zone"
    if value < 60:
        return "neutral"
    if value <= 70:
        return "resistance_zone"
    return "overbought"


def _round(value: float | None, digits: int = 4) -> float | None:
    if value is None or pd.isna(value):
        return None
    return round(float(value), digits)


def _pct_change(series: pd.Series, bars: int) -> float | None:
    if series is None or len(series) <= bars:
        return None
    start = float(series.iloc[-(bars + 1)])
    end = float(series.iloc[-1])
    if start == 0:
        return None
    return end / start - 1


def _last_rsi(frame: pd.DataFrame | None, min_bars: int = 20) -> float | None:
    if frame is None or len(frame) < min_bars:
        return None
    return float(rsi(frame.close).iloc[-1])


def _aligned_return(asset: pd.Series, bench: pd.Series, bars: int) -> dict[str, float | None]:
    joined = pd.concat({"asset": asset, "bench": bench}, axis=1).dropna()
    asset_ret = _pct_change(joined["asset"], bars)
    bench_ret = _pct_change(joined["bench"], bars)
    residual = None
    if asset_ret is not None and bench_ret is not None:
        residual = asset_ret - bench_ret
    return {
        "asset": _round(asset_ret, 4),
        "benchmark": _round(bench_ret, 4),
        "residual": _round(residual, 4),
    }


def drawdown_memory(bars: pd.DataFrame) -> dict[str, Any]:
    if bars is None or bars.empty:
        return {"ath": None, "week_52": None, "missing": ["price history"]}
    high = bars.high if "high" in bars else bars.close
    ath_idx = high.idxmax()
    ath_price = float(high.loc[ath_idx])
    price = float(bars.close.iloc[-1])
    window = bars.tail(252)
    week_idx = window.high.idxmax() if "high" in window else window.close.idxmax()
    week_price = float((window.high if "high" in window else window.close).loc[week_idx])
    last = bars.iloc[-1]
    day_range = None
    if "high" in last and "low" in last and float(last.low) > 0:
        day_range = float(last.high) - float(last.low)
        day_range_pct = day_range / float(last.close) if float(last.close) else None
    else:
        day_range_pct = None
    return {
        "ath": {
            "price": _round(ath_price, 6),
            "date": ath_idx.isoformat(),
            "drawdown": _round(price / ath_price - 1, 4) if ath_price else None,
            "gap": _round(ath_price - price, 6),
        },
        "week_52": {
            "price": _round(week_price, 6),
            "date": week_idx.isoformat(),
            "drawdown": _round(price / week_price - 1, 4) if week_price else None,
        },
        "session": {
            "high": _round(float(last.high), 6) if "high" in last else None,
            "low": _round(float(last.low), 6) if "low" in last else None,
            "range": _round(day_range, 6),
            "range_pct": _round(day_range_pct, 4),
        },
        "missing": [],
    }


def ema_distance_stack(x: pd.DataFrame) -> list[dict[str, Any]]:
    row = x.iloc[-1]
    price = float(row.close)
    stack = []
    for period in (13, 27, 81):
        value = float(row[f"ema{period}"]) if f"ema{period}" in row and pd.notna(row[f"ema{period}"]) else None
        stack.append({
            "period": period,
            "ema": _round(value, 6),
            "distance_pct": _round(price / value - 1, 4) if value else None,
            "side": "above" if value and price >= value else "below" if value else "missing",
        })
    return stack


def horizon_returns(close: pd.Series) -> dict[str, float | None]:
    return {key: _round(_pct_change(close, bars), 4) for key, bars in HORIZON_BARS.items()}


def multi_horizon_rsi(frames: dict[str, pd.DataFrame]) -> dict[str, Any]:
    readings = {}
    for key, min_bars in (("1h", 20), ("4h", 20), ("1d", 20), ("1w", 20)):
        value = _last_rsi(frames.get(key), min_bars)
        zone = rsi_zone(value)
        readings[key] = {
            "available": value is not None,
            "rsi14": _round(value, 2),
            "zone": zone,
            "zone_label": ZONE_LABEL.get(zone) if zone else None,
        }
    ltf = next((readings[k] for k in ("1h", "4h", "1d") if readings[k]["available"]), None)
    htf = next((readings[k] for k in ("1w", "1d") if readings[k]["available"]), None)
    conflict = False
    if ltf and htf and ltf["zone"] and htf["zone"]:
        gap = abs(ZONE_ORDER.index(ltf["zone"]) - ZONE_ORDER.index(htf["zone"]))
        conflict = gap >= 2
    return {
        "readings": readings,
        "ltf": "1h" if readings["1h"]["available"] else "4h" if readings["4h"]["available"] else "1d",
        "htf": "1w" if readings["1w"]["available"] else "1d",
        "conflict": conflict,
    }


def relative_vs_benchmarks(
    asset_close: pd.Series,
    benchmarks: dict[str, pd.Series],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    missing: list[str] = []
    for name in ("BTC", "ETH"):
        series = benchmarks.get(name)
        if series is None or series.empty:
            missing.append(f"{name} benchmark series")
            out[name] = {key: {"asset": None, "benchmark": None, "residual": None} for key in HORIZON_BARS}
            continue
        out[name] = {key: _aligned_return(asset_close, series, bars) for key, bars in HORIZON_BARS.items()}
    return {"benchmarks": out, "missing": missing}


def build_relative_strength(
    bars: pd.DataFrame,
    frames: dict[str, pd.DataFrame] | None = None,
    benchmarks: dict[str, pd.Series] | None = None,
) -> dict[str, Any]:
    x = bars if {"ema13", "rsi14"} <= set(bars.columns) else enrich(bars)
    frames = dict(frames or {})
    frames.setdefault("1d", bars[["open", "high", "low", "close", "volume"]] if set("open high low close volume".split()) <= set(bars.columns) else bars)
    rsi_pack = multi_horizon_rsi(frames)
    vs = relative_vs_benchmarks(x.close, benchmarks or {})
    memory = drawdown_memory(x)
    readings = rsi_pack["readings"]
    ltf_key, htf_key = rsi_pack["ltf"], rsi_pack["htf"]
    chip = []
    if readings[ltf_key]["available"]:
        chip.append(f"{ltf_key.upper()} {readings[ltf_key]['rsi14']:.0f} {readings[ltf_key]['zone_label']}")
    if readings[htf_key]["available"]:
        chip.append(f"HTF {htf_key.upper()} {readings[htf_key]['rsi14']:.0f} {readings[htf_key]['zone_label']}")
    if rsi_pack["conflict"]:
        chip.append("conflict")
    missing = list(vs["missing"]) + list(memory.get("missing") or [])
    if not readings["1h"]["available"]:
        missing.append("1h RSI")
    if not readings["4h"]["available"]:
        missing.append("4h RSI")
    return {
        "chip": " · ".join(chip) if chip else "RSI unavailable",
        "conflict": rsi_pack["conflict"],
        "rsi": rsi_pack,
        "returns": horizon_returns(x.close),
        "vs": vs["benchmarks"],
        "ema_stack": ema_distance_stack(x),
        "drawdown": memory,
        "missing": missing,
        "note": "Relative strength is context. It does not change the evidence split or action state.",
    }


def empty_tape(reason: str) -> dict[str, Any]:
    return {
        "as_of": None,
        "members": [],
        "missing": ["total crypto market cap", "bitcoin dominance", reason],
        "note": "Market Tape uses the same Yahoo public chart endpoints. Broad-market cap and BTC.D stay missing until a dedicated breadth source exists.",
    }


def build_market_tape(members: list[dict[str, Any]], as_of: str | None = None) -> dict[str, Any]:
    missing = ["total crypto market cap", "bitcoin dominance"]
    if not members:
        missing.append("major tape quotes")
    return {
        "as_of": as_of,
        "members": members,
        "missing": missing,
        "note": "Tape quotes are last regular session closes from Yahoo. Dominance and aggregate market cap are not inferred.",
    }
