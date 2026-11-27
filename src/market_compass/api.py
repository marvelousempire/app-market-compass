from __future__ import annotations

import json
import os
import re
import signal
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from threading import Timer
from urllib.error import URLError
from urllib.request import Request as URLRequest, urlopen

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .ai import AnalystRequest, AnalystRouter
from . import alpaca_connect
from .ai.providers import ProviderError
from .asset_channel import read_asset_channel
from .backtest import backtest_frame
from .data import get_market_data, latest_available_bar, search_symbols
from .decision_readiness import calculate_readiness
from .engine import analyze
from .hcck_profiles import ProfiledSimulationRequest, profile_directory, run_profiled_simulation
from .intelthat_bridge import read_snapshot
from .intelthat_native import build_native_workspace
from .pack002 import desk_from_bars
from .registry import NODE_REGISTRY, node_output
from .research_lenses import build_day_trader_lens
from .research_sources import alpaca_latest_trade, alpaca_quote, edgar_filings
from .simulation import SimulationRequest, simulate

app = FastAPI(title="Market Compass", version="0.8.1")
analyst_router = AnalystRouter()
WEB_DIR = Path(__file__).with_name("web")
PREVIEW_STARTED_AT = datetime.now(UTC).isoformat()
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class AlpacaConnectCredentials(BaseModel):
    client_id: str
    client_secret: str


def _local_settings_request(request: Request) -> None:
    origin = request.headers.get("origin", "")
    if request.url.hostname not in {"market-compass.localhost", "127.0.0.1", "localhost"}:
        raise HTTPException(403, "Open the local Market Compass app to change its connection.")
    if origin != f"{request.url.scheme}://{request.headers.get('host', '')}":
        raise HTTPException(403, "Open Market Compass Settings before changing its connection.")


@app.get("/api/alpaca-connect/status")
def alpaca_connect_status():
    return JSONResponse(alpaca_connect.status(), headers={"Cache-Control": "no-store"})


@app.post("/api/alpaca-connect/configure")
def alpaca_connect_configure(credentials: AlpacaConnectCredentials, request: Request):
    _local_settings_request(request)
    try:
        return JSONResponse(alpaca_connect.configure(credentials.client_id, credentials.client_secret),
                            headers={"Cache-Control": "no-store"})
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc


@app.post("/api/alpaca-connect/start")
def alpaca_connect_start(request: Request):
    _local_settings_request(request)
    try:
        return JSONResponse({"url": alpaca_connect.authorization_url()}, headers={"Cache-Control": "no-store"})
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@app.get("/api/alpaca-connect/callback")
def alpaca_connect_callback(code: str = "", state: str = "", error: str = ""):
    if error:
        return RedirectResponse("/?alpaca=declined#market-settings", status_code=303)
    try:
        alpaca_connect.exchange(code, state)
    except Exception:
        return RedirectResponse("/?alpaca=failed#market-settings", status_code=303)
    return RedirectResponse("/?alpaca=connected#market-settings", status_code=303)

SYMBOL_OWNER = "http://act-v5.localhost"
SYMBOL_REVISION = re.compile(r"^[a-f0-9]{40}$")


def _symbol_owner_read(path: str) -> bytes:
    try:
        request = URLRequest(SYMBOL_OWNER + path, headers={"Cache-Control": "no-cache"})
        with urlopen(request, timeout=3) as response:
            return response.read(512_001)
    except (OSError, URLError) as exc:
        raise HTTPException(503, "The shared symbol catalog is unavailable.") from exc


@app.get("/api/ui-symbols/manifest")
def ui_symbol_manifest():
    try:
        manifest = json.loads(_symbol_owner_read("/core/v1/manifest.json"))
        revision = manifest["revision"]
    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(503, "The shared symbol catalog is unavailable.") from exc
    if not isinstance(revision, str) or not SYMBOL_REVISION.fullmatch(revision):
        raise HTTPException(503, "The shared symbol revision is invalid.")
    return JSONResponse({"revision": revision}, headers={"Cache-Control": "no-store"})


