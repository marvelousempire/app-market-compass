(() => {
  const frame = document.getElementById('intelthat-app-frame');
  if (!frame) return;
  let report = null;
  const send = () => {
    if (!frame.contentWindow || !report) return;
    const meta = report.data_meta || {};
    frame.contentWindow.postMessage({type:'market-compass-intel-asset', symbol:meta.resolved_symbol || report.symbol}, location.origin);
  };
  window.addEventListener('marketcompassreport', event => {report = event.detail.report; send();});
  frame.addEventListener('load', send);
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.type !== 'market-compass-intel-height') return;
    const height = Number(event.data.height);
    if (Number.isFinite(height) && height >= 400 && height <= 12000) frame.style.height = `${height}px`;
  });
})();
