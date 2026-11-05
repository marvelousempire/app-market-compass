from pathlib import Path


WEB = Path(__file__).parents[1] / "src" / "market_compass" / "web"


def test_act_v1_is_the_outer_shell_not_an_inner_label():
    html = (WEB / "index.html").read_text()
    assert '<aside class="act-shell-rail"' in html
    assert 'aria-label="Market Compass rooms"' in html
    assert 'ADMINISTRATIVE CONTROL TOWER · ACT V1' not in html
    assert '/static/act-v1-shell.css' in html
    assert '/static/act-v1-shell.js' in html


def test_shell_rooms_target_real_market_compass_work():
    html = (WEB / "index.html").read_text()
    for target in ("market-overview", "actor-spaces", "market-exchange", "market-workspace", "intelthat-panel"):
        assert f'href="#{target}"' in html
        assert f'id="{target}"' in html


def test_shell_preserves_research_boundary_and_product_identity():
    html = (WEB / "index.html").read_text()
    assert "Research only" in html
    assert "Trading off" in html
    assert "Market Compass" in html
    assert "READYPLAY" not in html


def test_shell_has_light_calm_default_and_accessible_active_navigation():
    css = (WEB / "act-v1-shell.css").read_text()
    script = (WEB / "act-v1-shell.js").read_text()
    assert "--act-canvas:#f8fafc" in css
    assert "--act-surface:#fff" in css
    assert "prefers-reduced-motion" in css
    assert "aria-current" in script
    assert "IntersectionObserver" in script
