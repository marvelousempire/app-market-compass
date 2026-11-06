/* Research Actors bind to the current report; none can score, approve, or trade. */
(() => {
  const actors = {
    omo: { name: 'Omo', mark: 'O', role: 'Evidence Scout', summary: 'Surfaces current catalysts, source age, and counter-evidence without converting headlines into authority.', psychology: 'Evidence-first: prefer named sources, recent timestamps, and explicit counter-evidence; hold when provenance is missing.' },
    prince: { name: 'Prince', mark: 'P', role: 'Scenario Steward', summary: 'Frames route, horizon, bus stops, and invalidation as a research scenario—not a promise or order plan.', psychology: 'Scenario discipline: state the horizon and invalidation first; treat mixed evidence as a reason to wait.' },
    wuda: { name: 'Wuda', mark: 'W', role: 'Trend & Notables Actor', summary: 'Reads directional trend and notable RSI crossings at 35, 50, and 65 from the isolated source lens.', psychology: 'Freshness-sensitive: prefer confirmed directional crossings; never infer a trade from a threshold alone.' },
    'browns-barometers': { name: 'Brown’s Barometers', mark: 'B', role: 'Metrics & Instrument Actor', summary: 'Owns measured market/process metrics and the technical instruments formerly scattered across the app.', psychology: 'Measurement-first: compare timeframes and formulas; distinguish instrument output from outcome probability.' }
  };
  const canvas = document.getElementById('cassette-canvas');
  const tabs = [...document.querySelectorAll('[data-cassette]')];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const fmt = (value, digits = 2) => Number.isFinite(Number(value)) ? Number(value).toFixed(digits) : 'unavailable';
  let active = 'omo';
  let report = null;
  let lens = null;

  function evidenceFor(id) {
    if (!report) return { groups: [{ title: 'Status', items: ['Waiting for the first completed report'] }], evidence: [] };
    const tf = report.timeframes || {};
    if (id === 'omo') {
      const catalysts = (report.catalysts || []).slice(0, 5);
      return {
        groups: [{ title: 'Evidence intake', items: [`${catalysts.length} recent sources`, report.data_meta?.provider || 'provider unavailable', report.data_meta?.resolved_symbol || report.symbol] }, { title: 'Interpretation guard', items: ['Headline ≠ verified fact', 'Counter-evidence retained', 'No score authority'] }],
        evidence: catalysts.map(item => ({ label: item.title, state: item.sentiment > 0 ? 'positive tag' : item.sentiment < 0 ? 'negative tag' : 'neutral tag', detail: `${item.publisher || 'unknown publisher'} · ${fmt(item.age_days, 1)} days old · ${(item.risk_tags || []).join(', ') || 'no risk tag'}`, timestamp: item.published, provenance: item.url }))
      };
    }
    if (id === 'prince') {
      const route = report.route || {};
      return {
        groups: [{ title: 'Scenario', items: [`${report.horizon_days} day horizon`, `${route.direction || 'unclear'} direction`, report.action] }, { title: 'Route controls', items: [`Invalidation ${fmt(route.invalidation)}`, `Reward/risk ${fmt(route.reward_risk)}`, `${(route.next_bus_stops || []).length} next stops`] }],
        evidence: [
          { label: 'Route direction', state: route.direction || 'unclear', detail: `Inputs: price ${fmt(report.price)}; horizon ${report.horizon_days} days`, timestamp: report.as_of, provenance: 'Market Compass route layer' },
          { label: 'Invalidation', state: fmt(route.invalidation), detail: `Next stops: ${(route.next_bus_stops || []).map(value => fmt(value)).join(' · ') || 'none'}`, timestamp: report.as_of, provenance: 'Market Compass route layer' },
          { label: 'Evidence balance', state: report.action, detail: `Bull ${fmt(report.bull_evidence, 0)} · Bear ${fmt(report.bear_evidence, 0)} · confidence ${fmt(report.confidence * 100, 1)}%`, timestamp: report.as_of, provenance: 'Market Compass report' }
        ]
      };
    }
    if (id === 'wuda') {
      const thresholds = lens?.micro_slices?.notable_thresholds || [];
      return {
        groups: [{ title: 'Trends', items: Object.entries(tf).filter(([, value]) => value?.available).map(([name, value]) => `${name.toUpperCase()} ${value.trend_state || 'unclear'}`).slice(0, 4) }, { title: 'Notable thresholds', items: thresholds.map(item => `${item.direction === 'none' ? 'No cross at' : `Crossed ${item.direction}`} ${item.inputs?.threshold}`) }, { title: 'Freshness', items: [lens?.data?.last_bar || report.as_of, lens?.data?.freshness || 'provider-bound', 'Daily timeframe'] }],
        evidence: thresholds.map(item => ({ label: item.label, state: item.state, detail: `${item.evidence} · ${item.timeframe} · ${item.formula}`, timestamp: item.timestamp, provenance: `${item.provenance?.source} @ ${item.provenance?.revision}` }))
      };
    }
    const pack = report.data_meta?.pack_002?.desk || {};
    const setups = lens?.micro_slices?.setup_scanner?.filter(item => item.owner === "Brown's Barometers") || [];
    return {
      groups: [{ title: 'Metrics', items: [`Breadth ${fmt(report.bull_evidence, 0)}/${fmt(report.bear_evidence, 0)}`, `Momentum ${tf['1d']?.momentum_state || tf['4h']?.momentum_state || 'unavailable'}`, `Volume ${fmt(pack.supply?.volume_vs_avg, 2)}× average`, `Confidence ${fmt(report.confidence * 100, 1)}%`] }, { title: 'Measuring tools', items: [`RSI14 ${fmt(pack.rsi?.rsi14, 1)}`, `SMA20 ${fmt(pack.sma_stack?.sma20)}`, `SMA50 ${fmt(pack.sma_stack?.sma50)}`, 'MACD', 'ATR', 'Bollinger Bands'] }, { title: 'View governance', items: ['Inputs before conclusions', 'Daily and multi-timeframe context', 'Formula receipt required'] }],
      evidence: setups.map(item => ({ label: item.label, state: item.state, detail: `${item.evidence} · ${item.formula}`, timestamp: item.timestamp, provenance: `${item.provenance?.source} @ ${item.provenance?.revision}` }))
    };
  }

  function receiptFor(id) {
    const actor = actors[id];
    return { schema: 'market-compass.actor-receipt.v1', actor: actor.name, role: actor.role, symbol: report?.symbol || null, timeframe: id === 'wuda' ? '1D' : `${report?.horizon_days || 'unbound'} day report`, timestamp: report?.as_of || null, provenance: { report_provider: report?.data_meta?.provider || null, source_lens: lens?.source || null }, confidence: { value: report?.confidence ?? null, meaning: 'report evidence confidence; not outcome probability' }, inputs: evidenceFor(id), source_receipt: lens?.receipt || report?.data_meta?.pack_002?.receipt || null, authority: { research_only: true, signal_generation: true, score_influence: false, trade_execution: false, money_movement: false } };
  }

  function exportReceipt(id) {
    const payload = JSON.stringify(receiptFor(id), null, 2);
    const url = URL.createObjectURL(new Blob([payload], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url; link.download = `market-compass-${id}-${report?.symbol || 'unbound'}-receipt.json`;
    document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
  }

  function render(id) {
    active = id;
    const actor = actors[id];
    const data = evidenceFor(id);
    const groups = data.groups.map(group => `<section class="cassette-tool-group"><h4>${esc(group.title)}</h4><div class="cassette-tools">${(group.items.length ? group.items : ['No current observations']).map(item => `<span>${esc(item)}</span>`).join('')}</div></section>`).join('');
    const evidence = data.evidence.map(item => `<article class="actor-evidence"><div><b>${esc(item.label)}</b><span>${esc(item.state)}</span></div><p>${esc(item.detail)}</p><small>${esc(item.timestamp || 'timestamp unavailable')} · ${esc(item.provenance || 'provenance unavailable')}</small></article>`).join('') || '<p class="muted">No current evidence rows. Complete an analysis to populate this Actor.</p>';
    canvas.innerHTML = `<div class="cassette-mark" aria-hidden="true">${actor.mark}</div><p class="eyebrow">${esc(actor.name.toUpperCase())} · ACTOR SPACE</p><h3>${esc(actor.name)}</h3><p>${esc(actor.summary)}</p><section class="actor-comp-card" aria-label="${esc(actor.name)} comp card"><div><span>Actor</span><strong>${esc(actor.name)}</strong></div><div><span>Role</span><strong>${esc(actor.role)}</strong></div><div><span>Trading psychology</span><strong>${esc(actor.psychology)}</strong></div><div><span>Authority</span><strong>Research and signals only · no scores or execution</strong></div><div><span>Current asset</span><strong>${esc(report?.symbol || 'Loading…')}</strong></div><div><span>As of</span><strong>${esc(report?.as_of ? new Date(report.as_of).toLocaleString() : 'waiting for report')}</strong></div></section><div class="cassette-tool-groups">${groups}</div><div class="actor-actions"><button type="button" class="secondary" data-actor-evidence>View evidence</button><button type="button" class="secondary" data-actor-export ${report ? '' : 'disabled'}>Export receipt</button></div><section class="actor-evidence-list" hidden aria-label="${esc(actor.name)} evidence">${evidence}</section><small>Inputs, formula context, timeframe, timestamp, provenance, and confidence travel with exported receipts.</small>`;
    canvas.querySelector('[data-actor-evidence]').addEventListener('click', event => { const root = canvas.querySelector('.actor-evidence-list'); root.hidden = !root.hidden; event.currentTarget.textContent = root.hidden ? 'View evidence' : 'Hide evidence'; if (!root.hidden) root.scrollIntoView({ block: 'nearest' }); });
    canvas.querySelector('[data-actor-export]').addEventListener('click', () => exportReceipt(id));
    tabs.forEach(tab => { const selected = tab.dataset.cassette === id; tab.classList.toggle('active', selected); tab.setAttribute('aria-selected', String(selected)); });
  }

  async function bindReport(nextReport) {
    report = nextReport; lens = null; render(active);
    try {
      const response = await fetch(`/api/research-lenses/day-trader/${encodeURIComponent(report.symbol)}`, { headers: { Accept: 'application/json' } });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || 'Lens unavailable');
      lens = payload;
    } catch (error) { lens = { error: error.message, micro_slices: { setup_scanner: [], notable_thresholds: [] } }; }
    render(active);
  }

  tabs.forEach(tab => tab.addEventListener('click', () => render(tab.dataset.cassette)));
  window.addEventListener('marketcompassreport', event => bindReport(event.detail.report));
  render(active);
})();
