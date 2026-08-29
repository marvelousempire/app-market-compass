from market_compass.data import _choose_quote
from market_compass.engine import analyze_frame
from market_compass.registry import NODE_REGISTRY, node_output
from market_compass.technical import enrich, rsi


def test_registry_has_all_115_nodes():
    assert len(NODE_REGISTRY) == 115


def test_rsi_bounds(sample_data):
    values = rsi(sample_data.bars.close)
    assert values.between(0, 100).all()


def test_complete_report_and_contrast(sample_data):
    r = analyze_frame("TEST", sample_data, horizon=20)
    assert r.bull_evidence + r.bear_evidence == 100
    assert 0 <= r.confidence <= 1
    assert {"foundation", "trend", "momentum", "route", "news", "history", "memory", "relationships", "narrative"} <= set(r.layers)
    assert r.summary
    assert node_output(r, "L2-001")["key"] == "momentum"


def test_default_emas_exist(sample_data):
    x = enrich(sample_data.bars)
    for c in ["ema13", "ema27", "ema81", "rsi14", "macd", "hist"]:
        assert c in x


def test_symbol_resolver_prefers_related_symbol():
    quotes = [{"symbol": "HYPE32196-USD"}, {"symbol": "OTHER"}]
    assert _choose_quote("HYPE-USD", quotes)["symbol"] == "HYPE32196-USD"
