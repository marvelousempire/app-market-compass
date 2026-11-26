(()=>{
  let latest=null;
  const human=window.MarketCompassHuman;
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const rule=value=>String(value??'').replace(/>=\s*([\d.]+)/g,'at least $1').replace(/<=\s*([\d.]+)/g,'at most $1').replace(/\bnone\b/gi,'no gaps');
  const render=data=>{
    const state=document.getElementById('decision-gate-state');
    const grid=document.getElementById('decision-gate-grid');
    const formula=document.getElementById('calculate-that-formula');
    const next=document.getElementById('decision-gate-next');
    if(!state||!grid||!formula||!next)return;
    const tone=data.state==='DO_NOT_GO_SIGNAL'?'stop':data.state==='GO_SIGNAL'?'ready':'review';
    state.className=`gate-state ${tone}`;state.textContent=data.state==='GO_SIGNAL'?'Ready for research review':data.state==='DO_NOT_GO_SIGNAL'?'Do not proceed':'Needs review';
    grid.innerHTML=(data.gates||[]).map(g=>`<article class="gate-card ${g.passed?'pass':'fail'}"><strong>${esc(g.label)}</strong><i>${g.passed?'Met':'Needs attention'}</i><small>Current: ${esc(human.value(g.actual))}</small><small>Needed: ${esc(rule(g.requirement))}${g.hard_stop?' · required to proceed':''}</small></article>`).join('');
    formula.textContent=`Research signals: Active\nDirection: ${human.value(data.signal?.direction)}\nPositive evidence: ${human.value(data.signal?.bull_evidence)}\nNegative evidence: ${human.value(data.signal?.bear_evidence)}\nConfidence: ${human.value(data.signal?.confidence)}\nEvidence balance: ${human.value(data.formula?.evidence_edge_value)}\nReadiness: ${human.value(data.formula?.readiness)}\nScores cannot be changed here. Orders cannot be placed here.`;
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
