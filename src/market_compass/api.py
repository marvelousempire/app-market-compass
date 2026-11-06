from __future__ import annotations

import json
import os
import signal
import socket
from datetime import UTC, datetime
from pathlib import Path
from threading import Timer
from urllib.error import URLError

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .ai import AnalystRequest, AnalystRouter
from .ai.providers import ProviderError
from .backtest import backtest_frame
from .data import get_market_data, search_symbols
from .decision_readiness import calculate_readiness
from .engine import analyze
from .intelthat_bridge import read_snapshot
from .pack002 import desk_from_bars
from .registry import NODE_REGISTRY, node_output
from .research_lenses import build_day_trader_lens

app = FastAPI(title="Market Compass", version="0.7.0")
analyst_router = AnalystRouter()
WEB_DIR = Path(__file__).with_name("web")
PREVIEW_STARTED_AT = datetime.now(UTC).isoformat()
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
        "pack_002": True,
        "analyst": analyst_router.health()["status"],
    }


def operator_status():
    commissioned = os.getenv("MARKET_COMPASS_COMMISSIONED", "false").lower() == "true"
    return {
        "state": "live", "host": socket.gethostname(), "pid": os.getpid(),
        "started_at": PREVIEW_STARTED_AT,
        "bind": os.getenv("MARKET_COMPASS_BIND", "127.0.0.1:8000"),
        "mode": "research_only", "preview_only": not commissioned, "commissioned": commissioned,
        "trade_execution": False, "signal_generation": True, "score_influence": False,
        "authority": os.getenv("MARKET_COMPASS_AUTHORITY", "github-preview-unverified"),
        "source_revision": os.getenv("MARKET_COMPASS_SOURCE_REVISION", "unverified"),
    }


@app.get("/api/operator/plan")
def operator_plan():
    return {
        "job": "market-first-look", "state": "ready",
        "steps": [
            "Verify the pinned preview source and local runtime.",
            "Open Market Compass with intelTHAT receipts in read-only mode.",
            "Keep missing evidence visible and keep trading disabled.",
        ],
        "prohibits": ["broker-order", "git-merge", "git-push", "gitea-authority-cutover"],
        "launch_owner": "GitThat",
    }


@app.get("/api/operator/status")
def operator_status_api():
    return operator_status()


@app.post("/api/operator/launch")
def operator_launch_api():
    return {**operator_status(), "result": "already-running", "message": "The preview is live and ready."}


@app.get("/api/operator/receipts")
def operator_receipts(symbol: str = Query("QQQ", min_length=1, max_length=24)):
    return {"runtime": operator_status(), "health": health(), "research": read_snapshot(symbol)}


def _stop_preview():
    os.kill(os.getpid(), signal.SIGTERM)


@app.post("/api/operator/stop")
def operator_stop_api():
    Timer(0.35, _stop_preview).start()
    return {
        "state": "stopping",
        "message": "The local preview is stopping. Run GitThat again to relaunch it.",
        "trade_execution": False,
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


@app.get("/api/decision-readiness")
def decision_readiness_api(symbol: str = Query(min_length=1), horizon: int = Query(20, ge=1, le=120)):
    try:
        return calculate_readiness(analyze(symbol, horizon))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/desk")
def desk_api(symbol: str = Query(min_length=1)):
    try:
        data = get_market_data(symbol)
        return desk_from_bars(symbol, data.bars)
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


@app.get("/api/intelthat/{symbol}")
def intelthat_api(symbol: str):
    try:
        return read_snapshot(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/research-lenses/day-trader/{symbol}")
def day_trader_lens_api(symbol: str):
    """Read one source-bound lens; never execute donor or brokerage code."""
    try:
        data = get_market_data(symbol)
        return build_day_trader_lens(symbol, data.bars, data_meta=data.meta)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
