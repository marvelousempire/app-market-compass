from fastapi.testclient import TestClient

from market_compass.api import app


def test_intelthat_source_panel_and_assets_exist(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_INTELTHAT_DIR", raising=False)
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="intelthat-panel"' in page.text
    assert 'id="intelthat-load"' in page.text
    assert 'id="intelthat-local"' in page.text
    assert 'id="intelthat-filter"' in page.text
    assert 'id="intelthat-export"' in page.text
    assert '/static/intelthat.js' in page.text
    assert '/static/intelthat.css' in page.text
    script = client.get("/static/intelthat.js")
    assert script.status_code == 200
    assert "/api/intelthat/" in script.text
    assert "/api/intelthat-workspace/" in script.text
    assert "Export Receipt" not in script.text
    assert "textContent" in script.text
    assert client.get("/static/intelthat.css").status_code == 200
    payload = client.get("/api/intelthat/QQQ")
    assert payload.status_code == 200
    assert payload.json()["proof_health"]["missing"] == 4
    assert payload.json()["trade_execution"] is False
    assert payload.json()["score_influence"] is False


def test_intelthat_is_a_real_application_surface():
    client = TestClient(app)
    page = client.get("/intelthat/")
    assert page.status_code == 200
    for text in (
        "Research Application", "Research Cockpit", "Market Pack", "Macro Conditions",
        "News Intelligence", "SEC Monitor", "Run History", "Run all research",
        "Read owner receipts", "Save run", "Export receipt",
    ):
        assert text in page.text
    for boundary in (
        "signal_generation=true", "trade_execution=false", "broker_credentials=false",
        "money_movement=false", "score_influence=false",
    ):
        assert boundary in page.text
    assert '/static/intelthat-app.js' in page.text
    assert '/static/intelthat-app.css' in page.text

    script = client.get("/static/intelthat-app.js")
    assert script.status_code == 200
    assert "/api/intelthat-workspace/" in script.text
    assert "/api/intelthat/" in script.text
    assert "/api/symbols" in script.text
    assert "localStorage" in script.text
    assert "broker OAuth" not in script.text
    assert client.get("/static/intelthat-app.css").status_code == 200


def test_market_compass_presents_intelthat_as_app_and_bridge():
    client = TestClient(app)
    page = client.get("/")
    assert 'href="/intelthat/"' in page.text
    assert "intelTHAT App" in page.text
    assert "INTELTHAT APP BRIDGE" in page.text


def test_intelthat_api_refuses_bad_symbol():
    client = TestClient(app)
    response = client.get("/api/intelthat/QQQ%3F")
    assert response.status_code == 400
