from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from .engine import analyze
from .registry import NODE_REGISTRY, node_output

app = FastAPI(title="Market Compass", version="0.1.0")

PAGE = r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Market Compass</title><style>
body{font-family:system-ui,sans-serif;max-width:1000px;margin:40px auto;padding:0 18px;background:#0b1220;color:#e8eef7}input,button{font:inherit;padding:10px;border-radius:8px;border:1px solid #42516a}input{background:#111b2e;color:white}button{background:#dde8f6;color:#111827;font-weight:700;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.card{background:#121d30;border:1px solid #25324a;border-radius:12px;padding:16px;margin:12px 0}.meter{height:16px;background:#361d25;border-radius:10px;overflow:hidden}.bull{height:100%;background:#3da56a}small{color:#9cacbf}pre{white-space:pre-wrap}.layer{border-top:1px solid #25324a;padding:10px 0}.bad{color:#ffadad}.good{color:#a8e6b6}</style></head><body>
<h1>Market Compass</h1><p>Evidence, counter-evidence, price memory, bus stops, news, history, relationships and narrative. The score is evidence balance, not a promise.</p>
<div class="card"><input id="symbol" value="HYPE-USD" aria-label="symbol"><input id="horizon" type="number" value="20" min="1" max="120" aria-label="horizon"><button onclick="go()">Analyze</button><small id="status"></small></div>
<div id="out"></div><script>
const esc=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function go(){let s=document.getElementById('symbol').value.trim(),h=document.getElementById('horizon').value,status=document.getElementById('status'),out=document.getElementById('out');status.textContent=' Working...';out.innerHTML='';try{let r=await fetch(`/api/analyze?symbol=${encodeURIComponent(s)}&horizon=${h}`);let d=await r.json();if(!r.ok)throw Error(d.detail||'Analysis failed');status.textContent='';let layers=Object.values(d.layers).map(x=>`<div class="layer"><b>${esc(x.label)}</b> · ${esc(x.state)} · score ${x.score.toFixed(2)} · confidence ${(x.confidence*100).toFixed(0)}%<br><small>${esc((x.evidence[0]||{}).text||'No supporting evidence recorded.')} ${esc((x.counter_evidence[0]||{}).text||'')}</small></div>`).join('');out.innerHTML=`<div class="grid"><div class="card"><h2>${esc(d.symbol)}</h2><b>${esc(d.action)}</b><br>Price ${d.price}</div><div class="card"><h2>${d.bull_evidence} / ${d.bear_evidence}</h2><div class="meter"><div class="bull" style="width:${d.bull_evidence}%"></div></div><small>Bull / Bear evidence</small></div><div class="card"><h2>${(d.confidence*100).toFixed(0)}%</h2><small>Confidence</small></div><div class="card"><b>Next bus stop</b><br>${esc(d.route.next_bus_stops[0]??'unclear')}<br><small>Invalidation ${esc(d.route.invalidation??'unclear')}</small></div></div><div class="card"><h3>Simple read</h3>${esc(d.summary)}</div><div class="card"><h3>Evidence layers</h3>${layers}</div><details class="card"><summary>Technical details</summary><pre>${esc(d.technical_summary)}</pre></details>`}catch(e){status.textContent='';out.innerHTML=`<div class="card bad">${esc(e.message)}</div>`}}
go();</script></body></html>'''


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE


@app.get("/health")
def health():
    return {"status": "ok", "nodes": len(NODE_REGISTRY)}


@app.get("/api/analyze")
def analyze_api(symbol: str = Query(min_length=1), horizon: int = Query(20, ge=1, le=120)):
    try:
        return analyze(symbol, horizon).model_dump(mode="json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/nodes")
def nodes():
    return NODE_REGISTRY


@app.get("/api/nodes/{node_id}")
def run_node_api(node_id: str, symbol: str, horizon: int = 20):
    try:
        return node_output(analyze(symbol, horizon), node_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
