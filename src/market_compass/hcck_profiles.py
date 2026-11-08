"""Domain schedules for Market Compass Hybrid CCK draft profiles.

CCK That remains the profile authority (77 fields). Schema That Studio is
the indexed schema authority. These are local domain projections only;
no claim of a canonical CCK validation, minted identity, scheduled job, or
upstream source authorization is made by this module.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from .simulation import SimulationRequest, simulate


# Named founding seats are display references only. Current research actors remain
# Omo, Prince, Wuda, and Brown's Barometers in research-cassettes.js.
# These labels do not replace, impersonate, merge or authorize those Actors.
PARTICIPANT_SEATS = (
    {"id":"seat-omos-intel","name":"Omo's Intel","profile_id":"participant-v1","participant_id":"omos-intel","card":{"title":"King of Clubs","suit":"clubs"},"research_actor":"omo","state":"draft-not-certified"},
    {"id":"seat-princes-principles","name":"Prince's Principles","profile_id":"participant-v1","participant_id":"princes-principles","card":{"title":"King of Diamonds","suit":"diamonds"},"research_actor":"prince","state":"draft-not-certified"},
    {"id":"seat-princes-intel","name":"Prince's Intel","profile_id":"participant-v1","participant_id":"princes-intel","card":None,"research_actor":None,"state":"awaiting-owner-content"},
    {"id":"seat-marvins-metrics","name":"Marvin's Metrics","profile_id":"participant-v1","participant_id":"marvins-metrics","card":{"title":"King of Spades","suit":"spades"},"research_actor":None,"state":"awaiting-owner-content"},
    {"id":"seat-wudas-watch","name":"Wuda's Watch","profile_id":"participant-v1","participant_id":"wudas-watch","card":{"title":"King of Hearts","suit":"hearts"},"research_actor":"wuda","state":"draft-not-certified"},
)

CCK_OWNER = "marvelousempire/cck-that"
SCHEMA_OWNER = "marvelousempire/schema-that-studio"
CCK_MINIMUM = {
    "crown": [
        "artifact_id", "artifact_name", "artifact_type", "version",
        "owner", "status", "evidence_state", "source_commit",
    ],
    "character": [
        "purpose", "intent", "role", "responsibility", "condition", "environment",
    ],
    "key": [
        "required_fields_present", "cck_completeness_score",
        "queen_yeah_right_witness", "sha_witness",
    ],
}

# A schedule says *when an observation belongs*, not that a background
# scheduler is deployed. Each required field is a domain envelope, not an
# assertion of independently verified source truth.
PROFILES = (
    {
        "id": "readyplay-player-v1", "title": "READYPLAY player performance",
        "subject_kind": "player_profile", "domain": "sport",
        "source_owner": "READYPLAY", "fields": (
            "player_ref", "sport", "season", "source_scope", "consent_ref",
        ),
        "schedule": {"clock": "event", "cadence": "accepted-game-or-session",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": True, "automatic_job": False},
        "example_metrics": ("points", "defensive_events", "workout_reps"),
        "notes": "Accepted games and training are separate source books. Market Compass cannot certify READYPLAY evidence.",
    },
    {
        "id": "equity-v1", "title": "Stock or listed-equity study",
        "subject_kind": "equity", "domain": "equity",
        "source_owner": "user-specified-data-provider", "fields": (
            "symbol", "exchange", "quote_currency", "source_id",
        ),
        "schedule": {"clock": "calendar", "cadence": "source-session-or-daily",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": True, "automatic_job": False},
        "example_metrics": ("close", "volume", "volatility"),
        "notes": "Simulation is non-monetary, even if source measurements include a quoted currency.",
    },
    {
        "id": "option-v1", "title": "Options contract study",
        "subject_kind": "option", "domain": "options",
        "source_owner": "user-specified-data-provider", "fields": (
            "underlying", "expiry", "right", "strike", "quote_currency", "source_id",
        ),
        "schedule": {"clock": "calendar", "cadence": "quote-snapshot",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": True, "automatic_job": False},
        "example_metrics": ("implied_volatility", "open_interest", "spread_width"),
        "notes": "Options labels describe an observation contract. No option order, quote verification, or broker adapter.",
    },
    {
        "id": "device-v1", "title": "Phones, computers and cameras",
        "subject_kind": "device", "domain": "inventory",
        "source_owner": "subject-data-owner", "fields": (
            "device_category", "model", "inventory_ref",
        ),
        "schedule": {"clock": "event", "cadence": "inspection-or-reading",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": False, "automatic_job": False},
        "example_metrics": ("battery_health", "physical_wear", "uptime"),
        "notes": "Device observations are descriptive; no implied resale value.",
    },
    {
        "id": "batch-v1", "title": "Eggs, products and physical batches",
        "subject_kind": "batch", "domain": "goods",
        "source_owner": "subject-data-owner", "fields": (
            "batch_ref", "category", "quantity_unit",
        ),
        "schedule": {"clock": "event", "cadence": "batch-inspection",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": False, "automatic_job": False},
        "example_metrics": ("count", "quality_score", "freshness"),
        "notes": "Supply and condition studies use a user-declared method, not a commodity market.",
    },
    {
        "id": "participant-v1", "title": "Market Compass named participant",
        "subject_kind": "participant", "domain": "participant",
        "source_owner": "participant-or-delegated-owner", "fields": (
            "participant_id", "role_ref", "source_scope",
        ),
        "schedule": {"clock": "event", "cadence": "authorized-method-or-evidence-update",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": True, "automatic_job": False},
        "example_metrics": ("owner_authored_metric",),
        "notes": "Spades, Diamonds, Clubs and Hearts are display role mappings. Prince's Intel has no card assignment. No person ownership or access grant.",
    },
    {
        "id": "general-v1", "title": "Any authorized measurable subject",
        "subject_kind": None, "domain": "general",
        "source_owner": "subject-data-owner", "fields": ("category", "source_ref"),
        "schedule": {"clock": "event", "cadence": "source-observation",
                     "timestamp": "observation.at", "timezone": "UTC",
                     "evidence_required": False, "automatic_job": False},
        "example_metrics": ("user_defined_metric",),
        "notes": "Owner-authored methods must remain labeled with authorship, units and version.",
    },
)


def profile_directory() -> dict:
    return {
        "schema": "market-compass.hybrid-cck-profile-schedule/v1",
        "authority": {"cck_owner": CCK_OWNER, "schema_owner": SCHEMA_OWNER,
                      "canonical_registration": "not-registered",
                      "cck_witness_verified": False},
        "cck_minimum_fields": CCK_MINIMUM,
        "schedules_running": False,
        "participant_instances": [dict(item) for item in PARTICIPANT_SEATS],
        "profiles": [
            {**p, "fields": list(p["fields"]), "example_metrics": list(p["example_metrics"]),
             "schedule": dict(p["schedule"])}
            for p in PROFILES
        ],
    }


def get_profile(profile_id: str) -> dict | None:
    return next((dict(p) for p in PROFILES if p["id"] == profile_id), None)


class ProfiledSimulationRequest(BaseModel):
    profile_id: str = Field(min_length=1, max_length=100)
    # Source-domain fields are declared references, not verified identity.
    source_fields: dict[str, str] = Field(default_factory=dict, max_length=20)
    # CCK link is an unverified draft reference until CCK That reads it back.
    cck_profile_ref: str = Field(min_length=1, max_length=200)
    simulation: SimulationRequest


def run_profiled_simulation(request: ProfiledSimulationRequest) -> dict:
    profile = get_profile(request.profile_id)
    if profile is None:
        return {"state": "held", "reasons": ["unknown-profile-id"], "simulation": None}
    needed = set(profile["fields"])
    missing = sorted(k for k in needed if not request.source_fields.get(k, "").strip())
    extras = sorted(k for k in request.source_fields if k not in needed)
    kind = request.simulation.subject.kind
    reasons = []
    if profile["subject_kind"] and kind != profile["subject_kind"]:
        reasons.append("subject-kind-does-not-match-profile")
    if missing:
        reasons.append("missing-source-fields")
    if extras:
        reasons.append("unrecognized-source-fields")
    if profile["schedule"]["evidence_required"] and any(
        not (o.evidence_ref and o.evidence_ref.strip())
        for o in request.simulation.observations
    ):
        reasons.append("observation-evidence-reference-missing")
    if reasons:
        return {
            "schema": "market-compass.profiled-simulation/v1",
            "state": "held", "profile_id": profile["id"],
            "reasons": reasons, "missing_fields": missing,
            "unrecognized_fields": extras, "simulation": None,
            "cck_witness_verified": False, "source_verified": False,
        }
    result = simulate(request.simulation)
    return {
        "schema": "market-compass.profiled-simulation/v1",
        "state": "draft-shape-matched",
        "profile_id": profile["id"], "cck_profile_ref": request.cck_profile_ref,
        "schedule": dict(profile["schedule"]),
        "source_fields": request.source_fields,
        "cck_witness_verified": False, "source_verified": False,
        "automatic_job_running": False, "simulation": result,
        "notice": "Profile fields match the draft template only. CCK certification, source evidence, and ELSE method authority are unverified.",
    }
