"""Pack #2 slice 15 — Volume and supply glance.
Circulating / max supply come from the fixture metadata, not a live chain call.
"""
from __future__ import annotations

def run(bars, meta=None):
    meta = meta or {}
    vols = [b.get("volume", 0) for b in bars[-30:]]
    avg = (sum(vols) / len(vols)) if vols else 0.0
    last_vol = bars[-1].get("volume", 0) if bars else 0
    circ = meta.get("circulating_supply")
    mx = meta.get("max_supply")
    issued_pct = None
    if circ and mx:
        issued_pct = round(circ / mx, 4)
    return {
        "slice": "15_supply_metrics",
        "pack": "#2",
        "last_volume": last_vol,
        "avg_volume_30": round(avg, 2),
        "volume_vs_avg": None if avg == 0 else round(last_vol / avg, 3),
        "circulating_supply": circ,
        "max_supply": mx,
        "issued_pct": issued_pct,
        "source": "fixture_meta",
    }
