"""HCCK draft schedules: visible registry, bounded execution and refusal gates."""
import json
from pathlib import Path

from fastapi.testclient import TestClient

from market_compass.api import app

CLIENT = TestClient(app)


def fixture(profile="device-v1", kind="device"):
    return {
        "profile_id": profile,
        "cck_profile_ref": "draft:local-example",
        "source_fields": {
            "device_category": "laptop", "model": "illustrative laptop",
            "inventory_ref": "fixture-001",
        },
        "simulation": {
            "subject": {
                "id": "fixture-001", "name": "Illustrative laptop", "kind": kind,
                "source_owner": "fixture-owner", "authorized_use": True,
            },
            "method": {
                "id": "local-condition", "version": "v1",
                "author": "fixture-author", "provenance": "synthetic-only",
                "metrics": [
                    {"id": "battery", "label": "Battery", "unit": "percent",
                     "lower": 0, "upper": 100, "weight": 2, "favorable": "higher"},
                    {"id": "wear", "label": "Wear", "unit": "points",
                     "lower": 0, "upper": 10, "weight": 1, "favorable": "lower"},
                ],
            },
            "observations": [
                {"at": "2026-01-01T12:00:00Z",
                 "values": {"battery": 100, "wear": 0}, "evidence_ref": "fixture:1"},
                {"at": "2026-02-01T12:00:00Z",
                 "values": {"battery": 80, "wear": 2}, "evidence_ref": "fixture:2"},
            ],
            "purpose": "simulation",
        },
    }


def test_seven_profile_schedules_and_cck_authority_boundary():
    r = CLIENT.get("/api/hcck/profiles")
    assert r.status_code == 200
    d = r.json()
    assert d["schema"] == "market-compass.hybrid-cck-profile-schedule/v1"
    assert d["authority"]["cck_owner"] == "marvelousempire/cck-that"
    assert d["authority"]["schema_owner"] == "marvelousempire/schema-that-studio"
    assert d["authority"]["canonical_registration"] == "not-registered"
    assert d["authority"]["cck_witness_verified"] is False
    assert d["schedules_running"] is False
    ids = {p["id"] for p in d["profiles"]}
    assert ids == {"athlete-performance-v1", "equity-v1", "option-v1",
                   "device-v1", "batch-v1", "general-v1", "participant-v1"}
    assert len(d["cck_minimum_fields"]["crown"]) == 8
    assert len(d["cck_minimum_fields"]["character"]) == 6
    assert len(d["cck_minimum_fields"]["key"]) == 4
    assert all(p["schedule"]["automatic_job"] is False for p in d["profiles"])


def test_device_profiled_simulation_runs_without_claiming_cck_authority():
    r = CLIENT.post("/api/hcck/simulate", json=fixture())
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["state"] == "draft-shape-matched"
    assert d["profile_id"] == "device-v1"
    assert d["cck_witness_verified"] is False
    assert d["source_verified"] is False
    assert d["automatic_job_running"] is False
    assert d["simulation"]["mode"] == "hypothetical-non-monetary"
    assert d["simulation"]["trade_execution"] is False
    assert d["simulation"]["score_influence"] is False
    assert [point["index_points"] for point in d["simulation"]["records"]] == [100.0, 80.0]


def test_missing_or_extra_metadata_is_held_not_scored():
    payload = fixture()
    del payload["source_fields"]["inventory_ref"]
    d = CLIENT.post("/api/hcck/simulate", json=payload).json()
    assert d["state"] == "held"
    assert d["missing_fields"] == ["inventory_ref"]
    assert d["simulation"] is None
    payload = fixture()
    payload["source_fields"]["made_up"] = "surprise"
    d = CLIENT.post("/api/hcck/simulate", json=payload).json()
    assert d["state"] == "held"
    assert d["unrecognized_fields"] == ["made_up"]


