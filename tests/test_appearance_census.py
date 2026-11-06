from pathlib import Path

WEB = Path(__file__).parents[1] / "src" / "market_compass" / "web"


def test_appearance_bridge_covers_every_known_legacy_dark_island():
    html = (WEB / "index.html").read_text()
    css = (WEB / "act-v1-appearance.css").read_text()
    assert html.index("/static/act-v1-appearance.css") > html.index("/static/decision-gates.css")
    for selector in (
        ".panel",
        ".operator-action",
        ".cassette-canvas",
        ".stub-card",
        ".intelthat-card",
        ".analyst-result",
        ".exchange-console",
        ".exchange-toolbar button",
        ".exchange-dashboard strong",
        ".stop.current",
        ".stop.invalidation",
        ".tf-card.active",
        ".gate-state.stop",
        ".exchange-inspector-tabs button[aria-selected=\"true\"]",
        ".calibration-hero span",
        ".timeline-item",
        ".board-node text",
        ".action-pill.good",
        ".error",
    ):
        assert selector in css


def test_light_dark_and_system_share_semantic_surface_tokens():
    css = (WEB / "act-v1-appearance.css").read_text()
    assert "--act-fill: #ffffff" in css
    assert 'html[data-act-color="dark"]' in css
    assert 'html[data-act-color="system"]' in css
    assert "@media (prefers-color-scheme: dark)" in css
    assert "--act-canvas: #0a0a0a" in css
    assert "--act-surface: #171717" in css
    assert "background: var(--act-blue-fill)" in css
    assert "color: var(--act-blue)" in css


def test_demo_width_consent_and_contract_tabs_have_non_collapsing_layouts():
    css = (WEB / "act-v1-appearance.css").read_text()
    assert "grid-template-columns: repeat(5, minmax(0, 1fr))" in css
    assert ".analyst-controls .cloud-consent" in css
    assert "grid-column: 1 / -1" in css
    assert ".analyst-controls select { width: 100%; min-width: 0; }" in css
