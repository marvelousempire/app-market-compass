"""READYPLAY-inspired, finance-native Market Studio room registry.

A study room is a navigation/capability contract, NOT an imported sports rating.
The catalog never claims outside feeds or live commissioning. Consumers must
respect source ownership, provenance, and read-only research boundaries.
"""
from __future__ import annotations

SOURCE = "marvelousempire/red-e-play-app"
SOURCE_GUIDE = "docs/plans/Plan-Player-Market-Studio-Hub.md"

ROOMS = (
    {"id": "pulse", "name": "Market Pulse", "description": "Read price state, evidence balance and confidence.", "target": "summary-grid", "state": "mapped-existing", "source": "Market Compass analysis"},
    {"id": "chart", "name": "Chart & Indicator Lab", "description": "Candles, EMA, RSI, MACD and Fibonacci studies.", "target": "price-chart", "state": "mapped-existing", "source": "Market Compass technical series"},
    {"id": "translation", "name": "Research Translation", "description": "Inspect Omo's Intel receipts. Automatic publication and cross-engine promotion are not enabled.", "target": "intelthat-panel", "state": "partial-read-only", "source": "intelTHAT local published receipts"},
    {"id": "levels", "name": "Levels & Signals", "description": "Price memory, support, resistance, invalidation and route stops.", "target": "price-memory", "state": "mapped-existing", "source": "Market Compass route and memory"},
    {"id": "context", "name": "Timeframe & Context", "description": "Inspect 4H/1D/1W context; missing timeframes remain unavailable.", "target": "timeframe-grid", "state": "mapped-existing", "source": "Market Compass timeframe availability"},
    {"id": "scenarios", "name": "Scenario Desk", "description": "Forecast and historical analog studies, not options orders or future guarantees.", "target": "forecast-panel", "state": "mapped-existing", "source": "Market Compass historical forecast"},
    {"id": "proof", "name": "Proof Health", "description": "Inspect missing source evidence and existing read-only receipt checks.", "target": "intelthat-panel", "state": "partial-read-only", "source": "intelTHAT observed/held/excluded/missing states"},
    {"id": "my-desk", "name": "My Market Desk", "description": "Local watchlist and analysis snapshots. No server sync or trade execution.", "target": "watchlist", "state": "mapped-existing", "source": "Browser-local Market Compass storage"},
    {"id": "method", "name": "Method & Safety", "description": "Inspect calculations, evidence limitations, source identities and refusal gates.", "target": "invalidation", "state": "mapped-existing", "source": "Market Compass uncertainty and source checks"},
    {"id": "newsroom", "name": "Market Newsroom", "description": "Source-timestamped catalysts when available; not a complete events calendar.", "target": "catalyst-timeline", "state": "mapped-existing", "source": "Market Compass news layer"},
)
BOOKS = (
    {"id": "trend-book", "name": "Trend Book", "layer_keys": ["trend", "momentum"], "meaning": "Technical trend and momentum (not player offense)."},
    {"id": "risk-book", "name": "Risk Book", "layer_keys": ["route", "memory"], "meaning": "Routes, invalidation and price-memory risks (not player defense)."},
    {"id": "evidence-book", "name": "Evidence Book", "layer_keys": ["foundation", "news", "history", "relationships", "narrative"], "meaning": "Independent input context; no official rating or financial permission."},
)


def studio_registry() -> dict:
    return {
        "schema": "market-compass.studio-rooms/v1",
        "pattern_origin": SOURCE,
        "pattern_reference": SOURCE_GUIDE,
        "source_policy": "adapt-patterns-do-not-copy-sports-facts",
        "market_compass_owns_financial_analysis": True,
        "readyplay_owns_player_data": True,
        "score_influence": False,
        "trade_execution": False,
        "commissioned": False,
        "rooms": [dict(room) for room in ROOMS],
        "books": [dict(book) for book in BOOKS],
    }
