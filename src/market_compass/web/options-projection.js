/* Hypothetical European-option projection. Does not use or imply live quotes. */
(() => {
  const el = id => document.getElementById(id);
  const fmt = n => new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}).format(n);
  const normal = x => {
    const a = Math.abs(x), t = 1 / (1 + .2316419 * a);
    const pdf = Math.exp(-a*a/2) / Math.sqrt(2*Math.PI);
    const c = 1 - pdf * (.319381530*t - .356563782*t*t + 1.781477937*t**3 - 1.821255978*t**4 + 1.330274429*t**5);
    return x < 0 ? 1-c : c;
  };
  const pdf = x => Math.exp(-x*x/2)/Math.sqrt(2*Math.PI);
  const model = (s,k,d,iv,typ) => {
    if (d <= 0) return Math.max(0, typ === 'call' ? s-k : k-s);
    const t=d/365, v=iv/100, r=.04, root=Math.sqrt(t);
    const d1=(Math.log(s/k)+(r+v*v/2)*t)/(v*root), d2=d1-v*root;
    return typ==='call' ? s*normal(d1)-k*Math.exp(-r*t)*normal(d2) : k*Math.exp(-r*t)*normal(-d2)-s*normal(-d1);
  };
  const baseDays = () => Math.max(0, Math.ceil((new Date(el('expiry').value+'T16:00:00')-new Date())/86400000));
  const quote = (s,k,d,iv,typ) => Math.round(model(s,k,d,iv,typ)*100)/100;
  const projected = () => ({s:Number(el('projected-spot').value),d:Number(el('projected-days').value),iv:Number(el('projected-iv').value)});
  const updateLimits = () => {
    const spot=assets[asset], max=baseDays(), slider=el('projected-spot');
    slider.min=(spot*.5).toFixed(2);slider.max=(spot*1.5).toFixed(2);slider.value=spot;
    el('projected-days').max=max;el('projected-days').value=max;
  };
  const oldRender = render;
  premium = s => Math.max(.01, quote(assets[asset],s,baseDays(),30,kind));
  payoff = x => {
    const q=Number(el('quantity').value||1), side=el('side').value==='buy'?1:-1;
    const {d,iv}=projected();
    return (quote(x,strike,d,iv,kind)-premium(strike))*100*q*side;
  };
  draw = () => {
    const svg=el('chart');
    if (strike===null) {svg.innerHTML='<text x="20" y="110">Select a contract to preview returns</text>';return;}
    const {s,d,iv}=projected(), spot=assets[asset], priceAxis=el('axis').value==='price', maxDays=baseDays();
    const x0=priceAxis?spot*.5:0, x1=priceAxis?spot*1.5:Math.max(1,maxDays);
    const points=Array.from({length:101},(_,i)=>{
      const x=x0+(x1-x0)*i/100;
      return {x,y:priceAxis?(quote(x,strike,d,iv,kind)-premium(strike))*100*Number(el('quantity').value||1)*(el('side').value==='buy'?1:-1):(quote(s,strike,x,iv,kind)-premium(strike))*100*Number(el('quantity').value||1)*(el('side').value==='buy'?1:-1)};
    });
    const bound=Math.max(100,...points.map(p=>Math.abs(p.y))), px=x=>35+(x-x0)/(x1-x0)*425, py=y=>110-y/bound*88;
    const line=points.map((p,i)=>(i?'L':'M')+px(p.x).toFixed(1)+' '+py(p.y).toFixed(1)).join(' ');
    const cursor=px(priceAxis?s:d), current=payoff(s);
    svg.innerHTML=`<line x1="35" y1="110" x2="460" y2="110" stroke="#587465"/><path d="${line}" fill="none" stroke="#a8ee83" stroke-width="3"/><line x1="${cursor}" y1="18" x2="${cursor}" y2="198" stroke="#eaf0ed" stroke-dasharray="4 4"/><circle cx="${cursor}" cy="${py(current)}" r="5" fill="#eaf0ed"/><text x="35" y="215">${priceAxis?fmt(x0):'Expiration'}</text><text x="400" y="215">${priceAxis?fmt(x1):maxDays+' days'}</text><text x="38" y="28">+${fmt(bound)}</text><text x="38" y="190">−${fmt(bound)}</text>`;
    svg.setAttribute('aria-label',`Projected profit and loss ${priceAxis?'across underlying prices':'across time'}, selected return ${fmt(current)}`);
  };
  render = () => {oldRender(); const {s,d,iv}=projected();
    el('projected-spot-label').textContent=fmt(s);el('projected-days-label').textContent=d+' days';el('projected-iv-label').textContent=iv+'%';
    if(strike===null){el('projected-value').textContent='—';el('projected-return').textContent='—';el('projected-percent').textContent='—';el('greeks').textContent='Select a contract to see sensitivity.';return;}
    const current=premium(strike), future=quote(s,strike,d,iv,kind), gain=payoff(s), initial=current*100*Number(el('quantity').value||1);
    el('projected-value').textContent=fmt(future);el('projected-return').textContent=fmt(gain);el('projected-return').className=gain<0?'danger':'tag';el('projected-percent').textContent=(gain/initial*100).toFixed(1)+'%';
    const delta=(model(assets[asset]+.01,strike,baseDays(),30,kind)-model(assets[asset]-.01,strike,baseDays(),30,kind))/.02;
    const theta=(model(assets[asset],strike,Math.max(0,baseDays()-1),30,kind)-current);
    const vega=(model(assets[asset],strike,baseDays(),31,kind)-current);
    el('greeks').textContent=`Approximate sensitivity per share · Δ ${delta.toFixed(3)} · 1 day ${fmt(theta)} · IV +1 point ${fmt(vega)}`;
  };
  updateLimits();
  for(const id of ['projected-spot','projected-days','projected-iv','axis'])el(id).addEventListener('input',render);
  el('asset').addEventListener('change',()=>{updateLimits();render()});
  el('expiry').addEventListener('change',()=>{updateLimits();render()});
  render();
})();
