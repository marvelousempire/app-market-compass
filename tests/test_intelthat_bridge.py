import json
from datetime import UTC, datetime, timedelta

import pytest

from market_compass.intelthat_bridge import read_snapshot

NOW = datetime(2026, 11, 3, 16, 0, tzinfo=UTC)

def publish(root, kind, data):
    folder = root / "QQQ"
    folder.mkdir(exist_ok=True)
    (folder / (kind + ".json")).write_text(json.dumps(data))

def test_unconfigured(monkeypatch):
    monkeypatch.delenv("MARKET_COMPASS_INTELTHAT_DIR", raising=False)
    result = read_snapshot("QQQ", now=NOW)
    assert not result["configured"]
    assert result["proof_health"]["missing"] == 4
    assert result["trade_execution"] is False
    assert result["score_influence"] is False

def test_pack_receipt_and_allowlist(tmp_path):
    publish(tmp_path, "pack", {"symbol": "QQQ", "asOfUtc": NOW.timestamp(),
            "readiness": {"planningReady": True, "executionReady": False},
            "diagnostics": {"passCount": 3}, "secret": "do-not-expose"})
    result = read_snapshot("QQQ", root=tmp_path, now=NOW)
    pack = result["sources"]["pack"]
    assert pack["state"] == "observed"
    assert pack["metrics"]["passCount"] == 3
    assert pack["metrics"]["executionReady"] is False
    assert len(pack["sha256"]) == 64
    assert "do-not-expose" not in json.dumps(result)

def test_existing_archived_pack(tmp_path):
    archive = tmp_path / "packs"
    archive.mkdir()
    (archive / "QQQ_2026-11-03.json").write_text(
        json.dumps({"symbol": "QQQ", "asOfUtc": NOW.timestamp()}))
    assert read_snapshot("QQQ", root=tmp_path, now=NOW)["sources"]["pack"]["state"] == "observed"

def test_mismatch_and_unbound_edgar(tmp_path):
    publish(tmp_path, "macro", {"symbol": "SPY", "asOf": NOW.isoformat()})
    publish(tmp_path, "edgar", {"asOfUtc": NOW.timestamp()})
    result = read_snapshot("QQQ", root=tmp_path, now=NOW)
    assert result["sources"]["macro"]["state"] == "excluded"
    assert result["sources"]["edgar"]["state"] == "held"

def test_stale_and_future(tmp_path):
    publish(tmp_path, "rss", {"symbol": "QQQ", "asOfUtc": (NOW-timedelta(days=8)).timestamp()})
    assert read_snapshot("QQQ", root=tmp_path, now=NOW)["sources"]["rss"]["state"] == "held"
    publish(tmp_path, "rss", {"symbol": "QQQ", "asOfUtc": (NOW+timedelta(days=1)).timestamp()})
    assert read_snapshot("QQQ", root=tmp_path, now=NOW)["sources"]["rss"]["state"] == "held"

def test_invalid_json_and_symlink(tmp_path):
    folder = tmp_path / "QQQ"
    folder.mkdir()
    (folder / "pack.json").write_text("{bad json")
    assert read_snapshot("QQQ", root=tmp_path, now=NOW)["sources"]["pack"]["state"] == "excluded"
    (folder / "pack.json").unlink()
    (folder / "pack.json").symlink_to(tmp_path / "outside.json")
    assert read_snapshot("QQQ", root=tmp_path, now=NOW)["sources"]["pack"]["state"] == "excluded"

@pytest.mark.parametrize("symbol", ["../QQQ", "A/B", "QQQ?"])
def test_traversal_rejected(symbol):
    with pytest.raises(ValueError):
        read_snapshot(symbol, now=NOW)
