"""Pack #2 acceptance. Offline fixture only."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fixtures.make_desk import build
from main import run

def test_desk():
    out = run(build())
    assert out["pack"] == "#2"
    assert out["label"] == "RELATIVE STRENGTH DESK + MARKET TAPE"
    desk = out["desk"]
    assert desk["rsi"]["zone"] in {"oversold", "overbought", "bullish_half", "bearish_half"}
    assert desk["relative"]["stance"] in {"leading_btc", "lagging_btc", "in_line_with_btc", "unknown"}
    assert desk["tape"]["bias"] in {"bid", "offer", "balanced"}
    assert desk["ath"]["drawdown"] <= 0
    assert desk["sma_stack"]["stack"] in {"bull_stack", "bear_stack", "mixed_stack"}
    assert desk["supply"]["issued_pct"] == 0.56
    assert "RSI" in desk["decision_sentence"]
    assert out["receipt"]["scoring_untouched"] is True
    assert out["receipt"]["evidence_sequence"] == "8001-preserved"
    assert len(out["receipt"]["slices"]) == 7
    print("PASS pack #2")
    print(desk["decision_sentence"])

if __name__ == "__main__":
    test_desk()
