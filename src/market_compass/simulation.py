"""Portable, non-monetary measurement simulation for arbitrary subjects.

ELSE is the independent methodology authority; this API accepts a *supplied*
versioned methodology but does not claim to call or authorize ELSE. No storage,
trade, ownership, wagering, person valuation or market-price fabrication.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from itertools import pairwise
from statistics import pstdev
from typing import Literal

from pydantic import BaseModel, Field, FiniteFloat, model_validator


class Subject(BaseModel):
    id: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=120)
    kind: Literal["person", "player_profile", "device", "product", "batch", "team", "organization", "equity", "option", "participant", "other"]
    source_owner: str = Field(min_length=1, max_length=120)
    authorized_use: bool = False


class Metric(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,49}$")
    label: str = Field(min_length=1, max_length=80)
    unit: str = Field(min_length=1, max_length=30)
    lower: FiniteFloat
    upper: FiniteFloat
    weight: FiniteFloat = Field(gt=0, le=100)
    favorable: Literal["higher", "lower"] = "higher"

    @model_validator(mode="after")
    def check_bounds(self):
        if self.upper <= self.lower:
            raise ValueError("metric upper must exceed lower")
        return self


class Method(BaseModel):
    id: str = Field(min_length=1, max_length=80)
    version: str = Field(min_length=1, max_length=40)
    author: str = Field(min_length=1, max_length=120)
    provenance: str = Field(min_length=1, max_length=200)
    metrics: list[Metric] = Field(min_length=1, max_length=12)

    @model_validator(mode="after")
    def unique_ids(self):
        if len({m.id for m in self.metrics}) != len(self.metrics):
            raise ValueError("metric IDs must be unique")
        return self


class Observation(BaseModel):
    at: datetime
    values: dict[str, FiniteFloat] = Field(max_length=12)
    evidence_ref: str | None = Field(default=None, max_length=200)


class SimulationRequest(BaseModel):
    subject: Subject
    method: Method
    observations: list[Observation] = Field(min_length=1, max_length=365)
    purpose: Literal["simulation"] = "simulation"

    @model_validator(mode="after")
    def authorized_and_ordered(self):
        if not self.subject.authorized_use:
            raise ValueError("subject data-use authorization is required")
        times = [o.at for o in self.observations]
        if any(t.utcoffset() is None for t in times):
            raise ValueError("observation timestamps must carry a timezone")
        if times != sorted(times) or len(times) != len(set(times)):
            raise ValueError("observations must be strictly chronological")
        return self


def simulate(request: SimulationRequest) -> dict:
    """Calculate a weighted 0-100 study index with missing-source holds.

    Index is relative to the supplied method's ranges, NOT an intrinsic
    monetary or human value. Volatility is population standard deviation of
    consecutive observed index changes in *points per observation*, not annualized.
    """
    metrics = request.method.metrics
    wanted = {m.id for m in metrics}
    total_weight = sum(float(m.weight) for m in metrics)
    records = []
    values: list[float] = []
    for observation in request.observations:
        present = set(observation.values)
        missing = sorted(wanted - present)
        extra = sorted(present - wanted)
        if missing or extra:
            records.append({
                "at": observation.at.isoformat(), "state": "held",
                "reason": "missing-or-unrecognized-metrics",
                "missing": missing, "unrecognized": extra,
                "index_points": None, "evidence_ref": observation.evidence_ref,
            })
            continue
        weighted = 0.0
        for metric in metrics:
            raw = float(observation.values[metric.id])
            proportion = min(1.0, max(0.0, (raw - float(metric.lower)) / (float(metric.upper) - float(metric.lower))))
            if metric.favorable == "lower":
                proportion = 1.0 - proportion
            weighted += proportion * float(metric.weight)
        score = round(100.0 * weighted / total_weight, 4)
        values.append(score)
        records.append({
            "at": observation.at.isoformat(), "state": "calculated",
            "reason": "method-applied-to-user-supplied-observations",
            "missing": [], "unrecognized": [],
            "index_points": score, "evidence_ref": observation.evidence_ref,
        })
    changes = [round(b - a, 4) for a, b in pairwise(values)]
    volatility = round(pstdev(changes), 4) if len(changes) > 1 else None
    canonical = json.dumps(request.model_dump(mode="json"), sort_keys=True, separators=(",", ":"), allow_nan=False)
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    inputs = request.model_dump(mode="json")
    formula = (
        "index_points = 100 * sum(weight * clamp((value-lower)/(upper-lower), 0, 1) "
        "with lower-favorable metrics inverted) / sum(weight)"
    )
    result = {
        "schema": "market-compass.simulation/v1",
        "mode": "hypothetical-non-monetary",
        "subject": request.subject.model_dump(exclude={"authorized_use"}),
        "method": {"id": request.method.id, "version": request.method.version,
                   "author": request.method.author, "provenance": request.method.provenance},
        "records": records,
        "observed_points": len(values),
        "held_points": len(records) - len(values),
        "index_unit": "method-relative-points",
        "changes_in_points": changes,
        "volatility_points_per_observation": volatility,
        "inputs": inputs,
        "formula": formula,
        "timeframe": {
            "kind": "observation-series",
            "start": request.observations[0].at.isoformat(),
            "end": request.observations[-1].at.isoformat(),
            "observations": len(request.observations),
        },
        "timestamp": request.observations[-1].at.isoformat(),
        "provenance": {
            "method_id": request.method.id,
            "method_version": request.method.version,
            "method_author": request.method.author,
            "method_provenance": request.method.provenance,
            "source_owner": request.subject.source_owner,
            "source_verified": False,
        },
        "confidence": {
            "value": None,
            "meaning": "unrated because inputs, evidence, and method authority are user supplied and unverified",
        },
        "input_sha256": digest,
        "data_stored": False,
        "money_involved": False,
        "trading_enabled": False,
        "trade_execution": False,
        "broker_credentials": False,
        "money_movement": False,
        "signal_generation": True,
        "score_influence": False,
        "source_verified": False,
        "else_connected": False,
        "notice": "Study index only; supplied inputs and method are not independently verified. Persons are never financial securities.",
    }
    receipt_payload = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)
    result["receipt_sha256"] = hashlib.sha256(receipt_payload.encode()).hexdigest()
    return result
