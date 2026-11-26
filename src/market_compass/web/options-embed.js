(() => {
  const frame = document.getElementById('options-lab-frame');
  if (!frame) return;
  let latestReport = null;
  const sendTheme = () => {
    if (!frame.contentWindow) return;
    const css = getComputedStyle(document.documentElement);
    const keys = ['canvas', 'surface', 'ink', 'muted', 'line', 'brand', 'fill-recessed', 'fill-selected'];
    const values = Object.fromEntries(keys.map(key => [key, css.getPropertyValue(`--act-${key}`).trim()]));
    frame.contentWindow.postMessage({type: 'market-compass-options-theme', values}, location.origin);
  };
  const sendReport = () => {
    if (!frame.contentWindow || !latestReport) return;
    const report = latestReport, meta = report.data_meta || {}, quote = meta.quote || {};
    frame.contentWindow.postMessage({type: 'market-compass-options-asset', asset: {
      requested: meta.requested_symbol || report.symbol,
      symbol: meta.resolved_symbol || report.symbol,
      kind: quote.quoteType || quote.typeDisp || '',
      price: report.price,
      asOf: report.chart?.date?.at(-1) || report.as_of,
      provider: meta.provider || 'Market Compass desk'
    }}, location.origin);
  };
  window.addEventListener('marketcompassoptionsview', event => frame.contentWindow?.postMessage({type:'market-compass-options-select-view',view:event.detail.view},location.origin));
  window.addEventListener('marketcompassreport', event => { latestReport = event.detail.report; sendReport(); });
  frame.addEventListener('load', () => { sendTheme(); sendReport(); });
  window.addEventListener('actappearancechange', sendTheme);
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.type !== 'market-compass-options-height') return;
    const height = Number(event.data.height);
    if (Number.isFinite(height) && height > 300 && height < 12000) frame.style.height = `${Math.ceil(height + 12)}px`;
  });
})();
