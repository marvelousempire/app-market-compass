/* GitThat preview controls. Localhost-only; never enables trading or forge promotion. */
(() => {
  const $ = id => document.getElementById(id);
  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);
  const state = $('operator-state');
  const result = $('operator-result');

  function setState(label, kind) { state.textContent = label; state.dataset.state = kind; }
  function show(title, payload) {
    let summary = '';
    let facts = [];
    if (payload.steps) {
      summary = 'The research preview is ready. These are the steps it will follow:';
      facts = payload.steps;
    } else if (payload.runtime && payload.research) {
      const proof = payload.research.proof_health || {};
      summary = `Market Compass is running. Research for ${payload.research.symbol || 'this asset'} has ${proof.observed || 0} observed and ${proof.missing || 0} missing source modules.`;
      facts = [payload.research.configured ? 'Research sources are configured.' : 'Research sources are not configured yet.', 'Trading is disabled.'];
    } else if (payload.state === 'held' || payload.reason) {
      summary = payload.reason || 'This action needs attention.';
    } else if (payload.state === 'opened') {
      summary = 'Opened another local Market Compass view.';
    } else if (payload.state === 'stopping') {
      summary = 'The local research preview is stopping.';
    } else {
      summary = payload.message || (payload.state === 'live' ? 'Market Compass is running on this Mac.' : 'The local research preview is ready.');
      facts = [payload.mode === 'research_only' ? 'Research only. Trading is disabled.' : '', payload.commissioned ? 'Running the approved main source.' : 'Source promotion is unavailable here.'].filter(Boolean);
    }
    result.innerHTML = `<h3>${escapeHtml(title)}</h3><p>${escapeHtml(summary)}</p>${facts.length ? `<ul>${facts.map(fact => `<li>${escapeHtml(fact)}</li>`).join('')}</ul>` : ''}`;
    result.focus({ preventScroll: true });
  }
  async function request(path, options) {
    const response = await fetch(path, options);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || `Request failed (${response.status})`);
    return payload;
  }
  async function run(action, button) {
    button.disabled = true;
    setState('Working…', 'busy');
    try {
      if (action === 'open') {
        window.open('/', '_blank', 'noopener');
        show('Live preview', { state: 'opened', address: 'http://market-compass.localhost/', local_only: true });
      } else if (action === 'stop') {
        if (!window.confirm('Stop this local preview? Trading is already off. GitThat can relaunch it later.')) {
          setState('Live · research only', 'live');
          return;
        }
        const payload = await request('/api/operator/stop', { method: 'POST' });
        show('Stopping safely', payload);
        setState('Stopping…', 'stopping');
        document.querySelectorAll('[data-operator-action]').forEach(control => { control.disabled = true; });
        return;
      } else {
        const symbol = document.getElementById('symbol')?.value?.trim() || 'QQQ';
        const routes = {
          plan: '/api/operator/plan', status: '/api/operator/status',
          launch: '/api/operator/launch',
          receipts: `/api/operator/receipts?symbol=${encodeURIComponent(symbol)}`
        };
        const payload = await request(routes[action], action === 'launch' ? { method: 'POST' } : undefined);
        show(button.querySelector('strong').textContent, payload);
      }
      setState('Live · research only', 'live');
    } catch (error) {
      setState('Needs attention', 'error');
      show('Action held', { state: 'held', reason: error.message, trade_execution: false });
    } finally {
      if (action !== 'stop') button.disabled = false;
    }
  }
  document.querySelectorAll('[data-operator-action]').forEach(button => {
    button.addEventListener('click', () => run(button.dataset.operatorAction, button));
  });
  request('/api/operator/status').then(payload => {
    setState('Live · research only', 'live');
    result.dataset.ready = 'true';
    const source = payload.commissioned
      ? `Canonical Gitea source ${payload.source_revision}`
      : 'Gitea promotion is unavailable here';
    result.querySelector('p').textContent = `Ready on ${payload.host}. Trading stays off; ${source}.`;
  }).catch(error => {
    setState('Needs attention', 'error');
    show('Runtime check held', { reason: error.message });
  });
})();
