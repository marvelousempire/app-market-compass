const state={report:null,nodes:null,tab:'simple'};
const $=id=>document.getElementById(id);
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=(value,digits=2)=>Number.isFinite(Number(value))?Number(value).toLocaleString(undefined,{maximumFractionDigits:digits}):'—';
const pct=(value,digits=0)=>Number.isFinite(Number(value))?`${(Number(value)*100).toFixed(digits)}%`:'—';
const price=value=>{const n=Number(value);if(!Number.isFinite(n))return '—';const digits=Math.abs(n)<1?6:Math.abs(n)<100?3:2;return n.toLocaleString(undefined,{maximumFractionDigits:digits});};
const badge=(text,tone='')=>`<span class="badge ${tone}">${esc(text)}</span>`;
const toneScore=score=>Number(score)>.12?'good':Number(score)<-.12?'bad':'warn';
const layer=key=>state.report?.layers?.[key]||{};

function evidenceItems(items,tone,empty='No evidence recorded.'){
  if(!items?.length)return `<p class="muted">${esc(empty)}</p>`;
  return `<div class="evidence-list">${items.map(x=>`<div class="evidence-item ${tone}">${esc(x.text)}<small>${esc(x.source||'calculation')} · strength ${pct(x.strength)}</small></div>`).join('')}</div>`;
}
function metricCards(metrics,keys){
  return `<div class="metric-grid">${keys.filter(([_,key])=>metrics?.[key]!==undefined&&metrics?.[key]!==null).map(([label,key,format])=>`<div class="metric"><span>${esc(label)}</span><b>${esc(format?format(metrics[key]):num(metrics[key],4))}</b></div>`).join('')}</div>`;
}
function renderIdentity(d){
  const m=d.data_meta||{},q=m.quote||{};
  const type=q.quoteType||q.typeDisp||'asset';
  const retrieved=m.retrieved_at?new Date(m.retrieved_at).toLocaleString():'unknown';
  $('identity-strip').innerHTML=`<div class="identity-main"><strong>${esc(d.symbol)}</strong><span>${esc(type)}</span><span>$${price(d.price)}</span></div><div class="identity-meta"><span>Requested ${esc(m.requested_symbol||d.symbol)}</span><span>Resolved ${esc(m.resolved_symbol||d.symbol)}</span><span>${num(m.bars,0)} bars</span><span>Data ${esc(retrieved)}</span><span>As of ${esc(new Date(d.as_of).toLocaleString())}</span></div>`;
}
function renderSummary(d){
  const foundation=layer('foundation'),momentum=layer('momentum');
  const evidenceTone=d.bull_evidence>d.bear_evidence?'good':d.bull_evidence<d.bear_evidence?'bad':'warn';
  $('summary-grid').innerHTML=`
  <article class="panel summary-card"><p class="eyebrow">ASSET REALITY</p><div class="value">${esc(foundation.state||'unknown')}</div>${badge(`confidence ${pct(foundation.confidence)}`,toneScore(foundation.score))}<p class="meta">${esc(foundation.evidence?.[0]?.text||foundation.counter_evidence?.[0]?.text||'Limited asset-quality data.')}</p></article>
  <article class="panel summary-card"><p class="eyebrow">MARKET STATE</p><div class="value">${esc(momentum.state||d.action)}</div>${badge(d.action,toneScore(momentum.score))}<p class="meta">Reversal and continuation evidence are kept separate from the final action state.</p></article>
  <article class="panel summary-card"><p class="eyebrow">EVIDENCE</p><div class="value">${d.bull_evidence} / ${d.bear_evidence}</div><div class="evidence-meter"><i class="bull" style="width:${Math.max(0,Math.min(100,d.bull_evidence))}%"></i><i class="bear" style="width:${Math.max(0,Math.min(100,d.bear_evidence))}%"></i></div>${badge('bull / bear',evidenceTone)}<p class="meta">Evidence balance, not calibrated probability.</p></article>
  <article class="panel summary-card"><p class="eyebrow">CONFIDENCE</p><div class="value">${pct(d.confidence)}</div>${badge(d.confidence>=.7?'higher':d.confidence>=.45?'medium':'low',d.confidence>=.7?'good':d.confidence>=.45?'warn':'bad')}<p class="meta">Authority is reduced when data is missing, weak, correlated, or unvalidated.</p></article>`;
}
function routeStop(kind,value,extra=''){
  return `<div class="stop ${extra}"><span class="kind">${esc(kind)}</span><span class="price">${value===null||value===undefined?'—':`$${price(value)}`}</span></div>`;
}
function renderRoute(d){
  const r=d.route||{},downs=[...(r.downside_stops||[])],ups=[...(r.next_bus_stops||[])];
  $('route-badge').innerHTML=badge(`route ${r.direction||'unclear'}`,r.direction==='up'?'good':r.direction==='down'?'bad':'warn');
  const down2=downs[1]??null,down1=downs[0]??null,up1=ups[0]??null,up2=ups[1]??null;
  $('route').innerHTML=`<div class="route-track">${routeStop('Downside 2',down2)}${routeStop('Downside 1',down1)}${routeStop('Last Stop',r.last_bus_stop)}${routeStop('Current',d.price,'current')}${routeStop('Upside 1',up1)}${routeStop('Upside 2',up2)}${routeStop('Invalidation',r.invalidation,'invalidation')}</div><div class="route-meta"><span>Reward / risk: <b>${num(r.reward_risk,2)}</b></span><span>Direction: <b>${esc(r.direction||'unclear')}</b></span><span>Fib levels: <b>${Object.keys(r.fibonacci||{}).length}</b></span></div>`;
}
function polyline(values,w,h,min,max){
  const clean=values.map((v,i)=>[i,Number(v)]).filter(([,v])=>Number.isFinite(v));
  if(!clean.length)return '';
  const x=i=>20+(i/Math.max(values.length-1,1))*(w-40),y=v=>20+(max-v)/Math.max(max-min,1e-9)*(h-40);
  return clean.map(([i,v])=>`${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
}
function renderChart(d){
  const c=d.chart||{},series=[c.close||[],c.ema13||[],c.ema27||[],c.ema81||[]];
  const all=series.flat().map(Number).filter(Number.isFinite);
  if(!all.length){$('price-chart').innerHTML='<p>No chart data.</p>';return;}
  const min=Math.min(...all),max=Math.max(...all),w=760,h=280;
  const grids=[.2,.4,.6,.8].map(p=>`<line class="chart-grid" x1="20" x2="740" y1="${20+p*240}" y2="${20+p*240}"/>`).join('');
  $('price-chart').innerHTML=`<svg class="chart-svg" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" role="img" aria-label="Price chart with EMA 13, 27 and 81">${grids}<polyline class="chart-close" points="${polyline(c.close||[],w,h,min,max)}"/><polyline class="chart-ema13" points="${polyline(c.ema13||[],w,h,min,max)}"/><polyline class="chart-ema27" points="${polyline(c.ema27||[],w,h,min,max)}"/><polyline class="chart-ema81" points="${polyline(c.ema81||[],w,h,min,max)}"/></svg><div class="legend"><span>Price</span><span>EMA 13</span><span>EMA 27</span><span>EMA 81</span><span>Range $${price(min)} – $${price(max)}</span></div>`;
}
function levelList(items,type){
  if(!items?.length)return '<p class="muted">No well-tested level found.</p>';
  return `<div class="memory-list">${items.slice(0,4).map(x=>`<div class="level ${type}"><div class="level-top"><strong>$${price(x.price)}</strong><span>${pct(x.strength)}</span></div><small>${x.touches} tests · ${x.span_days}d span · reaction ${pct(x.avg_reaction,1)} · erosion ${pct(x.erosion)}</small><div class="strength-bar"><i style="width:${Math.min(100,Number(x.strength||0)*100)}%"></i></div></div>`).join('')}</div>`;
}
function renderMemory(){
  const m=layer('memory'),supports=m.metrics?.supports||[],resistances=m.metrics?.resistances||[];
  $('price-memory').innerHTML=`<div class="memory-columns"><div><p class="eyebrow">SUPPORT</p>${levelList(supports,'support')}</div><div><p class="eyebrow">RESISTANCE</p>${levelList(resistances,'resistance')}</div></div><p class="simple-only">${esc(m.state||'No price-memory state.')}</p><p class="technical-only">Layer score ${num(m.score,3)} · confidence ${pct(m.confidence)}.</p>`;
}
function renderSignals(d){
  const trend=layer('trend'),mom=layer('momentum'),route=layer('route'),foundation=layer('foundation');
  const cards=[
    ['TREND','Trend',trend,metricCards(trend.metrics,[['EMA 13','ema13',price],['EMA 27','ema27',price],['EMA 81','ema81',price],['Slope','slope',v=>num(v,5)]])],
    ['MOMENTUM','Momentum',mom,metricCards(mom.metrics,[['RSI 14','rsi14',v=>num(v,1)],['MACD','macd',v=>num(v,4)],['Signal','macd_signal',v=>num(v,4)],['Histogram','histogram',v=>num(v,4)]])],
    ['FIBONACCI','Route Structure',route,metricCards(route.metrics,[['Reward / Risk','reward_risk',v=>num(v,2)],['Fib Direction','fibonacci_direction',v=>String(v)]])],
    ['REVERSAL','Asset + State',mom,`<div class="metric-grid"><div class="metric"><span>Reversal state</span><b>${esc(mom.state||'unknown')}</b></div><div class="metric"><span>Asset gate</span><b>${esc(foundation.state||'unknown')}</b></div></div>`]
  ];
  $('signal-grid').innerHTML=cards.map(([eye,title,l,metrics])=>`<article class="panel signal-card"><p class="eyebrow">${eye}</p><h2>${esc(title)}</h2><div class="signal-state">${esc(l.state||'unknown')}</div>${badge(`score ${num(l.score,2)}`,toneScore(l.score))}${metrics}</article>`).join('');
}
function renderNews(){
  const n=layer('news'),m=n.metrics||{};
  $('news-panel').innerHTML=`<div class="stat-row"><div class="stat"><strong>${num(m.headline_count,0)}</strong><small>headlines</small></div><div class="stat"><strong>${num(m.sentiment,2)}</strong><small>sentiment</small></div><div class="stat"><strong>${m.market_reaction_confirms?'Yes':'No'}</strong><small>reaction confirms</small></div></div><h3>Supporting</h3>${evidenceItems(n.evidence,'good')}<h3>Opposing</h3>${evidenceItems(n.counter_evidence,'bad')}<div class="risk-list">${(m.event_risk_headlines||[]).map(x=>`<div class="risk">⚠ ${esc(x)}</div>`).join('')}</div>`;
}
function renderHistory(){
  const h=layer('history'),m=h.metrics||{};
  $('history-panel').innerHTML=`<div class="stat-row"><div class="stat"><strong>${num(m.analog_count,0)}</strong><small>analogs</small></div><div class="stat"><strong>${pct(m.positive_rate)}</strong><small>positive</small></div><div class="stat"><strong>${pct(m.mean_forward_return,1)}</strong><small>mean forward</small></div></div><p>${esc(h.state||'No historical state.')}</p>${evidenceItems(h.evidence,'good','No supporting analog summary.')}<h3>Counterexamples</h3>${evidenceItems(h.counter_evidence,'bad','No counterexamples returned.')}<details><summary>Analog dates</summary><p class="muted">${(m.dates||[]).map(x=>esc(new Date(x).toLocaleDateString())).join(' · ')||'—'}</p></details>`;
}
function renderEvidenceBoard(d){
  const b=d.evidence_board||{},nodes=(b.nodes||[]).slice(0,20),edges=b.edges||[];
  if(!nodes.length){$('evidence-board').innerHTML='<p class="muted">No relationship graph data.</p>';$('board-detail').innerHTML='<p>No graph details.</p>';return;}
  const w=760,h=390,cx=w/2,cy=h/2,r=Math.min(w,h)*.36;
  const assetIndex=Math.max(0,nodes.findIndex(n=>n.id===d.symbol));
  const ordered=[nodes[assetIndex],...nodes.filter((_,i)=>i!==assetIndex)];
  const pos=new Map();pos.set(ordered[0].id,{x:cx,y:cy});
  ordered.slice(1).forEach((n,i)=>{const a=(i/Math.max(ordered.length-1,1))*Math.PI*2-Math.PI/2;pos.set(n.id,{x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r});});
  const visible=new Set(ordered.map(n=>n.id));
  const lines=edges.filter(e=>visible.has(e.from)&&visible.has(e.to)).map(e=>{const a=pos.get(e.from),z=pos.get(e.to),tone=Number(e.sentiment)>.05?'positive':Number(e.sentiment)<-.05?'negative':'';return `<line class="board-edge ${tone}" x1="${a.x}" y1="${a.y}" x2="${z.x}" y2="${z.y}"/>`;}).join('');
  const nodeSvg=ordered.map((n,i)=>{const p=pos.get(n.id),asset=i===0,label=String(n.id).length>19?String(n.id).slice(0,17)+'…':n.id;return `<g class="board-node ${asset?'asset':''}" data-node-index="${i}" transform="translate(${p.x},${p.y})"><circle r="${asset?30:23}"></circle><text text-anchor="middle" dy="4">${esc(label)}</text></g>`;}).join('');
  $('evidence-board').innerHTML=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Evidence relationship graph">${lines}${nodeSvg}</svg>`;
  const show=n=>{const connected=edges.filter(e=>e.from===n.id||e.to===n.id).slice(0,12);$('board-detail').innerHTML=`<h3>${esc(n.id)}</h3>${badge(n.type||'entity',n.type==='asset'?'good':'warn')}<p>${esc(b.warning||'')}</p><h4>Connected evidence</h4>${connected.length?connected.map(e=>`<div class="evidence-item ${Number(e.sentiment)<0?'bad':Number(e.sentiment)>0?'good':''}"><b>${esc(e.from)} → ${esc(e.to)}</b><small>${esc(e.type)} · inferred ${e.inferred?'yes':'no'} · mentions ${e.mentions||1}</small><small>${esc(e.source||'No source title recorded')}</small></div>`).join(''):'<p class="muted">No visible edges.</p>'}`;};
  show(ordered[0]);
  document.querySelectorAll('.board-node').forEach(el=>el.addEventListener('click',()=>show(ordered[Number(el.dataset.nodeIndex)])));
}
function renderNarrative(){
  const n=layer('narrative'),m=n.metrics||{};
  $('narrative-panel').innerHTML=`<div class="stat-row"><div class="stat"><strong>${esc(m.dominant||'No clear narrative')}</strong><small>dominant</small></div><div class="stat"><strong>${esc(m.stage||'unclear')}</strong><small>stage</small></div><div class="stat"><strong>${num(m.sentiment,2)}</strong><small>sentiment</small></div></div>${evidenceItems(n.evidence,'good')}${n.counter_evidence?.length?'<h3>Counter-narrative</h3>'+evidenceItems(n.counter_evidence,'bad'):''}<details><summary>Narrative counts</summary><pre class="technical-block">${esc(JSON.stringify(m.counts||{},null,2))}</pre></details>`;
}
function renderForecast(d){
  const f=d.forecast||{},usable=f.beats_baseline===true;
  $('forecast-panel').innerHTML=`<div class="stat-row"><div class="stat"><strong>${esc(f.state||'unknown')}</strong><small>state</small></div><div class="stat"><strong>${f.expected_return===null||f.expected_return===undefined?'withheld':pct(f.expected_return,1)}</strong><small>expected return</small></div><div class="stat"><strong>${pct(f.confidence)}</strong><small>confidence</small></div></div>${badge(usable?'Beat baseline':'No production influence',usable?'good':'warn')}<p class="simple-only">${usable?'The current Ridge model beat its simple baseline in chronological validation, so it is allowed to contribute.':'The forecast did not earn influence over the final score. Market Compass keeps it visible but gates it out.'}</p><div class="technical-only">${metricCards(f,[['Raw model return','raw_model_return',v=>pct(v,2)],['CV MAE','cv_mae',v=>num(v,5)],['Baseline MAE','baseline_mae',v=>num(v,5)]])}</div>`;
}
function allEvidence(direction){
  const rows=[];Object.values(state.report?.layers||{}).forEach(l=>{const items=direction>0?l.evidence:l.counter_evidence;(items||[]).forEach(e=>rows.push({...e,layer:l.label,weight:Number(e.strength||0)*Number(l.confidence||0)}));});return rows.sort((a,b)=>b.weight-a.weight);
}
function renderContrast(){
  $('bull-case').innerHTML=evidenceItems(allEvidence(1).slice(0,8),'good','No bullish evidence recorded.');
  $('bear-case').innerHTML=evidenceItems(allEvidence(-1).slice(0,8),'bad','No bearish evidence recorded.');
}
function renderInvalidation(d){
  const missing=[];Object.values(d.layers||{}).forEach(l=>(l.missing||[]).forEach(x=>missing.push(`${l.label}: ${x}`)));
  const strongestBear=allEvidence(-1)[0];
  $('invalidation').innerHTML=`<div class="stat-row"><div class="stat"><strong>${d.route?.invalidation?`$${price(d.route.invalidation)}`:'Unclear'}</strong><small>route invalidation</small></div><div class="stat"><strong>${esc(strongestBear?.layer||'No dominant counter-case')}</strong><small>strongest opposition</small></div><div class="stat"><strong>${missing.length}</strong><small>missing-data flags</small></div></div>${strongestBear?`<p><b>Strongest counter-evidence:</b> ${esc(strongestBear.text)}</p>`:''}<div class="missing-grid">${missing.map(x=>`<span class="missing-chip">${esc(x)}</span>`).join('')||'<span class="badge good">No layer-level missing-data flags</span>'}</div>`;
}
function sourceRows(d){
  const m=d.data_meta||{},rows=[['Provider',m.provider],['Requested symbol',m.requested_symbol],['Resolved symbol',m.resolved_symbol],['Retrieved at',m.retrieved_at],['Bars',m.bars]];
  const sources=new Map();Object.values(d.layers||{}).forEach(l=>[...(l.evidence||[]),...(l.counter_evidence||[])].forEach(e=>sources.set(e.source,(sources.get(e.source)||0)+1)));
  sources.forEach((count,source)=>rows.push([`Evidence source · ${source}`,`${count} item${count===1?'':'s'}`]));return rows;
}
function renderExplorer(){
  const d=state.report;if(!d)return;document.querySelectorAll('.explorer-tab').forEach(x=>x.classList.toggle('active',x.dataset.tab===state.tab));
  if(state.tab==='simple'){$('explorer-content').innerHTML=`<h3>${esc(d.action)}</h3><p>${esc(d.summary)}</p><p><b>Next decision condition:</b> route remains valid above/below the stated invalidation while opposing evidence is monitored.</p>`;return;}
  if(state.tab==='technical'){$('explorer-content').innerHTML=`<pre class="technical-block">${esc(d.technical_summary)}</pre><details><summary>Complete report contract</summary><pre class="technical-block">${esc(JSON.stringify(d,null,2))}</pre></details>`;return;}
  if(state.tab==='sources'){$('explorer-content').innerHTML=`<table class="source-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>${sourceRows(d).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(v??'—')}</td></tr>`).join('')}</tbody></table>`;return;}
  if(state.tab==='nodes'){renderNodes();return;}
  if(state.tab==='backtest'){renderBacktest();}
}
async function loadNodes(){if(state.nodes)return state.nodes;const r=await fetch('/api/nodes');if(!r.ok)throw Error('Could not load node registry');state.nodes=await r.json();return state.nodes;}
async function renderNodes(){
  $('explorer-content').innerHTML='<p>Loading 115-node registry…</p>';
  try{const nodes=await loadNodes();const entries=Object.entries(nodes);$('explorer-content').innerHTML=`<div class="node-grid"><div class="node-list">${entries.map(([id,group])=>`<button class="node-button" data-node="${esc(id)}"><b>${esc(id)}</b><span>${esc(group)}</span></button>`).join('')}</div><div><pre id="node-result" class="json-view">Select a node to inspect its current output for ${esc(state.report.symbol)}.</pre></div></div>`;document.querySelectorAll('.node-button').forEach(btn=>btn.addEventListener('click',()=>runNode(btn.dataset.node)));}catch(e){$('explorer-content').innerHTML=`<div class="error">${esc(e.message)}</div>`;}
}
async function runNode(id){const out=$('node-result');out.textContent=`Running ${id}…`;try{const s=encodeURIComponent(state.report.symbol),h=state.report.horizon_days,r=await fetch(`/api/nodes/${encodeURIComponent(id)}?symbol=${s}&horizon=${h}`),d=await r.json();if(!r.ok)throw Error(d.detail||'Node failed');out.textContent=JSON.stringify(d,null,2);}catch(e){out.textContent=e.message;}}
function renderBacktest(){
  $('explorer-content').innerHTML=`<div class="backtest-controls"><p>Run the current research backtest for <b>${esc(state.report.symbol)}</b>. It is a signal-observation test, not a brokerage simulator.</p><button id="run-backtest" class="primary">Run backtest</button></div><div id="backtest-result"></div>`;
  $('run-backtest').addEventListener('click',runBacktest);
}
async function runBacktest(){const out=$('backtest-result');out.innerHTML='<p>Running research backtest…</p>';try{const s=encodeURIComponent(state.report.symbol),h=state.report.horizon_days,r=await fetch(`/api/backtest?symbol=${s}&horizon=${h}`),d=await r.json();if(!r.ok)throw Error(d.detail||'Backtest failed');out.innerHTML=`<div class="stat-row"><div class="stat"><strong>${d.trades}</strong><small>signals</small></div><div class="stat"><strong>${pct(d.win_rate)}</strong><small>win rate</small></div><div class="stat"><strong>${pct(d.mean_return,2)}</strong><small>mean return</small></div></div><pre class="technical-block">${esc(JSON.stringify(d,null,2))}</pre>`;}catch(e){out.innerHTML=`<div class="error">${esc(e.message)}</div>`;}}
function renderAll(d){state.report=d;$('workspace').classList.remove('hidden');renderIdentity(d);renderSummary(d);renderRoute(d);renderChart(d);renderMemory();renderSignals(d);renderNews();renderHistory();renderEvidenceBoard(d);renderNarrative();renderForecast(d);renderContrast();renderInvalidation(d);renderExplorer();}
async function analyze(){
  const symbol=$('symbol').value.trim(),horizon=$('horizon').value;if(!symbol)return;
  $('error').classList.add('hidden');$('workspace').classList.add('hidden');$('run-status').textContent='Collecting evidence…';$('analyze').disabled=true;
  try{const r=await fetch(`/api/analyze?symbol=${encodeURIComponent(symbol)}&horizon=${encodeURIComponent(horizon)}`),d=await r.json();if(!r.ok)throw Error(d.detail||'Analysis failed');renderAll(d);$('run-status').textContent=`Complete · ${new Date(d.as_of).toLocaleTimeString()}`;}catch(e){$('error').textContent=e.message;$('error').classList.remove('hidden');$('run-status').textContent='Analysis failed';}finally{$('analyze').disabled=false;}
}
$('analyze').addEventListener('click',analyze);$('symbol').addEventListener('keydown',e=>{if(e.key==='Enter')analyze();});
document.querySelectorAll('.mode').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.mode').forEach(x=>x.classList.remove('active'));btn.classList.add('active');document.body.classList.toggle('technical-mode',btn.dataset.mode==='technical');}));
document.querySelectorAll('.explorer-tab').forEach(btn=>btn.addEventListener('click',()=>{state.tab=btn.dataset.tab;renderExplorer();}));
analyze();
