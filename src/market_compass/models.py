from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    text: str
    direction: int = Field(ge=-1, le=1)
    strength: float = Field(default=0.5, ge=0, le=1)
    source: str = "calculation"


class LayerResult(BaseModel):
    key: str
    label: str
    state: str
    score: float = Field(ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    evidence: list[Evidence] = Field(default_factory=list)
    counter_evidence: list[Evidence] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    missing: list[str] = Field(default_factory=list)


class Route(BaseModel):
    direction: str = "unclear"
    last_bus_stop: float | None = None
    next_bus_stops: list[float] = Field(default_factory=list)
    downside_stops: list[float] = Field(default_factory=list)
    invalidation: float | None = None
    reward_risk: float | None = None
    fibonacci: dict[str, float] = Field(default_factory=dict)
    fibonacci_anchors: dict[str, Any] = Field(default_factory=dict)
    confluence: list[dict[str, Any]] = Field(default_factory=list)


class Report(BaseModel):
    symbol: str
    as_of: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    horizon_days: int
    price: float
    action: str
    bull_evidence: int
    bear_evidence: int
    confidence: float
    summary: str
    technical_summary: str
    route: Route
    layers: dict[str, LayerResult]
    forecast: dict[str, Any] = Field(default_factory=dict)
    evidence_board: dict[str, Any] = Field(default_factory=dict)
    data_meta: dict[str, Any] = Field(default_factory=dict)
    chart: dict[str, list[Any]] = Field(default_factory=dict)
    timeframes: dict[str, Any] = Field(default_factory=dict)
    contributions: list[dict[str, Any]] = Field(default_factory=list)
    catalysts: list[dict[str, Any]] = Field(default_factory=list)
    calibration: dict[str, Any] = Field(default_factory=dict)
