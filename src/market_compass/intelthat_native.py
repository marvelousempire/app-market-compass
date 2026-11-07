"""Native research-only intelTHAT workspace built from Market Compass sources."""

from __future__ import annotations

import os
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from urllib.parse import quote

import numpy as np

from .data import MarketData, _get_json, _search_symbol, direct_market_data
from .engine import analyze_frame
from .intelthat_contract import KINDS, evidence, symbol, workspace

_BULL = ("beat", "growth", "rally", "gain", "upgrade", "record high", "rate cut", "dovish")
_BEAR = ("miss", "decline", "selloff", "downgrade", "layoff", "recession", "rate hike", "hawkish")
_RISK = ("fed", "inflation", "tariff", "sanction", "lawsuit", "investigation", "earnings")


def native_market_data(symbol_value: str) -> MarketData:
    """Fetch bars and headlines concurrently without turning name search into a serial gate."""
    with ThreadPoolExecutor(max_workers=2) as pool:
        bars_future = pool.submit(direct_market_data, symbol_value, "5y", "1d")
        news_future = pool.submit(_search_symbol, symbol_value)
        bars = bars_future.result()
        try:
            selected, news, _ = news_future.result()
        except (OSError, ValueError, KeyError, TypeError, IndexError, TimeoutError):
            selected, news = bars.quote, []
    return MarketData(bars.bars, selected or bars.quote, news, bars.meta)


def _freshness(data: MarketData, retrieved: str) -> tuple[str, str]:
    last = data.bars.index[-1].to_pydatetime().astimezone(UTC)
    age = datetime.fromisoformat(retrieved) - last
    return last.isoformat(), "current" if age.days <= 4 else "held-stale"


def _pack(symbol_value: str, data: MarketData, retrieved: str, options: dict) -> dict:
    frames = {"1d": data.bars, "1w": data.bars.resample("W-FRI").agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
    }).dropna(subset=["close"])}
    report = analyze_frame(symbol_value, data, timeframe_frames=frames)
    momentum = report.layers["momentum"].metrics
    trend = report.layers["trend"].metrics
    as_of, freshness = _freshness(data, retrieved)
    state = "observed" if freshness == "current" else "held"
    inputs = {
        "price": report.price,
        "bars": len(data.bars),
        "interval": data.meta.get("interval", "1d"),
        "ema13": trend.get("ema13"),
        "ema27": trend.get("ema27"),
        "ema81": trend.get("ema81"),
        "rsi14": momentum.get("rsi14"),
        "macd": momentum.get("macd"),
        "macd_signal": momentum.get("macd_signal"),
        "options": options.get("inputs", {}),
    }
    option_state = options.get("state", "held")
    return evidence(
        "pack", state=state,
        reason=("Native price and technical research is current; options context is " + option_state +
                ". No execution readiness is claimed.") if state == "observed" else "Market bars are stale.",
        as_of=as_of, timeframe="1d with 1w context", inputs=inputs,
        formula="Wilder RSI(14); EMA(13,27,81); MACD(12,26,9); put/call OI ratio = total put OI / max(total call OI, 1)",
        metrics={"price": report.price, "action": report.action, "rsi14": momentum.get("rsi14"),
                 "trend": report.layers["trend"].state, "momentum": report.layers["momentum"].state,
                 "timeframeAgreement": report.timeframes.get("consensus", {}).get("agreement"),
                 **options.get("metrics", {})},
        confidence=report.confidence,
        source_urls=["https://query1.finance.yahoo.com/", options.get("source_url")],
        retrieved_at=retrieved, freshness=freshness,
    )


def _options(symbol_value: str, retrieved: str, getter: Callable[..., dict]) -> dict:
    url = f"https://query2.finance.yahoo.com/v7/finance/options/{quote(symbol_value)}"
    try:
        payload = getter(url, timeout=7)
        results = payload.get("optionChain", {}).get("result", [])
        chain = (results[0].get("options") or [{}])[0] if results else {}
        calls = chain.get("calls") or []
        puts = chain.get("puts") or []
        call_oi = sum(int(row.get("openInterest") or 0) for row in calls)
        put_oi = sum(int(row.get("openInterest") or 0) for row in puts)
        call_volume = sum(int(row.get("volume") or 0) for row in calls)
        put_volume = sum(int(row.get("volume") or 0) for row in puts)
        if not calls and not puts:
            raise ValueError("No chain rows returned.")
        return {
            "state": "observed",
            "inputs": {"callContracts": len(calls), "putContracts": len(puts),
                       "callOpenInterest": call_oi, "putOpenInterest": put_oi,
                       "callVolume": call_volume, "putVolume": put_volume},
            "metrics": {"optionsState": "observed", "callContracts": len(calls),
                        "putContracts": len(puts), "putCallOIRatio": round(put_oi / max(call_oi, 1), 3),
                        "putCallVolumeRatio": round(put_volume / max(call_volume, 1), 3)},
            "source_url": url, "retrieved_at": retrieved,
        }
    except (OSError, ValueError, KeyError, TypeError, IndexError, TimeoutError) as exc:
        return {"state": "held", "inputs": {},
                "metrics": {"optionsState": "held", "optionsReason": type(exc).__name__},
                "source_url": url, "retrieved_at": retrieved}