def test_wrong_subject_kind_and_unknown_profile_held():
    payload = fixture(kind="person")
    d = CLIENT.post("/api/hcck/simulate", json=payload).json()
    assert "subject-kind-does-not-match-profile" in d["reasons"]
    assert d["simulation"] is None
    payload = fixture()
    payload["profile_id"] = "does-not-exist"
    d = CLIENT.post("/api/hcck/simulate", json=payload).json()
    assert d["state"] == "held"
    assert d["simulation"] is None


def test_athlete_profile_requires_declared_observation_references():
    payload = fixture("athlete-performance-v1", "player_profile")
    payload["source_fields"] = {
        "player_ref": "synthetic-person", "sport": "basketball",
        "season": "2026", "source_scope": "demo",
        "consent_ref": "fixture-consent-only",
    }
    payload["simulation"]["observations"][0]["evidence_ref"] = None
    d = CLIENT.post("/api/hcck/simulate", json=payload).json()
    assert d["state"] == "held"
    assert "observation-evidence-reference-missing" in d["reasons"]
    payload["simulation"]["observations"][0]["evidence_ref"] = "fixture:1"
    d = CLIENT.post("/api/hcck/simulate", json=payload).json()
    assert d["state"] == "draft-shape-matched"
    assert d["cck_witness_verified"] is False
    assert d["source_verified"] is False


def test_equity_and_option_schedules_do_not_mean_broker_trading():
    for profile, kind, envelope in (
        ("equity-v1", "equity", {
            "symbol": "DEMO", "exchange": "fictional", "quote_currency": "USD",
            "source_id": "fixture"}),
        ("option-v1", "option", {
            "underlying": "DEMO", "expiry": "2026-12-18",
            "right": "call", "strike": "50", "quote_currency": "USD",
            "source_id": "fixture"}),
    ):
        payload = fixture(profile, kind)
        payload["source_fields"] = envelope
        d = CLIENT.post("/api/hcck/simulate", json=payload).json()
        assert d["state"] == "draft-shape-matched"
        assert d["simulation"]["money_involved"] is False
        assert d["simulation"]["trade_execution"] is False
        assert d["simulation"]["score_influence"] is False


def test_authorization_remains_required():
    payload = fixture()
    payload["simulation"]["subject"]["authorized_use"] = False
    assert CLIENT.post("/api/hcck/simulate", json=payload).status_code == 422
    payload = fixture()
    payload["cck_profile_ref"] = ""
    assert CLIENT.post("/api/hcck/simulate", json=payload).status_code == 422


def test_named_sections_share_participant_template_without_impersonation():
    d = CLIENT.get("/api/hcck/profiles").json()
    instances = d["participant_instances"]
    assert len(instances) == 4
    assert {p["profile_id"] for p in instances} == {"participant-v1"}
    cards = {p["name"]: p["card"]["title"] if p["card"] else None for p in instances}
    assert cards["Brown's Barometers"] == "King of Spades"
    assert cards["Prince's Principles"] == "King of Diamonds"
    assert cards["Omo's Intel"] == "King of Clubs"
    assert cards["Wuda's Watch"] == "King of Hearts"
    assert all(p["state"] == "draft-not-certified" for p in instances)
    assert next(p for p in instances if p["name"] == "Brown's Barometers")["research_actor"] == "browns-barometers"


def test_draft_schedule_json_schema_is_parseable_and_matches_profiles():
    root = Path(__file__).resolve().parents[1]
    path = root / "contracts" / "hcck-profile-schedule.v1.schema.json"
    definition = json.loads(path.read_text(encoding="utf-8"))
    assert definition["$schema"].endswith("/2020-12/schema")
    assert definition["additionalProperties"] is False
    assert definition["properties"]["schedule"]["properties"]["automatic_job"]["const"] is False
    profiles = CLIENT.get("/api/hcck/profiles").json()["profiles"]
    required = set(definition["required"])
    for profile in profiles:
        assert required <= set(profile)
        assert set(profile["schedule"]) == set(definition["properties"]["schedule"]["required"])
        assert profile["schedule"]["timezone"] == "UTC"
        assert profile["schedule"]["timestamp"] == "observation.at"
        assert profile["schedule"]["automatic_job"] is False
