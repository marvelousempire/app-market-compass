let symbolTimer;

async function loadSymbolSuggestions() {
  const query = $('symbol').value.trim();
  if (!query) return;
  try {
    const response = await fetch(`/api/symbols?q=${encodeURIComponent(query)}`);
    if (!response.ok) return;
    const results = await response.json();
    $('symbol-suggestions').innerHTML = results.map(item =>
      `<option value="${esc(item.display_symbol)}">${esc(item.name)} · ${esc(item.type)} · ${esc(item.symbol)}</option>`
    ).join('');
  } catch (_) {
    // Search assistance is best effort; direct analysis still resolves provider symbols.
  }
}

async function loadAnalystProviders() {
  try {
    const response = await fetch('/api/analyst/providers');
    const providers = await response.json();
    const select = $('analyst-provider');
    select.innerHTML = '<option value="auto">Auto · Nephew routes</option>' + providers.map(provider =>
      `<option value="${esc(provider.id)}" ${provider.configured ? '' : 'disabled'}>${esc(provider.label)} · ${esc(provider.model)}${provider.configured ? '' : ' · not configured'}</option>`
    ).join('');
    const ready = providers.filter(provider => provider.configured).length;
    $('analyst-lane').textContent = `${ready} provider${ready === 1 ? '' : 's'} ready`;
  } catch (error) {
    $('analyst-lane').textContent = 'Analyst unavailable';
  }
}

function analystList(title, items, tone) {
  return `<div><h3>${esc(title)}</h3>${items?.length
    ? `<ul class="${tone}">${items.map(item => `<li>${esc(item)}</li>`).join('')}</ul>`
    : '<p class="muted">None returned.</p>'}</div>`;
}

function renderAnalyst(result) {
  const receipt = result.receipt || {};
  $('analyst-result').innerHTML = `
    <h3>${esc(result.summary)}</h3>
    <p>${esc(result.market_state)}</p>
    <div class="analyst-columns">
      ${analystList('Why it may work', result.bull_case, 'pos')}
      ${analystList('Strongest challenge', result.bear_case, 'neg')}
    </div>
    <p><b>Main conflict:</b> ${esc(result.main_conflict)}</p>
    <p><b>Invalidation:</b> ${esc(result.invalidation_interpretation)}</p>
    ${analystList('Missing information', result.missing_information, '')}
    <div class="analyst-receipt">${esc(receipt.lane)} · ${esc(receipt.provider)} · ${esc(receipt.model)} · ${num(receipt.latency_ms, 0)} ms · report ${esc(String(receipt.report_hash || '').slice(0, 12))}</div>
    <p class="trust-note">${esc(result.warning)}</p>`;
}

async function askNephew() {
  if (!state.report) {
    $('analyst-result').innerHTML = '<p class="muted">Run a market analysis first.</p>';
    return;
  }
  const button = $('ask-nephew');
  button.disabled = true;
  $('analyst-result').innerHTML = '<p>Asking Nephew…</p>';
  try {
    const response = await fetch('/api/analyst', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        report: state.report,
        question: $('analyst-question').value,
        provider: $('analyst-provider').value,
        depth: $('analyst-depth').value,
        cloud_allowed: $('cloud-allowed').checked,
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Analyst request failed');
    renderAnalyst(result);
  } catch (error) {
    $('analyst-result').innerHTML = `<p class="error">${esc(error.message)}</p>`;
  } finally {
    button.disabled = false;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  $('symbol').addEventListener('input', () => {
    clearTimeout(symbolTimer);
    symbolTimer = setTimeout(loadSymbolSuggestions, 220);
  });
  $('ask-nephew').addEventListener('click', askNephew);
  loadSymbolSuggestions();
  loadAnalystProviders();
});
