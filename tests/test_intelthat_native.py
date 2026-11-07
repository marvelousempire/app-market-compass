from __future__ import annotations

from datetime import UTC

import numpy as np
import pandas as pd

from market_compass.data import MarketData
from market_compass.intelthat_contract import CONTRACT, SOURCE_REVISION, evidence, workspace
from market_compass.intelthat_native import build_native_workspace


def market_data(symbol: str) -> MarketData:
    index = pd.date_range("2026-04-01", periods=180, freq="B", tz=UTC)
    base = np.linspace(100, 130, len(index)) + np.sin(np.arange(len(index)) / 5)
    frame = pd.DataFrame({
        "open": base - .2,
        "high": base + 1,
        "low": base - 1,
        "close": base,
        "volume": np.linspace(1_000_000, 1_400_000, len(index)),
    }, index=index)
    news = [
        {"title": "Apple growth outlook beats estimates", "publisher": "Wire A",
         "published": "2026-11-05T15:00:00+00:00", "url": "https://example.test/a"},
        {"title": "Fed rate hike risk before earnings", "publisher": "Wire B",
         "published": "2026-11-05T14:00:00+00:00", "url": "https://example.test/b"},
    ]
    return MarketData(frame, {"symbol": symbol}, news,
                      {"provider": "fixture", "interval": "1d", "resolved_symbol": symbol})


def option_data(_url, **_kwargs):
    return {"optionChain": {"result": [{"options": [{
        "calls": [{"openInterest": 100, "volume": 20}, {"openInterest": 50, "volume": 10}],
        "puts": [{"openInterest": 120, "volume": 30}],
    }]}]}}


def test_contract_receipt_has_inputs_formula_provenance_and_boundaries():
    item = evidence("pack", state="observed", reason="test", as_of="2026-11-06T00:00:00+00:00",
                    timeframe="1d", inputs={"close": 100}, formula="close",
                    metrics={"close": 100}, confidence=.8,
                    source_urls=["https://example.test"], retrieved_at="2026-11-06T00:00:00+00:00",
                    freshness="current")
    result = workspace("AAPL", {kind: {**item, "kind": kind} for kind in ("pack", "macro", "rss", "edgar")},
                       as_of="2026-11-06T00:00:00+00:00")
    assert result["contract"] == CONTRACT
    assert result["trade_execution"] is False
    assert result["broker_credentials"] is False
    assert result["money_movement"] is False
    assert result["score_influence"] is False
    assert len(result["receipt_sha256"]) == 64
    assert item["formula"] and item["inputs"]
    assert item["provenance"]["outside_source_revision"] == SOURCE_REVISION


def test_native_workspace_builds_all_safe_research_kinds_and_holds_edgar(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_SEC_CONTACT", raising=False)
    result = build_native_workspace("AAPL", market_fetcher=market_data, options_getter=option_data)
    assert list(result["sources"]) == ["pack", "macro", "rss", "edgar"]
    assert result["sources"]["pack"]["state"] == "observed"
    assert result["sources"]["macro"]["state"] == "observed"
    assert result["sources"]["rss"]["state"] == "observed"
    assert result["sources"]["edgar"]["state"] == "held"
    assert "SEC fair-access contact" in result["sources"]["edgar"]["reason"]
    assert result["sources"]["rss"]["metrics"]["headlineCount"] == 2
    assert result["sources"]["pack"]["metrics"]["putCallOIRatio"] == .8
    assert "E*TRADE OAuth and credentials" in result["source_refinery"]["rejected"]


def test_native_workspace_reads_edgar_only_with_contact(monkeypatch):
    monkeypatch.setenv("MARKET_COMPASS_SEC_CONTACT", "research@example.test")

    def getter(url, **_kwargs):
        if "company_tickers" in url:
            return {"0": {"ticker": "AAPL", "cik_str": 320193}}
        return {"filings": {"recent": {"form": ["8-K", "10-Q", "S-8"],
                                          "filingDate": ["2026-11-05", "2026-10-31", "2026-10-01"]}}}

    result = build_native_workspace("AAPL", market_fetcher=market_data, edgar_getter=getter,
                                    options_getter=option_data)
    item = result["sources"]["edgar"]
    assert item["state"] == "observed"
    assert item["metrics"]["filingCount"] == 2
    assert item["inputs"]["cik"] == "0000320193"
    assert "research@example.test" not in str(result)


def test_native_workspace_returns_exportable_held_receipt_when_market_source_fails(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_SEC_CONTACT", raising=False)

    def unavailable(_symbol):
        raise TimeoutError("source timeout")

    result = build_native_workspace("QQQ", market_fetcher=unavailable, options_getter=option_data)
    assert result["sources"]["pack"]["state"] == "held"
    assert result["sources"]["rss"]["state"] == "held"
    assert result["sources"]["macro"]["state"] == "held"
    assert result["sources"]["edgar"]["state"] == "held"
    assert len(result["receipt_sha256"]) == 64
