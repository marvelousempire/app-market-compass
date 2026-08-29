from __future__ import annotations

import json
import ssl
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

import certifi
import pandas as pd

UA = "Mozilla/5.0 MarketCompass/0.3"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


@dataclass
class MarketData:
    bars: pd.DataFrame
    quote: dict
    news: list[dict]
    meta: dict


def _get_json(url: str, timeout: int = 12) -> dict:
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urlopen(req, timeout=timeout, context=SSL_CONTEXT) as r:
        return json.loads(r.read().decode("utf-8"))


def _normalize_bars(df: pd.DataFrame) -> pd.DataFrame:
    rename = {c: c.lower().replace("adj close", "close") for c in df.columns}
    df = df.rename(columns=rename)
    needed = ["open", "high", "low", "close", "volume"]
    missing = [c for c in needed if c not in df]
    if missing:
        raise ValueError(f"Market data missing columns: {missing}")
    df = df[needed].apply(pd.to_numeric, errors="coerce").dropna(subset=["close"])
    df.index = pd.to_datetime(df.index, utc=True)
    return df.sort_index()


def _resample_bars(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    return _normalize_bars(df.resample(rule).agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
    }).dropna(subset=["close"]))


def load_csv(path: str | Path) -> MarketData:
    raw = pd.read_csv(path)
    date_col = next((c for c in raw.columns if c.lower() in {"date", "datetime", "timestamp"}), None)
    if not date_col:
        raise ValueError("CSV needs a date, datetime, or timestamp column")
    raw = raw.set_index(date_col)
    return MarketData(_normalize_bars(raw), {}, [], {"provider": "csv", "path": str(path)})


def _choose_quote(symbol: str, quotes: list[dict]) -> dict:
    wanted = symbol.upper()
    exact = next((x for x in quotes if x.get("symbol", "").upper() == wanted), None)
    if exact:
        return exact
    root = wanted.split("-")[0]
    related = [x for x in quotes if x.get("symbol", "").upper().startswith(root)]
    return related[0] if related else (quotes[0] if quotes else {})


def _search_symbol(symbol: str, news_count: int = 20) -> tuple[dict, list[dict], list[dict]]:
    query = quote(symbol, safe="")
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=8&newsCount={news_count}"
    try:
        search = _get_json(url)
    except (OSError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        search = {}
    quotes = search.get("quotes") or []
    selected = _choose_quote(symbol, quotes)
    news: list[dict] = []
    for item in search.get("news") or []:
        ts = item.get("providerPublishTime")
        news.append({
            "title": item.get("title", ""),
            "publisher": item.get("publisher", ""),
            "url": item.get("link", ""),
            "published": datetime.fromtimestamp(ts, UTC).isoformat() if ts else None,
        })
    return selected, news, quotes


def search_symbols(query: str, limit: int = 8) -> list[dict]:
    """Return provider symbols for a friendly ticker fragment such as HYPE or BTC."""
    value = query.strip().upper()
    if not value:
        return []
    encoded = quote(value, safe="")
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={encoded}&quotesCount={limit}&newsCount=0"
    payload = _get_json(url)
    results = []
    for item in payload.get("quotes") or []:
        symbol = str(item.get("symbol") or "").upper()
        if not symbol:
            continue
        results.append({
            "input": value,
            "symbol": symbol,
            "display_symbol": symbol.removesuffix("-USD"),
            "name": item.get("longname") or item.get("shortname") or symbol,
            "type": item.get("quoteType") or item.get("typeDisp") or "asset",
            "exchange": item.get("exchange") or item.get("exchDisp") or "",
        })
    return results[:limit]


def _chart_bars(resolved: str, range_: str, interval: str) -> tuple[pd.DataFrame, dict]:
    safe = quote(resolved, safe="")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{safe}?range={range_}&interval={interval}&events=div%2Csplits"
    payload = _get_json(url).get("chart", {})
    results = payload.get("result") or []
    if not results:
        raise ValueError(payload.get("error", {}).get("description") or f"No market data found for {resolved}")
    chart = results[0]
    timestamps = chart.get("timestamp") or []
    q = (chart.get("indicators", {}).get("quote") or [{}])[0]
    rows = {
        "open": q.get("open", []), "high": q.get("high", []), "low": q.get("low", []),
        "close": q.get("close", []), "volume": q.get("volume", []),
    }
    return _normalize_bars(pd.DataFrame(rows, index=pd.to_datetime(timestamps, unit="s", utc=True))), chart.get("meta", {})


def yahoo_market_data(symbol: str, range_: str = "5y", interval: str = "1d") -> MarketData:
    selected, news, _ = _search_symbol(symbol)
    resolved = selected.get("symbol") or symbol
    df, meta = _chart_bars(resolved, range_, interval)
    meta = meta | {
        "provider": "yahoo", "requested_symbol": symbol, "resolved_symbol": resolved,
        "retrieved_at": datetime.now(UTC).isoformat(), "interval": interval,
        "quote": selected, "bars": len(df),
    }
    return MarketData(df, selected, news, meta)


def get_market_data(symbol: str, csv_path: str | None = None) -> MarketData:
    return load_csv(csv_path) if csv_path else yahoo_market_data(symbol)


def get_timeframe_bars(symbol: str, daily: MarketData) -> dict[str, pd.DataFrame]:
    """Best-effort 4H / 1D / 1W frames. Failure of intraday data never blocks daily analysis."""
    frames = {"1d": daily.bars}
    frames["1w"] = _resample_bars(daily.bars, "W-FRI")
    if daily.meta.get("provider") != "yahoo":
        return frames
    resolved = daily.meta.get("resolved_symbol") or symbol
    try:
        hourly, _ = _chart_bars(resolved, "6mo", "1h")
        four_hour = _resample_bars(hourly, "4h")
        if len(four_hour) >= 90:
            frames["4h"] = four_hour
    except (OSError, URLError, TimeoutError, ValueError, KeyError, TypeError):
        return frames
    return frames
