from market_compass import asset_channel


def test_channel_only_accepts_exact_ticker_and_safe_source_links(monkeypatch):
    rows = [
        {"title": "BlackBerry report", "publisher": "Example", "url": "https://example.com/bb", "related_symbols": ["BB"], "media_type": "STORY", "published": "2026-11-26T12:00:00Z"},
        {"title": "Another company", "publisher": "Example", "url": "https://example.com/other", "related_symbols": ["AAPL"], "media_type": "STORY"},
        {"title": "Unsafe link", "publisher": "Example", "url": "javascript:alert(1)", "related_symbols": ["BB"], "media_type": "VIDEO"},
        {"title": "BlackBerry clip", "publisher": "Example", "url": "https://example.com/video", "related_symbols": ["BB"], "media_type": "VIDEO"},
    ]
    monkeypatch.setattr(asset_channel, "_search_symbol", lambda value, news_count: ({"symbol": "BB", "longname": "BlackBerry Limited"}, rows, []))
    monkeypatch.setattr(asset_channel, "edgar_filings", lambda value: {"state": "held", "reason": "Unavailable"})
    result = asset_channel.read_asset_channel("bb")
    assert [item["title"] for item in result["items"]] == ["BlackBerry report", "BlackBerry clip"]
    assert [item["kind"] for item in result["items"]] == ["article", "video"]
    assert result["audio_available"] is False
    assert result["trade_execution"] is False


def test_channel_keeps_empty_source_explicit(monkeypatch):
    monkeypatch.setattr(asset_channel, "_search_symbol", lambda value, news_count: ({"symbol": "BB"}, [], []))
    monkeypatch.setattr(asset_channel, "edgar_filings", lambda value: {"state": "held", "reason": "Unavailable"})
    assert asset_channel.read_asset_channel("BB")["items"] == []
