from __future__ import annotations

import re
from datetime import datetime, timezone
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from .models import Evidence, LayerResult

POS = {"beat", "beats", "growth", "grow", "upgrade", "approval", "approved", "record", "profit", "partnership", "launch", "adoption", "bullish", "surge", "rally", "wins", "gain"}
NEG = {"miss", "misses", "downgrade", "lawsuit", "hack", "hacked", "breach", "shutdown", "war", "attack", "ban", "regulation", "dilution", "unlock", "loss", "bearish", "drop", "plunge", "fraud"}
RISK = {"fed", "rate", "inflation", "shutdown", "war", "attack", "earnings", "lawsuit", "regulation", "hack", "unlock", "election", "tariff", "sanction"}
NARRATIVES = {
    "AI / chips": {"ai", "artificial", "intelligence", "chip", "gpu", "semiconductor"},
    "Rates / Fed": {"fed", "rate", "rates", "inflation", "yield"},
    "Crypto adoption": {"crypto", "bitcoin", "ethereum", "blockchain", "token", "exchange", "defi"},
    "Regulation": {"regulation", "regulator", "sec", "law", "ban", "approval"},
    "Geopolitics": {"war", "attack", "sanction", "tariff", "china", "russia", "iran"},
}


def _sentiment(title: str) -> float:
    words = set(re.findall(r"[a-zA-Z]+", title.lower()))
    p, n = len(words & POS), len(words & NEG)
    return (p - n) / max(p + n, 1)


def foundation_layer(x: pd.DataFrame, quote: dict) -> LayerResult:
    history_days = max((x.index[-1] - x.index[0]).days, 1)
    dollar_vol = float((x.close * x.volume).tail(30).median())
    liquid = dollar_vol > 5_000_000
    short_history = history_days < 365
    score = (.35 if liquid else -.25) + (-.2 if short_history else .2)
    market_cap = quote.get("marketCap")
    if market_cap:
        score += .1
    missing = [k for k in ("marketCap", "quoteType") if not quote.get(k)]
    if str(quote.get("quoteType", "")).upper() in {"CRYPTOCURRENCY", "CRYPTO"}:
        missing += ["token utility", "circulating/total supply", "unlock schedule", "holder concentration"]
    state = "acceptable" if score > .2 else "speculative" if score > -.25 else "weak or thin"
    ev, ce = [], []
    (ev if liquid else ce).append(Evidence(text=f"Median 30-day dollar volume is about ${dollar_vol:,.0f}.", direction=1 if liquid else -1, strength=.75))
    (ev if not short_history else ce).append(Evidence(text=f"Price history covers {history_days} days.", direction=1 if not short_history else -1, strength=.55))
    return LayerResult(
        key="foundation", label="Asset Reality & Quality", state=state,
        score=float(np.clip(score, -1, 1)), confidence=.72 if len(missing) < 2 else .45,
        evidence=ev, counter_evidence=ce,
        metrics={"history_days": history_days, "median_dollar_volume_30d": dollar_vol, "market_cap": market_cap, "quote_type": quote.get("quoteType")},
        missing=missing,
    )


def news_layer(x: pd.DataFrame, news: list[dict], symbol: str) -> LayerResult:
    if not news:
        return LayerResult(key="news", label="Human Factor & News", state="no current news data", score=0, confidence=.15, missing=["headlines"], metrics={"timeline": []})
    now = datetime.now(timezone.utc)
    scored, risk_hits, timeline = [], [], []
    for n in news[:30]:
        title = n.get("title", "")
        s = _sentiment(title)
        try:
            dt = datetime.fromisoformat(n["published"]) if n.get("published") else now
            age_days = max((now - dt).total_seconds() / 86400, 0)
        except Exception:
            dt, age_days = now, 7
        decay = np.exp(-age_days / 10)
        words = set(re.findall(r"[a-zA-Z]+", title.lower()))
        risk = sorted(words & RISK)
        if risk:
            risk_hits.append(title)
        scored.append((float(s * decay), n))
        timeline.append({
            "title": title, "publisher": n.get("publisher", ""), "url": n.get("url", ""),
            "published": dt.isoformat(), "age_days": round(float(age_days), 2),
            "sentiment": round(float(s), 3), "risk_tags": risk,
        })
    net = float(np.mean([s for s, _ in scored])) if scored else 0
    daily = float(x.close.pct_change().iloc[-1])
    confirms = np.sign(net) == np.sign(daily) if abs(net) > .05 and abs(daily) > .002 else False
    score = float(np.clip(net * .8 + np.sign(net) * .1 * confirms, -1, 1))
    top_pos = sorted(scored, reverse=True, key=lambda z: z[0])[:3]
    top_neg = sorted(scored, key=lambda z: z[0])[:3]
    timeline = sorted(timeline, key=lambda z: z["published"], reverse=True)
    return LayerResult(
        key="news", label="Human Factor & News", state="positive" if score > .1 else "negative" if score < -.1 else "mixed or quiet",
        score=score, confidence=min(.82, .35 + len(news) / 45),
        evidence=[Evidence(text=n["title"], direction=1, strength=min(1, abs(s) + .3), source=n.get("publisher") or "news") for s, n in top_pos if s > 0],
        counter_evidence=[Evidence(text=n["title"], direction=-1, strength=min(1, abs(s) + .3), source=n.get("publisher") or "news") for s, n in top_neg if s < 0],
        metrics={
            "headline_count": len(news), "sentiment": net, "latest_daily_return": daily,
            "market_reaction_confirms": bool(confirms), "event_risk_headlines": risk_hits[:6], "timeline": timeline[:20],
        },
    )


