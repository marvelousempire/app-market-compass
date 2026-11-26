/* Read-only research context; never changes virtual positions or illustrative prices. */
(() => {
  const asset = document.getElementById('asset');
  const alpaca = document.getElementById('alpaca-context');
  const edgar = document.getElementById('edgar-context');
  const refresh = document.getElementById('context-refresh');
  if (!asset || !alpaca || !edgar || !refresh) return;
  let requestId = 0;
  const line = (text, parent) => { const node = document.createElement('div'); node.textContent = text; parent.append(node); };
  async function load() {
    const id = ++requestId, ticker = asset.value;
    if (!ticker) { alpaca.textContent = 'Select a supported equity or ETF in the main desk.'; edgar.textContent = 'No company is selected.'; refresh.disabled = true; return; }
    alpaca.textContent = 'Loading quote context…';
    edgar.textContent = 'Loading company filings…';
    refresh.disabled = true;
    try {
      const response = await fetch(`/api/options-context/${encodeURIComponent(ticker)}`, {cache: 'no-store'});
      if (!response.ok) throw new Error(`Research service returned ${response.status}`);
      const data = await response.json();
      if (id !== requestId) return;
      alpaca.replaceChildren();
      if (data.alpaca?.state === 'observed') {
        line(`Bid $${data.alpaca.bid.toFixed(2)} · Ask $${data.alpaca.ask.toFixed(2)}`, alpaca);
        line(`As of ${data.alpaca.asOf || 'time unavailable'} · source: Alpaca`, alpaca);
      } else line(data.alpaca?.reason || 'Quote unavailable.', alpaca);
      edgar.replaceChildren();
      const item = data.edgar;
      if (item?.state !== 'observed') { line(item?.reason || 'Filings unavailable.', edgar); return; }
      const filings = item.inputs?.filings || [];
      line(`${filings.length} selected filings · latest ${item.as_of || 'unknown'}`, edgar);
      const list = document.createElement('ul'); list.className = 'filing-list';
      filings.slice(0, 8).forEach(f => { const li = document.createElement('li'); li.textContent = `${f.form} · ${f.filed || 'date unavailable'}`; list.append(li); });
      edgar.append(list);
      const link = document.createElement('a'); link.href = `https://www.sec.gov/edgar/browse/?CIK=${encodeURIComponent(item.metrics.cik)}`;
      link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Open SEC company filings'; edgar.append(link);
    } catch (error) {
      if (id === requestId) { alpaca.textContent = `Research unavailable: ${error.message}`; edgar.textContent = 'SEC filings unavailable.'; }
    } finally { if (id === requestId) refresh.disabled = false; }
  }
  window.addEventListener('marketcompassasset', load);
  refresh.addEventListener('click', load);
  load();
})();
