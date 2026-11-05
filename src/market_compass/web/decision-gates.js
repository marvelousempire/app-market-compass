(()=>{
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const render=data=>{
    const state=document.getElementById('decision-gate-state');
    const grid=document.getElementById('decision-gate-grid');
    const formula=document.getElementById('calculate-that-formula');
    const next=document.getElementById('decision-gate-next');
    if(!state||!grid||!formula||!next)return;
    const tone=data.state==='DO_NOT_GO_SIGNAL'?'stop':data.state==='GO_SIGNAL'?'ready':'review';
    state.className=`gate-state ${tone}`;state.textContent=data.state.replaceAll('_',' ');
    grid.innerHTML=(data.gates||[]).map(g=>`<article class="gate-card ${g.passed?'pass':'fail'}"><strong>${esc(g.label)}</strong><i>${g.passed?'PASS':'HOLD'}</i><small>Actual: ${esc(typeof g.actual==='object'?JSON.stringify(g.actual):g.actual)}</small><small>Rule: ${esc(g.requirement)}${g.hard_stop?' · hard stop':''}</small></article>`).join('');
    formula.textContent=`signal generation = ACTIVE\ndirection = ${data.signal?.direction || '—'}\nbull / bear = ${data.signal?.bull_evidence ?? '—'} / ${data.signal?.bear_evidence ?? '—'}\nconfidence = ${data.signal?.confidence ?? '—'}\nevidence edge = ${data.formula?.evidence_edge_value ?? '—'}\nreadiness = ${data.formula?.readiness || '—'}\nscore mutation = off\nbroker execution = unavailable`;
    next.textContent=data.next_action||'Review the gates.';
  };
  const load=async()=>{
    const root=document.getElementById('decision-gates');if(!root)return;
    const symbol=document.getElementById('symbol')?.value?.trim()||'BB';
    const horizon=document.getElementById('horizon')?.value||20;
    root.setAttribute('aria-busy','true');
    try{const response=await fetch(`/api/decision-readiness?symbol=${encodeURIComponent(symbol)}&horizon=${encodeURIComponent(horizon)}`);const data=await response.json();if(!response.ok)throw new Error(data.detail||'Readiness calculation failed');render(data);}catch(error){document.getElementById('decision-gate-next').textContent=error.message;}finally{root.setAttribute('aria-busy','false');}
  };
  document.addEventListener('DOMContentLoaded',()=>{document.getElementById('calculate-that-run')?.addEventListener('click',load);document.getElementById('analyze')?.addEventListener('click',()=>setTimeout(load,0));load();});
})();
