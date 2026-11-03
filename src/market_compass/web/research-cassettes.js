/* FlowThat-shaped cassette selector. Names are operator-owned; no data authority is inferred. */
(() => {
  const cassettes = {
    omo: { name: 'Omo', mark: 'O', role: 'Research Actor', summary: 'Ready to receive research.', groups: [] },
    prince: { name: 'Prince', mark: 'P', role: 'Research Actor', summary: 'Ready to receive research.', groups: [] },
    wuda: {
      name: 'Wuda', mark: 'W', role: 'Trend & Notables Actor', summary: 'Trends, hottest pointers, and notable threshold events.',
      groups: [
        { title: 'Trends', items: ['Direction', 'Strength', 'Acceleration'] },
        { title: 'Hottest pointers', items: ['RSI crosses above 65', 'RSI crosses above 50', 'RSI crosses below 35'] },
        { title: 'Notables', items: ['Threshold event', 'Timeframe', 'Evidence receipt'] }
      ]
    },
    'browns-barometers': {
      name: 'Brown’s Barometers', mark: 'B', role: 'Metrics & Instrument Actor', summary: 'The measurement and instrument bench for technical analysis and the rules that shape how evidence is viewed.',
      groups: [
        { title: 'Metrics', items: ['Breadth', 'Momentum', 'Volatility', 'Volume'] },
        { title: 'Measuring tools', items: ['RSI', 'MACD', 'Moving averages', 'ATR', 'Bollinger Bands'] },
        { title: 'View governance', items: ['Preferences', 'Process rules', 'Timeframe rules'] }
      ]
    }
  };
  const canvas = document.getElementById('cassette-canvas');
  const tabs = [...document.querySelectorAll('[data-cassette]')];
  function render(id) {
    const cassette = cassettes[id];
    const groups = cassette.groups.map(group => `<section class="cassette-tool-group"><h4>${group.title}</h4><div class="cassette-tools">${group.items.map(item => `<span>${item}</span>`).join('')}</div></section>`).join('');
    canvas.innerHTML = `<div class="cassette-mark" aria-hidden="true">${cassette.mark}</div>
      <p class="eyebrow">${cassette.name.toUpperCase()} · ACTOR SPACE</p><h3>${cassette.name}</h3>
      <p>${cassette.summary} No bound market data, score influence, broker action, or approval authority is declared yet.</p>
      <section class="actor-comp-card" aria-label="${cassette.name} comp card">
        <div><span>Actor</span><strong>${cassette.name}</strong></div>
        <div><span>Role</span><strong>${cassette.role}</strong></div>
        <div><span>Trading psychology</span><strong>Preferences and rules not configured</strong></div>
        <div><span>Authority</span><strong>Research presentation only</strong></div>
      </section>
      <div class="cassette-tool-groups">${groups}</div>
      <button type="button" class="secondary cassette-open" data-open-cassette="${id}">Open ${cassette.name}</button>
      <small>Presentation only · source and owner receipts required before activation</small>`;
    canvas.querySelector('.cassette-open').addEventListener('click', event => {
      event.currentTarget.textContent = `${cassette.name} is open`; event.currentTarget.disabled = true;
    });
    tabs.forEach(tab => { const active = tab.dataset.cassette === id; tab.classList.toggle('active', active); tab.setAttribute('aria-selected', String(active)); });
  }
  tabs.forEach(tab => tab.addEventListener('click', () => render(tab.dataset.cassette)));
  render('omo');
})();
