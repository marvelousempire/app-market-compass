"""Pack #2 adapter. Glance desk. Does not touch scoring weights."""
from __future__ import annotations

from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any

import pandas as pd

PACK_ROOT = Path(__file__).resolve().parents[2] / "slices" / "pack-002"


def _bars(df: pd.DataFrame) -> list[dict]:
    out = []
    for ts, row in df.iterrows():
        out.append({
            "date": ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": float(row.get("volume", 0) or 0),
        })
    return out


def _load_pack():
    return SourceFileLoader("pack002_main", str(PACK_ROOT / "main.py")).load_module()


def desk_from_bars(symbol: str, bars: pd.DataFrame, btc: pd.DataFrame | None = None, eth: pd.DataFrame | None = None, meta: dict | None = None) -> dict[str, Any]:
    payload = {
        "asset": symbol.upper(),
        "bars": _bars(bars),
        "btc": _bars(btc if btc is not None and len(btc) else bars),
        "eth": _bars(eth if eth is not None and len(eth) else bars),
        "meta": meta or {},
    }
    return _load_pack().run(payload)


def attach(report_meta: dict, symbol: str, bars: pd.DataFrame) -> dict:
    """Hang Pack #2 on data_meta. Scoring already finished."""
    try:
        desk = desk_from_bars(symbol, bars)
    except Exception as exc:
        return report_meta | {"pack_002": {"available": False, "reason": str(exc)}}
    return report_meta | {
        "pack_002": {
            "available": True,
            "scoring_untouched": True,
            "evidence_sequence": "8001-preserved",
            "desk": desk.get("desk"),
            "receipt": desk.get("receipt"),
        }
    }
