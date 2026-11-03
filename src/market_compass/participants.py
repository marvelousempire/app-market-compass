"""Founder-named Market Compass participants.

A display name is not a source-of-truth transfer, owner authorization, or
commissioning receipt. Only Omo's Intel has an implemented read-only adapter.
"""
from __future__ import annotations

# Card symbolism is an identity/display mapping, not an authorization hierarchy.
KING_CARDS = {
    "marvins-metrics": {"rank": "king", "suit": "spades", "symbol": "♠", "title": "King of Spades"},
    "princes-principles": {"rank": "king", "suit": "diamonds", "symbol": "♦", "title": "King of Diamonds"},
    "omos-intel": {"rank": "king", "suit": "clubs", "symbol": "♣", "title": "King of Clubs"},
}
RESERVED_CARDS = (
    {"rank": "king", "suit": "hearts", "symbol": "♥", "title": "King of Hearts",
     "status": "reserved-unassigned", "assigned_participant_id": None},
)

PARTICIPANTS = (
    {
        "id": "omos-intel",
        "name": "Omo's Intel",
        "aliases": ["Omo Intel", "intelTHAT"],
        "source_app": "intelTHAT",
        "source_repository_candidate": "marvelousempire/intelTHAT",
        "status": "adapter-implemented-not-commissioned",
        "description": "Omo's view of existing intelTHAT options, macro, news and SEC research receipts.",
        "evidence_endpoint": "/api/intelthat/{symbol}",
    },
    {
        "id": "princes-principles",
        "name": "Prince's Principles",
        "aliases": [],
        "source_app": None,
        "status": "awaiting-owner-content",
        "description": "Prince's principles and decision rules. No rules have been supplied yet.",
        "evidence_endpoint": None,
    },
    {
        "id": "princes-intel",
        "name": "Prince's Intel",
        "aliases": [],
        "source_app": None,
        "status": "awaiting-owner-content",
        "description": "Prince's market watch items and intelligence. Definitions and evidence still to be supplied.",
        "evidence_endpoint": None,
    },
    {
        "id": "marvins-metrics",
        "name": "Marvin's Metrics",
        "aliases": [],
        "source_app": None,
        "status": "awaiting-owner-content",
        "description": "Marvin's metrics and measures. Definitions and calculations still to be supplied.",
        "evidence_endpoint": None,
    },
)


def participant_directory() -> dict:
    """Return display-only metadata with explicitly bounded permissions."""
    return {
        "schema": "market-compass.participants/v1",
        "commissioned": False,
        "trade_execution": False,
        "score_influence": False,
        "participants": [
            {**item, "card": dict(KING_CARDS[item["id"]]) if item["id"] in KING_CARDS else None}
            for item in PARTICIPANTS
        ],
        "reserved_cards": [dict(card) for card in RESERVED_CARDS],
    }
