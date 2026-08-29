from __future__ import annotations

import hashlib
import json
from typing import Any

from ..contracts import AnalystResponse, EvidenceCitation, ModelReceipt, ProviderStatus
from .base import AnalystProvider


def report_hash(report: dict[str, Any]) -> str:
    raw = json.dumps(report, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


class GroundedMockProvider(AnalystProvider):
    id = "grounded-offline"
    label = "Grounded Offline Analyst"
    lane = "offline"
    model = "deterministic-v1"
    cloud = False

    def status(self) -> ProviderStatus:
        return ProviderStatus(
            id=self.id, label=self.label, lane=self.lane, model=self.model,
            cloud=False, configured=True, healthy=True,
            reason="Always available; validates the analyst contract without an LLM.",
        )

    def analyze(self, report: dict[str, Any], question: str, depth: str) -> AnalystResponse:
        layers = report.get("layers") or {}
        bull: list[tuple[float, str, str]] = []
        bear: list[tuple[float, str, str]] = []
        missing: list[str] = []
        for key, layer in layers.items():
            for item in layer.get("evidence") or []:
                bull.append((float(item.get("strength", 0)), key, str(item.get("text", ""))))
            for item in layer.get("counter_evidence") or []:
                bear.append((float(item.get("strength", 0)), key, str(item.get("text", ""))))
            missing.extend(f"{key}: {x}" for x in layer.get("missing") or [])
        bull.sort(reverse=True)
        bear.sort(reverse=True)
        citations = [
            EvidenceCitation(node_id=key, claim=text)
            for _strength, key, text in (bull[:3] + bear[:3]) if text
        ]
        route = report.get("route") or {}
        balance = f"{report.get('bull_evidence', 0)}/{report.get('bear_evidence', 0)}"
        summary = (
            f"{report.get('symbol', 'Asset')} is a {report.get('action', 'watch')} setup with "
            f"a {balance} bull/bear evidence balance and "
            f"{float(report.get('confidence', 0)):.0%} confidence."
        )
        return AnalystResponse(
            summary=summary,
            market_state=str(report.get("summary") or "Evidence is mixed."),
            bull_case=[x[2] for x in bull[:4]],
            bear_case=[x[2] for x in bear[:4]],
            main_conflict=(bear[0][2] if bear else "No explicit counter-evidence was returned."),
            invalidation_interpretation=(
                f"The current route is invalidated near {route.get('invalidation')}."
                if route.get("invalidation") is not None else "No numeric route invalidation is available."
            ),
            missing_information=missing[:10],
            next_research_actions=["Resolve the declared evidence gaps.", "Re-run when source data is stale."],
            citations=citations,
            receipt=ModelReceipt(
                provider=self.id, model=self.model, lane=self.lane,
                report_hash=report_hash(report), latency_ms=0,
            ),
        )
