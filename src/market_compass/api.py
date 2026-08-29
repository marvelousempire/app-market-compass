from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .backtest import backtest_frame
from .data import get_market_data
from .engine import analyze
from .registry import NODE_REGISTRY, node_output

app = FastAPI(title="Market Compass", version="0.3.0")
WEB_DIR = Path(__file__).with_name("web")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_class=FileResponse)
def home():
    return WEB_DIR / "index.html"


@app.get("/health")
def health():
    return {"status": "ok", "nodes": len(NODE_REGISTRY), "surface": "application-v0.3"}


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
