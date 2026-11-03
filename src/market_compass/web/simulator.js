/* Local universal simulation workbench, no persistence or broker transport. */
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('universal-input');
  const output = document.getElementById('universal-output');
  const load = document.getElementById('universal-example');
  const run = document.getElementById('universal-run');
  const exporter = document.getElementById('universal-export');
  let lastExport = null;
  if (!input || !output || !load || !run || !exporter) return;

  const demo = {
    subject: {id: 'demo-old-laptop', name: 'Illustrative old laptop', kind: 'device',
      source_owner: 'local example', authorized_use: true},
    method: {id: 'example-condition', version: '0.1-demo', author: 'Example operator',
      provenance: 'Local illustrative fixture; not an ELSE-issued method',
      metrics: [
        {id: 'battery', label: 'Battery health', unit: 'percent', lower: 0, upper: 100, weight: 2, favorable: 'higher'},
        {id: 'wear', label: 'Visible wear', unit: 'score', lower: 0, upper: 10, weight: 1, favorable: 'lower'}
      ]},
    observations: [
      {at: '2026-01-01T12:00:00Z', values: {battery: 100, wear: 0}, evidence_ref: 'demo:1'},
      {at: '2026-02-01T12:00:00Z', values: {battery: 80, wear: 2}, evidence_ref: 'demo:2'},
      {at: '2026-03-01T12:00:00Z', values: {battery: 60, wear: 6}, evidence_ref: 'demo:3'}
    ],
    purpose: 'simulation'
  };
  const el = (tag, text, className) => {
    const node = document.createElement(tag);
    node.textContent = String(text ?? '');
    if (className) node.className = className;
    return node;
  };
  function drawChart(records) {
    const rows = records.filter(x => x.state === 'calculated' && typeof x.index_points === 'number');
    if (!rows.length) return el('p', 'No complete observations to chart.');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 640 200');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Method-relative simulation index from 0 to 100 points over time.');
    svg.classList.add('universal-chart');
    const step = rows.length > 1 ? 580 / (rows.length - 1) : 0;
    const points = rows.map((r, i) => `${40 + step * i},${175 - 1.5 * r.index_points}`).join(' ');
    const poly = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    poly.setAttribute('points', points);
    poly.setAttribute('fill', 'none');
    poly.setAttribute('stroke', 'currentColor');
    poly.setAttribute('stroke-width', '3');
    svg.appendChild(poly);
    rows.forEach((r,i) => {
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('cx', String(40 + step * i));
      dot.setAttribute('cy', String(175 - 1.5 * r.index_points));
      dot.setAttribute('r', '5');
      dot.setAttribute('fill', 'currentColor');
      const title = document.createElementNS('http://www.w3.org/2000/svg','title');
      title.textContent = `${r.at}: ${r.index_points} points`;
      dot.appendChild(title);
      svg.appendChild(dot);
    });
    return svg;
  }
  input.addEventListener('input', () => {
    lastExport = null;
    exporter.disabled = true;
  });
  exporter.addEventListener('click', () => {
    if (!lastExport) return;
    const blob = new Blob([JSON.stringify(lastExport, null, 2) + '\n'], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'market-compass-simulation.json';
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  });
  load.addEventListener('click', () => {
    input.value = JSON.stringify(demo, null, 2);
    lastExport = null;
    exporter.disabled = true;
    output.replaceChildren(el('p', 'Illustrative laptop data loaded. Select Simulate to calculate.'));
  });
  run.addEventListener('click', async () => {
    let request;
    try { request = JSON.parse(input.value); }
    catch (err) {
      output.replaceChildren(el('p', 'Invalid JSON: ' + err.message));
      return;
    }
    run.disabled = true;
    exporter.disabled = true;
    lastExport = null;
    output.replaceChildren(el('p', 'Calculating supplied measurements without storing them…'));
    try {
      const response = await fetch('/api/simulate', {
        method: 'POST', headers: {'Content-Type': 'application/json', Accept: 'application/json'},
        credentials: 'same-origin', body: JSON.stringify(request)
      });
      const result = await response.json();
      if (!response.ok) {
        const detail = typeof result.detail === 'string' ? result.detail
          : (result.detail || []).map(x => (x.loc || []).join('.') + ': ' + x.msg).slice(0, 5).join('; ');
        throw new Error(detail || 'Request rejected.');
      }
      const panel = el('div', '', 'universal-result');
      panel.appendChild(el('h3', result.subject.name + ' · ' + result.method.id));
      panel.appendChild(el('p', result.observed_points + ' calculated · ' + result.held_points + ' held · 0–100 method-relative points'));
      panel.appendChild(drawChart(result.records));
      panel.appendChild(el('p', 'Volatility: ' +
        (result.volatility_points_per_observation == null ? 'not enough observations' : result.volatility_points_per_observation + ' index points per observation')));
      const list = el('div', '', 'universal-records');
      for (const row of result.records) {
        list.appendChild(el('p', row.at + ' · ' + row.state + ' · ' +
          (row.index_points == null ? (row.reason + ': ' + row.missing.join(', ')) : row.index_points + ' points')));
      }
      panel.appendChild(list);
      panel.appendChild(el('small', 'Input SHA-256: ' + result.input_sha256));
      panel.appendChild(el('small', 'Synthetic study only. No money, ownership transfer, real market, live ELSE link, or record storage.'));
      lastExport = {
        schema: 'market-compass.portable-study/v1',
        exported_at: new Date().toISOString(),
        user_supplied_input: request,
        hypothetical_result: result
      };
      exporter.disabled = false;
      output.replaceChildren(panel);
    } catch (err) {
      output.replaceChildren(el('p', 'Simulation held: ' + err.message));
    } finally { run.disabled = false; }
  });
});
