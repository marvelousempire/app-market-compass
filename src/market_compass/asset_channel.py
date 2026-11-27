"""Read-only, symbol-scoped editorial channel for Market Compass."""
from __future__ import annotations

import re
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
    filings = edgar_filings(resolved)
    financial_reports = [row for row in filings.get("inputs", {}).get("filings", [])
                         if row.get("form") in {"10-Q", "10-K", "20-F", "40-F"}
                         or "2.02" in (row.get("items") or "")]
    issuer_word = company.split()[0].casefold()
    earnings = [row for row in articles if
                (re.search(r"(?<![A-Za-z])" + re.escape(ticker) + r"(?![A-Za-z])", row["title"], re.I)
                 or (len(issuer_word) > 2 and issuer_word in row["title"].casefold()))
                and any(word in row["title"].lower()
                for word in ("earnings", "quarterly results", "financial results"))]
    recent_events = []
    for row in articles:
        try:
            published = datetime.fromisoformat(str(row.get("published")))
            age = (datetime.now(UTC) - published).total_seconds() / 86400
        except (ValueError, TypeError):
            continue
        matches = [word for word in ("acquisition", "merger", "investigation", "lawsuit", "guidance",
                   "buyback", "contract", "patent", "restructuring", "bankruptcy", "approval")
                   if word in row["title"].lower()]
        if 0 <= age <= 30 and matches:
            recent_events.append({**row, "reason": "Headline mentions " + ", ".join(matches),
                                  "assessment": "Candidate for review; significance and attention are unverified."})
    return {"symbol": resolved, "company": company, "retrieved_at": datetime.now(UTC).isoformat(),
            "source": "Yahoo Finance search", "items": articles, "filings": filings,
            "earnings": {"releases": earnings, "financial_reports": financial_reports,
                         "next_date": None, "calendar_state": "unavailable",
                         "reason": "No verified future earnings calendar is connected."},
            "recent_events": recent_events,
            "audio_available": False, "trade_execution": False}
