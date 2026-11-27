from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from market_compass import alpaca_connect
from market_compass.api import app


def test_authorization_requests_paper_data_only(monkeypatch):
    monkeypatch.setattr(alpaca_connect, "_read", lambda account: "client123" if account == "client-id" else "secret123")
    url = urlparse(alpaca_connect.authorization_url())
    params = parse_qs(url.query)
    assert url.scheme == "https" and url.hostname == "app.alpaca.markets"
    assert params["scope"] == ["data"]
    assert params["env"] == ["paper"]
    assert params["redirect_uri"] == [alpaca_connect.CALLBACK]
    assert "trading" not in url.query


def test_exchange_refuses_trading_scope(monkeypatch):
    monkeypatch.setattr(alpaca_connect, "_read", lambda account: "client123" if account == "client-id" else "secret123")
    saved = []
    monkeypatch.setattr(alpaca_connect, "_save", lambda account, value: saved.append(account))
    url = alpaca_connect.authorization_url()
    state = parse_qs(urlparse(url).query)["state"][0]

    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return None

    monkeypatch.setattr(alpaca_connect, "urlopen", lambda request, timeout: Response())
    monkeypatch.setattr(alpaca_connect.json, "load", lambda response: {
        "access_token": "token", "token_type": "bearer", "scope": "data trading"})
    with pytest.raises(ValueError, match="beyond market data"):
        alpaca_connect.exchange("code", state)
    assert saved == []


def test_connection_settings_refuse_cross_origin_write(monkeypatch):
    monkeypatch.setattr(alpaca_connect, "configure", lambda *args: pytest.fail("should not save"))
    response = TestClient(app).post("/api/alpaca-connect/configure", json={
        "client_id": "client123", "client_secret": "secret123"},
        headers={"Origin": "http://other.localhost", "Host": "market-compass.localhost"})
    assert response.status_code == 403


def test_configure_requires_keychain_readback(monkeypatch):
    stored = {}
    monkeypatch.setattr(alpaca_connect, "_read", lambda account: stored.get(account, ""))
    monkeypatch.setattr(alpaca_connect, "_save", lambda account, value: stored.__setitem__(account, value) if account == "client-id" else None)
    monkeypatch.setattr(alpaca_connect, "_delete", lambda account: stored.pop(account, None))
    with pytest.raises(RuntimeError, match="could not be confirmed"):
        alpaca_connect.configure("client123", "secret123")
    assert stored.get("client-id") == "client123"
    assert not alpaca_connect.status()["configured"]


def test_configure_reports_saved_only_after_readback(monkeypatch):
    stored = {}
    monkeypatch.setattr(alpaca_connect, "_read", lambda account: stored.get(account, ""))
    monkeypatch.setattr(alpaca_connect, "_save", lambda account, value: stored.__setitem__(account, value))
    monkeypatch.setattr(alpaca_connect, "_delete", lambda account: stored.pop(account, None))
    result = alpaca_connect.configure("client123", "secret123")
    assert result["configured"] is True
    assert "client_secret" not in result
