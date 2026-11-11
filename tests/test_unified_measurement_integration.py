"""No-subtraction proof: current v0.7 market and ACT experience stays present."""
from fastapi.testclient import TestClient

from market_compass.api import app

client = TestClient(app)

def test_current_commissioned_market_surfaces_are_preserved():
    page = client.get("/")
    assert page.status_code == 200
    html = page.text
    for marker in (
        'id="actor-spaces"', 'id="market-exchange"', 'id="market-workspace"',
        'id="intelthat-panel"', 'id="decision-gates"', 'id="operator-deck"',
        'id="analyze"', 'id="symbol"', 'id="watchlist"', 'id="price-chart"',
        'id="rsi-chart"', 'id="macd-chart"', 'id="forecast-panel"',
        'id="evidence-board"', 'id="cassette-canvas"', 'data-cassette="omo"',
        'data-cassette="prince"', 'data-cassette="wuda"',
        'data-cassette="browns-barometers"', 'data-act-shell-room="desk"',
        'data-act-shell-room="exchange"',
    ):
        assert marker in html, f"Original feature missing: {marker}"
    for path in (
        "/api/operator/status", "/api/operator/plan", "/api/analyst/health",
        "/api/nodes", "/health",
    ):
        assert client.get(path).status_code == 200, path
    status = client.get("/api/operator/status").json()
    assert status["mode"] == "research_only"
    assert status["trade_execution"] is False


def test_universal_measurement_is_a_new_navigable_room_not_a_second_app():
    html = client.get("/").text
    for marker in (
        'id="measurement-studio"', 'data-act-shell-room="measurement"',
        'id="hcck-profile-select"', 'id="hcck-seat-select"',
        'id="universal-simulator"', 'id="universal-run"',
        'id="universal-export"', '/static/hcck.js',
        '/static/simulator.js', '/static/simulator.css',
    ):
        assert marker in html
    shell = client.get("/static/act-v1-shell.js").text
    assert "measurement: [[" in shell
    assert "exchange: [[" in shell
    assert "actors: [[" in shell
    main = client.get("/static/app.js").text
    assert "runAnalysis();" in main
    assert "/api/analyze?symbol=" in main
    assert "renderWatchlist();" in main


def test_universal_contracts_do_not_claim_external_owner_authority():
    profiles = client.get("/api/hcck/profiles")
    assert profiles.status_code == 200
    d = profiles.json()
    assert len(d["profiles"]) == 7
    assert len(d["participant_instances"]) == 4
    assert d["authority"]["canonical_registration"] == "not-registered"
    assert d["authority"]["cck_witness_verified"] is False
    assert d["schedules_running"] is False
    seat = {x["name"]: x for x in d["participant_instances"]}
    assert seat["Omo's Intel"]["research_actor"] == "omo"
    assert seat["Prince's Principles"]["research_actor"] == "prince"
    assert seat["Wuda's Watch"]["research_actor"] == "wuda"
    assert seat["Brown's Barometers"]["research_actor"] == "browns-barometers"
    assert "Marvin's Metrics" not in seat
