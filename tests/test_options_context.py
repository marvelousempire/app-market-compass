from market_compass import research_sources
from market_compass.api import options_context_api


def test_alpaca_unconfigured_is_held(monkeypatch):
    monkeypatch.setattr(research_sources, "data_token", lambda: "")
    monkeypatch.delenv('MARKET_COMPASS_ALPACA_KEY_ID', raising=False)
    monkeypatch.delenv('MARKET_COMPASS_ALPACA_SECRET_KEY', raising=False)
    result = research_sources.alpaca_quote('AAPL')
    assert result['state'] == 'held'
    assert result['symbol'] == 'AAPL'


def test_context_preserves_independent_source_states(monkeypatch):
    monkeypatch.setattr('market_compass.api.alpaca_quote', lambda symbol: {'state': 'held', 'symbol': symbol})
    monkeypatch.setattr('market_compass.api.edgar_filings', lambda symbol: {'state': 'observed', 'symbol': symbol})
    result = options_context_api('AAPL')
    assert result['alpaca']['state'] == 'held'
    assert result['edgar']['state'] == 'observed'


def test_options_bookmark_returns_to_main_room():
    from market_compass.api import options_desk
    assert options_desk() == '/#options-lab'


def test_main_room_embeds_options_without_old_link():
    from market_compass.api import WEB_DIR
    page = (WEB_DIR / 'index.html').read_text()
    assert 'id="options-lab"' in page
    assert 'id="options-lab-frame"' in page
    assert 'href="/options"' not in page
