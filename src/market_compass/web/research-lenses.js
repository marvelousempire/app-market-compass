/* Imported research lenses are read-only and never influence scores or orders. */
document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('day-trader-lens-output');
  const button = document.getElementById('day-trader-lens-load');
  const symbolField = document.getElementById('symbol');
  if (!root || !button || !symbolField) return;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const render = data => {
    const events = [...(data.micro_slices?.setup_scanner || []), ...(data.micro_slices?.notable_thresholds || [])];
    root.innerHTML = `<div class="lens-summary"><strong>${esc(data.state)}</strong><p>${esc(data.summary)}</p></div><div class="lens-grid">${events.map(item => `<article class="lens-event ${item.state}"><span>${esc(item.owner)}</span><b>${esc(item.label)}</b><small>${esc(item.evidence)}</small></article>`).join('')}</div><details><summary>Source and refusal receipt</summary><p>${esc(data.source.url)} @ ${esc(data.source.revision)}</p><p>${esc(data.source.license)} · ${esc(data.source.adaptation)}</p><p>Rejected: ${esc((data.rejected || []).join(' · '))}</p><p>${esc(data.warning)}</p></details>`;
  };
  const load = async () => {
    const symbol = symbolField.value.trim();
    if (!symbol) return;
    button.disabled = true;
    root.textContent = 'Reading the source-bound research lens…';
    try {
      const response = await fetch(`/api/research-lenses/day-trader/${encodeURIComponent(symbol)}`, {headers:{Accept:'application/json'}});
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Lens unavailable');
      render(data);
    } catch (error) { root.textContent = `Lens unavailable: ${error.message}`; }
    finally { button.disabled = false; }
  };
  button.addEventListener('click', load);
  window.addEventListener('marketcompassreport', load);
});
