"""Founder non-subtraction guard: original Market Compass remains usable.

New generic simulations and profile schedules are additive; they must never
silently disable auto-analysis or remove the existing market, indicator,
research, and watchlist controls.  A deliberate product change requires
separate review of these acceptance expectations.
"""
import re
from fastapi.testclient import TestClient
from market_compass.api import app

ORIGINAL_CONTROLS = (
    "symbol", "symbol-suggestions", "horizon", "analyze",
    "watch-current", "save-snapshot", "run-status", "watchlist",
    "snapshot-chips", "error", "workspace", "identity-strip",
    "action-pill", "decision-sentence", "summary-grid", "signal-grid",
    "route-badge", "route", "analyst-lane", "analyst-provider",
    "analyst-depth", "cloud-allowed", "analyst-question", "ask-nephew",
    "analyst-result", "timeframe-consensus", "timeframe-grid",
    "chart-timeframes", "price-chart", "chart-legend", "price-memory",
    "rsi-state", "rsi-chart", "rsi-readout", "macd-state",
    "macd-chart", "macd-readout", "contributions", "calibration",
    "bull-case", "bear-case", "catalyst-timeline", "history-panel",
    "forecast-panel", "evidence-board", "board-detail",
    "narrative-panel", "invalidation", "explorer-content",
)


def test_all_original_market_compass_controls_still_exist():
    client = TestClient(app)
    html = client.get("/").text
    missing = [control for control in ORIGINAL_CONTROLS
               if f'id="{control}"' not in html]
    assert missing == [], "Original Market Compass controls removed: " + repr(missing)
    for asset in ("app.js", "analyst.js", "intelthat.js",
                  "simulator.js", "hcck.js"):
        response = client.get("/static/" + asset)
        assert response.status_code == 200, asset
    assert 'data-view="quick"' in html
    assert 'data-view="research"' in html


def test_market_auto_analysis_is_preserved_even_with_simulation_features():
    client = TestClient(app)
    js = client.get("/static/app.js").text
    assert 'async function runAnalysis()' in js
    assert '/api/analyze?symbol=' in js
    assert re.search(r"document\.addEventListener\('DOMContentLoaded'.*runAnalysis\(\);\}\);\s*$",
                     js, flags=re.DOTALL), "Original automatic analysis has been suppressed"
    assert "get('mode') !== 'simulation'" not in js


def test_omo_readonly_panel_retains_original_research_position():
    client = TestClient(app)
    html = client.get("/").text
    start = html.index('<section class="research-only">')
    omo = html.index('id="intelthat-panel"')
    historical = html.index('id="history-panel"')
    assert start < omo < historical
    assert 'id="intelthat-load"' in html
    assert "Omo's Intel" in html
    assert '/static/hcck.js' in html
    assert 'id="hcck-profile-select"' in html
    assert 'id="universal-run"' in html
