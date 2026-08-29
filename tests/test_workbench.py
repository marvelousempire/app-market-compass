import numpy as np
import pandas as pd

from market_compass.data import MarketData
from market_compass.engine import analyze_frame


def _bars(n=700, seed=4):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-01", periods=n, freq="D", tz="UTC")
    close = 80 * np.exp(np.cumsum(rng.normal(.0007, .018, n)))
    open_ = close * (1 + rng.normal(0, .003, n))
    high = np.maximum(open_, close) * (1 + rng.uniform(.001, .015, n))
    low = np.minimum(open_, close) * (1 - rng.uniform(.001, .015, n))
    volume = rng.integers(1_000_000, 7_000_000, n)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=idx)


def test_report_contains_workbench_payloads():
    bars = _bars()
    weekly = bars.resample("W-FRI").agg({"open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna()
    data = MarketData(bars, {"marketCap": 2e9, "quoteType": "EQUITY", "sectorDisp": "Technology", "exchange": "NMS"}, [], {"provider":"test"})
    report = analyze_frame("TEST", data, 20, timeframe_frames={"1d": bars, "1w": weekly})
    assert report.bull_evidence + report.bear_evidence == 100
    assert {"open","high","low","close","ema13","ema27","ema50","ema81","rsi14","macd","signal","hist"} <= set(report.chart)
    assert report.route.fibonacci_anchors["low_date"]
    assert isinstance(report.route.confluence, list)
    assert report.contributions
    assert "1d" in report.timeframes
    assert report.calibration["state"] in {"analog_context", "insufficient_history"}
