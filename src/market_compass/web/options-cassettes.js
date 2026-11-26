/* One retained Options Lab document; each right-rail section owns the canvas. */
(() => {
  const byId = id => document.getElementById(id);
  const chain = byId('chain').closest('.card');
  const builder = byId('place').closest('.card');
  const returns = document.createElement('section');
  returns.className = 'card options-cassette';
  returns.id = 'returns-cassette';
  returns.innerHTML = '<h2>Simulate returns</h2><p class="muted">Change price, time, and volatility for the selected single option.</p>';
  returns.append(builder.querySelector('.projection-controls'), byId('chart'));
  returns.querySelector('.projection-controls .row.between strong')?.remove();
  builder.after(returns);
  const panels = {
    chain, builder, returns, strategies: byId('strategy-panel'),
    alpaca: byId('alpaca-context').closest('.card'),
    edgar: byId('edgar-context').closest('.card'),
    positions: byId('positions').closest('.card'),
    journal: byId('journal').closest('.card')
  };
  const stage = chain.parentElement;
  stage.classList.add('options-cassette-stage');
  chain.insertAdjacentHTML('afterbegin', '<h2>Option chain</h2>');
  for (const panel of Object.values(panels)) stage.append(panel);
  document.querySelector('.context-grid').hidden = true;
  document.querySelector('.below').hidden = true;
  for (const [name, panel] of Object.entries(panels)) {
    panel.classList.add('options-cassette');
    panel.dataset.optionsCassette = name;
  }
  const focusTargets = {
    chain: {expiry:'#expiry', types:'#types', strikes:'#chain'},
    builder: {action:'#side', risk:'.quote', order:'#place'},
    returns: {scenario:'#projected-spot', volatility:'#projected-iv', chart:'#chart'},
    strategies: {legs:'#strategy-kind', risk:'.strategy-metrics', chart:'#strategy-chart'},
    alpaca: {quote:'#alpaca-context', refresh:'#context-refresh'},
    edgar: {filings:'#edgar-context'},
    positions: {open:'#positions'},
    journal: {entries:'#journal'}
  };
  let current = 'chain';
  function select(view, focus) {
    if (!Object.hasOwn(panels, view)) return;
    current = view;
    for (const [name, panel] of Object.entries(panels)) panel.hidden = name !== view;
    byId('mode-single').classList.toggle('active', view !== 'strategies');
    byId('mode-strategy').classList.toggle('active', view === 'strategies');
    byId('mode-single').setAttribute('aria-pressed', String(view !== 'strategies'));
    byId('mode-strategy').setAttribute('aria-pressed', String(view === 'strategies'));
    document.body.dataset.optionsCassette = view;
    const target = focus && document.querySelector(focusTargets[view]?.[focus]);
    if (target) target.scrollIntoView({block:'start'});
    else document.scrollingElement?.scrollTo({top:0});
    parent.postMessage({type:'market-compass-options-view',view},location.origin);
    parent.postMessage({type:'market-compass-options-height',height:document.documentElement.scrollHeight},location.origin);
  }
  window.addEventListener('marketcompassoptionscassette', event => select(event.detail?.view,event.detail?.focus));
  select(current);
})();
