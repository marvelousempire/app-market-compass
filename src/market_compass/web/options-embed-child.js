if (new URLSearchParams(location.search).get('embedded') === '1') {
  document.body.classList.add('embedded');
  const themeNames = {canvas:'canvas', surface:'surface', ink:'ink', muted:'muted', line:'line', brand:'brand', 'fill-recessed':'recessed', 'fill-selected':'selected'};
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== parent || event.data?.type !== 'market-compass-options-theme') return;
    Object.entries(event.data.values || {}).forEach(([key, value]) => {
      if (themeNames[key] && /^#[0-9a-fA-F]{3,8}$|^rgb\([\d\s,]+\)$/.test(value)) document.documentElement.style.setProperty(`--mc-${themeNames[key]}`, value);
    });
  });
  const reportHeight = () => parent.postMessage({type: 'market-compass-options-height', height: document.documentElement.scrollHeight}, location.origin);
  new ResizeObserver(reportHeight).observe(document.body);
  window.addEventListener('load', reportHeight);
}