@app.get("/api/ui-symbols/r/{revision}/symbols.mjs")
def ui_symbol_module(revision: str):
    if not SYMBOL_REVISION.fullmatch(revision):
        raise HTTPException(404, "Unknown symbol revision.")
    manifest = ui_symbol_manifest().body
    if json.loads(manifest)["revision"] != revision:
        raise HTTPException(409, "The shared symbol revision changed. Reload this page.")
    path = f"/core/v1/r/{revision}/symbols.mjs"
    module = _symbol_owner_read(path)
    if len(module) > 512_000 or b"export const SYMBOL_CORE_REVISION=" not in module[:240]:
        raise HTTPException(503, "The shared symbol module is unavailable.")
    return Response(module, media_type="text/javascript", headers={"Cache-Control": "no-store"})


@app.get("/", response_class=FileResponse)
def home():
    return WEB_DIR / "index.html"


@app.get("/handbook", response_class=RedirectResponse)
@app.get("/handbook/", response_class=RedirectResponse)
def handbook():
    """Open the Market Compass book in its handbookTHAT reader."""
    return RedirectResponse("http://handbookthat.localhost/?handbook=Market%20Compass")


@app.get("/intelthat", response_class=FileResponse)
@app.get("/intelthat/", response_class=FileResponse)
def intelthat_app():
    """Serve the native intelTHAT application; its APIs remain research-only."""
    return WEB_DIR / "intelthat-app.html"


@app.get("/options", response_class=RedirectResponse)
def options_desk():
    """Keep existing bookmarks pointed at the integrated main workspace."""
    return "/#options-lab"


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


@app.get("/api/hcck/profiles")
def hybrid_cck_profiles_api():
    """Draft domain templates; does not issue CCK authorization."""
    return profile_directory()


@app.post("/api/hcck/simulate")
def hybrid_cck_simulation_api(request: ProfiledSimulationRequest):
    return run_profiled_simulation(request)


@app.post("/api/simulate")
def simulate_api(request: SimulationRequest):
    return simulate(request)


@app.get("/api/options-context/{symbol}")
def options_context_api(symbol: str):
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            alpaca_future = pool.submit(alpaca_quote, symbol)
            edgar_future = pool.submit(edgar_filings, symbol)
            return {"alpaca": alpaca_future.result(), "edgar": edgar_future.result()}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/market-price/{symbol}")
def market_price_api(symbol: str):
    """The newest observed price and its actual source time, separate from study bars."""
    try:
        observed = alpaca_latest_trade(symbol)
        if observed["state"] == "observed":
            return JSONResponse(observed, headers={"Cache-Control": "no-store"})
        return JSONResponse(latest_available_bar(symbol), headers={"Cache-Control": "no-store"})
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/asset-channel/{symbol}")
def asset_channel_api(symbol: str):
    try:
        return read_asset_channel(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/intelthat/{symbol}")
def intelthat_api(symbol: str):
    try:
        return read_snapshot(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/intelthat-workspace/{symbol}")
def intelthat_workspace_api(symbol: str):
    """Build the native research workspace; never authenticate a broker or place an order."""
    try:
        return build_native_workspace(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Research sources unavailable: {type(exc).__name__}.") from exc


@app.get("/api/research-lenses/day-trader/{symbol}")
def day_trader_lens_api(symbol: str):
    """Read one source-bound lens; never execute donor or brokerage code."""
    try:
        data = get_market_data(symbol)
        return build_day_trader_lens(symbol, data.bars, data_meta=data.meta)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/uploadthat/imports")
def uploadthat_imports_api(request: Request):
    from .uploadthat_resident import ImportUnavailable, read_imports
    try:
        return JSONResponse(read_imports(request.headers.get('cookie', '')),
                            headers={'Cache-Control': 'no-store'})
    except PermissionError as error:
        raise HTTPException(401, str(error)) from error
    except ImportUnavailable as error:
        raise HTTPException(503, str(error)) from error
