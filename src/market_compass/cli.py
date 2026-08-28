from __future__ import annotations

import json

import typer

from .backtest import backtest_frame
from .data import get_market_data
from .engine import analyze
from .registry import NODE_REGISTRY, node_output

app = typer.Typer(help="Market Compass: paired-evidence market intelligence.", no_args_is_help=True)


@app.command("analyze")
def analyze_cmd(symbol: str, horizon: int = 20, csv: str | None = None, stochastic: bool = False, json_output: bool = typer.Option(False, "--json")):
    """Run the complete Market Compass analysis."""
    r = analyze(symbol, horizon, csv, stochastic)
    if json_output:
        typer.echo(r.model_dump_json(indent=2))
        return
    typer.echo(f"{r.symbol}  price={r.price:.4g}  action={r.action}")
    typer.echo(f"Bull {r.bull_evidence} / Bear {r.bear_evidence}  confidence={r.confidence:.0%}")
    typer.echo(r.summary)


@app.command()
def node(node_id: str, symbol: str, horizon: int = 20, csv: str | None = None):
    """Run an addressable IP node and print its shared implementation result."""
    r = analyze(symbol, horizon, csv)
    typer.echo(json.dumps(node_output(r, node_id), indent=2, default=str))


@app.command("registry")
def registry_cmd():
    """List all 115 stable node IDs and their shared implementation groups."""
    for node_id, group in NODE_REGISTRY.items():
        typer.echo(f"{node_id}\t{group}")


@app.command("backtest")
def backtest_cmd(symbol: str, horizon: int = 20, csv: str | None = None, fee_bps: float = 10.0):
    """Run the compact past-only technical signal backtest."""
    data = get_market_data(symbol, csv)
    typer.echo(json.dumps(backtest_frame(data.bars, horizon, fee_bps), indent=2))


if __name__ == "__main__":
    app()