def historical_layer(x: pd.DataFrame, horizon: int = 20) -> LayerResult:
    cols = ["ret5", "ret20", "rsi14", "vol20", "vol_z"]
    f = x[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(f) < max(120, horizon * 4):
        return LayerResult(key="history", label="Historical Context", state="not enough history", score=0, confidence=.2, missing=["more historical observations"])
    forward = x.close.shift(-horizon) / x.close - 1
    candidates = f.iloc[:-(horizon + 5)]
    y = forward.reindex(candidates.index).dropna()
    candidates = candidates.loc[y.index]
    if len(candidates) < 50:
        return LayerResult(key="history", label="Historical Context", state="not enough completed analogs", score=0, confidence=.2)
    scaler = StandardScaler().fit(candidates)
    k = min(12, len(candidates))
    nn = NearestNeighbors(n_neighbors=k).fit(scaler.transform(candidates))
    dist, idx = nn.kneighbors(scaler.transform(f.iloc[[-1]]))
    analog_dates = candidates.index[idx[0]]
    outcomes = y.loc[analog_dates]
    mean_ret = float(outcomes.mean())
    score = float(np.clip(np.tanh(mean_ret * 6), -1, 1))
    counter = outcomes[outcomes < 0] if score >= 0 else outcomes[outcomes > 0]
    similarity = float(1 / (1 + np.mean(dist[0])))
    return LayerResult(
        key="history", label="Historical Context", state="past analogs leaned up" if score > .1 else "past analogs leaned down" if score < -.1 else "past analogs were mixed",
        score=score, confidence=min(.86, .35 + k / 24 + similarity * .12),
        evidence=[Evidence(text=f"{k} nearest past setups averaged {mean_ret:+.1%} over the next {horizon} bars.", direction=1 if mean_ret >= 0 else -1, strength=.7)],
        counter_evidence=[Evidence(text=f"Counterexample {dt.date()}: {val:+.1%}.", direction=-1 if score >= 0 else 1, strength=.55) for dt, val in counter.sort_values().head(4).items()],
        metrics={
            "analog_count": k, "similarity": similarity, "mean_forward_return": mean_ret,
            "median_forward_return": float(outcomes.median()), "positive_rate": float((outcomes > 0).mean()),
            "q25": float(outcomes.quantile(.25)), "q75": float(outcomes.quantile(.75)),
            "dates": [d.isoformat() for d in analog_dates],
        },
    )


def forecast(x: pd.DataFrame, horizon: int = 20) -> dict:
    cols = ["ret1", "ret5", "ret20", "rsi14", "vol20", "vol_z"]
    frame = x[cols].replace([np.inf, -np.inf], np.nan).copy()
    target = x.close.shift(-horizon) / x.close - 1
    train = frame.join(target.rename("target")).dropna()
    if len(train) < 140:
        return {"state": "insufficient_data", "expected_return": None, "confidence": .15}
    splits = min(5, max(3, len(train) // 60))
    cv = TimeSeriesSplit(n_splits=splits)
    maes, baselines = [], []
    for tr, te in cv.split(train):
        scaler = StandardScaler().fit(train.iloc[tr][cols])
        model = Ridge(alpha=3).fit(scaler.transform(train.iloc[tr][cols]), train.iloc[tr].target)
        pred = model.predict(scaler.transform(train.iloc[te][cols]))
        actual = train.iloc[te].target.values
        maes.append(mean_absolute_error(actual, pred))
        baselines.append(mean_absolute_error(actual, np.repeat(train.iloc[tr].target.mean(), len(te))))
    scaler = StandardScaler().fit(train[cols])
    model = Ridge(alpha=3).fit(scaler.transform(train[cols]), train.target)
    current = frame.dropna().iloc[[-1]]
    expected = float(model.predict(scaler.transform(current))[0])
    mae, base = float(np.mean(maes)), float(np.mean(baselines))
    beats = mae < base
    improvement = max(0.0, 1 - mae / base) if base else 0.0
    confidence = float(np.clip(.3 + .5 * improvement, .2, .8)) if base else .2
    return {
        "state": "usable" if beats else "baseline_not_beaten", "expected_return": expected if beats else None,
        "raw_model_return": expected, "cv_mae": mae, "baseline_mae": base,
        "baseline_improvement": improvement, "beats_baseline": beats, "confidence": confidence,
    }


def relationship_and_narrative(news: list[dict], symbol: str, quote: dict | None = None) -> tuple[LayerResult, LayerResult, dict]:
    quote = quote or {}
    g = nx.Graph()
    g.add_node(symbol, type="asset", verified=True)
    entity_scores: dict[str, list[float]] = {}
    for field, label in (("sectorDisp", "sector"), ("industryDisp", "industry"), ("exchange", "exchange"), ("quoteType", "instrument_type")):
        value = quote.get(field)
        if value:
            node = str(value)
            g.add_node(node, type=label, verified=True)
            g.add_edge(symbol, node, type=f"metadata_{label}", inferred=False, mentions=1, sentiments=[], source="market metadata")
    for n in news[:30]:
        title = n.get("title", "")
        sent = _sentiment(title)
        entities = re.findall(r"\b(?:[A-Z][A-Za-z0-9&.-]+(?:\s+[A-Z][A-Za-z0-9&.-]+){0,2})\b", title)
        entities = [e for e in entities if len(e) > 2 and e.lower() not in {"the", "this", "why", "how"}][:6]
        article_nodes = [symbol] + list(dict.fromkeys(e for e in entities if e != symbol))
        for e in article_nodes[1:]:
            g.add_node(e, type="inferred_entity", verified=False)
            entity_scores.setdefault(e, []).append(sent)
        for a, b in combinations(article_nodes, 2):
            if g.has_edge(a, b):
                edge = g[a][b]
                edge["mentions"] = edge.get("mentions", 0) + 1
                edge.setdefault("sentiments", []).append(sent)
            else:
                g.add_edge(a, b, type="news_co_mention", inferred=True, mentions=1, sentiments=[sent], source=title)
    edges = []
    for a, b, d in g.edges(data=True):
        avg = float(np.mean(d["sentiments"])) if d.get("sentiments") else 0
        edges.append({
            "from": a, "to": b, "type": d.get("type"), "inferred": bool(d.get("inferred", True)),
            "verified": not bool(d.get("inferred", True)), "mentions": d.get("mentions", 1),
            "sentiment": avg, "source": d.get("source"),
        })
    paths = []
    for target in list(g.nodes)[1:]:
        try:
            path = nx.shortest_path(g, symbol, target)
            if len(path) <= 4:
                paths.append({"to": target, "path": path, "degrees": len(path) - 1})
        except nx.NetworkXNoPath:
            pass
    rel_net = float(np.mean([np.mean(v) for v in entity_scores.values()])) if entity_scores else 0
    rel = LayerResult(
        key="relationships", label="Relationship Intelligence", state="verified context + inferred news graph",
        score=float(np.clip(rel_net * .4, -1, 1)), confidence=.55 if edges else .15,
        evidence=[Evidence(text=f"{e} is connected through current related news.", direction=1, strength=.35, source="inferred co-mention") for e, vals in list(entity_scores.items())[:5] if np.mean(vals) >= 0],
        counter_evidence=[Evidence(text=f"{e} is connected through negatively toned related news.", direction=-1, strength=.35, source="inferred co-mention") for e, vals in list(entity_scores.items())[:5] if np.mean(vals) < 0],
        metrics={"edge_count": len(edges), "path_count": len(paths), "verified_edge_count": sum(not e["inferred"] for e in edges)},
        missing=[] if edges else ["curated supplier/customer/ownership edges"],
    )
    counts = {name: 0 for name in NARRATIVES}
    sentiments = {name: [] for name in NARRATIVES}
    for n in news[:30]:
        words = set(re.findall(r"[a-zA-Z]+", n.get("title", "").lower()))
        for name, keys in NARRATIVES.items():
            if words & keys:
                counts[name] += 1
                sentiments[name].append(_sentiment(n.get("title", "")))
    dominant = max(counts, key=counts.get) if counts and max(counts.values(), default=0) else "No clear narrative"
    n = counts.get(dominant, 0)
    avg = float(np.mean(sentiments[dominant])) if dominant in sentiments and sentiments[dominant] else 0
    stage = "emerging" if 1 <= n <= 2 else "confirming" if n <= 4 else "mainstream/crowded" if n else "unclear"
    nar = LayerResult(
        key="narrative", label="Market Narrative", state=f"{dominant}: {stage}",
        score=float(np.clip(avg * min(1, n / 4), -1, 1)), confidence=min(.75, .25 + n * .1),
        evidence=[Evidence(text=f"Dominant story: {dominant} with {n} related headlines.", direction=1 if avg >= 0 else -1, strength=min(.8, .3 + n * .08))] if n else [],
        counter_evidence=[Evidence(text="A crowded story can reverse even when the headlines still look good.", direction=-1, strength=.35)] if n >= 5 and avg > 0 else [],
        metrics={"counts": counts, "dominant": dominant, "stage": stage, "sentiment": avg},
    )
    board = {
        "nodes": [{"id": node, **attrs} for node, attrs in g.nodes(data=True)], "edges": edges, "paths": paths[:40],
        "warning": "Verified metadata edges describe classification/context. News co-mentions are inferred relationships, not proof of causation.",
    }
    return rel, nar, board
