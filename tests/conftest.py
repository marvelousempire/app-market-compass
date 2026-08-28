import numpy as np
import pandas as pd
import pytest

from market_compass.data import MarketData


@pytest.fixture
def sample_data():
    n = 520
    idx = pd.date_range("2024-01-01", periods=n, freq="D", tz="UTC")
    rng = np.random.default_rng(7)
    drift = np.linspace(100, 150, n)
    wave = np.sin(np.arange(n) / 11) * 4
    close = drift + wave + rng.normal(0, .7, n)
    df = pd.DataFrame({
        "open": close + rng.normal(0, .5, n),
        "high": close + rng.uniform(.5, 2, n),
        "low": close - rng.uniform(.5, 2, n),
        "close": close,
        "volume": rng.integers(500_000, 2_000_000, n),
    }, index=idx)
    news = [
        {"title": "Acme AI Partnership Drives Growth", "publisher": "Example", "published": idx[-1].isoformat(), "url": ""},
        {"title": "Regulation Risk Remains for Crypto Market", "publisher": "Example", "published": idx[-2].isoformat(), "url": ""},
    ]
    return MarketData(df, {"quoteType": "EQUITY", "marketCap": 1_000_000_000}, news, {"provider": "test"})
