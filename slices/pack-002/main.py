"""Pack #2 — Relative Strength Desk + Market Tape.
Cold slices. Fixture or caller-supplied bars. Scoring model stays untouched.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from importlib.machinery import SourceFileLoader

def load(name):
    return SourceFileLoader(name, str(Path(__file__).resolve().parent / "slices" / f"{name}.py")).load_module()

def run(payload):
    asset = payload.get("asset", "ASSET")
    bars = payload["bars"]
    btc = payload["btc"]
    eth = payload["eth"]
    meta = payload.get("meta", {})
    closes = [b["close"] for b in bars]
    rsi = load("10_rsi_zones").run(closes)
    relative = load("11_relative_strength").run(closes, [b["close"] for b in btc], [b["close"] for b in eth])
    tape = load("12_market_tape").run(bars)
    ath = load("13_ath_drawdown").run(bars)
    stack = load("14_sma_stack").run(closes)
    supply = load("15_supply_metrics").run(bars, meta)
    wrapped = load("16_desk_receipt").run(asset, rsi, relative, tape, ath, stack, supply)
    return {
        "pack": "#2",
        "label": "RELATIVE STRENGTH DESK + MARKET TAPE",
        "asset": asset,
        "desk": wrapped["desk"],
        "receipt": wrapped["receipt"],
    }

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fixtures.make_desk import build
    print(json.dumps(run(build()), indent=2))
