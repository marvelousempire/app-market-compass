"""Exercise price handoff and saved-credential behavior in the required test lane."""
import subprocess
from pathlib import Path


def test_market_browser_behavior():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ['node', '--test', 'tests/desk-market-price.test.mjs',
         'tests/market-data-save-feedback.test.mjs'],
        cwd=root, capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
