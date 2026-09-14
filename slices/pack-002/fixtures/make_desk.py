"""Build the offline Pack #2 fixture. Deterministic. No network."""
from __future__ import annotations
import json, math
from pathlib import Path

def series(start, n, drift, vol, seed_offset=0):
    bars = []
    price = start
    for i in range(n):
        wave = math.sin((i + seed_offset) / 11.0) * vol
        price = max(0.01, price * (1.0 + drift) + wave)
        bars.append({
            "date": f"2026-{(i//28)%12+1:02d}-{(i%28)+1:02d}",
            "open": round(price - wave * 0.3, 6),
            "high": round(price * 1.012, 6),
            "low": round(price * 0.988, 6),
            "close": round(price, 6),
            "volume": 1_000_000 + abs(int(wave * 8_000_000)),
        })
    return bars

def build():
    return {
        "asset": "XRP-USD",
        "bars": series(0.52, 220, 0.0012, 0.008, 0),
        "btc": series(28000, 220, 0.0006, 400, 3),
        "eth": series(1800, 220, 0.0007, 30, 5),
        "meta": {"circulating_supply": 56_000_000_000, "max_supply": 100_000_000_000},
    }

if __name__ == "__main__":
    out = Path(__file__).with_name("desk.json")
    out.write_text(json.dumps(build(), indent=2) + "\n")
    print("wrote", out)
