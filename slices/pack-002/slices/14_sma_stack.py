"""Pack #2 slice 14 — SMA 20 / 50 / 200 stack."""
from __future__ import annotations

def sma(values, period):
    if len(values) < period:
        return None
    return sum(values[-period:]) / period

def run(closes):
    s20 = sma(closes, 20)
    s50 = sma(closes, 50)
    s200 = sma(closes, 200) if len(closes) >= 200 else sma(closes, min(len(closes), 100))
    last = closes[-1] if closes else None
    aligned_up = s20 is not None and s50 is not None and s200 is not None and last is not None and last > s20 > s50 > s200
    aligned_down = s20 is not None and s50 is not None and s200 is not None and last is not None and last < s20 < s50 < s200
    if aligned_up:
        stack = "bull_stack"
    elif aligned_down:
        stack = "bear_stack"
    else:
        stack = "mixed_stack"
    return {
        "slice": "14_sma_stack",
        "pack": "#2",
        "sma20": None if s20 is None else round(s20, 6),
        "sma50": None if s50 is None else round(s50, 6),
        "sma200_or_proxy": None if s200 is None else round(s200, 6),
        "last": last,
        "stack": stack,
        "price_above_sma20": None if s20 is None or last is None else last > s20,
    }
