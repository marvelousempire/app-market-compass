const output = document.getElementById('market-data-current');
const refresh = document.getElementById('market-data-refresh');
const connection = document.getElementById('alpaca-connect-status');
const form = document.getElementById('alpaca-connect-form');
const start = document.getElementById('alpaca-connect-start');
const saveButton = form?.querySelector('button[type="submit"]');

async function connectionStatus() {
  if (!connection) return;
  try {
    const response = await fetch('/api/alpaca-connect/status', {cache: 'no-store'});
    if (!response.ok) throw new Error('unavailable');
    const status = await response.json();
    connection.dataset.saveState = status.configured ? 'saved' : 'empty';
    window.dispatchEvent(new CustomEvent('marketcompassalpacastatus', {detail: {configured: status.configured, connected: status.connected}}));
    connection.textContent = status.connected ? 'Alpaca connection saved on this Mac. Check the price source below to confirm your feed. The secret fields stay blank for safety.'
      : status.configured ? 'App details saved on this Mac. Finish your app registration in Alpaca, then select Connect with Alpaca. The fields stay blank for safety.'
      : 'Alpaca is not connected. Add your Connect app credentials below.';
    if (start) start.disabled = !status.configured;
    return status;
  } catch {
    connection.dataset.saveState = 'error';
    window.dispatchEvent(new CustomEvent('marketcompassalpacastatus', {detail: null}));
    connection.textContent = 'Connection status unavailable. No credential was shown or changed.';
    if (start) start.disabled = true;
    return null;
  }
}

form?.addEventListener('submit', async event => {
  event.preventDefault();
  if (saveButton?.disabled) return;
  if (saveButton) saveButton.disabled = true;
  connection.classList.remove('just-saved');
  connection.dataset.saveState = 'saving';
  connection.textContent = 'Saving your Connect app in this Mac’s Keychain…';
  const client_id = form.elements.client_id.value.trim();
  const client_secret = form.elements.client_secret.value.trim();
  try {
    const response = await fetch('/api/alpaca-connect/configure', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, cache: 'no-store',
      body: JSON.stringify({client_id, client_secret})
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'The Connect app could not be saved.');
    }
    const saved = await response.json();
    if (!saved.configured) throw new Error('The app details could not be confirmed as saved. Please try again.');
    const verified = await connectionStatus();
    if (!verified?.configured) throw new Error('The app details were not confirmed after saving. Your entries are still here; try again.');
    form.reset();
    // A successful readback is the only event allowed to start the celebration.
    void connection.offsetWidth;
    connection.classList.add('just-saved');
  } catch (error) {
    connection.classList.remove('just-saved');
    connection.dataset.saveState = 'error';
    connection.textContent = error.message;
  } finally {
    if (saveButton) saveButton.disabled = false;
  }
});

start?.addEventListener('click', async () => {
  connection.textContent = 'Opening Alpaca sign-in for paper market data…';
  try {
    const response = await fetch('/api/alpaca-connect/start', {method:'POST', cache:'no-store'});
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Could not start Alpaca sign-in.');
    }
    const {url} = await response.json();
    window.location.assign(url);
  } catch (error) { connection.textContent = error.message; }
});

async function checkPriceSource() {
  if (!output) return;
  output.textContent = 'Checking the current price source…';
  try {
    const response = await fetch('/api/market-price/BB', {cache: 'no-store'});
    if (!response.ok) throw new Error('unavailable');
    const item = await response.json();
    if (item.state !== 'observed' || !Number.isFinite(Number(item.price))) throw new Error('unavailable');
    const when = new Date(item.as_of);
    const time = Number.isNaN(when.getTime()) ? 'time unavailable' : when.toLocaleString();
    const price = Number(item.price).toLocaleString(undefined, {style: 'currency', currency: 'USD'});
    const live = item.real_time && Date.now() - when.getTime() <= 120000;
    output.textContent = `BB ${price} · ${live ? 'Live' : 'Last observed'} · ${item.source} ${item.feed || ''} · ${time}`;
  } catch {
    output.textContent = 'Price source unavailable. Market Compass will not invent a price.';
  }
}

refresh?.addEventListener('click', checkPriceSource);
checkPriceSource();
const alpacaReturn = new URLSearchParams(window.location.search).get('alpaca');
connectionStatus().then(() => {
  if (alpacaReturn === 'failed') connection.textContent = 'Alpaca sign-in did not finish. Open Alpaca app setup to check its saved return address and registration status, then try again.';
  if (alpacaReturn === 'declined') connection.textContent = 'Alpaca sign-in was canceled. No connection was added.';
});
