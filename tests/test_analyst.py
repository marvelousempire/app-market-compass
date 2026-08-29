from fastapi.testclient import TestClient

from market_compass.ai import AnalystRequest, AnalystRouter
from market_compass.ai.providers import ProviderError
from market_compass.api import app
from market_compass.data import search_symbols


def _report():
    return {
        "symbol": "HYPE",
        "action": "watch",
        "bull_evidence": 58,
        "bear_evidence": 42,
        "confidence": 0.66,
        "summary": "Trend and momentum lean positive, but resistance remains.",
        "route": {"invalidation": 31.5},
        "layers": {
            "trend": {
                "evidence": [{"text": "EMA structure is rising.", "strength": 0.8}],
                "counter_evidence": [],
                "missing": [],
            },
            "memory": {
                "evidence": [],
                "counter_evidence": [{"text": "Resistance has rejected price twice.", "strength": 0.7}],
                "missing": ["longer intraday history"],
            },
        },
    }


def test_offline_analyst_is_grounded_and_receipted():
    router = AnalystRouter()
    response = router.analyze(AnalystRequest(report=_report()))
    assert "58/42" in response.summary
    assert response.bull_case == ["EMA structure is rising."]
    assert response.bear_case == ["Resistance has rejected price twice."]
    assert response.citations
    assert len(response.receipt.report_hash) == 64
    assert response.receipt.provider == "grounded-offline"


def test_cloud_provider_requires_explicit_consent():
    router = AnalystRouter()
    request = AnalystRequest(report=_report(), provider="openai-pro", cloud_allowed=False)
    try:
        router.select(request)
    except ProviderError as exc:
        assert "cloud approval" in str(exc)
    else:
        raise AssertionError("Cloud provider was selected without consent/configuration")


def test_analyst_api_contract_and_provider_inventory():
    client = TestClient(app)
    providers = client.get("/api/analyst/providers")
    assert providers.status_code == 200
    assert any(x["id"] == "grounded-offline" for x in providers.json())

    response = client.post("/api/analyst", json={"report": _report()})
    assert response.status_code == 200
    assert response.json()["receipt"]["provider"] == "grounded-offline"


def test_v04_ui_contains_nephew_and_friendly_symbol():
    page = TestClient(app).get("/")
    assert page.status_code == 200
    assert "NEPHEW ANALYST" in page.text
    assert 'value="HYPE"' in page.text
    assert "symbol-suggestions" in page.text


def test_friendly_symbol_search_hides_provider_suffix(monkeypatch):
    monkeypatch.setattr(
        "market_compass.data._get_json",
        lambda _url: {
            "quotes": [{
                "symbol": "HYPE-USD", "shortname": "Hyperliquid",
                "quoteType": "CRYPTOCURRENCY", "exchange": "CCC",
            }],
        },
    )
    result = search_symbols("hype")
    assert result[0]["display_symbol"] == "HYPE"
    assert result[0]["symbol"] == "HYPE-USD"
