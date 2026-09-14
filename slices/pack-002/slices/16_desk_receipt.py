"""Pack #2 slice 16 — Wrap the desk and close the books."""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone

def _utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _hash(obj):
    raw = json.dumps(obj, sort_keys=True, default=str)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()

def run(asset, rsi, relative, tape, ath, stack, supply):
    sentence_parts = [
        f"{asset} RSI {rsi['rsi14']} sits in the {rsi['zone'].replace('_', ' ')}.",
        f"Relative stance versus BTC equals {relative['stance'].replace('_', ' ')}.",
        f"Tape bias equals {tape['bias']}.",
        f"Drawdown from ATH equals {ath['drawdown_pct']} percent ({ath['state'].replace('_', ' ')}).",
        f"SMA stack equals {stack['stack'].replace('_', ' ')}.",
    ]
    if supply.get("issued_pct") is not None:
        sentence_parts.append(f"Issued supply equals {round(supply['issued_pct'] * 100, 1)} percent of max.")
    desk = {
        "schema_id": "market-compass.relative-strength-desk",
        "schema_version": "1.0.0",
        "pack": "#2",
        "asset": asset,
        "rsi": rsi,
        "relative": relative,
        "tape": {"bias": tape["bias"], "up_bars": tape["up_bars"], "down_bars": tape["down_bars"], "last_rows": tape["rows"][-5:]},
        "ath": ath,
        "sma_stack": stack,
        "supply": supply,
        "decision_sentence": " ".join(sentence_parts),
    }
    receipt = {
        "schema_id": "market-compass.pack-002-receipt",
        "schema_version": "1.0.0",
        "pack": "#2",
        "label": "RELATIVE STRENGTH DESK + MARKET TAPE",
        "asset": asset,
        "desk_digest": _hash(desk),
        "slices": [
            "10_rsi_zones",
            "11_relative_strength",
            "12_market_tape",
            "13_ath_drawdown",
            "14_sma_stack",
            "15_supply_metrics",
            "16_desk_receipt",
        ],
        "scoring_untouched": True,
        "evidence_sequence": "8001-preserved",
        "issued_at": _utc(),
    }
    receipt["content_digest"] = _hash({k: v for k, v in receipt.items() if k != "content_digest"})
    return {"desk": desk, "receipt": receipt}
