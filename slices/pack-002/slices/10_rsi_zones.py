"""Pack #2 slice 10 — RSI zones. Stdlib only. No live feed."""
from __future__ import annotations

def rsi14(closes):
    if len(closes) < 15:
        return 50.0
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(d if d > 0 else 0.0)
        losses.append(-d if d < 0 else 0.0)
    period = 14
    avg_g = sum(gains[:period]) / period
    avg_l = sum(losses[:period]) / period
    for g, l in zip(gains[period:], losses[period:]):
        avg_g = (avg_g * (period - 1) + g) / period
        avg_l = (avg_l * (period - 1) + l) / period
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return 100.0 - 100.0 / (1.0 + rs)

def zone(value):
    if value < 30:
        return "oversold"
    if value > 70:
        return "overbought"
    if value >= 50:
        return "bullish_half"
    return "bearish_half"

def run(closes):
    value = round(rsi14(closes), 2)
    prev = round(rsi14(closes[:-1]), 2) if len(closes) > 16 else value
    return {
        "slice": "10_rsi_zones",
        "pack": "#2",
        "rsi14": value,
        "zone": zone(value),
        "prev_rsi14": prev,
        "crossed_30_up": prev < 30 <= value,
        "crossed_50_up": prev < 50 <= value,
        "crossed_50_down": prev > 50 >= value,
        "crossed_70_down": prev > 70 >= value,
    }
