import ssl

from fastapi.testclient import TestClient

from market_compass import launcher
from market_compass.api import app
from market_compass.data import SSL_CONTEXT


def test_ssl_context_verifies_certificates():
    assert SSL_CONTEXT.check_hostname is True
    assert SSL_CONTEXT.verify_mode == ssl.CERT_REQUIRED


def test_browser_opens_when_server_is_ready(monkeypatch):
    opened = []
    monkeypatch.setattr(launcher, "_is_market_compass", lambda _port: True)
    monkeypatch.setattr(launcher.webbrowser, "open", lambda url: opened.append(url))
    launcher._open_when_ready(8000)
    assert opened == ["http://127.0.0.1:8000"]


def test_select_port_reuses_running_market_compass(monkeypatch):
    monkeypatch.setattr(launcher, "_is_market_compass", lambda port: port == 8000)
    assert launcher.select_port() == (8000, True)


def test_launcher_rejects_stale_market_compass(monkeypatch):
    monkeypatch.setattr(
        launcher,
        "_health",
        lambda _port: {"status": "ok", "surface": "application-v0.3"},
    )
    assert launcher._is_market_compass(8000) is False


def test_select_port_skips_unrelated_process(monkeypatch):
    monkeypatch.setattr(launcher, "_is_market_compass", lambda _port: False)
    monkeypatch.setattr(launcher, "_port_is_free", lambda port: port == 8001)
    assert launcher.select_port() == (8001, False)


def test_v03_workbench_surface_is_served():
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    for text in [
        "INTELLIGENCE OVERVIEW", "TRADING WORKBENCH", "PRICE MEMORY", "RSI 14", "MACD",
        "Historical Analogs", "Evidence Contributions", "Catalyst Timeline", "Evidence Board",
        "NEPHEW ANALYST",
    ]:
        assert text in page.text
    assert "lightweight-charts" in page.text

    script = client.get("/static/app.js")
    assert script.status_code == 200
    for function in [
        "renderIntelligenceOverview", "ASSET REALITY", "MARKET STATE", "FIBONACCI", "REVERSAL",
        "renderCharts", "renderContributions", "renderCatalysts", "saveSnapshot",
    ]:
        assert function in script.text


def test_health_identifies_application_surface():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["nodes"] == 115
    assert payload["surface"] == "application-v0.4"
    assert payload["analyst"] == "ok"
