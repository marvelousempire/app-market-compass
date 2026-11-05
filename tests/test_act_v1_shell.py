from pathlib import Path


WEB = Path(__file__).parents[1] / "src" / "market_compass" / "web"


def test_act_v1_is_the_outer_shell_not_an_inner_label():
    html = (WEB / "index.html").read_text()
    assert '<aside class="act-shell-rail"' in html
    assert 'aria-label="Market Compass rooms"' in html
    assert 'ADMINISTRATIVE CONTROL TOWER · ACT V1' not in html
    assert '/static/act-v1-shell.css' in html
    assert '/static/act-v1-appearance.css' in html
    assert '/static/act-v1-shell.js' in html
    for node in ('primary-rail', 'supporting-rail', 'bottom-rail'):
        assert f'data-shell-node="{node}"' in html
    assert 'class="act-mobile-tabs"' in html
    assert 'id="act-command-dialog"' in html


def test_shell_rooms_target_real_market_compass_work():
    html = (WEB / "index.html").read_text()
    for target in ("market-overview", "actor-spaces", "market-exchange", "market-workspace", "intelthat-panel"):
        assert f'href="#{target}"' in html
        assert f'id="{target}"' in html


def test_shell_preserves_research_boundary_and_product_identity():
    html = (WEB / "index.html").read_text()
    assert "Signals active" in html
    assert "No order execution" in html
    assert "Compass Desk" in html
    assert "Trading Desk" not in html
    assert "Market Compass" in html
    assert "READYPLAY" not in html


def test_shell_has_light_calm_default_and_accessible_active_navigation():
    css = (WEB / "act-v1-shell.css").read_text()
    appearance = (WEB / "act-v1-appearance.css").read_text()
    script = (WEB / "act-v1-shell.js").read_text()
    assert "--act-canvas:#f5f5f5" in css
    assert "--act-surface:#fff" in css
    assert "prefers-reduced-motion" in css
    assert "aria-current" in script
    assert "IntersectionObserver" in script
    assert "--act-fill: #ffffff" in appearance
    assert 'html[data-act-color="dark"]' in appearance
    for legacy_surface in (".operator-action", ".cassette-canvas", ".stub-card", ".intelthat-card"):
        assert legacy_surface in appearance


def test_shell_carries_readyplay_act_v1_controls_without_readyplay_identity():
    html = (WEB / "index.html").read_text()
    script = (WEB / "act-v1-shell.js").read_text()
    for group in ("Overview", "Studios", "Evidence"):
        assert f'data-nav-group="{group}"' in html
    for color in ("system", "light", "dark"):
        assert f'data-act-color="{color}"' in html
    for layout in ("control-room", "focus", "wide-canvas"):
        assert f'data-act-layout="{layout}"' in html
    assert 'id="act-rail-collapse"' in html
    assert 'id="act-layout-recovery"' in html
    assert "act-v1-group-" in script
    assert "act-v1-compact" in script
    assert "act-v1-layout" in script
    assert "act-v1-color" in script
    assert "READYPLAY" not in html


def test_shell_rooms_resolve_to_real_sections_and_not_fake_routes():
    html = (WEB / "index.html").read_text()
    targets = set()
    for token in html.split('href="#')[1:]:
        target = token.split('"', 1)[0]
        if target.startswith(("market-", "operator-", "actor-", "intelthat-", "route-", "timeframe-", "evidence-", "catalyst-")):
            targets.add(target)
    assert targets
    for target in targets:
        assert f'id="{target}"' in html
