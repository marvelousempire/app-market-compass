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
