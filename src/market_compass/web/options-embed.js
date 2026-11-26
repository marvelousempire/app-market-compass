(() => {
  const frame = document.getElementById('options-lab-frame');
  if (!frame) return;
  const sendTheme = () => {
    if (!frame.contentWindow) return;
    const css = getComputedStyle(document.documentElement);
    const keys = ['canvas', 'surface', 'ink', 'muted', 'line', 'brand', 'fill-recessed', 'fill-selected'];
    const values = Object.fromEntries(keys.map(key => [key, css.getPropertyValue(`--act-${key}`).trim()]));
    frame.contentWindow.postMessage({type: 'market-compass-options-theme', values}, location.origin);
  };
  frame.addEventListener('load', sendTheme);
  window.addEventListener('actappearancechange', sendTheme);
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.type !== 'market-compass-options-height') return;
    const height = Number(event.data.height);
    if (Number.isFinite(height) && height > 300 && height < 12000) frame.style.height = `${Math.ceil(height + 12)}px`;
  });
})();
