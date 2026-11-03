from fastapi.testclient import TestClient

from market_compass.api import app


def test_participants_have_exact_founder_names_and_bounded_status():
    payload = TestClient(app).get("/api/participants")
    assert payload.status_code == 200
    body = payload.json()
    assert body["schema"] == "market-compass.participants/v1"
    assert body["commissioned"] is False
    assert body["trade_execution"] is False
    assert body["score_influence"] is False
    participants = body["participants"]
    assert [entry["name"] for entry in participants] == [
        "Omo's Intel", "Prince's Principles", "Prince's Intel", "Marvin's Metrics"
    ]
    assert participants[0]["source_app"] == "intelTHAT"
    assert "intelTHAT" in participants[0]["aliases"]
    assert "Omo Intel" in participants[0]["aliases"]
    assert participants[0]["evidence_endpoint"] == "/api/intelthat/{symbol}"
    assert all(entry["status"] == "awaiting-owner-content" for entry in participants[1:])
    assert all(entry["evidence_endpoint"] is None for entry in participants[1:])


def test_participants_are_visible_without_market_analysis():
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="market-participants"' in page.text
    assert 'id="market-participants-output"' in page.text
    assert "Omo's Intel Research / Proof Health" in page.text
    assert 'id="intelthat-load"' in page.text
    js = client.get("/static/intelthat.js")
    assert js.status_code == 200
    assert "/api/participants" in js.text
    assert "textContent" in js.text
    assert 'id="intelthat-panel"' in page.text
