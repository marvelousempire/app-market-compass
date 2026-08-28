from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import pandas as pd

UA = "Mozilla/5.0 MarketCompass/0.1"


@dataclass
class MarketData:
    bars: pd.DataFrame
    quote: dict
    news: list[dict]
    meta: dict


def _get_json(url: str, timeout: int = 12) -> dict:
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as r:  # noqa: S310 - fixed public HTTPS endpoint
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


def yahoo_market_data(symbol: str, range_: str = "5y", interval: str = "1d") -> MarketData:
    # Resolve first because Yahoo occasionally uses an internal suffix (for example HYPE32196-USD).
    query = quote(symbol, safe="")
    search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=8&newsCount=20"
    try:
        search = _get_json(search_url)
    except Exception:
        search = {}
    quotes = search.get("quotes") or []
    selected = _choose_quote(symbol, quotes)
    resolved = selected.get("symbol") or symbol
    safe = quote(resolved, safe="")
    chart_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{safe}?range={range_}&interval={interval}&events=div%2Csplits"
    payload = _get_json(chart_url).get("chart", {})
    results = payload.get("result") or []
    if not results:
        raise ValueError(payload.get("error", {}).get("description") or f"No market data found for {symbol}")
    chart = results[0]
    timestamps = chart.get("timestamp") or []
    q = (chart.get("indicators", {}).get("quote") or [{}])[0]
    rows = {
        "open": q.get("open", []), "high": q.get("high", []), "low": q.get("low", []),
        "close": q.get("close", []), "volume": q.get("volume", []),
    }
    df = pd.DataFrame(rows, index=pd.to_datetime(timestamps, unit="s", utc=True))
    df = _normalize_bars(df)
    news = []
    for item in search.get("news") or []:
        ts = item.get("providerPublishTime")
        news.append({
            "title": item.get("title", ""),
            "publisher": item.get("publisher", ""),
            "url": item.get("link", ""),
            "published": datetime.fromtimestamp(ts, timezone.utc).isoformat() if ts else None,
        })
    meta = chart.get("meta", {}) | {
        "provider": "yahoo", "requested_symbol": symbol, "resolved_symbol": resolved,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
    return MarketData(df, selected, news, meta)


def get_market_data(symbol: str, csv_path: str | None = None) -> MarketData:
    return load_csv(csv_path) if csv_path else yahoo_market_data(symbol)
