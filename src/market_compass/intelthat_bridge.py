"""Read-only research receipts from intelTHAT, using explicit proof states."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

_SYMBOL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._^=-]{0,29}$")
KINDS = ("pack", "macro", "rss", "edgar")
MAX_SIZE = 8 * 1024 * 1024
AGE = {"pack": timedelta(hours=36), "macro": timedelta(days=7),
       "rss": timedelta(hours=36), "edgar": timedelta(days=7)}
FIELDS = {
    "pack": {"readiness": ("planningReady", "executionReady", "planningBlockedReason"),
             "diagnostics": ("passCount", "nearMissCount", "orbCount")},
    "macro": {"": ("weekType",), "scores": ("overallMacroScore", "eventRiskScore"),
              "decision": ("riskMode", "preferredStructure", "sizeMultiplier")},
    "rss": {"": ("regime", "score", "signalDirection", "confidence")},
    "edgar": {"": ("count", "totalCount", "filingCount")},
}

def _empty(kind: str, state: str, reason: str) -> dict:
    return {"kind": kind, "state": state, "reason": reason, "as_of": None,
            "sha256": None, "metrics": {}}

def _timestamp(payload: dict) -> datetime | None:
    for value in (payload.get("asOfUtc"), payload.get("asOf"),
                  payload.get("as_of"), payload.get("timestamp")):
        try:
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                return datetime.fromtimestamp(value, tz=UTC)
            if isinstance(value, str):
                result = datetime.fromisoformat(value)
                if result.tzinfo is not None:
                    return result.astimezone(UTC)
        except (ValueError, OverflowError, OSError):
            pass
    return None

def _path(root: Path, symbol: str, kind: str) -> Path:
    direct = root / symbol / (kind + ".json")
    if kind != "pack" or direct.exists() or direct.is_symlink():
        return direct
    archive = root / "packs"
    if archive.is_symlink() or not archive.is_dir():
        return direct
    matches = sorted(archive.glob(symbol + "_*.json"))
    return matches[-1] if matches else direct

def _one(root: Path, symbol: str, kind: str, now: datetime) -> dict:
    path = _path(root, symbol, kind)
    if path.is_symlink() or path.parent.is_symlink():
        return _empty(kind, "excluded", "Symlink source refused.")
    if not path.is_file():
        return _empty(kind, "missing", "No published local snapshot.")
    try:
        if not path.resolve().is_relative_to(root.resolve()):
            return _empty(kind, "excluded", "Source escapes root.")
        if path.stat().st_size > MAX_SIZE:
            return _empty(kind, "excluded", "Snapshot too large.")
        raw = path.read_bytes()
        if len(raw) > MAX_SIZE:
            return _empty(kind, "excluded", "Snapshot too large.")
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise TypeError("Expected object")
    except (OSError, TypeError, ValueError, UnicodeError):
        return _empty(kind, "excluded", "Invalid source JSON.")
    metrics = {}
    for parent, keys in FIELDS[kind].items():
        group = data.get(parent, {}) if parent else data
        if not isinstance(group, dict):
            continue
        for key in keys:
            value = group.get(key)
            if isinstance(value, str | bool | int | float):
                metrics[key] = value[:160] if isinstance(value, str) else value
    stamp = _timestamp(data)
    item = {"kind": kind, "sha256": hashlib.sha256(raw).hexdigest(),
            "as_of": stamp.isoformat() if stamp else None, "metrics": metrics}
    given = data.get("symbol")
    if not isinstance(given, str):
        item.update(state="held", reason="Asset binding absent.")
    elif given.upper() != symbol:
        item.update(state="excluded", reason="Asset binding mismatch.", metrics={})
    elif stamp is None:
        item.update(state="held", reason="Timestamp absent or ambiguous.")
    elif stamp > now + timedelta(minutes=5):
        item.update(state="held", reason="Future-dated snapshot.")
    elif now - stamp > AGE[kind]:
        item.update(state="held", reason="Stale snapshot.")
    else:
        item.update(state="observed", reason="Readable and current; not independently verified.")
    return item

def read_snapshot(symbol: str, *, root: Path | None = None,
                  now: datetime | None = None) -> dict:
    """Never execute intelTHAT, modify data, influence scores, or place orders."""
    if not _SYMBOL.fullmatch(symbol):
        raise ValueError("Invalid symbol.")
    symbol = symbol.upper()
    path = root if root is not None else os.environ.get("MARKET_COMPASS_INTELTHAT_DIR")
    configured = bool(path)
    source = Path(path).expanduser() if configured else None
    if source is None:
        items = {k: _empty(k, "missing", "Source directory unconfigured.") for k in KINDS}
    elif source.is_symlink() or not source.is_dir():
        items = {k: _empty(k, "missing", "Source directory unavailable.") for k in KINDS}
    else:
        when = now or datetime.now(UTC)
        if when.tzinfo is None:
            raise ValueError("Now must have timezone.")
        when = when.astimezone(UTC)
        items = {k: _one(source, symbol, k, when) for k in KINDS}
    counts = {s: sum(v["state"] == s for v in items.values())
              for s in ("observed", "held", "excluded", "missing")}
    return {"symbol": symbol, "configured": configured,
            "mode": "research_only", "trade_execution": False,
            "score_influence": False, "proof_health": counts, "sources": items}
