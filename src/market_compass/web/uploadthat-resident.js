import {marketCompassProjection} from '/static/vendor/bank-reader/market-compass-projection.mjs';
/* Read-only receiving leaves the mounted research, selection and simulations intact. */
(() => {
  const button = document.getElementById('load-reviewed-imports');
  const output = document.getElementById('reviewed-imports');
  if (!button || !output) return;
  const node = (tag, text) => { const element = document.createElement(tag); element.textContent = text; return element; };
  button.addEventListener('click', async () => {
    if (location.protocol === 'http:' && location.hostname === 'market-compass.localhost') {
      const link = node('a', 'Open secure Market Compass');
      link.href = 'https://market-compass.localhost/'; link.target = '_blank'; link.rel = 'noopener';
      output.replaceChildren(node('p', 'Family connects through the secure Door. Your research stays in this tab.'), link);
      return;
    }
    button.disabled = true;
    const status = node('p', 'Reading the confirmed imports and financial owner…');
    output.replaceChildren(status);
    try {
      const response = await fetch('/api/uploadthat/imports', {credentials: 'same-origin', cache: 'no-store'});
      const value = await response.json();
      if (response.status === 401 || response.status === 403) {
        status.textContent = 'Connect with Family, then return here. Your research stays in this tab.';
        const link = node('a', 'Connect with Family');
        link.className = 'secondary asset-channel-settings-link';
        link.href = 'https://market-compass.localhost/signin?return=%2F';
        link.target = '_blank'; link.rel = 'noopener';
        link.title = 'Open Family sign-in in a separate tab, then return here to read your reviewed imports.';
        output.replaceChildren(status, link);
        return;
      }
      if (!response.ok) throw Error(value.detail || 'The import owner is unavailable.');
      output.replaceChildren();
      if (!value.imports.length) output.append(node('p', 'No recent Market Compass uploads were returned.'));
      for (const imported of value.imports) {
        const section = node('section', ''); section.append(node('h3', imported.name));
        if (/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(imported.reviewId)) {
          const source = node('a', 'Open reviewed source'); source.className = 'secondary asset-channel-settings-link';
          source.href = 'https://uploadthat.localhost/?source=market-compass#' + encodeURIComponent(imported.reviewId);
          source.target = '_blank'; source.rel = 'noopener';
          source.title = 'Open this saved upload and its original details in a separate tab.';
          section.append(source);
        }
        if (imported.state !== 'verified') { section.append(node('p', imported.message)); output.append(section); continue; }
        const projection = marketCompassProjection(imported.operation, imported.scopes);
        section.append(node('p', `Bank-owned history · ${projection.period.first} to ${projection.period.last}`), node('p', projection.warning));
        for (const account of projection.accounts) {
          const group = node('section', ''); group.append(node('h4', account.name), node('p', account.broker || 'Broker not supplied by the owner'));
          const table = node('table', ''); table.setAttribute('aria-label', `${account.name} imported activity`);
          const head = node('thead', ''); const titles = node('tr', '');
          for (const title of ['Source date', 'Asset', 'Recorded action', 'Source quantity']) titles.append(node('th', title));
          head.append(titles); table.append(head); const body = node('tbody', ''); table.append(body);
          const paging = node('p', ''); const previous = node('button', 'Previous records'); const next = node('button', 'Next records');
          previous.className = next.className = 'secondary';
          previous.type = next.type = 'button'; let page = 0;
          const paint = () => {
            body.replaceChildren();
            for (const row of account.activities.slice(page * 100, (page + 1) * 100)) {
              const tr = node('tr', ''); for (const text of [row.date, row.symbol || row.token_symbol, row.transaction_type, row.quantity]) tr.append(node('td', text)); body.append(tr);
            }
            paging.textContent = `Records ${page * 100 + 1}–${Math.min((page + 1) * 100, account.activities.length)} of ${account.activities.length}`;
            previous.disabled = page === 0; next.disabled = (page + 1) * 100 >= account.activities.length;
          };
          previous.onclick = () => { page--; paint(); }; next.onclick = () => { page++; paint(); }; paint();
          const lane = node('div', ''); lane.className = 'reviewed-import-activity'; lane.tabIndex = 0;
          lane.setAttribute('role', 'region'); lane.setAttribute('aria-label', `${account.name} activity table`);
          lane.append(table);
          const actions = node('div', ''); actions.className = 'reviewed-import-actions'; actions.append(previous, next);
          group.append(lane, paging, actions); section.append(group);
        }
        output.append(section);
      }
    } catch (error) { status.textContent = error.message; output.replaceChildren(status); }
    finally { button.disabled = false; }
  });
})();
