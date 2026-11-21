"""Documentation guardrails for proposeTHAT and Market Compass owner workflow."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_handbook_links_two_modes_without_duplicate_engine():
    index = (ROOT / "handbook/index.md").read_text(encoding="utf-8")
    guide = (ROOT / "handbook/PROPOSETHAT.md").read_text(encoding="utf-8")
    assert "PROPOSETHAT.md" in index
    assert "owner-improvement" in guide
    assert "outside-trading-source" in guide
    assert "automatic_owner_intake=false" in guide
    assert "trade_execution=false" in guide
    assert "score_influence=false" in guide
    assert "not a verified in-app" in guide.lower()
    assert "do not create a competing Market Compass recommendation registry" in guide


def test_owner_intake_contract_identifies_scope_and_remaining_acceptance():
    contract = (ROOT / "docs/TRADING-SOURCE-INTAKE-AND-TWO-WAY-COMPARISON.md").read_text(encoding="utf-8")
    assert "Owner-improvement mode" in contract
    assert "source-only classifier" in contract
    assert "not automatic owner intake" in contract