def _macro(fetcher: Callable[[str], MarketData], retrieved: str) -> dict:
    observations: dict[str, float] = {}
    urls: list[str] = []
    failures: list[str] = []
    pairs = (("^VIX", "vix5dPct"), ("^TNX", "tenYearYield5dPct"),
             ("UUP", "dollar5dPct"), ("TLT", "longBond5dPct"))

    def read(pair):
        ticker, label = pair
        try:
            data = fetcher(ticker)
            close = data.bars.close.dropna()
            return label, round(float((close.iloc[-1] / close.iloc[-6] - 1) * 100), 3), None
        except (OSError, ValueError, KeyError, TypeError, IndexError, TimeoutError):
            return label, None, ticker

    with ThreadPoolExecutor(max_workers=4) as pool:
        for label, measured, failure in pool.map(read, pairs):
            if failure:
                failures.append(failure)
            else:
                observations[label] = measured
                urls.append("https://query1.finance.yahoo.com/")
    if len(observations) < 2:
        return evidence("macro", state="held", reason="Fewer than two macro proxies were readable.",
                        as_of=retrieved, timeframe="5 trading days", inputs=observations,
                        formula="No macro posture emitted unless at least two independent proxies are readable.",
                        metrics={"readableProxies": len(observations), "failedProxies": failures}, confidence=0,
                        source_urls=urls, retrieved_at=retrieved, freshness="unavailable")
    risk_pressure = observations.get("vix5dPct", 0) + observations.get("tenYearYield5dPct", 0)
    relief = observations.get("longBond5dPct", 0) - observations.get("dollar5dPct", 0)
    score = round(float(np.tanh((relief - risk_pressure) / 20)), 3)
    return evidence("macro", state="observed", reason="Public macro proxies were measured; this is context, not a forecast.",
                    as_of=retrieved, timeframe="5 trading days", inputs=observations,
                    formula="tanh(((TLT 5d% - UUP 5d%) - (VIX 5d% + ^TNX 5d%)) / 20)",
                    metrics={"macroContext": score, "direction": "supportive" if score > .15 else "restrictive" if score < -.15 else "mixed", "failedProxies": failures},
                    confidence=min(1, len(observations) / 4), source_urls=sorted(set(urls)),
                    retrieved_at=retrieved, freshness="current")


def _rss(data: MarketData, retrieved: str) -> dict:
    rows = data.news[:20]
    if not rows:
        return evidence("rss", state="missing", reason="The selected source returned no current headlines.",
                        as_of=None, timeframe="36 hours preferred", inputs={"headlines": []},
                        formula="No headline score without headlines.", metrics={}, confidence=0,
                        source_urls=[], retrieved_at=retrieved, freshness="missing")
    bull = bear = 0
    risk_flags: set[str] = set()
    publishers: set[str] = set()
    latest = None
    safe_rows = []
    for row in rows:
        title = str(row.get("title") or "")[:240]
        text = title.lower()
        bull += sum(token in text for token in _BULL)
        bear += sum(token in text for token in _BEAR)
        risk_flags.update(token for token in _RISK if token in text)
        publishers.add(str(row.get("publisher") or "unknown")[:80])
        published = row.get("published")
        latest = max(latest, published) if latest and published else published or latest
        safe_rows.append({"title": title, "publisher": str(row.get("publisher") or "")[:80], "published": published, "url": row.get("url")})
    total = bull + bear
    score = round((bull - bear) / max(total, 1), 3)
    confidence = min(1, len(rows) / 12) * min(1, len(publishers) / 3)
    return evidence("rss", state="observed", reason="Current headlines were measured with a disclosed lexical lens; source truth is not independently verified.",
                    as_of=latest or retrieved, timeframe="latest 20 provider headlines", inputs={"headlines": safe_rows},
                    formula="(bullish keyword hits - bearish keyword hits) / max(all directional hits, 1)",
                    metrics={"headlineCount": len(rows), "publisherCount": len(publishers), "score": score,
                             "direction": "bullish" if score > .15 else "bearish" if score < -.15 else "mixed", "riskFlags": sorted(risk_flags)},
                    confidence=confidence, source_urls=sorted({str(row.get("url")) for row in rows if row.get("url")}),
                    retrieved_at=retrieved, freshness="current")


