from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class EvidenceCitation(BaseModel):
    node_id: str
    claim: str
    source: str = "market-compass"


class ModelReceipt(BaseModel):
    provider: str
    model: str
    lane: str
    prompt_version: str = "market-analyst-v1"
    report_hash: str
    latency_ms: int = Field(ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AnalystRequest(BaseModel):
    report: dict[str, Any]
    question: str = Field(default="Give me a grounded analysis.", min_length=1, max_length=4000)
    provider: str = "auto"
    depth: Literal["fast", "deep", "super-heavy"] = "deep"
    cloud_allowed: bool = False


class AnalystResponse(BaseModel):
    summary: str
    market_state: str
    bull_case: list[str] = Field(default_factory=list)
    bear_case: list[str] = Field(default_factory=list)
    main_conflict: str
    invalidation_interpretation: str
    missing_information: list[str] = Field(default_factory=list)
    next_research_actions: list[str] = Field(default_factory=list)
    citations: list[EvidenceCitation] = Field(default_factory=list)
    receipt: ModelReceipt
    warning: str = "AI interprets Market Compass evidence; it does not calculate or alter the score."


class ProviderStatus(BaseModel):
    id: str
    label: str
    lane: str
    model: str
    cloud: bool
    configured: bool
    healthy: bool
    reason: str = ""
