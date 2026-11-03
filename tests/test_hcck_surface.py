"""Smoke proof for the selectable HCCK browser workbench and guarded routing."""
from fastapi.testclient import TestClient

from market_compass.api import app


def test_hcck_selector_assets_and_two_simulation_routes():
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    html = page.text
    for marker in (
        'id="hcck-profile-select"',
        'id="hcck-profile-detail"',
        'id="hcck-load-example"',
        'id="universal-simulator"',
        'id="universal-input"',
        'id="universal-run"',
        'id="universal-export"',
        '/static/hcck.js',
        '/static/simulator.js',
    ):
        assert marker in html

    selector = client.get("/static/hcck.js")
    assert selector.status_code == 200
    source = selector.text
    assert "/api/hcck/profiles" in source
    assert "draft:synthetic-only" in source
    assert "target.dispatchEvent" in source
    assert 'selector.addEventListener' in source

    simulator = client.get("/static/simulator.js")
    assert simulator.status_code == 200
    assert "'/api/hcck/simulate'" in simulator.text
    assert "'/api/simulate'" in simulator.text
    assert "payload.state === 'held'" in simulator.text
    assert "profile_check:" in simulator.text
    assert 'input_sha256' in simulator.text
    assert 'textContent' in simulator.text

    directory = client.get("/api/hcck/profiles")
    assert directory.status_code == 200
    assert len(directory.json()["profiles"]) == 7
    assert directory.json()["schedules_running"] is False


def test_non_profile_route_remains_available():
    client = TestClient(app)
    data = {
        "subject": {"id": "fixture-batch", "name": "Example eggs", "kind": "batch",
                    "source_owner": "fixture", "authorized_use": True},
        "method": {"id": "example", "version": "v1", "author": "fixture",
                   "provenance": "synthetic",
                   "metrics": [{"id": "count", "label": "Count", "unit": "eggs",
                                "lower": 0, "upper": 12, "weight": 1,
                                "favorable": "higher"}]},
        "observations": [
            {"at": "2026-01-01T00:00:00Z", "values": {"count": 6}, "evidence_ref": "demo:1"}
        ],
        "purpose": "simulation"
    }
    result = client.post("/api/simulate", json=data)
    assert result.status_code == 200
    assert result.json()["records"][0]["index_points"] == 50
    assert result.json()["money_involved"] is False
