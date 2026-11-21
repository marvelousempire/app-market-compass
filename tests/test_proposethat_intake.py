"""Offline safety/receiving tests for proposeTHAT's Market Compass API."""
from fastapi.testclient import TestClient
from market_compass.api import app

def _sample(mode="owner-improvement"):
    return {
        "mode": mode,
        "subject": "Market Compass" if mode == "owner-improvement" else "Outside Bot",
        "goal": "Research one measurable and reversible improvement",
        "source_url": None if mode == "owner-improvement" else "https://example.org/trading",
        "source_revision": None,
    }

def test_ui_is_separate_from_existing_market_app():
    client = TestClient(app)
    page = client.get("/proposethat/")
    assert page.status_code == 200
    assert "Research &amp; Improvements" in page.text
    assert "No trading" in page.text
    assert "/proposethat/" in client.get("/").text
    script = client.get("/static/proposethat.js")
    assert script.status_code == 200
    assert "textContent" in script.text
    assert "innerHTML" not in script.text
    assert client.get("/static/proposethat.css").status_code == 200


def test_private_intake_end_to_end(monkeypatch, tmp_path):
    monkeypatch.setenv("MARKET_COMPASS_PROPOSAL_DIR", str(tmp_path))
    monkeypatch.setenv("MARKET_COMPASS_SOURCE_REVISION", "sandbox-source-123")
    client = TestClient(app)
    payload = _sample()
    result = client.post("/api/proposethat/intakes", json=payload)
    assert result.status_code == 201
    record = result.json()
    assert record["research_completed"] is False
    assert record["source_authority"]["market_compass_revision"] == "sandbox-source-123"
    assert len(record["recommendations"]) == 3
    assert record["authority"]["trade_execution"] is False
    assert record["authority"]["score_influence"] is False
    identifier = record["id"]
    assert client.get("/api/proposethat/intakes/" + identifier).json() == record
    assert client.post("/api/proposethat/intakes", json=payload).json()["id"] == identifier
    assert len(client.get("/api/proposethat/intakes").json()["intakes"]) == 1
    filename = next(tmp_path.glob("mcpt-*.json"))
    assert (filename.stat().st_mode & 0o777) == 0o600


def test_outside_source_is_not_automatically_verified(monkeypatch, tmp_path):
    monkeypatch.setenv("MARKET_COMPASS_PROPOSAL_DIR", str(tmp_path))
    record = TestClient(app).post("/api/proposethat/intakes", json=_sample("outside-trading-source")).json()
    assert record["evidence_state"]["source_fetched"] is False
    assert record["evidence_state"]["source_verified"] is False
    assert record["authority"]["automatic_research"] is False
    assert record["existing_capability_checklist"][0]["outside_source_state"].startswith("unknown")


def test_remote_and_cross_origin_are_forbidden(monkeypatch, tmp_path):
    monkeypatch.setenv("MARKET_COMPASS_PROPOSAL_DIR", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/proposethat/intakes", json=_sample(), headers={"Origin": "http://malicious.example"}).status_code == 403
    assert client.get("/api/proposethat/intakes", headers={"Host": "evil.example"}).status_code == 403
    assert not list(tmp_path.iterdir())


def test_excess_fields_and_invalid_ids_are_refused(monkeypatch, tmp_path):
    monkeypatch.setenv("MARKET_COMPASS_PROPOSAL_DIR", str(tmp_path))
    client = TestClient(app)
    unsafe = {**_sample(), "trade_execution": True}
    assert client.post("/api/proposethat/intakes", json=unsafe).status_code == 422
    unsafe_url = {**_sample(), "source_url": "file:///private/secrets"}
    assert client.post("/api/proposethat/intakes", json=unsafe_url).status_code == 422
    assert client.get("/api/proposethat/intakes/..%2F..%2Fetc").status_code in {400, 404}
    assert not list(tmp_path.glob("mcpt-*.json"))
