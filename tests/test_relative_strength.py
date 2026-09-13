from market_compass.engine import analyze_frame
from market_compass.relative_strength import build_relative_strength, rsi_zone


def test_rsi_zone_labels():
    assert rsi_zone(22) == "oversold"
    assert rsi_zone(31) == "support_zone"
    assert rsi_zone(50) == "neutral"
    assert rsi_zone(66) == "resistance_zone"
    assert rsi_zone(81) == "overbought"
    assert rsi_zone(None) is None


def test_relative_strength_desk_from_sample(sample_data):
    weekly = sample_data.bars.resample("W-FRI").agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
    }).dropna(subset=["close"])
    pack = build_relative_strength(sample_data.bars, {"1d": sample_data.bars, "1w": weekly}, {})
    assert pack["rsi"]["readings"]["1d"]["available"]
    assert pack["rsi"]["readings"]["1d"]["zone"] in {
        "oversold", "support_zone", "neutral", "resistance_zone", "overbought",
    }
    assert pack["returns"]["7d"] is not None
    assert pack["ema_stack"][0]["period"] == 13
    assert pack["drawdown"]["ath"]["price"]
    assert "BTC benchmark series" in pack["missing"]
    assert "evidence split" in pack["note"]


def test_analyze_frame_exposes_desk_without_live_tape(sample_data):
    report = analyze_frame("TEST", sample_data, horizon=20)
    assert report.relative_strength["rsi"]["readings"]["1d"]["available"]
    assert report.market_tape["missing"]
    assert report.bull_evidence + report.bear_evidence == 100
