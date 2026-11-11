"""Universal simulation acceptance: no financial or official player writes."""

from fastapi.testclient import TestClient

from market_compass.api import app

CLIENT = TestClient(app)


def example(kind="device"):
    return {
        "subject": {
            "id": "demo-laptop", "name": "Illustrative old laptop",
            "kind": kind, "source_owner": "example operator", "authorized_use": True,
        },
        "method": {
            "id": "example-condition-method", "version": "0.1-illustrative",
            "author": "example operator", "provenance": "local teaching fixture",
            "metrics": [
                {"id": "battery", "label": "Battery health", "unit": "percent",
                 "lower": 0, "upper": 100, "weight": 2, "favorable": "higher"},
                {"id": "wear", "label": "Visible wear", "unit": "score",
                 "lower": 0, "upper": 10, "weight": 1, "favorable": "lower"},
            ],
        },
        "observations": [
            {"at": "2026-01-01T12:00:00Z", "values": {"battery": 100, "wear": 0}, "evidence_ref": "demo:1"},
            {"at": "2026-02-01T12:00:00Z", "values": {"battery": 80, "wear": 2}, "evidence_ref": "demo:2"},
            {"at": "2026-03-01T12:00:00Z", "values": {"battery": 60, "wear": 6}, "evidence_ref": "demo:3"},
        ],
        "purpose": "simulation",
    }


def test_any_authorized_subject_gets_non_monetary_index():
    response = CLIENT.post("/api/simulate", json=example())
    assert response.status_code == 200, response.text
    d = response.json()
    assert d["schema"] == "market-compass.simulation/v1"
    assert [r["index_points"] for r in d["records"]] == [100, 80, 53.3333]
    assert d["observed_points"] == 3
    assert d["held_points"] == 0
    assert d["volatility_points_per_observation"] is not None
    assert len(d["input_sha256"]) == 64
    assert d["money_involved"] is False
    assert d["trade_execution"] is False
    assert d["signal_generation"] is True
    assert d["score_influence"] is False
    assert d["data_stored"] is False
    assert d["else_connected"] is False
    assert d["source_verified"] is False
    assert d["inputs"]["method"]["id"] == "example-condition-method"
    assert d["formula"].startswith("index_points = 100")
    assert d["timeframe"]["observations"] == 3
    assert d["timestamp"] == "2026-03-01T12:00:00+00:00"
    assert d["provenance"]["source_verified"] is False
    assert d["confidence"]["value"] is None
    assert len(d["receipt_sha256"]) == 64
    assert CLIENT.post("/api/simulate", json=example()).json()["input_sha256"] == d["input_sha256"]


def test_authorization_required_even_for_profile():
    payload = example("player_profile")
    payload["subject"]["authorized_use"] = False
    assert CLIENT.post("/api/simulate", json=payload).status_code == 422


def test_missing_metric_is_held_not_silently_zero_filled():
    payload = example("batch")
    del payload["observations"][1]["values"]["wear"]
    d = CLIENT.post("/api/simulate", json=payload).json()
    assert d["held_points"] == 1
    assert d["records"][1]["state"] == "held"
    assert d["records"][1]["index_points"] is None
    assert d["records"][1]["missing"] == ["wear"]


def test_nonfinite_and_duplicate_metric_definitions_refused():
    payload = example()
    payload["observations"][0]["values"]["battery"] = "NaN"
    assert CLIENT.post("/api/simulate", json=payload).status_code == 422
    payload = example()
    payload["method"]["metrics"][1]["id"] = "battery"
    assert CLIENT.post("/api/simulate", json=payload).status_code == 422


def test_duplicated_or_naive_dates_refused():
    payload = example()
    payload["observations"][1]["at"] = payload["observations"][0]["at"]
    assert CLIENT.post("/api/simulate", json=payload).status_code == 422
    payload = example()
    payload["observations"][0]["at"] = "2026-01-01T12:00:00"
    assert CLIENT.post("/api/simulate", json=payload).status_code == 422
