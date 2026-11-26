"""Read-only external context for the Options Lab."""
from __future__ import annotations

import os
from datetime import UTC, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import json

from .intelthat_contract import symbol
from .intelthat_native import _edgar


def alpaca_quote(value: str) -> dict:
    ticker = symbol(value)
    key = os.getenv('MARKET_COMPASS_ALPACA_KEY_ID', '').strip()
    secret = os.getenv('MARKET_COMPASS_ALPACA_SECRET_KEY', '').strip()
    if not key or not secret:
        return {'state': 'held', 'reason': 'Alpaca market-data credentials are not configured.', 'symbol': ticker,
                'requiredSettings': ['MARKET_COMPASS_ALPACA_KEY_ID', 'MARKET_COMPASS_ALPACA_SECRET_KEY']}
    url = f'https://data.alpaca.markets/v2/stocks/{quote(ticker)}/quotes/latest'
    request = Request(url, headers={'APCA-API-KEY-ID': key, 'APCA-API-SECRET-KEY': secret,
                                    'Accept': 'application/json', 'User-Agent': 'MarketCompass/0.8 research-only'})
    try:
        with urlopen(request, timeout=6) as response:
            payload = json.load(response)
        row = payload.get('quote') or {}
        bid, ask = float(row['bp']), float(row['ap'])
        if bid <= 0 or ask <= 0 or ask < bid:
            raise ValueError('Invalid quote spread')
        return {'state': 'observed', 'symbol': ticker, 'bid': bid, 'ask': ask,
                'midpoint': round((bid + ask) / 2, 4), 'asOf': row.get('t'),
                'retrievedAt': datetime.now(UTC).isoformat(), 'sourceUrl': url,
                'reason': 'Latest available stock quote. Data entitlement and feed may limit coverage.'}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return {'state': 'held', 'symbol': ticker, 'reason': f'Alpaca quote unavailable: {type(exc).__name__}.'}


def edgar_filings(value: str) -> dict:
    ticker = symbol(value)
    return _edgar(ticker, datetime.now(UTC).isoformat())
