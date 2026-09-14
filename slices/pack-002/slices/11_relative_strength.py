"""Pack #2 slice 11 — Relative performance vs BTC and ETH benches."""
from __future__ import annotations

def _ret(series, bars):
    if len(series) <= bars or series[-1 - bars] == 0:
        return None
    return series[-1] / series[-1 - bars] - 1.0

def _rel(asset, bench, bars):
    a = _ret(asset, bars)
    b = _ret(bench, bars)
    if a is None or b is None:
        return None
    return a - b

def run(asset_closes, btc_closes, eth_closes):
    windows = (7, 30, 90)
    vs_btc = {str(w): _rel(asset_closes, btc_closes, w) for w in windows}
    vs_eth = {str(w): _rel(asset_closes, eth_closes, w) for w in windows}
    latest_btc = vs_btc.get("30")
    latest_eth = vs_eth.get("30")
    if latest_btc is None:
        stance = "unknown"
    elif latest_btc > 0.02:
        stance = "leading_btc"
    elif latest_btc < -0.02:
        stance = "lagging_btc"
    else:
        stance = "in_line_with_btc"
    def _r(v):
        return None if v is None else round(v, 4)
    return {
        "slice": "11_relative_strength",
        "pack": "#2",
        "vs_btc": {k: _r(v) for k, v in vs_btc.items()},
        "vs_eth": {k: _r(v) for k, v in vs_eth.items()},
        "stance": stance,
        "eth_stance": (
            "leading_eth" if latest_eth is not None and latest_eth > 0.02
            else "lagging_eth" if latest_eth is not None and latest_eth < -0.02
            else "in_line_with_eth" if latest_eth is not None else "unknown"
        ),
    }
