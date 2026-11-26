/* Hypothetical European-option projection. Does not use or imply live quotes. */
(async () => {
  const el = id => document.getElementById(id);
  const fmt = n => new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}).format(n);
  const controls=['asset','expiry','side','quantity','projected-spot','projected-days','projected-iv','axis'];
  controls.forEach(id => { el(id).disabled=true; });
  let wasm;
  try {
    const response=await fetch('/static/options_engine.wasm',{cache:'no-store'});
    if(!response.ok) throw new Error('Rust engine asset unavailable');
    const instance=await WebAssembly.instantiate(await response.arrayBuffer());
    wasm=instance.instance.exports;
    if(wasm.market_compass_engine_abi?.()!==1 || typeof wasm.option_price!=='function' || typeof wasm.option_return!=='function') throw new Error('Rust engine contract mismatch');
  } catch (error) {
    el('notice').textContent='Options projection unavailable: '+error.message;
    return;
  }
  const flag = typ => typ==='call'?0:1;
  const model=(s,k,d,iv,typ)=>wasm.option_price(s,k,d,iv,flag(typ));
  const baseDays = () => Math.max(0, Math.ceil((new Date(el('expiry').value+'T16:00:00')-new Date())/86400000));
  const quote = (s,k,d,iv,typ) => wasm.option_quote(s,k,d,iv,flag(typ));
  const projected = () => ({s:Number(el('projected-spot').value),d:Number(el('projected-days').value),iv:Number(el('projected-iv').value)});
  const updateLimits = () => {
    const spot=assets[asset], max=baseDays(), slider=el('projected-spot'); if(!Number.isFinite(spot)) return;
    slider.min=(spot*.5).toFixed(2);slider.max=(spot*1.5).toFixed(2);slider.step=spot<20?'0.05':spot<100?'0.25':'0.5';slider.value=spot;
    el('projected-days').max=max;el('projected-days').value=max;
  };
  const oldRender = render;
  premium = s => quote(assets[asset],s,baseDays(),30,kind);
  payoff = x => {
    const {d,iv}=projected();
    return wasm.option_return(assets[asset],x,strike,baseDays(),d,30,iv,flag(kind),el('side').value==='buy'?1:-1,Number(el('quantity').value||1));
  };
  draw = () => {
    const svg=el('chart');
    if (strike===null) {svg.innerHTML='<text x="20" y="110">Select a contract to preview returns</text>';return;}
    const {s,d,iv}=projected(), spot=assets[asset], priceAxis=el('axis').value==='price', maxDays=baseDays();
    const x0=priceAxis?spot*.5:0, x1=priceAxis?spot*1.5:Math.max(1,maxDays);
    const points=Array.from({length:101},(_,i)=>{
      const x=x0+(x1-x0)*i/100;
      return {x,y:priceAxis?wasm.option_return(spot,x,strike,maxDays,d,30,iv,flag(kind),el('side').value==='buy'?1:-1,Number(el('quantity').value||1)):wasm.option_return(spot,s,strike,maxDays,x,30,iv,flag(kind),el('side').value==='buy'?1:-1,Number(el('quantity').value||1))};
    });
    const bound=Math.max(100,...points.map(p=>Math.abs(p.y))), px=x=>35+(x-x0)/(x1-x0)*425, py=y=>110-y/bound*88;
    const line=points.map((p,i)=>(i?'L':'M')+px(p.x).toFixed(1)+' '+py(p.y).toFixed(1)).join(' ');
    const cursor=px(priceAxis?s:d), current=payoff(s);
    svg.innerHTML=`<line x1="35" y1="110" x2="460" y2="110" stroke="var(--mc-line)"/><path d="${line}" fill="none" stroke="var(--mc-brand)" stroke-width="3"/><line x1="${cursor}" y1="18" x2="${cursor}" y2="198" stroke="var(--mc-ink)" stroke-dasharray="4 4"/><circle cx="${cursor}" cy="${py(current)}" r="5" fill="var(--mc-ink)"/><text x="35" y="215">${priceAxis?fmt(x0):'Expiration'}</text><text x="400" y="215">${priceAxis?fmt(x1):maxDays+' days'}</text><text x="38" y="28">+${fmt(bound)}</text><text x="38" y="190">−${fmt(bound)}</text>`;
    svg.setAttribute('aria-label',`Projected profit and loss ${priceAxis?'across underlying prices':'across time'}, selected return ${fmt(current)}`);
  };
  render = () => {oldRender(); const {s,d,iv}=projected();
    el('projected-spot-label').textContent=fmt(s);el('projected-days-label').textContent=d+' days';el('projected-iv-label').textContent=iv+'%';
    if(strike===null){el('projected-value').textContent='—';el('projected-return').textContent='—';el('projected-percent').textContent='—';el('greeks').textContent='Select a contract to see sensitivity.';return;}
    const current=premium(strike), future=quote(s,strike,d,iv,kind), gain=payoff(s), initial=current*100*Number(el('quantity').value||1);
    el('projected-value').textContent=fmt(future);el('projected-return').textContent=fmt(gain);el('projected-return').className=gain<0?'danger':'tag';el('projected-percent').textContent=(gain/initial*100).toFixed(1)+'%';
    const delta=wasm.option_delta(assets[asset],strike,baseDays(),30,flag(kind));
    const theta=wasm.option_theta_day(assets[asset],strike,baseDays(),30,flag(kind));
    const vega=wasm.option_vega_point(assets[asset],strike,baseDays(),30,flag(kind));
    el('greeks').textContent=`Approximate sensitivity per share · Δ ${delta.toFixed(3)} · 1 day ${fmt(theta)} · IV +1 point ${fmt(vega)}`;
  };
  updateLimits();
  for(const id of ['projected-spot','projected-days','projected-iv','axis'])el(id).addEventListener('input',render);
  el('asset').addEventListener('change',()=>{updateLimits();render()});
  el('expiry').addEventListener('change',()=>{updateLimits();render()});
  controls.forEach(id => { el(id).disabled=id==='asset'||!Number.isFinite(assets[asset]); });
  render();
  window.addEventListener('marketcompassasset', () => {updateLimits(); controls.forEach(id => {el(id).disabled=id==='asset'||!Number.isFinite(assets[asset]);}); render();});
})();
