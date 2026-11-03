/* intelTHAT independent research receipt panel. Never sends an order. */
document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('intelthat-load');
  const root = document.getElementById('intelthat-output');
  const symbolField = document.getElementById('symbol');
  if (!button || !root || !symbolField) return;

  const el = (tag, text, cls) => {
    const node = document.createElement(tag);
    node.textContent = String(text ?? '');
    if (cls) node.className = cls;
    return node;
  };

  function show(data) {
    root.replaceChildren();
    const stats = data.proof_health || {};
    root.appendChild(el('p',
      'Proof health: ' + ['observed', 'held', 'excluded', 'missing']
        .map(key => key + ' ' + (stats[key] ?? 0)).join(' · ')));
    if (!data.configured) {
      root.appendChild(el('p',
        'The intelTHAT runs directory has not been configured on this server. Set MARKET_COMPASS_INTELTHAT_DIR before launching the app.'));
    }
    const grid = el('div', '', 'intelthat-grid');
    for (const kind of ['pack', 'macro', 'rss', 'edgar']) {
      const item = data.sources?.[kind] || {};
      const card = el('article', '', 'intelthat-card');
      card.appendChild(el('h3', kind.toUpperCase() + ' · ' + (item.state || 'unknown')));
      card.appendChild(el('p', item.reason || 'No receipt found.'));
      if (item.as_of) card.appendChild(el('small', 'Source as of: ' + item.as_of));
      if (item.sha256) card.appendChild(el('small', 'File SHA-256: ' + item.sha256.slice(0, 16) + '…'));
      const info = el('dl');
      for (const [label, value] of Object.entries(item.metrics || {})) {
        info.appendChild(el('dt', label));
        info.appendChild(el('dd', value));
      }
      card.appendChild(info);
      grid.appendChild(card);
    }
    root.appendChild(grid);
  }

  button.addEventListener('click', async () => {
    const symbol = symbolField.value.trim();
    if (!symbol) return;
    button.disabled = true;
    root.replaceChildren(el('p', 'Reading local intelTHAT research receipts…'));
    try {
      const response = await fetch('/api/intelthat/' + encodeURIComponent(symbol), {
        headers: { Accept: 'application/json' }, credentials: 'same-origin'
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Receipt request refused.');
      show(data);
    } catch (err) {
      root.replaceChildren(el('p', 'Source unavailable: ' + err.message));
    } finally {
      button.disabled = false;
    }
  });
});
