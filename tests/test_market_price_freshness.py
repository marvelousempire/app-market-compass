from __future__ import annotations

import pandas as pd

from market_compass import data
from market_compass import research_sources
from market_compass.engine import analyze_frame


def test_alpaca_credentials_read_keychain_without_exposing_values(monkeypatch):
    monkeypatch.delenv('MARKET_COMPASS_ALPACA_KEY_ID', raising=False)
    monkeypatch.delenv('MARKET_COMPASS_ALPACA_SECRET_KEY', raising=False)
    monkeypatch.setattr(research_sources.os, 'uname', lambda: type('U', (), {'sysname': 'Darwin'})())
    calls = []
    def lookup(command, **kwargs):
        calls.append(command)
        return type('Result', (), {'stdout': 'private-value\n'})()
    monkeypatch.setattr(research_sources.subprocess, 'run', lookup)
    assert research_sources._alpaca_credentials() == ('private-value', 'private-value')
    assert [call[-2] for call in calls] == ['key-id', 'secret-key']


def test_report_study_close_keeps_source_bar_time(sample_data):
    report = analyze_frame("TEST", sample_data)
    assert report.data_meta["price_session_date"] == sample_data.bars.index[-1].date().isoformat()
    assert report.data_meta["price_kind"] == "daily_bar_close"


def test_latest_bar_never_claims_realtime(monkeypatch):
    at = pd.Timestamp("2026-11-25T21:00:00Z")
    bars = pd.DataFrame({"close": [8.50]}, index=[at])
    monkeypatch.setattr(data, "_chart_bars", lambda symbol, range_, interval: (bars, {"currency": "USD"}))
    observed = data.latest_available_bar("BB")
    assert observed["price"] == 8.50
    assert observed["as_of"] == at.isoformat()
    assert observed["real_time"] is False
    assert observed["kind"] == "minute bar close"


def test_latest_bar_refuses_invalid_symbol():
    try:
        data.latest_available_bar("BB/../../other")
    except ValueError:
        pass
    else:
        raise AssertionError("Unexpected symbol was accepted")


def test_alpaca_trade_requires_data_credentials(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_ALPACA_KEY_ID", raising=False)
    monkeypatch.delenv("MARKET_COMPASS_ALPACA_SECRET_KEY", raising=False)
    result = research_sources.alpaca_latest_trade("BB")
    assert result["state"] == "held"
    assert "credentials" in result["reason"]
