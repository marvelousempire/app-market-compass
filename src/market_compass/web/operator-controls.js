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
    result.innerHTML = `<h3>${escapeHtml(title)}</h3><pre>${escapeHtml(JSON.stringify(payload, null, 2))}</pre>`;
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
        show('Live preview', { state: 'opened', address: 'http://127.0.0.1:8000', local_only: true });
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
    result.querySelector('p').textContent = `Ready on ${payload.host}. Trading stays off; Gitea promotion is unavailable here.`;
  }).catch(error => {
    setState('Needs attention', 'error');
    show('Runtime check held', { reason: error.message });
  });
})();
