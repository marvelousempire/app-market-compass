/* Source health and company evidence. No score, order, or attention claims. */
(() => {
  let generation = 0, selected = '';
  const health = (id, text, good = false) => {
    const row = document.getElementById(id); if (!row) return;
    row.querySelector('b').textContent = text;
    row.querySelector('span').className = good ? 'good' : 'warn';
  };
  const line = (parent, text, url) => {
    const row = document.createElement('p');
    let safe = false; try { safe = new URL(url).protocol === 'https:'; } catch {}
    if (safe) { const a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = text; row.append(a); }
    else row.textContent = text;
    parent.append(row);
  };
  const when = value => { const date = new Date(value); return Number.isNaN(date.getTime()) ? 'Date unavailable' : date.toLocaleDateString(); };
  const populate = (id, rows, empty, format) => {
    const host = document.getElementById(id); host.replaceChildren();
    if (!rows?.length) line(host, empty);
    else rows.slice(0,8).forEach(row => line(host, format(row), row.url));
  };
  window.addEventListener('marketcompassprice', event => {
    const price = event.detail.observation;
    health('health-market-data', price ? `${price.source} ${price.feed}` : 'Checking / unavailable', price?.source === 'Alpaca');
    const row = document.getElementById('health-market-data');
    if (row) row.title = price ? `${price.real_time ? 'Recent trade' : 'Last observed'} · ${price.as_of}` : 'No usable market observation for the selected symbol.';
  });
  window.addEventListener('marketcompassalpacastatus', event => health('health-alpaca', event.detail?.connected ? 'Connected' : 'Not connected', event.detail?.connected));
  async function load() {
    if (!selected) return;
    const id = ++generation;
    health('health-sec', 'Checking'); health('health-earnings', 'Checking'); health('health-events', 'Checking');
    for (const name of ['desk-filings','desk-earnings','desk-events']) populate(name, [], 'Checking sources…', x => x);
    try {
      const response = await fetch(`/api/asset-channel/${encodeURIComponent(selected)}`, {cache:'no-store'});
      if (!response.ok) throw new Error('unavailable');
      const data = await response.json(); if (id !== generation || data.symbol !== selected) return;
      const filings = data.filings, earnings = data.earnings || {}, events = data.recent_events || [];
      health('health-sec', filings?.state === 'observed' ? 'Available' : 'Unavailable', filings?.state === 'observed');
      const count = (earnings.releases?.length || 0) + (earnings.financial_reports?.length || 0);
      health('health-earnings', count ? 'Reports found' : 'Unavailable', count > 0);
      health('health-events', events.length ? `${events.length} candidates` : 'None found', events.length > 0);
      populate('desk-filings', filings?.inputs?.filings, filings?.reason || 'No filings found.', row => `${row.form} · ${when(row.filed)}`);
      populate('desk-earnings', [...(earnings.releases || []), ...(earnings.financial_reports || [])], 'No earnings reports available from connected sources.', row => row.title ? `${row.title} · ${row.publisher} · ${when(row.published)}` : `${row.form} · ${when(row.filed)} · financial report`);
      line(document.getElementById('desk-earnings'), earnings.reason || 'No verified future earnings calendar is connected.');
      populate('desk-events', events, 'No matching significant-event candidates in the last 30 days of available headlines. Coverage is limited.', row => `${row.title} · ${row.publisher} · ${when(row.published)} · ${row.reason} · ${row.assessment}`);
    } catch {
      if (id !== generation) return;
      for (const name of ['sec','earnings','events']) health(`health-${name}`, 'Unavailable');
      for (const name of ['desk-filings','desk-earnings','desk-events']) populate(name, [], 'Source unavailable. Refresh research to retry.', x => x);
    }
  }
  window.addEventListener('marketcompassreport', event => { selected = event.detail.report.symbol; load(); });
  document.getElementById('desk-research-refresh')?.addEventListener('click', load);
})();
