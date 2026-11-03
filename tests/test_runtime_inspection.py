"""Keep the live-server inspection receipt honest, additive and local-only."""
import json

import pytest
from fastapi.testclient import TestClient
from market_compass.api import app
from market_compass.runtime_inspection import inspect_runtime, save_receipt


def _served(path: str) -> bytes:
    response = TestClient(app).get(path)
    assert response.status_code == 200, path
    return response.content


def test_runtime_inspection_matches_current_market_and_hcck_routes(tmp_path):
    evidence = inspect_runtime(
        "http://127.0.0.1:18340", fetch=_served, source_commit="fixture-commit"
    )
    assert evidence["status"] == "http-contract-passed"
    assert evidence["http_contract_verified"] is True
    assert evidence["failed_checks"] == []
    assert all(evidence["checks"].values())
    assert len(evidence["response_sha256"]) == 7
    assert evidence["source_commit"] == "fixture-commit"
    for key in (
        "browser_render_verified", "live_market_feed_verified",
        "cck_certified", "readyplay_connected", "else_connected",
        "gitea_authority_verified", "five_mac_commissioned",
    ):
        assert evidence[key] is False
    location = tmp_path / "runtime-inspection.json"
    save_receipt(evidence, location)
    assert json.loads(location.read_text())["status"] == "http-contract-passed"


def test_missing_original_market_control_fails_the_runtime_gate():
    def without_watchlist(path: str) -> bytes:
        content = _served(path)
        if path == "/":
            return content.replace(b'id="watchlist"', b'id="removed-watchlist"')
        return content

    evidence = inspect_runtime(
        "http://127.0.0.1:18340", fetch=without_watchlist, source_commit="fixture"
    )
    assert evidence["status"] == "held"
    assert evidence["http_contract_verified"] is False
    assert "original_market_controls_served" in evidence["failed_checks"]
    assert evidence["five_mac_commissioned"] is False


def test_missing_http_response_cannot_be_reported_as_success():
    def missing(path: str) -> bytes:
        if path == "/static/app.js":
            raise ConnectionError("fixture: unavailable")
        return _served(path)

    evidence = inspect_runtime(
        "http://127.0.0.1:18340", fetch=missing, source_commit="fixture"
    )
    assert evidence["status"] == "held"
    assert any("/static/app.js:" in item for item in evidence["errors"])


@pytest.mark.parametrize("url", [
    "https://127.0.0.1:18340", "http://localhost:18340",
    "http://192.168.1.10:18340", "http://127.0.0.1",
    "http://127.0.0.1:18340/path", "http://127.0.0.1:18340/?bad=true",
])
def test_probe_refuses_noncanonical_or_nonlocal_urls(url):
    with pytest.raises(ValueError, match="127.0.0.1"):
        inspect_runtime(url, fetch=_served, source_commit="fixture")
