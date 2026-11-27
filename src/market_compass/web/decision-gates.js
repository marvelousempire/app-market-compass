(()=>{
  let latest=null;
  const human=window.MarketCompassHuman;
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const rule=value=>String(value??'').replace(/>=\s*([\d.]+)/g,'at least $1').replace(/<=\s*([\d.]+)/g,'at most $1').replace(/\bnone\b/gi,'no gaps');
  const money=value=>Number.isFinite(Number(value))&&value!=null?Number(value).toLocaleString(undefined,{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}):'Unavailable';
  const percent=value=>Number.isFinite(Number(value))?`${(Number(value)*100).toFixed(1)}%`:'Unavailable';
  const fact=(label,value)=>`<div class="decision-fact"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`;
  const render=data=>{
    const state=document.getElementById('decision-gate-state');
    const grid=document.getElementById('decision-gate-grid');
    const formula=document.getElementById('calculate-that-formula');
    const reality=document.getElementById('decision-trade-context');
    const next=document.getElementById('decision-gate-next');
    if(!state||!grid||!formula||!reality||!next)return;
    const tone=data.state==='DO_NOT_GO_SIGNAL'?'stop':data.state==='GO_SIGNAL'?'ready':'review';
    state.className=`gate-state ${tone}`;state.textContent=data.state==='GO_SIGNAL'?'Ready for research review':data.state==='DO_NOT_GO_SIGNAL'?'Do not proceed':'Needs review';
    grid.innerHTML=(data.gates||[]).map(g=>`<article class="gate-card ${g.passed?'pass':'fail'}"><strong>${esc(g.label)}</strong><i>${g.passed?'Met':'Needs attention'}</i><small>Current: ${esc(human.value(g.actual).replace(/marketCap/g,'market capitalization'))}</small><small>Needed: ${esc(rule(g.requirement))}${g.hard_stop?' · required to proceed':''}</small></article>`).join('');
    const context=data.trade_context||{};
    reality.innerHTML=`<div class="decision-facts">${fact('Study close',money(context.current_price))}${fact('Route direction',human.label(context.direction||'unclear'))}${fact('Next route level',money(context.next_route_level))}${fact('Invalidation level',money(context.invalidation))}${fact('Reward to risk',context.reward_risk==null?'Unavailable':`${Number(context.reward_risk).toFixed(2)} to 1`)}</div><p class="decision-context-note">${esc(data.symbol)} · session ${esc(context.as_of||'unavailable')} · ${esc(human.label(context.provider||'source unavailable'))}. Levels are research references, not an order or a promised outcome.</p>`;
    const direction={BULLISH:'More positive evidence',BEARISH:'More negative evidence',NEUTRAL:'Evidence is balanced'}[data.signal?.direction]||'Direction unavailable';
    formula.innerHTML=`<p class="decision-direction">${esc(direction)}</p><div class="decision-facts">${fact('Positive evidence',human.value(data.signal?.bull_evidence))}${fact('Negative evidence',human.value(data.signal?.bear_evidence))}${fact('Evidence gap',`${human.value(data.formula?.evidence_edge_value)} points`)}${fact('Evidence confidence',percent(data.signal?.confidence))}</div><p class="decision-context-note">Confidence describes the evidence, not the chance of a profitable trade. A failed required check blocks a go signal.</p>`;
    next.textContent=data.next_action||'Review the gates.';
    latest=data;const exportButton=document.getElementById('calculate-that-export');if(exportButton)exportButton.disabled=!data.receipt?.exportable;
  };
  const load=async()=>{
    const root=document.getElementById('decision-gates');if(!root)return;
    const symbol=document.getElementById('symbol')?.value?.trim()||'BB';
    const horizon=document.getElementById('horizon')?.value||20;
    root.setAttribute('aria-busy','true');
    try{const response=await fetch(`/api/decision-readiness?symbol=${encodeURIComponent(symbol)}&horizon=${encodeURIComponent(horizon)}`);const data=await response.json();if(!response.ok)throw new Error(data.detail||'Readiness calculation failed');render(data);}catch(error){document.getElementById('decision-gate-next').textContent=error.message;}finally{root.setAttribute('aria-busy','false');}
  };
  const exportReceipt=()=>{if(!latest)return;const url=URL.createObjectURL(new Blob([JSON.stringify(latest,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download=`market-compass-${latest.symbol}-signal-receipt.json`;document.body.appendChild(link);link.click();link.remove();URL.revokeObjectURL(url);};
  document.addEventListener('DOMContentLoaded',()=>{document.getElementById('calculate-that-run')?.addEventListener('click',load);document.getElementById('calculate-that-export')?.addEventListener('click',exportReceipt);document.getElementById('analyze')?.addEventListener('click',()=>setTimeout(load,0));load();});
})();
