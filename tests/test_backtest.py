from market_compass.backtest import backtest_frame


def test_backtest_returns_metrics(sample_data):
    r = backtest_frame(sample_data.bars, horizon=20)
    assert r["trades"] >= 0
    assert "win_rate" in r
