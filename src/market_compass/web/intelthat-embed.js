(() => {
  const frame = document.getElementById('intelthat-app-frame');
  if (!frame) return;
  let report = null;
  let selectedView = 'cockpit';
  const send = () => {
    if (!frame.contentWindow || !report) return;
    const meta = report.data_meta || {};
    frame.contentWindow.postMessage({type:'market-compass-intel-asset', symbol:meta.resolved_symbol || report.symbol}, location.origin);
  };
  const sendView = () => frame.contentWindow?.postMessage({type:'market-compass-intel-select-view',view:selectedView},location.origin);
  window.addEventListener('marketcompassreport', event => {report = event.detail.report; send();});
  window.addEventListener('marketcompassintelview', event => {selectedView = event.detail.view; sendView();});
  frame.addEventListener('load', () => {send(); sendView();});
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.type !== 'market-compass-intel-height') return;
    const height = Number(event.data.height);
    if (Number.isFinite(height) && height >= 400 && height <= 12000) frame.style.height = `${height}px`;
  });
})();
