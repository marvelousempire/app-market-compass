/* One dated market observation shared by Compass Desk and Options Lab. Study bars stay intact. */
(() => {
  let report = null, sequence = 0;
  const publish = observation => window.dispatchEvent(new CustomEvent('marketcompassprice', {
    detail: {symbol: report?.symbol, observation}
  }));
  const paint = (observation, message) => {
    const host = document.getElementById('identity-strip');
    if (!host) return;
    document.getElementById('desk-market-price')?.remove();
    const row = document.createElement('div'); row.id = 'desk-market-price'; row.className = 'identity-main';
    row.setAttribute('role', 'status');
    const value = document.createElement('strong');
    value.textContent = observation
      ? `Market price $${observation.price.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:6})}`
      : message;
    row.append(value);
    if (observation) {
      const source = document.createElement('span');
      source.textContent = `${observation.source} ${observation.feed} · ${observation.real_time ? 'Recent trade' : 'Last observed'} · ${new Date(observation.as_of).toLocaleString()}`;
      row.append(source);
    }
    const refresh = document.createElement('button'); refresh.type = 'button';
    refresh.textContent = 'Refresh market price'; refresh.onclick = load; row.append(refresh); host.prepend(row);
  };
  async function load() {
    if (!report) return;
    const id = ++sequence, symbol = report.data_meta?.resolved_symbol || report.symbol;
    publish(null); paint(null, 'Checking market price…');
    try {
      const response = await fetch(`/api/market-price/${encodeURIComponent(symbol)}`, {cache:'no-store'});
      if (!response.ok) throw new Error('Market price request failed');
      const observation = await response.json();
      if (id !== sequence) return;
      const age = Date.now() - Date.parse(observation.as_of);
      if (observation.state !== 'observed' || observation.symbol !== symbol ||
          typeof observation.price !== 'number' || !Number.isFinite(observation.price) || observation.price <= 0 ||
          !Number.isFinite(age) || age < -60000 || age > 5 * 86400000 || !observation.source || !observation.feed) {
        throw new Error('No usable dated price');
      }
      paint(observation); publish(observation);
    } catch {
      if (id !== sequence) return;
      paint(null, 'Market price unavailable. Refresh to retry.'); publish(null);
    }
  }
  window.addEventListener('marketcompassreport', event => { report = event.detail.report; load(); });
})();
