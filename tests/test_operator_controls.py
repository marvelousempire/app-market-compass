from fastapi.testclient import TestClient

from market_compass.api import app


def test_operator_control_surface_and_assets_exist():
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    for action in ("plan", "status", "launch", "open", "receipts", "stop"):
        assert f'data-operator-action="{action}"' in page.text
    assert "/static/operator-controls.js" in page.text
    assert "/static/operator-controls.css" in page.text
    assert client.get("/static/operator-controls.js").status_code == 200
    assert client.get("/static/operator-controls.css").status_code == 200


def test_default_assets_and_flowthat_cassettes_are_visible():
    client = TestClient(app)
    page = client.get("/")
    assert 'id="symbol" value="BB"' in page.text
    for cassette in ("omo", "prince", "wuda", "browns-barometers"):
        assert f'data-cassette="{cassette}"' in page.text
    assert 'data-cassette="marvins-metrics"' not in page.text
    assert "/static/research-cassettes.js" in page.text
    assert "/static/research-cassettes.css" in page.text

    app_script = client.get("/static/app.js").text
    for symbol in ("BB", "AAPL", "QQQ", "SPCX"):
        assert f"'{symbol}'" in app_script
    assert "['HYPE','BTC','NVDA']" in app_script  # one-time migration of the old untouched default

    cassette_script = client.get("/static/research-cassettes.js").text
    assert "No bound market data" in cassette_script
    assert "broker action" in cassette_script
    for label in ("Brown’s Barometers", "Breadth", "Momentum", "Volatility", "Volume", "RSI crosses above 65", "RSI crosses above 50", "RSI crosses below 35", "Trading psychology", "actor-comp-card", "Preferences and rules not configured"):
        assert label in cassette_script
    assert "Marvin’s Metrics" not in cassette_script
    assert "Trading psychology', items" not in cassette_script


def test_operator_plan_status_launch_and_receipts_are_safe(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_INTELTHAT_DIR", raising=False)
    monkeypatch.delenv("MARKET_COMPASS_AUTHORITY", raising=False)
    monkeypatch.delenv("MARKET_COMPASS_COMMISSIONED", raising=False)
    monkeypatch.delenv("MARKET_COMPASS_SOURCE_REVISION", raising=False)
    client = TestClient(app)

    plan = client.get("/api/operator/plan")
    assert plan.status_code == 200
    assert "broker-order" in plan.json()["prohibits"]
    assert "gitea-authority-cutover" in plan.json()["prohibits"]

    status = client.get("/api/operator/status")
    assert status.status_code == 200
    assert status.json()["mode"] == "research_only"
    assert status.json()["trade_execution"] is False
    assert status.json()["commissioned"] is False

    launch = client.post("/api/operator/launch")
    assert launch.status_code == 200
    assert launch.json()["result"] == "already-running"
    assert launch.json()["trade_execution"] is False

    receipts = client.get("/api/operator/receipts?symbol=QQQ")
    assert receipts.status_code == 200
    assert receipts.json()["research"]["proof_health"]["missing"] == 4
    assert receipts.json()["research"]["trade_execution"] is False


def test_operator_status_can_report_canonical_source_without_enabling_trading(monkeypatch):
    monkeypatch.setenv("MARKET_COMPASS_AUTHORITY", "gitea:averygoodman/app-market-compass")
    monkeypatch.setenv("MARKET_COMPASS_COMMISSIONED", "true")
    monkeypatch.setenv("MARKET_COMPASS_SOURCE_REVISION", "394ecdd")
    status = TestClient(app).get("/api/operator/status").json()
    assert status["authority"] == "gitea:averygoodman/app-market-compass"
    assert status["commissioned"] is True
    assert status["preview_only"] is False
    assert status["source_revision"] == "394ecdd"
    assert status["trade_execution"] is False


def test_stop_route_is_post_only_and_source_keeps_relaunch_truth():
    client = TestClient(app)
    assert client.get("/api/operator/stop").status_code == 405
    script = client.get("/static/operator-controls.js").text
    assert "GitThat can relaunch it later" in script
    assert "window.confirm" in script
