/* Native intelTHAT research workspace. Never authenticates a broker or sends an order. */
document.addEventListener('DOMContentLoaded', () => {
  const refresh = document.getElementById('intelthat-load');
  const local = document.getElementById('intelthat-local');
  const exportButton = document.getElementById('intelthat-export');
  const filter = document.getElementById('intelthat-filter');
  const root = document.getElementById('intelthat-output');
  const symbolField = document.getElementById('symbol');
  if (!refresh || !local || !exportButton || !filter || !root || !symbolField) return;

  let receipt = null;
  let receiptLabel = '';
  const el = (tag, text, cls) => {
    const node = document.createElement(tag);
    node.textContent = String(text ?? '');
    if (cls) node.className = cls;
    return node;
  };
  const value = input => typeof input === 'object' ? JSON.stringify(input) : String(input ?? '—');

  function visible(item) {
    if (filter.value === 'all') return true;
    if (filter.value === 'observed') return item.state === 'observed';
    return item.state !== 'observed';
  }

  function detail(label, content) {
    const block = document.createElement('details');
    block.appendChild(el('summary', label));
    block.appendChild(el('pre', value(content)));
    return block;
  }

  function card(kind, item) {
    const node = el('article', '', 'intelthat-card');
    node.dataset.state = item.state || 'missing';
    const head = el('div', '', 'intelthat-card-head');
    head.appendChild(el('h3', kind.toUpperCase()));
    head.appendChild(el('span', item.state || 'unknown', 'intelthat-state'));
    node.appendChild(head);
    node.appendChild(el('p', item.reason || 'No evidence reason supplied.'));
    const facts = el('dl');
    const rows = [
      ['Timeframe', item.timeframe], ['As of', item.as_of], ['Freshness', item.freshness],
      ['Confidence', item.confidence == null ? '—' : Math.round(Number(item.confidence) * 100) + '%'],
      ...Object.entries(item.metrics || {})
    ];
    rows.forEach(([label, entry]) => {
      facts.appendChild(el('dt', label));
      facts.appendChild(el('dd', value(entry)));
    });
    node.appendChild(facts);
    if (item.formula) node.appendChild(detail('Formula', item.formula));
    if (item.inputs) node.appendChild(detail('Inputs', item.inputs));
    if (item.provenance) node.appendChild(detail('Provenance', item.provenance));
    else if (item.sha256) node.appendChild(detail('Legacy source fingerprint', { sha256: item.sha256 }));
    return node;
  }

  function show(data, sourceLabel) {
    receipt = data;
    receiptLabel = sourceLabel;
    exportButton.disabled = false;
    root.replaceChildren();
    const summary = el('div', '', 'intelthat-summary');
    const copy = el('div');
    copy.appendChild(el('strong', `${data.symbol || symbolField.value.toUpperCase()} · ${sourceLabel}`));
    copy.appendChild(el('p', `${data.contract || 'legacy owner-receipt contract'} · receipt ${data.receipt_sha256 ? data.receipt_sha256.slice(0, 16) + '…' : 'source fingerprints shown per card'}`));
    summary.appendChild(copy);
    const proof = el('div', '', 'intelthat-proof');
    Object.entries(data.proof_health || {}).forEach(([state, count]) => proof.appendChild(el('span', `${state} ${count}`)));
    summary.appendChild(proof);
    root.appendChild(summary);
    const grid = el('div', '', 'intelthat-grid');
    for (const kind of ['pack', 'macro', 'rss', 'edgar']) {
      const item = data.sources?.[kind] || { state: 'missing', reason: 'No evidence object returned.' };
      if (visible(item)) grid.appendChild(card(kind, item));
    }
    if (!grid.childElementCount) grid.appendChild(el('p', 'No evidence matches this filter.', 'muted'));
    root.appendChild(grid);
  }

  async function load(path, button, sourceLabel) {
    const selected = symbolField.value.trim();
    if (!selected) return;
    button.disabled = true;
    root.replaceChildren(el('div', `Reading ${sourceLabel.toLowerCase()} for ${selected.toUpperCase()}…`, 'intelthat-empty'));
    try {
      const response = await fetch(path + encodeURIComponent(selected), {
        headers: { Accept: 'application/json' }, credentials: 'same-origin'
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Evidence request refused.');
      show(data, sourceLabel);
    } catch (error) {
      receipt = null;
      exportButton.disabled = true;
      root.replaceChildren(el('div', `Evidence unavailable: ${error.message}`, 'intelthat-error'));
    } finally {
      button.disabled = false;
    }
  }

  refresh.addEventListener('click', () => load('/api/intelthat-workspace/', refresh, 'Native live evidence'));
  local.addEventListener('click', () => load('/api/intelthat/', local, 'Owner-published receipts'));
  filter.addEventListener('change', () => { if (receipt) show(receipt, receiptLabel); });
  exportButton.addEventListener('click', () => {
    if (!receipt) return;
    const selected = String(receipt.symbol || 'market').toLowerCase();
    const blob = new Blob([JSON.stringify(receipt, null, 2) + '\n'], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `market-compass-intelthat-${selected}-receipt.json`;
    link.click();
    URL.revokeObjectURL(link.href);
  });
});
