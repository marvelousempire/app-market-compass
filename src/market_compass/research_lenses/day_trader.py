"""Clean-room Market Compass lens inspired by day-trader-skill.

The upstream repository is evidence and design input. This module does not
import or execute upstream code, create orders, size positions, or touch an
account. Its outputs are read-only research receipts.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

SOURCE = {
    "name": "day-trader-skill",
    "url": "https://github.com/marvelousempire/day-trader-skill",
    "revision": "3d0f4ef6986f4984b7c6bd46f7ff4f87744c3abd",
    "license": "MIT",
    "copyright": "Copyright (c) 2026 Jake Schincariol",
    "adaptation": "clean-room concepts; no upstream module is executed",
}


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    relative = gain / loss.replace(0, float("nan"))
    return (100 - 100 / (1 + relative)).fillna(100)


def _event(event_id: str, label: str, state: str, evidence: str, owner: str) -> dict[str, Any]:
    return {"id": event_id, "label": label, "state": state, "evidence": evidence,
            "owner": owner, "authority": "research_only"}


def build_day_trader_lens(symbol: str, bars: pd.DataFrame) -> dict[str, Any]:
    """Return deterministic daily setup and threshold MicroSlices."""
    if len(bars) < 30:
        raise ValueError("The day-trader lens requires at least 30 completed bars")
    frame = bars.sort_index().copy()
    close = frame["close"].astype(float)
    last, prior = float(close.iloc[-1]), float(close.iloc[-2])
    ma20 = close.rolling(20).mean()
    rsi = _rsi(close)
    twenty_high = float(close.iloc[-21:-1].max())
    runup = float(close.iloc[-6] / close.iloc[-16] - 1)
    flag_range = float((close.iloc[-5:].max() - close.iloc[-5:].min()) / close.iloc[-5:].min())
    setups = [
        _event("breakout_20d", "20-day closing-high breakout", "observed" if last > twenty_high else "not_observed", f"close {last:.4g}; prior 20-day closing high {twenty_high:.4g}", "Brown's Barometers"),
        _event("reclaim_ma20", "Reclaimed 20-day average", "observed" if prior < float(ma20.iloc[-2]) and last > float(ma20.iloc[-1]) else "not_observed", f"close {last:.4g}; MA20 {float(ma20.iloc[-1]):.4g}", "Brown's Barometers"),
        _event("bull_flag", "Compact flag after 10-session run", "observed" if runup > .10 and flag_range <= .05 else "not_observed", f"run {runup:.1%}; five-session range {flag_range:.1%}", "Brown's Barometers"),
        _event("oversold", "RSI below 30", "observed" if float(rsi.iloc[-1]) < 30 else "not_observed", f"RSI14 {float(rsi.iloc[-1]):.1f}", "Wuda"),
        _event("oversold_bounce", "RSI oversold bounce", "observed" if float(rsi.iloc[-2]) < 30 and last > prior else "not_observed", f"prior RSI14 {float(rsi.iloc[-2]):.1f}; close change {(last / prior - 1):.1%}", "Wuda"),
    ]
    thresholds = []
    for level in (35, 50, 65):
        before, now = float(rsi.iloc[-2]), float(rsi.iloc[-1])
        direction = "above" if before < level <= now else "below" if before > level >= now else "none"
        thresholds.append(_event(f"rsi_{level}_cross", f"RSI crossed {direction} {level}" if direction != "none" else f"RSI {level} threshold", "observed" if direction != "none" else "not_observed", f"RSI14 {before:.1f} → {now:.1f}", "Wuda"))
    observed = [item["label"] for item in setups + thresholds if item["state"] == "observed"]
    return {
        "lens_id": "day-trader-research", "symbol": symbol.upper(),
        "state": "observed" if observed else "quiet",
        "summary": "; ".join(observed) if observed else "No admitted daily setup or RSI crossing is active.",
        "micro_slices": {"setup_scanner": setups, "notable_thresholds": thresholds,
            "opening_range": {"state": "held", "reason": "Intraday bars are not present in the default daily feed."},
            "historical_scenario": {"state": "reference", "reason": "Use Market Compass Historical Analogs and Backtest; simulations are not predictions."}},
        "source": SOURCE,
        "data": {"bars": len(frame), "last_bar": frame.index[-1].isoformat(), "freshness": "provider-bound"},
        "authority": {"research_only": True, "score_influence": False, "trade_execution": False, "money_movement": False},
        "rejected": ["trader-broker", "order submission", "account credentials", "position sizing as an account action", "unattended alerts that imply execution"],
        "warning": "A setup is a chart condition, not a recommendation or prediction.",
    }
