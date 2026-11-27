(() => {
  const frame = document.getElementById('options-lab-frame');
  if (!frame) return;
  let latestReport = null;
  let marketPrice = null;
  let requestedView = null;
  const sendTheme = () => {
    if (!frame.contentWindow) return;
    const css = getComputedStyle(document.documentElement);
    const keys = ['canvas', 'surface', 'ink', 'muted', 'line', 'brand', 'fill-recessed', 'fill-selected'];
    const values = Object.fromEntries(keys.map(key => [key, css.getPropertyValue(`--act-${key}`).trim()]));
    const selected = document.documentElement.dataset.actColor;
    const colorScheme = selected === 'system'
      ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : selected;
    frame.contentWindow.postMessage({type: 'market-compass-options-theme', values, colorScheme}, location.origin);
  };
  const sendReport = () => {
    if (!frame.contentWindow || !latestReport) return;
    const report = latestReport, meta = report.data_meta || {}, quote = meta.quote || {};
    frame.contentWindow.postMessage({type: 'market-compass-options-asset', asset: {
      requested: meta.requested_symbol || report.symbol,
      symbol: meta.resolved_symbol || report.symbol,
      kind: quote.quoteType || quote.typeDisp || '',
      price: marketPrice?.price,
      asOf: marketPrice?.as_of,
      provider: marketPrice?.source,
      feed: marketPrice?.feed,
      realTime: marketPrice?.real_time
    }}, location.origin);
  };
  window.addEventListener('marketcompassoptionsview', event => {
    requestedView = {type:'market-compass-options-select-view',view:event.detail.view,focus:event.detail.focus};
    frame.contentWindow?.postMessage(requestedView,location.origin);
  });
  window.addEventListener('marketcompassreport', event => { latestReport = event.detail.report; marketPrice = null; sendReport(); });
  window.addEventListener('marketcompassprice', event => {
    if (event.detail.symbol !== latestReport?.symbol) return;
    marketPrice = event.detail.observation; sendReport();
  });
  frame.addEventListener('load', () => { sendTheme(); sendReport(); if (requestedView) frame.contentWindow?.postMessage(requestedView,location.origin); });
  window.addEventListener('actappearancechange', sendTheme);
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.type !== 'market-compass-options-height') return;
    const height = Number(event.data.height);
    if (Number.isFinite(height) && height > 300 && height < 12000) frame.style.height = `${Math.ceil(height + 12)}px`;
  });
})();
