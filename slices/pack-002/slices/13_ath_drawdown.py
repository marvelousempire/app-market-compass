"""Pack #2 slice 13 — ATH and current drawdown."""
from __future__ import annotations

def run(bars):
    if not bars:
        return {"slice": "13_ath_drawdown", "pack": "#2", "ath": None, "drawdown": None}
    ath_bar = max(bars, key=lambda b: b["high"])
    last = bars[-1]["close"]
    ath = ath_bar["high"]
    drawdown = 0.0 if ath == 0 else last / ath - 1.0
    return {
        "slice": "13_ath_drawdown",
        "pack": "#2",
        "ath": ath,
        "ath_date": ath_bar.get("date", ""),
        "last": last,
        "drawdown": round(drawdown, 4),
        "drawdown_pct": round(drawdown * 100, 2),
        "state": "near_ath" if drawdown > -0.05 else "deep_drawdown" if drawdown < -0.40 else "off_ath",
    }
