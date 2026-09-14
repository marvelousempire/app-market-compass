"""Pack #2 slice 12 — Market tape. Last N bars as glanceable rows."""
from __future__ import annotations

def run(bars, limit=12):
    rows = []
    window = bars[-limit:]
    for i, bar in enumerate(window):
        prev_close = window[i - 1]["close"] if i else bar["open"]
        change = bar["close"] - prev_close
        pct = 0.0 if prev_close == 0 else change / prev_close
        rows.append({
            "date": bar.get("date", ""),
            "open": bar["open"],
            "high": bar["high"],
            "low": bar["low"],
            "close": bar["close"],
            "volume": bar.get("volume", 0),
            "change": round(change, 6),
            "change_pct": round(pct, 4),
            "direction": "up" if change > 0 else "down" if change < 0 else "flat",
        })
    up = sum(1 for r in rows if r["direction"] == "up")
    down = sum(1 for r in rows if r["direction"] == "down")
    return {
        "slice": "12_market_tape",
        "pack": "#2",
        "rows": rows,
        "up_bars": up,
        "down_bars": down,
        "bias": "bid" if up > down else "offer" if down > up else "balanced",
    }
