"""Read-only, symbol-scoped editorial channel for Market Compass."""
from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import urlparse

from .data import _search_symbol
from .intelthat_contract import symbol
from .research_sources import edgar_filings


def read_asset_channel(value: str) -> dict:
    ticker = symbol(value)
    quote, news, _ = _search_symbol(ticker, news_count=30)
    resolved = ticker
    company = str(quote.get("longname") or quote.get("shortname") or ticker) if str(quote.get("symbol") or "").upper() == ticker else ticker
    seen: set[str] = set()
    articles = []
    for item in news:
        related = {str(part).upper() for part in item.get("related_symbols") or []}
        address = str(item.get("url") or "")
        title = str(item.get("title") or "").strip()
        parsed = urlparse(address)
        if resolved not in related or not title or parsed.scheme != "https" or not parsed.netloc or address in seen:
            continue
        seen.add(address)
        kind = "video" if str(item.get("media_type") or "").upper() == "VIDEO" else "article"
        articles.append({"title": title[:300], "publisher": str(item.get("publisher") or "Publisher unavailable")[:100],
                         "url": address, "published": item.get("published"), "kind": kind})
    return {"symbol": resolved, "company": company, "retrieved_at": datetime.now(UTC).isoformat(),
            "source": "Yahoo Finance search", "items": articles, "filings": edgar_filings(resolved),
            "audio_available": False, "trade_execution": False}
