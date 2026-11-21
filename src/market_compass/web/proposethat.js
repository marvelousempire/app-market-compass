/* proposeTHAT local intake: never render user-supplied text as HTML. */
(() => {
  const q = (selector) => document.querySelector(selector);
  const form = q('#pt-form');
  const result = q('#pt-result');
  const history = q('#pt-history');
  const message = q('#pt-message');
  const exportButton = q('#pt-export');
  let active = null;

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  }
  function section(name) {
    const node = element('section', undefined, 'receipt-section');
    node.append(element('h3', name));
    return node;
  }
  async function client(path, options) {
    const response = await fetch(path, { credentials: 'same-origin', cache: 'no-store', ...options });
    const payload = await response.json();
    if (!response.ok) throw Error(typeof payload.detail === 'string' ? payload.detail : 'Request failed: ' + response.status);
    return payload;
  }
  function render(record) {
    active = record;
    exportButton.disabled = false;
    result.replaceChildren(
      element('span', record.status, 'pill'),
      element('div', record.request.subject, 'record-subject'),
      element('div', 'Receipt ' + record.id + ' · ' + (record.received_at || 'undated'), 'receipt-id'),
      element('p', 'Mode: ' + record.mode + '. Research complete: no. Source independently verified: no. Saved privately on this Mac.', 'muted')
    );
    const inventory = section('Existing Market Compass capabilities to inspect');
    (record.existing_capability_checklist || []).forEach((item) => {
      const article = element('article');
      article.append(element('strong', item.capability));
      article.append(element('small', item.market_compass_source_claim + ' · ' + item.source_path));
      inventory.append(article);
    });
    result.append(inventory);
    const candidates = section('Research plan · not yet executed');
    (record.recommendations || []).forEach((item) => {
      const article = element('article');
      article.append(element('strong', item.id.slice(-3) + ' · ' + item.title));
      article.append(element('small', item.function));
      candidates.append(article);
    });
    result.append(candidates);
    const next = section('Next proof');
    next.append(element('p', record.next_action));
    next.append(element('small', 'No broker access or score changes. Outside sources are never fetched by this intake.'));
    result.append(next);
  }
  async function loadHistory() {
    try {
      const data = await client('/api/proposethat/intakes');
      history.replaceChildren();
      if (!data.intakes.length) {
        history.append(element('p', 'No saved requests yet.', 'muted'));
        return;
      }
      const items = element('div', undefined, 'history-items');
      data.intakes.forEach((item) => {
        const button = element('button', item.subject);
        button.type = 'button';
        button.append(element('small', item.mode + ' · ' + (item.received_at || 'unknown date')));
        button.addEventListener('click', async () => {
          try {
            render(await client('/api/proposethat/intakes/' + encodeURIComponent(item.id)));
            result.scrollIntoView({ behavior: 'smooth' });
          } catch (error) { message.textContent = error.message; }
        });
        items.append(button);
      });
      history.append(items);
    } catch (error) {
      history.textContent = 'Saved records unavailable: ' + error.message;
    }
  }
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const submit = q('#pt-submit');
    const payload = Object.fromEntries(new FormData(form));
    if (!payload.source_url) payload.source_url = null;
    if (!payload.source_revision) payload.source_revision = null;
    submit.disabled = true;
    message.textContent = 'Receiving local research request…';
    try {
      const record = await client('/api/proposethat/intakes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      render(record);
      message.textContent = 'Saved on this Mac. Independent research has not been performed yet.';
      await loadHistory();
    } catch (error) {
      message.textContent = 'Could not receive: ' + error.message;
    } finally {
      submit.disabled = false;
    }
  });
  exportButton.addEventListener('click', () => {
    if (!active) return;
    const blob = new Blob([JSON.stringify(active, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = element('a');
    link.href = url;
    link.download = active.id + '.json';
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  });
  q('#pt-refresh').addEventListener('click', loadHistory);
  q('#pt-example-owner').addEventListener('click', () => {
    q('#pt-mode').value = 'owner-improvement';
    q('#pt-subject').value = 'Market Compass';
    q('#pt-goal').value = 'Inspect the real daily research workflow. Find one useful, non-duplicate improvement, preserving all 115 nodes and existing Actors, with independent acceptance.';
    q('#pt-source').value = '';
    q('#pt-revision').value = '';
  });
  q('#pt-example-outside').addEventListener('click', () => {
    q('#pt-mode').value = 'outside-trading-source';
    q('#pt-subject').value = '';
    q('#pt-goal').value = 'Compare what the external source actually proves with Market Compass in both directions; find a small safe research-only experiment.';
    q('#pt-source').value = '';
    q('#pt-revision').value = '';
    q('#pt-subject').focus();
  });
  q('#pt-mode').addEventListener('change', () => {
    if (q('#pt-mode').value === 'owner-improvement' && !q('#pt-subject').value) q('#pt-subject').value = 'Market Compass';
  });
  client('/api/proposethat/status').then((state) => {
    q('#pt-connection').textContent = state.local_only && state.trade_execution === false
      ? 'Local intake available' : 'Service state needs review';
  }).catch((error) => { q('#pt-connection').textContent = 'Unavailable: ' + error.message; });
  loadHistory();
})();
