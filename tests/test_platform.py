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

    class Connection:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

    monkeypatch.setattr(launcher.socket, "create_connection", lambda *_args, **_kwargs: Connection())
    monkeypatch.setattr(launcher.webbrowser, "open", lambda url: opened.append(url))

    launcher._open_when_ready()

    assert opened == [launcher.URL]


def test_rich_application_surface_is_served():
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert "Bus Stop Route" in page.text
    assert "Evidence Board" in page.text
    assert "115 Nodes" in page.text
    assert "/static/app.js" in page.text

    script = client.get("/static/app.js")
    assert script.status_code == 200
    assert "renderEvidenceBoard" in script.text
    assert "runBacktest" in script.text


def test_health_identifies_application_surface():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["nodes"] == 115
    assert payload["surface"] == "application-v0.2"
