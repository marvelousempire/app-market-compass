"""Private, local-only proposeTHAT research intake. No external requests or trading."""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator

SCHEMA = "market-compass.proposethat-intake.v1"
ID_PATTERN = re.compile(r"^mcpt-[0-9a-f]{24}$")


class IntakeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    mode: Literal["owner-improvement", "outside-trading-source"]
    subject: str = Field(min_length=2, max_length=160)
    goal: str = Field(min_length=5, max_length=1500)
    source_url: str | None = Field(default=None, max_length=700)
    source_revision: str | None = Field(default=None, max_length=160)

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Provide an HTTP(S) source URL without credentials.")
        return value


# Documented capabilities, NOT independently inspected live/runtime facts.
EXISTING_CAPABILITIES = (
    ("Technical evidence", "EMA, RSI, MACD, Fibonacci, Bus Stops and Price Memory", "src/market_compass/technical.py"),
    ("Two-sided reasoning", "Bull/bear evidence, counter-case, confidence and invalidation", "src/market_compass/scoring.py"),
    ("Research view", "Chart, research desk, 115 node IDs and report views", "src/market_compass/registry.py"),
    ("Actor research", "Omo, Prince, Wuda and Brown's Barometers", "src/market_compass/web/research-cassettes.js"),
    ("Market data research", "intelTHAT and the Day Trader evidence lens", "src/market_compass/intelthat_native.py"),
    ("Universal measurement", "Hypothetical simulations and draft HCCK profiles", "src/market_compass/simulation.py"),
)


def _request_digest(payload: dict) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_record(request: IntakeRequest, *, source_revision: str = "unverified") -> dict:
    """An owner handoff, never a claim of completed source research."""
    payload = request.model_dump(mode="json")
    fingerprint = _request_digest(payload)
    record_id = f"mcpt-{fingerprint[:24]}"
    owner_mode = request.mode == "owner-improvement"
    candidates = [
        ("Verify current owner/source truth", "Compare Gitea, GitHub study and FiveMac receipt; identify what already exists."),
        ("Close one measured workflow gap", "Measure the requested task before and after one reversible change; preserve existing nodes and Actors."),
        ("Independently prove the result", "Run owner tests and independent Niece result readback; record live proof separately."),
    ] if owner_mode else [
        ("Verify the outside source", "Confirm identity, revision, license, actual behavior and missing evidence."),
        ("Compare both directions", "Separate evidenced outside advantages, Compass advantages, overlap and intentional exclusions."),
        ("Trial one read-only research slice", "Test a licensed, non-executing technique without broker access or score changes."),
    ]
    recommendations = [{
        "id": f"{record_id}-r{number:02d}",
        "function_owner": "Nephew / approved proposeTHAT research agent",
        "result_owner": "Niece / independent receiving check",
        "title": title,
        "function": function,
        "expected_result": "Dated source-linked evidence and independently reproducible PASS/FAIL receipt",
        "status": "proposed-not-executed",
    } for number, (title, function) in enumerate(candidates, 1)]
    return {
        "schema": SCHEMA,
        "id": record_id,
        "request_sha256": fingerprint,
        "mode": request.mode,
        "status": "received-local-research-request",
        "research_completed": False,
        "request": payload,
        "owner": "marvelousempire/app-market-compass",
        "research_owner": "marvelousempire/proposeTHAT",
        "source_authority": {"market_compass_revision": source_revision, "five_mac_runtime_verified": False},
        "evidence_state": {
            "provided_source_url": request.source_url,
            "provided_source_revision": request.source_revision,
            "source_fetched": False, "source_verified": False, "market_compass_live_inspected": False,
        },
        "existing_capability_checklist": [{
            "capability": name,
            "market_compass_source_claim": description,
            "source_path": path,
            "market_compass_runtime_state": "not inspected in this intake",
            "outside_source_state": "not applicable" if owner_mode else "unknown; source not fetched",
        } for name, description, path in EXISTING_CAPABILITIES],
        "recommendations": recommendations,
        "next_action": "Research current owner sources, pin evidence, run one reversible pilot and independent readback.",
        "authority": {
            "research_only": True, "automatic_owner_intake": True, "automatic_research": False,
            "trade_execution": False, "broker_credentials": False,
            "score_influence": False, "money_movement": False,
        },
    }


def _root() -> Path:
    raw = os.getenv("MARKET_COMPASS_PROPOSAL_DIR")
    root = Path(raw).expanduser() if raw else Path.home() / ".market-compass" / "private" / "proposethat"
    if root.is_symlink():
        raise ValueError("Intake directory must not be a symlink.")
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Invalid intake directory.")
    return root


def receive(request: IntakeRequest, *, source_revision: str = "unverified") -> dict:
    record = build_record(request, source_revision=source_revision)
    filename = _root() / f"{record['id']}.json"
    if filename.is_symlink():
        raise ValueError("Intake record must not be a symlink.")
    if filename.exists():
        previous = json.loads(filename.read_text(encoding="utf-8"))
        if previous.get("request_sha256") != record["request_sha256"]:
            raise ValueError("Existing intake ID has a different source digest.")
        return previous
    record["received_at"] = datetime.now(UTC).isoformat()
    encoded = (json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(filename, flags, 0o600)
    except FileExistsError:
        return receive(request, source_revision=source_revision)
    with os.fdopen(fd, "wb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    return record


def read_intake(record_id: str) -> dict:
    if not ID_PATTERN.fullmatch(record_id):
        raise ValueError("Invalid intake ID")
    filename = _root() / f"{record_id}.json"
    if not filename.is_file() or filename.is_symlink():
        raise FileNotFoundError("Intake not found")
    record = json.loads(filename.read_text(encoding="utf-8"))
    if record.get("id") != record_id:
        raise ValueError("Stored intake does not match its filename")
    return record


def list_intakes(limit: int = 25) -> list[dict]:
    results = []
    for filename in sorted(_root().glob("mcpt-*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        if len(results) >= limit:
            break
        if not ID_PATTERN.fullmatch(filename.stem) or filename.is_symlink():
            continue
        try:
            record = read_intake(filename.stem)
        except (ValueError, OSError, json.JSONDecodeError):
            continue
        results.append({
            "id": record["id"], "mode": record["mode"],
            "subject": record["request"]["subject"],
            "status": record["status"], "received_at": record.get("received_at"),
        })
    return results
