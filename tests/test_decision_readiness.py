from market_compass.decision_readiness import calculate_readiness
from market_compass.models import LayerResult, Report, Route


def report(**overrides):
    values = {
        "symbol": "BB", "horizon_days": 20, "price": 8.0, "action": "wait",
        "bull_evidence": 70, "bear_evidence": 30, "confidence": 0.8,
        "summary": "", "technical_summary": "",
        "route": Route(direction="up", invalidation=7.0, reward_risk=2.5),
        "layers": {"foundation": LayerResult(key="foundation", label="Asset Reality", state="acceptable", score=0.5, confidence=0.8)},
        "timeframes": {"consensus": {"agreement": 0.75}},
    }
    values.update(overrides)
    return Report(**values)


def test_calculatethat_generates_signal_without_execution_or_score_mutation():
    result = calculate_readiness(report())
    assert result["instrument"] == "calculateTHAT"
    assert result["state"] == "GO_SIGNAL"
    assert result["signal_generation"] is True
    assert result["signal"]["active"] is True
    assert result["signal"]["direction"] == "BULLISH"
    assert result["trade_execution"] is False
    assert result["score_influence"] is False
    assert result["approval_required_for_signal"] is False
    assert result["signal"]["inputs"]["bull_evidence"] == 70
    assert result["signal"]["formula"]
    assert result["signal"]["timeframe"].startswith("20D")
    assert result["signal"]["timestamp"]
    assert result["signal"]["confidence_receipt"]["meaning"].endswith("not outcome probability")
    assert result["receipt"]["exportable"] is True
    assert len(result["receipt"]["sha256"]) == 64


def test_hard_stop_outranks_positive_triggers():
    result = calculate_readiness(report(confidence=0.4))
    confidence = next(gate for gate in result["gates"] if gate["key"] == "confidence")
    assert confidence["hard_stop"] is True
    assert confidence["passed"] is False
    assert result["state"] == "DO_NOT_GO_SIGNAL"


def test_surface_names_calculatethat_and_trigger_boundary():
    from pathlib import Path
    web = Path(__file__).parents[1] / "src" / "market_compass" / "web"
    html = (web / "index.html").read_text()
    assert 'id="decision-gates"' in html
    assert "calculateTHAT" in html
    assert "Signals are active research outputs, not orders" in html
    assert "/static/decision-gates.js" in html
