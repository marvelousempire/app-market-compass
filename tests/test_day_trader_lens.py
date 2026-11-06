import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

from market_compass.api import app
from market_compass.research_lenses.day_trader import SOURCE, build_day_trader_lens


def bars(values):
    close = np.asarray(values, dtype=float)
    index = pd.date_range("2026-01-01", periods=len(close), freq="D", tz="UTC")
    return pd.DataFrame({"open": close, "high": close * 1.01, "low": close * .99,
                         "close": close, "volume": 1_500_000}, index=index)


def test_lens_detects_breakout_and_preserves_authority_boundary():
    lens = build_day_trader_lens("test", bars([100 + i * .1 for i in range(30)] + [110]))
    assert lens["micro_slices"]["setup_scanner"][0]["state"] == "observed"
    assert lens["source"]["revision"] == SOURCE["revision"]
    assert lens["authority"] == {"research_only": True, "score_influence": False,
                                  "trade_execution": False, "money_movement": False}
    assert "trader-broker" in lens["rejected"]


def test_lens_holds_intraday_claim_without_intraday_bars():
    lens = build_day_trader_lens("test", bars(np.linspace(100, 105, 40)))
    assert lens["micro_slices"]["opening_range"]["state"] == "held"
    assert lens["micro_slices"]["historical_scenario"]["state"] == "reference"


def test_each_signal_carries_an_exportable_calculation_receipt():
    lens = build_day_trader_lens("test", bars(np.linspace(100, 110, 40)))
    events = lens["micro_slices"]["setup_scanner"] + lens["micro_slices"]["notable_thresholds"]
    assert lens["receipt"]["exportable"] is True
    assert len(lens["receipt"]["sha256"]) == 64
    for event in events:
        assert event["inputs"]
        assert event["formula"]
        assert event["timeframe"] == "1D"
        assert event["timestamp"]
        assert event["provenance"]["revision"] == SOURCE["revision"]
        assert event["confidence"]["meaning"].startswith("deterministic formula")


def test_lens_refuses_short_history():
    try:
        build_day_trader_lens("test", bars(np.linspace(100, 105, 20)))
    except ValueError as error:
        assert "30 completed bars" in str(error)
    else:
        raise AssertionError("short history should be refused")


def test_read_only_api_contract(monkeypatch):
    frame = bars(np.linspace(100, 110, 40))
    market = type("Market", (), {"bars": frame, "meta": {"provider": "test"}})()
    monkeypatch.setattr("market_compass.api.get_market_data", lambda symbol: market)
    response = TestClient(app).get("/api/research-lenses/day-trader/QQQ")
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "QQQ"
    assert payload["authority"]["trade_execution"] is False
