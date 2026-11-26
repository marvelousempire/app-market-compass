if (new URLSearchParams(location.search).get('embedded') === '1') {
  document.body.classList.add('embedded');
  const themeNames = {canvas:'canvas', surface:'surface', ink:'ink', muted:'muted', line:'line', brand:'brand', 'fill-recessed':'recessed', 'fill-selected':'selected'};
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== parent) return;
    if (event.data?.type === 'market-compass-options-theme') {
      Object.entries(event.data.values || {}).forEach(([key, value]) => {
        if (themeNames[key] && /^#[0-9a-fA-F]{3,8}$|^rgb\([\d\s,]+\)$/.test(value)) document.documentElement.style.setProperty(`--mc-${themeNames[key]}`, value);
      });
    }
    if (event.data?.type === 'market-compass-options-select-view') {
      const views = {chain:'#chain',builder:'#place',returns:'.projection-controls',alpaca:'#alpaca-context',edgar:'#edgar-context',positions:'#positions',journal:'#journal'};
      const selector = views[event.data.view];
      const element = selector && document.querySelector(selector);
      const target = ['chain','builder','alpaca','edgar','positions','journal'].includes(event.data.view) ? element?.closest('.card') : element;
      target?.scrollIntoView({block:'start',behavior:'smooth'});
    }
    if (event.data?.type === 'market-compass-options-asset') {
      const next = event.data.asset || {}, symbol = String(next.symbol || '').toUpperCase();
      const price = Number(next.price), kind = String(next.kind || '').toUpperCase();
      const age = Date.now() - Date.parse(next.asOf);
      const supported = /^[A-Z][A-Z0-9.]{0,9}$/.test(symbol) && ['EQUITY','ETF'].includes(kind) && Number.isFinite(price) && price > 0 && Number.isFinite(age) && age >= -86400000 && age < 5*86400000;
      for (const key of Object.keys(assets)) delete assets[key];
      const select = document.getElementById('asset'); select.replaceChildren();
      if (supported) {
        assets[symbol] = price; asset = symbol;
        select.add(new Option(symbol, symbol));
        sourceInfo = {provider: String(next.provider || 'Market Compass desk'), asOf: String(next.asOf), spot: price};
        strike = null;
        document.getElementById('notice').textContent = '';
      } else {
        asset = ''; strike = null; sourceInfo = null;
        select.add(new Option(symbol || 'No asset', ''));
        document.getElementById('notice').textContent = `Options scenarios unavailable for ${symbol || 'this asset'}: supported equity or ETF price evidence is required.`;
      }
      window.dispatchEvent(new Event('marketcompassasset'));
    }
  });
  const reportHeight = () => parent.postMessage({type: 'market-compass-options-height', height: document.documentElement.scrollHeight}, location.origin);
  new ResizeObserver(reportHeight).observe(document.body);
  window.addEventListener('load', reportHeight);
}
