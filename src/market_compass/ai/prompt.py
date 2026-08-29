from __future__ import annotations

import json
from typing import Any

SYSTEM_PROMPT = """You are Nephew acting as the Market Compass Analyst.
Market Compass is the source of calculated truth. Interpret the supplied report without changing
its scores, inventing market facts, or treating evidence balance as profit probability. Cite the
report layer key or stable node ID for every material claim. Show both sides, missing information,
the strongest conflict, and what invalidates the interpretation. Return only JSON matching the
requested schema."""


def build_prompt(report: dict[str, Any], question: str, depth: str) -> str:
    schema = {
        "summary": "string",
        "market_state": "string",
        "bull_case": ["string"],
        "bear_case": ["string"],
        "main_conflict": "string",
        "invalidation_interpretation": "string",
        "missing_information": ["string"],
        "next_research_actions": ["string"],
        "citations": [{"node_id": "layer-or-node-id", "claim": "string", "source": "string"}],
    }
    return (
        f"Question: {question}\nDepth: {depth}\nRequired JSON schema: "
        f"{json.dumps(schema, separators=(',', ':'))}\nMarket Compass report: "
        f"{json.dumps(report, separators=(',', ':'), default=str)}"
    )
