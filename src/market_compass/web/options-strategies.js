/* Same-expiration two-leg research projections. Prices and returns come from Rust. */
(() => {
  const el = id => document.getElementById(id);
  const fmt = n => new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}).format(n);
  const first = el('strategy-first'), second = el('strategy-second');
  const kind = el('strategy-kind'), quantity = el('strategy-quantity');
  const spotSlider = el('strategy-spot'), daysSlider = el('strategy-days'), ivSlider = el('strategy-iv');
  let currentAsset = '', engine = null;

  function mode(value) {
    const strategy = value === 'strategy';
    el('mode-single').classList.toggle('active', !strategy);
    el('mode-strategy').classList.toggle('active', strategy);
    el('mode-single').setAttribute('aria-pressed', String(!strategy));
    el('mode-strategy').setAttribute('aria-pressed', String(strategy));
    document.querySelectorAll('.single-panel').forEach(panel => { panel.hidden = strategy; });
    el('strategy-panel').hidden = !strategy;
    if (strategy) render();
    window.dispatchEvent(new CustomEvent('marketcompassoptionscassette', {detail: {view: strategy ? 'strategies' : 'chain'}}));
    parent.postMessage({type:'market-compass-options-height',height:document.documentElement.scrollHeight},location.origin);
  }
  el('mode-single').onclick = () => mode('single');
  el('mode-strategy').onclick = () => mode('strategy');
  mode('single');

  function expiryDays() {
    return Math.max(0, Math.ceil((new Date(el('expiry').value + 'T16:00:00') - new Date()) / 86400000));
  }
  function availableStrikes(spot) {
    const target = spot * .05, power = 10 ** Math.floor(Math.log10(target));
    const step = Math.max(.01, [1,2,5,10].map(n => n * power).find(n => n >= target) || power * 10);
    const center = Math.round(spot / step) * step;
    return Array.from({length:13}, (_, i) => Number((center + (i - 6) * step).toFixed(4))).filter(n => n > 0);
  }
  function legs(type, a, b) {
    if (type === 'bull-call') return [{strike:a,kind:0,side:1},{strike:b,kind:0,side:-1}];
    if (type === 'bear-put') return [{strike:b,kind:1,side:1},{strike:a,kind:1,side:-1}];
    if (type === 'straddle') return [{strike:a,kind:0,side:1},{strike:a,kind:1,side:1}];
    return [{strike:b,kind:0,side:1},{strike:a,kind:1,side:1}];
  }
  function refreshAsset() {
    const spot = assets[asset];
    if (!Number.isFinite(spot) || spot <= 0) {
      currentAsset = ''; first.replaceChildren(); second.replaceChildren(); render(); return;
    }
    currentAsset = asset;
    const strikes = availableStrikes(spot), middle = Math.floor(strikes.length / 2);
    for (const select of [first,second]) {
      select.replaceChildren(...strikes.map(strike => new Option(fmt(strike),String(strike))));
    }
    first.selectedIndex = Math.max(0,middle - 1);
    second.selectedIndex = Math.min(strikes.length - 1,middle + 1);
    second.disabled = kind.value === 'straddle';
    if (second.disabled) second.value = first.value;
    spotSlider.min = (spot * .5).toFixed(2); spotSlider.max = (spot * 1.5).toFixed(2);
    spotSlider.step = spot < 20 ? '.05' : spot < 100 ? '.25' : '.5'; spotSlider.value = spot;
    daysSlider.max = expiryDays(); daysSlider.value = daysSlider.max; ivSlider.value = 30;
    render();
  }
  function clear(message) {
    el('strategy-legs').textContent = message;
    for (const id of ['strategy-debit','strategy-gain','strategy-loss']) el(id).textContent = '—';
    el('strategy-result').textContent = message; el('strategy-return').textContent = '';
    el('strategy-chart').replaceChildren();
  }
  function render() {
    if (!engine) { clear('Rust strategy model is loading.'); return; }
    const spot = assets[asset], a = Number(first.value), b = Number(second.value), qty = Number(quantity.value);
    const type = kind.value, days = expiryDays(), projectedSpot = Number(spotSlider.value);
    const projectedDays = Number(daysSlider.value), iv = Number(ivSlider.value);
    el('strategy-spot-label').textContent = Number.isFinite(projectedSpot) ? fmt(projectedSpot) : '—';
    el('strategy-days-label').textContent = projectedDays + ' days';
    el('strategy-iv-label').textContent = iv + '%';
    if (!Number.isFinite(spot) || currentAsset !== asset) { clear('Analyze a supported equity or ETF first.'); return; }
    if (!Number.isInteger(qty) || qty < 1 || qty > 100) { clear('Choose 1 to 100 contracts per leg.'); return; }
    if ((type !== 'straddle' && !(a < b)) || !Number.isFinite(a) || !Number.isFinite(b)) {
      clear('Choose a lower first strike and a higher second strike.'); return;
    }
    const [left,right] = legs(type,a,b);
    const args = [left.strike,left.kind,left.side,right.strike,right.kind,right.side];
    const entry = engine.option_two_leg_entry(spot,days,30,...args);
    const returnsAt = (price,remaining) => engine.option_two_leg_return(spot,price,days,remaining,30,iv,...args,qty);
    const gain = returnsAt(projectedSpot,projectedDays);
    if (![entry,gain].every(Number.isFinite)) { clear('This strategy is outside the model’s supported range.'); return; }
    el('strategy-legs').textContent = [left,right].map(leg => `${leg.side === 1 ? 'Buy' : 'Sell'} ${fmt(leg.strike)} ${leg.kind === 0 ? 'call' : 'put'}`).join('  +  ');
    const debit = entry * 100 * qty;
    el('strategy-debit').textContent = fmt(debit);
    const expiryReturns = [0,a,b,Math.max(spot * 3,b * 3)].map(price => engine.option_two_leg_return(spot,price,days,0,30,iv,...args,qty));
    if (!expiryReturns.every(Number.isFinite)) { clear('Expiration bounds are unavailable for these strikes.'); return; }
    const maxLoss = Math.min(...expiryReturns), maxGain = Math.max(...expiryReturns);
    el('strategy-loss').textContent = fmt(Math.max(0,-maxLoss));
    el('strategy-gain').textContent = type === 'bull-call' || type === 'bear-put' ? fmt(maxGain) : 'Unlimited above';
    el('strategy-result').textContent = `Projected return ${fmt(gain)}`;
    el('strategy-result').className = gain < 0 ? 'danger' : 'tag';
    el('strategy-return').textContent = debit > 0 ? `${(gain / debit * 100).toFixed(1)}% of net debit` : 'Credit strategy';
    const x0 = spot * .5, x1 = spot * 1.5;
    const points = Array.from({length:81},(_,i) => ({x:x0+(x1-x0)*i/80,y:returnsAt(x0+(x1-x0)*i/80,projectedDays)}));
    const bound = Math.max(100,...points.map(p => Math.abs(p.y))), px = x => 35 + (x-x0)/(x1-x0)*425;
    const py = y => 110 - y/bound*88;
    const path = points.map((p,i) => `${i ? 'L' : 'M'}${px(p.x).toFixed(1)} ${py(p.y).toFixed(1)}`).join(' ');
    const cursor = px(projectedSpot);
    el('strategy-chart').innerHTML = `<line x1="35" y1="110" x2="460" y2="110" stroke="var(--mc-line)"/><path d="${path}" fill="none" stroke="var(--mc-brand)" stroke-width="3"/><line x1="${cursor}" y1="18" x2="${cursor}" y2="198" stroke="var(--mc-ink)" stroke-dasharray="4 4"/><circle cx="${cursor}" cy="${py(gain)}" r="5" fill="var(--mc-ink)"/><text x="35" y="215">${fmt(x0)}</text><text x="400" y="215">${fmt(x1)}</text><text x="38" y="28">+${fmt(bound)}</text><text x="38" y="190">−${fmt(bound)}</text>`;
    el('strategy-chart').setAttribute('aria-label',`${type.replace('-',' ')} projected return ${fmt(gain)} at ${fmt(projectedSpot)} with ${projectedDays} days remaining`);
  }
  kind.addEventListener('change', () => { second.disabled = kind.value === 'straddle'; if (second.disabled) second.value = first.value; render(); });
  first.addEventListener('change', () => { if (kind.value === 'straddle') second.value = first.value; render(); });
  for (const control of [first,second,quantity,spotSlider,daysSlider,ivSlider,el('expiry')]) control.addEventListener('input', render);
  el('expiry').addEventListener('change', () => { daysSlider.max = expiryDays(); daysSlider.value = daysSlider.max; render(); });
  window.addEventListener('marketcompassasset', refreshAsset);
  window.addEventListener('marketcompassoptionsmodel', () => {engine=window.marketCompassOptionsModel; refreshAsset();});
  if (window.marketCompassOptionsModel) {engine=window.marketCompassOptionsModel; refreshAsset();}
})();
