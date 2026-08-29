from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_intention_names_every_core_feature():
    intention = (ROOT / "docs" / "PRODUCT-INTENTION.md").read_text()
    required = {
        "Asset Reality",
        "Market State",
        "Bull/bear evidence",
        "Confidence",
        "Trend",
        "Momentum",
        "Reversal versus continuation",
        "Fibonacci and Bus Stop route",
        "Price Memory",
        "Multi-timeframe analysis",
        "News and event risk",
        "Historical Analogs",
        "Evidence Board",
        "Nephew Analyst",
        "Local model lanes",
        "Approved cloud models",
        "Model routing and receipts",
    }
    for feature in required:
        assert f"| {feature} |" in intention


def test_change_log_and_feature_journal_are_separate_and_discoverable():
    root_readme = (ROOT / "README.md").read_text()
    docs_readme = (ROOT / "docs" / "README.md").read_text()
    journal = (ROOT / "docs" / "FEATURE-JOURNAL.md").read_text()
    change_log = (ROOT / "CHANGELOG.md").read_text()

    assert "docs/PRODUCT-INTENTION.md" in root_readme
    assert "CHANGELOG.md" in root_readme
    assert "docs/FEATURE-JOURNAL.md" in root_readme
    assert "PRODUCT-INTENTION.md" in docs_readme
    assert "Founder direction" in journal
    assert "shipped repository changes" in change_log.lower()
