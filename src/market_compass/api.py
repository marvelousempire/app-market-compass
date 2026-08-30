from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .ai import AnalystRequest, AnalystRouter
from .ai.providers import ProviderError
from .backtest import backtest_frame
from .data import get_market_data, search_symbols
from .engine import analyze
from .registry import NODE_REGISTRY, node_output

app = FastAPI(title="Market Compass", version="0.5.0")
analyst_router = AnalystRouter()
WEB_DIR = Path(__file__).with_name("web")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_class=FileResponse)
def home():
    return WEB_DIR / "index.html"


@app.get("/health")
def health():
    return {
        "status": "ok",
        "nodes": len(NODE_REGISTRY),
        "surface": "application-v0.5",
        "analyst": analyst_router.health()["status"],
    }


@app.get("/api/symbols")
def symbols(q: str = Query(min_length=1, max_length=40), limit: int = Query(8, ge=1, le=20)):
    try:
        return search_symbols(q, limit)
    except (OSError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/analyst/health")
def analyst_health():
    return analyst_router.health()


@app.get("/api/analyst/providers")
def analyst_providers():
    return [x.model_dump(mode="json") for x in analyst_router.statuses()]


@app.post("/api/analyst")
def analyst(request: AnalystRequest):
    try:
        return analyst_router.analyze(request).model_dump(mode="json")
    except ProviderError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/analyze")
def analyze_api(symbol: str = Query(min_length=1), horizon: int = Query(20, ge=1, le=120)):
    try:
        return analyze(symbol, horizon).model_dump(mode="json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/nodes")
def nodes():
    return NODE_REGISTRY


@app.get("/api/nodes/{node_id}")
def run_node_api(node_id: str, symbol: str, horizon: int = 20):
    try:
        return node_output(analyze(symbol, horizon), node_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/backtest")
def backtest_api(
    symbol: str = Query(min_length=1),
    horizon: int = Query(20, ge=1, le=120),
    fee_bps: float = Query(10.0, ge=0, le=1000),
):
    try:
        data = get_market_data(symbol)
        result = backtest_frame(data.bars, horizon=horizon, fee_bps=fee_bps)
        return {"symbol": symbol.upper(), "provider": data.meta.get("provider"), "resolved_symbol": data.meta.get("resolved_symbol", symbol.upper()), **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
