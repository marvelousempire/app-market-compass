/* intelTHAT application shell. Research-only: never authenticates a broker or sends an order. */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#intel-run-form');
  const symbolInput = document.querySelector('#intel-symbol');
  const suggestions = document.querySelector('#intel-symbols');
  const ownerButton = document.querySelector('#intel-owner');
  const runButton = document.querySelector('#intel-run');
  const saveButton = document.querySelector('#intel-save');
  const exportButton = document.querySelector('#intel-export');
  const output = document.querySelector('#intel-output');
  const progress = document.querySelector('#intel-progress');
  const proof = document.querySelector('#proof-health');
  const facts = document.querySelector('#run-facts');
  const activeSymbol = document.querySelector('#active-symbol');
  const runtimeState = document.querySelector('#runtime-state');
  const viewTitle = document.querySelector('#view-title');
  const viewDescription = document.querySelector('#view-description');
  const stageKicker = document.querySelector('#stage-kicker');
  const stageTitle = document.querySelector('#stage-title');
  const stageCopy = document.querySelector('#stage-copy');
  const views = [...document.querySelectorAll('[data-intel-view]')];
  if (!form || !symbolInput || !output) return;

  const kinds = ['pack', 'macro', 'rss', 'edgar'];
  const labels = { pack: 'Market Pack', macro: 'Macro Conditions', rss: 'News Intelligence', edgar: 'SEC Monitor' };
  const descriptions = {
    cockpit: 'Run and inspect provenance-bound market research.',
    pack: 'Price, trend, momentum, timeframe agreement, and bounded aggregate options context.',
    macro: 'Public volatility, rates, dollar, and long-bond proxy measurements.',
    rss: 'Current provider headlines measured with a disclosed lexical lens.',
    edgar: 'Policy-gated SEC company submissions under a fair-access identity.',
    receipts: 'Saved research runs and their exact exportable receipts.'
  };
  const companyAliases = {
    apple: 'AAPL', blackberry: 'BB', microsoft: 'MSFT', nvidia: 'NVDA',
    tesla: 'TSLA', amazon: 'AMZN', alphabet: 'GOOGL', google: 'GOOGL'
  };
  const safeStore = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); return true; } catch { return false; } }
  };
  let receipt = null;
  let sourceLabel = '';
  let activeView = 'cockpit';
  let saved = false;
  let startedAt = 0;
  let timer = null;

  const el = (tag, text, cls) => { const node = document.createElement(tag); node.textContent = String(text ?? ''); if (cls) node.className = cls; return node; };
  const value = (input) => typeof input === 'object' ? JSON.stringify(input, null, 2) : String(input ?? '—');
  const history = () => { try { const rows = JSON.parse(safeStore.get('intelthat-app-runs') || '[]'); return Array.isArray(rows) ? rows : []; } catch { return []; } };

  function setProgress(state, message) {
    progress.dataset.state = state;
    progress.querySelector('p').textContent = message;
    runtimeState.textContent = state === 'running' ? 'Researching' : state === 'error' ? 'Held' : 'Ready';
    clearInterval(timer);
    if (state === 'running') {
      startedAt = Date.now();
      timer = setInterval(() => { progress.querySelector('time').textContent = `${((Date.now() - startedAt) / 1000).toFixed(1)}s elapsed`; }, 100);
    } else {
      progress.querySelector('time').textContent = startedAt ? `${((Date.now() - startedAt) / 1000).toFixed(1)}s` : '';
    }
  }

  function details(label, content) {
    const node = document.createElement('details');
    node.appendChild(el('summary', label));
    node.appendChild(el('pre', value(content)));
    return node;
  }

  function card(kind, item) {
    const node = el('article', '', 'module-card');
    node.dataset.state = item.state || 'missing';
    const head = el('div', '', 'module-head');
    head.appendChild(el('h3', labels[kind] || kind));
    head.appendChild(el('span', item.state || 'unknown'));
    node.appendChild(head);
    node.appendChild(el('p', item.reason || 'No reason supplied.'));
    const list = document.createElement('dl');
    const rows = [
      ['Timeframe', item.timeframe], ['As of', item.as_of], ['Freshness', item.freshness],
      ['Confidence', item.confidence == null ? '—' : `${Math.round(Number(item.confidence) * 100)}%`],
      ...Object.entries(item.metrics || {})
    ];
    rows.forEach(([label, entry]) => { list.appendChild(el('dt', label)); list.appendChild(el('dd', value(entry))); });
    node.appendChild(list);
    if (item.formula) node.appendChild(details('Formula', item.formula));
    if (item.inputs) node.appendChild(details('Inputs', item.inputs));
    if (item.provenance) node.appendChild(details('Provenance', item.provenance));
    else if (item.sha256) node.appendChild(details('Source fingerprint', { sha256: item.sha256 }));
    return node;
  }

  function renderFacts() {
    const short = receipt?.receipt_sha256 ? `${receipt.receipt_sha256.slice(0, 12)}…` : '—';
    const rows = [['Symbol', receipt?.symbol || symbolInput.value.toUpperCase()], ['Source', sourceLabel || 'Not run'], ['Receipt', short], ['Saved', saved ? 'Yes' : 'No']];
    facts.replaceChildren();
    rows.forEach(([label, entry]) => { facts.appendChild(el('dt', label)); facts.appendChild(el('dd', entry)); });
  }

  function renderProof() {
    proof.replaceChildren();
    Object.entries(receipt?.proof_health || {}).forEach(([state, count]) => proof.appendChild(el('span', `${state} ${count}`)));
  }

  function renderHistory() {
    stageKicker.textContent = 'RUN HISTORY';
    stageTitle.textContent = 'Saved research sessions';
    stageCopy.textContent = 'Saved locally in this browser; each row restores the exact receipt captured at that time.';
    output.className = 'history-list';
    const rows = history();
    if (!rows.length) {
      output.replaceChildren(el('p', 'No saved intelTHAT runs yet.', 'empty-state'));
      return;
    }
    output.replaceChildren(...rows.map((row, index) => {
      const button = el('button', '', 'history-item');
      const copy = el('span');
      copy.appendChild(el('strong', `${row.receipt.symbol} · ${row.sourceLabel}`));
      copy.appendChild(el('small', `${row.savedAt} · ${row.receipt.receipt_sha256?.slice(0, 16) || 'legacy receipt'}…`));
      button.appendChild(copy);
      button.appendChild(el('b', '→'));
      button.addEventListener('click', () => {
        receipt = row.receipt; sourceLabel = row.sourceLabel; saved = true; symbolInput.value = receipt.symbol;
        activeSymbol.textContent = receipt.symbol; activeView = 'cockpit'; selectView('cockpit');
      });
      button.dataset.historyIndex = String(index);
      return button;
    }));
  }

  function renderReceipt() {
    if (activeView === 'receipts') { renderHistory(); renderFacts(); renderProof(); return; }
    if (!receipt) return;
    const selectedKinds = activeView === 'cockpit' ? kinds : [activeView];
    stageKicker.textContent = activeView === 'cockpit' ? 'WHOLE RESEARCH RUN' : labels[activeView].toUpperCase();
    stageTitle.textContent = `${receipt.symbol} · ${sourceLabel}`;
    stageCopy.textContent = `${receipt.contract || 'owner-receipt contract'} · as of ${receipt.as_of || 'source timestamps shown below'}`;
    output.className = 'module-grid';
    output.replaceChildren(...selectedKinds.map((kind) => card(kind, receipt.sources?.[kind] || { state: 'missing', reason: 'No evidence object returned.' })));
    renderFacts(); renderProof();
  }

  function selectView(view) {
    activeView = view;
    views.forEach((button) => button.classList.toggle('active', button.dataset.intelView === view));
    viewTitle.textContent = view === 'cockpit' ? 'Research Cockpit' : view === 'receipts' ? 'Run History' : labels[view];
    viewDescription.textContent = descriptions[view];
    if (receipt || view === 'receipts') renderReceipt();
  }

  async function resolveSymbol(raw) {
    const query = raw.trim();
    if (!query) throw new Error('Enter a company or symbol.');
    const alias = companyAliases[query.toLowerCase()];
    if (alias) return alias;
    if (/^[A-Za-z0-9.^=_-]{1,10}$/.test(query)) return query.toUpperCase();
    const response = await fetch(`/api/symbols?q=${encodeURIComponent(query)}&limit=5`, { headers: { Accept: 'application/json' }, credentials: 'same-origin' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Company search was unavailable.');
    const rows = Array.isArray(data) ? data : data.results || [];
    const match = rows.find((row) => row.symbol || row.resolved_symbol);
    if (!match) throw new Error(`No symbol matched ${query}.`);
    return String(match.symbol || match.resolved_symbol).toUpperCase();
  }

  async function load(mode) {
    runButton.disabled = true; ownerButton.disabled = true; saveButton.disabled = true; exportButton.disabled = true;
    saved = false; receipt = null; renderFacts(); proof.replaceChildren();
    setProgress('running', 'Resolving the symbol, then reading the four bounded research modules in parallel. Total work is source-dependent; no percentage is claimed.');
    output.className = 'empty-state'; output.replaceChildren(el('strong', 'Research run in progress…'), el('p', 'Market Pack, Macro Conditions, News Intelligence, and SEC Monitor will settle independently. Missing or policy-held evidence remains visible.'));
    try {
      const symbol = await resolveSymbol(symbolInput.value);
      symbolInput.value = symbol; activeSymbol.textContent = symbol;
      const path = mode === 'live' ? '/api/intelthat-workspace/' : '/api/intelthat/';
      const response = await fetch(path + encodeURIComponent(symbol), { headers: { Accept: 'application/json' }, credentials: 'same-origin' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Research request was refused.');
      receipt = data; sourceLabel = mode === 'live' ? 'Live research' : 'Owner receipts';
      activeSymbol.textContent = receipt.symbol || symbol; exportButton.disabled = false; saveButton.disabled = false;
      setProgress('ready', `Completed ${sourceLabel.toLowerCase()} for ${receipt.symbol}. Each module reports its own proof state.`);
      renderReceipt();
    } catch (error) {
      setProgress('error', `Research held: ${error.message}`);
      output.className = 'error-state'; output.replaceChildren(el('strong', 'intelTHAT could not finish this run.'), el('p', error.message));
    } finally { runButton.disabled = false; ownerButton.disabled = false; }
  }

  form.addEventListener('submit', (event) => { event.preventDefault(); load('live'); });
  ownerButton.addEventListener('click', () => load('owner'));
  views.forEach((button) => button.addEventListener('click', () => selectView(button.dataset.intelView)));
  saveButton.addEventListener('click', () => {
    if (!receipt) return;
    const rows = history().filter((row) => row.receipt?.receipt_sha256 !== receipt.receipt_sha256);
    rows.unshift({ savedAt: new Date().toISOString(), sourceLabel, receipt });
    saved = safeStore.set('intelthat-app-runs', JSON.stringify(rows.slice(0, 5)));
    setProgress(saved ? 'ready' : 'error', saved ? `Saved ${receipt.symbol} to this browser's intelTHAT run history.` : 'This browser did not allow the run to be saved. Export remains available.');
    renderFacts();
  });
  exportButton.addEventListener('click', () => {
    if (!receipt) return;
    const blob = new Blob([JSON.stringify(receipt, null, 2) + '\n'], { type: 'application/json' });
    const link = document.createElement('a'); link.href = URL.createObjectURL(blob);
    link.download = `intelthat-${String(receipt.symbol || 'market').toLowerCase()}-${sourceLabel === 'Live research' ? 'live' : 'owner'}-receipt.json`;
    link.click(); URL.revokeObjectURL(link.href);
  });
  let searchTimer = null;
  symbolInput.addEventListener('input', () => {
    clearTimeout(searchTimer); const query = symbolInput.value.trim(); if (query.length < 2) return;
    searchTimer = setTimeout(async () => { try { const response = await fetch(`/api/symbols?q=${encodeURIComponent(query)}&limit=6`); const data = await response.json(); const rows = Array.isArray(data) ? data : data.results || []; suggestions.replaceChildren(...rows.filter((row) => row.symbol).map((row) => { const option = document.createElement('option'); option.value = row.symbol; option.label = row.name || row.shortname || row.symbol; return option; })); } catch {} }, 220);
  });
  document.querySelectorAll('[data-color]').forEach((button) => button.addEventListener('click', () => {
    const color = button.dataset.color; document.documentElement.dataset.color = color; safeStore.set('act-v1-color', color);
    document.querySelectorAll('[data-color]').forEach((item) => item.setAttribute('aria-checked', String(item.dataset.color === color)));
  }));
  const initialColor = safeStore.get('act-v1-color') || 'system'; document.documentElement.dataset.color = initialColor;
  document.querySelectorAll('[data-color]').forEach((item) => item.setAttribute('aria-checked', String(item.dataset.color === initialColor)));
  renderFacts(); selectView('cockpit');
});
