from fastapi.testclient import TestClient

from market_compass.api import app


def test_intelthat_source_panel_and_assets_exist(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_INTELTHAT_DIR", raising=False)
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="intelthat-panel"' in page.text
    assert 'id="intelthat-load"' in page.text
    assert '/static/intelthat.js' in page.text
    assert '/static/intelthat.css' in page.text
    script = client.get("/static/intelthat.js")
    assert script.status_code == 200
    assert "/api/intelthat/" in script.text
    assert "textContent" in script.text
    assert client.get("/static/intelthat.css").status_code == 200
    payload = client.get("/api/intelthat/QQQ")
    assert payload.status_code == 200
    assert payload.json()["proof_health"]["missing"] == 4
    assert payload.json()["trade_execution"] is False
    assert payload.json()["score_influence"] is False


def test_intelthat_api_refuses_bad_symbol():
    client = TestClient(app)
    response = client.get("/api/intelthat/QQQ%3F")
    assert response.status_code == 400
