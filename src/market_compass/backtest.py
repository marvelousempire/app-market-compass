from __future__ import annotations

import numpy as np
import pandas as pd

from .technical import enrich


def backtest_frame(df: pd.DataFrame, horizon: int = 20, fee_bps: float = 10.0) -> dict:
    x = enrich(df).dropna(subset=["ema13", "ema27", "ema81", "rsi14", "hist"]).copy()
    # Past-only signal. No future values enter the signal calculation.
    bull = (x.ema13 > x.ema27) & (x.rsi14 > 50) & (x["hist"] > 0)
    bear = (x.ema13 < x.ema27) & (x.rsi14 < 50) & (x["hist"] < 0)
    signal = pd.Series(np.select([bull, bear], [1.0, -1.0], default=0.0), index=x.index)
    forward = x.close.shift(-horizon) / x.close - 1
    valid = forward.notna()
    gross = signal[valid] * forward[valid]
    costs = signal[valid].diff().abs().fillna(signal[valid].abs()) * fee_bps / 10_000
    net = gross - costs
    active = signal[valid] != 0
    trades = net[active]
    if trades.empty:
        return {"trades": 0, "mean_return": 0.0, "win_rate": 0.0, "max_loss": 0.0, "note": "No qualifying signals."}
    return {
        "trades": len(trades),
        "mean_return": float(trades.mean()),
        "median_return": float(trades.median()),
        "win_rate": float((trades > 0).mean()),
        "max_loss": float(trades.min()),
        "max_gain": float(trades.max()),
        "fee_bps": fee_bps,
        "horizon_bars": horizon,
        "note": "Research backtest only. Overlapping horizon trades are counted as signal observations, not a cash-account simulation.",
    }
