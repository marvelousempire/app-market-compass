"""Clean-room Market Compass lens inspired by day-trader-skill.

The upstream repository is evidence and design input. This module does not
import or execute upstream code, create orders, size positions, or touch an
account. Its outputs are read-only research receipts.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
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


def _event(
    event_id: str,
    label: str,
    state: str,
    evidence: str,
    owner: str,
    *,
    inputs: dict[str, Any],
    formula: str,
    timestamp: str,
    direction: str = "none",
) -> dict[str, Any]:
    return {"id": event_id, "label": label, "state": state, "evidence": evidence,
            "owner": owner, "direction": direction, "inputs": inputs,
            "formula": formula, "timeframe": "1D", "timestamp": timestamp,
            "provenance": {"source": SOURCE["url"], "revision": SOURCE["revision"]},
            "confidence": {"value": 1.0, "meaning": "deterministic formula execution; not outcome probability"},
            "authority": "research_only"}


def build_day_trader_lens(
    symbol: str, bars: pd.DataFrame, *, data_meta: dict[str, Any] | None = None
) -> dict[str, Any]:
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
    timestamp = frame.index[-1].isoformat()
    provenance = {
        "provider": (data_meta or {}).get("provider", "provided-bars"),
        "requested_symbol": (data_meta or {}).get("requested_symbol", symbol.upper()),
        "resolved_symbol": (data_meta or {}).get("resolved_symbol", symbol.upper()),
    }
    setups = [
        _event("breakout_20d", "20-day closing-high breakout", "observed" if last > twenty_high else "not_observed", f"close {last:.4g}; prior 20-day closing high {twenty_high:.4g}", "Brown's Barometers", inputs={"close": last, "prior_20d_closing_high": twenty_high}, formula="close > max(prior 20 daily closes)", timestamp=timestamp, direction="above" if last > twenty_high else "none"),
        _event("reclaim_ma20", "Reclaimed 20-day average", "observed" if prior < float(ma20.iloc[-2]) and last > float(ma20.iloc[-1]) else "not_observed", f"close {last:.4g}; MA20 {float(ma20.iloc[-1]):.4g}", "Brown's Barometers", inputs={"prior_close": prior, "close": last, "prior_ma20": float(ma20.iloc[-2]), "ma20": float(ma20.iloc[-1])}, formula="prior_close < prior_MA20 and close > MA20", timestamp=timestamp, direction="above" if prior < float(ma20.iloc[-2]) and last > float(ma20.iloc[-1]) else "none"),
        _event("bull_flag", "Compact flag after 10-session run", "observed" if runup > .10 and flag_range <= .05 else "not_observed", f"run {runup:.1%}; five-session range {flag_range:.1%}", "Brown's Barometers", inputs={"ten_session_run": runup, "five_session_range": flag_range}, formula="ten_session_run > 10% and five_session_range <= 5%", timestamp=timestamp),
        _event("oversold", "RSI below 30", "observed" if float(rsi.iloc[-1]) < 30 else "not_observed", f"RSI14 {float(rsi.iloc[-1]):.1f}", "Wuda", inputs={"rsi14": float(rsi.iloc[-1]), "threshold": 30}, formula="RSI14 < 30", timestamp=timestamp, direction="below" if float(rsi.iloc[-1]) < 30 else "none"),
        _event("oversold_bounce", "RSI oversold bounce", "observed" if float(rsi.iloc[-2]) < 30 and last > prior else "not_observed", f"prior RSI14 {float(rsi.iloc[-2]):.1f}; close change {(last / prior - 1):.1%}", "Wuda", inputs={"prior_rsi14": float(rsi.iloc[-2]), "prior_close": prior, "close": last}, formula="prior_RSI14 < 30 and close > prior_close", timestamp=timestamp, direction="above" if float(rsi.iloc[-2]) < 30 and last > prior else "none"),
    ]
    thresholds = []
    for level in (35, 50, 65):
        before, now = float(rsi.iloc[-2]), float(rsi.iloc[-1])
        direction = "above" if before < level <= now else "below" if before > level >= now else "none"
        thresholds.append(_event(f"rsi_{level}_cross", f"RSI crossed {direction} {level}" if direction != "none" else f"RSI {level} threshold", "observed" if direction != "none" else "not_observed", f"RSI14 {before:.1f} → {now:.1f}", "Wuda", inputs={"prior_rsi14": before, "rsi14": now, "threshold": level}, formula=f"prior_RSI14 < {level} <= RSI14 or prior_RSI14 > {level} >= RSI14", timestamp=timestamp, direction=direction))
    observed = [item["label"] for item in setups + thresholds if item["state"] == "observed"]
    result = {
        "lens_id": "day-trader-research", "symbol": symbol.upper(),
        "state": "observed" if observed else "quiet",
        "summary": "; ".join(observed) if observed else "No admitted daily setup or RSI crossing is active.",
        "micro_slices": {"setup_scanner": setups, "notable_thresholds": thresholds,
            "opening_range": {"state": "held", "reason": "Intraday bars are not present in the default daily feed."},
            "historical_scenario": {"state": "reference", "reason": "Use Market Compass Historical Analogs and Backtest; simulations are not predictions."}},
        "source": SOURCE,
        "data": {"bars": len(frame), "last_bar": timestamp, "freshness": "provider-bound", **provenance},
        "authority": {"research_only": True, "score_influence": False, "trade_execution": False, "money_movement": False},
        "rejected": ["trader-broker", "order submission", "account credentials", "position sizing as an account action", "unattended alerts that imply execution"],
        "warning": "A setup is a chart condition, not a recommendation or prediction.",
    }
    receipt_payload = {
        "lens_id": result["lens_id"], "symbol": result["symbol"],
        "events": setups + thresholds, "data": result["data"], "source": SOURCE,
        "authority": result["authority"],
    }
    result["receipt"] = {
        "schema": "market-compass.research-lens-receipt.v1",
        "issued_at": datetime.now(UTC).isoformat(),
        "sha256": hashlib.sha256(json.dumps(receipt_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "exportable": True,
    }
    return result