def _edgar(symbol_value: str, retrieved: str, getter: Callable[..., dict] = _get_json) -> dict:
    contact = os.getenv("MARKET_COMPASS_SEC_CONTACT", "").strip()
    if not contact or "@" not in contact:
        return evidence("edgar", state="held", reason="SEC fair-access contact is not configured; no EDGAR request was sent.",
                        as_of=None, timeframe="latest company submissions", inputs={"symbol": symbol_value},
                        formula="Resolve ticker to CIK, then count recent 8-K, 10-K, 10-Q, 4 and 13D filings.",
                        metrics={"requiredSetting": "MARKET_COMPASS_SEC_CONTACT"}, confidence=0,
                        source_urls=["https://www.sec.gov/os/accessing-edgar-data"], retrieved_at=retrieved,
                        freshness="held-policy")
    try:
        user_agent = f"MarketCompass/0.8 research-only ({contact})"
        ticker_map = getter("https://www.sec.gov/files/company_tickers.json", timeout=6,
                            user_agent=user_agent)
        row = next((x for x in ticker_map.values() if str(x.get("ticker", "")).upper() == symbol_value), None)
        if not row:
            raise ValueError("Ticker is absent from the SEC company map.")
        cik = str(row["cik_str"]).zfill(10)
        filings = getter(f"https://data.sec.gov/submissions/CIK{quote(cik)}.json", timeout=6,
                         user_agent=user_agent)
        recent = filings.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        wanted = {"8-K", "10-K", "10-Q", "4", "SC 13D", "SC 13G"}
        selected = [{"form": form, "filed": dates[i] if i < len(dates) else None}
                    for i, form in enumerate(forms) if form in wanted][:25]
        latest = selected[0]["filed"] if selected else None
        counts = {form: sum(x["form"] == form for x in selected) for form in sorted(wanted)}
        return evidence("edgar", state="observed", reason="SEC company submissions were read under the configured fair-access identity.",
                        as_of=latest, timeframe="latest 25 high-signal filings", inputs={"symbol": symbol_value, "cik": cik, "filings": selected},
                        formula="Count the latest admitted 8-K, 10-K, 10-Q, Form 4, Schedule 13D and 13G filings.",
                        metrics={"filingCount": len(selected), "formCounts": counts, "cik": cik},
                        confidence=1 if selected else .5, source_urls=["https://www.sec.gov/files/company_tickers.json", f"https://data.sec.gov/submissions/CIK{cik}.json"],
                        retrieved_at=retrieved, freshness="current" if selected else "no-recent-admitted-forms")
    except (OSError, ValueError, KeyError, TypeError, IndexError, TimeoutError) as exc:
        return evidence("edgar", state="held", reason=f"EDGAR evidence unavailable: {type(exc).__name__}.",
                        as_of=None, timeframe="latest company submissions", inputs={"symbol": symbol_value},
                        formula="No filing metric is emitted after a source or parse failure.", metrics={}, confidence=0,
                        source_urls=["https://www.sec.gov/files/company_tickers.json"], retrieved_at=retrieved, freshness="unavailable")


def _unavailable(kind: str, retrieved: str, failure: str) -> dict:
    return evidence(kind, state="held", reason=f"Live source unavailable: {failure}.", as_of=None,
                    timeframe="source-dependent", inputs={},
                    formula="No metric is emitted when required source evidence is unavailable.",
                    metrics={}, confidence=0, source_urls=[], retrieved_at=retrieved,
                    freshness="unavailable")


def build_native_workspace(
    symbol_value: str,
    *,
    market_fetcher: Callable[[str], MarketData] = native_market_data,
    edgar_getter: Callable[..., dict] = _get_json,
    options_getter: Callable[..., dict] = _get_json,
) -> dict:
    selected = symbol(symbol_value)
    retrieved = datetime.now(UTC).isoformat()
    macro_fetcher = direct_market_data if market_fetcher is native_market_data else market_fetcher
    with ThreadPoolExecutor(max_workers=4) as pool:
        data_future = pool.submit(market_fetcher, selected)
        macro_future = pool.submit(_macro, macro_fetcher, retrieved)
        edgar_future = pool.submit(_edgar, selected, retrieved, edgar_getter)
        options_future = pool.submit(_options, selected, retrieved, options_getter)
        try:
            data = data_future.result()
            data_failure = None
        except (OSError, ValueError, KeyError, TypeError, IndexError, TimeoutError) as exc:
            data = None
            data_failure = type(exc).__name__
        macro = macro_future.result()
        edgar = edgar_future.result()
        options = options_future.result()
    items = {
        "pack": _pack(selected, data, retrieved, options) if data is not None else _unavailable("pack", retrieved, data_failure),
        "macro": macro,
        "rss": _rss(data, retrieved) if data is not None else _unavailable("rss", retrieved, data_failure),
        "edgar": edgar,
    }
    assert tuple(items) == KINDS
    return workspace(selected, items, as_of=retrieved)
