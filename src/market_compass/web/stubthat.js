/* Governed stubTHAT module foundry. Source owners remain authoritative. */
(() => {
  const exchangeSurfaces = [
    ['dashboard', 'Exchange Dashboard', 'Product, enabled, external and connector totals', 'admin:/marketplace'],
    ['catalog', 'Catalog', 'Filterable cards for agents, externals and connectors', 'admin:/marketplace/catalog'],
    ['products', 'All Products', 'Searchable product table with type, metadata, API and install state', 'admin:/marketplace/products'],
    ['product-editor', 'Product Editor', 'General, UI, API/auth, SSO and install contract panels', 'admin:/marketplace/products/:id'],
    ['installed', 'Installed Tools', 'Installed plugin and application inventory', 'admin:/installed'],
    ['api-observatory', 'API Observatory', 'API and MCP health, routes and owner evidence', 'admin:/api-observatory'],
  ].map(([id, name, purpose, source]) => ({
    id: `exchange-${id}`, name, purpose, source, family: 'Market Exchange',
    console: 'Exchange Admin', owner: 'Market Exchange owner', classification: 'admin-surface',
  }));
  const exchangeProducts = [
    ['bishop-cluster','agent','Bishop Cluster','Kingdom factory, SSO issuer and audit'],
    ['dustpan','agent','DustPan','Disk rescue and cleanup'],
    ['github-control','agent','GitHub Control','Repositories, pull requests and actions'],
    ['server-operator','agent','Server Operator','VPS files, SSH and metrics'],
    ['dockyard','agent','Dockyard','Local container operator'],
    ['clinic','agent','Clinic','Diagnostic case register'],
    ['automata-pad','agent','Automata Pad','Belief-system desktop shell'],
    ['market-source-refinery','agent','Market Source Refinery','Provenance-bound intake for repositories, URLs, files and pasted text'],
    ['gitlab','external','GitLab CE','Self-hosted Git and CI'],
    ['n8n','external','n8n','Workflow automation'],
    ['portainer','external','Portainer','Container fleet UI'],
    ['roborock','connector','Roborock','Vacuum and mop connector slot'],
    ['smartlife','connector','Samsung SmartLife','Smart-device connector slot'],
    ['apple-shortcuts','connector','Apple Shortcuts','Home-automation bridge slot'],
    ['home-assistant','connector','Home Assistant','Unified smart-home hub slot'],
  ].map(([id, kind, name, purpose]) => ({
    id: `exchange-product-${id}`, name, purpose, source: `catalog:${id}`, family: 'Market Exchange',
    console: `${kind[0].toUpperCase()}${kind.slice(1)} tools`, owner: 'Market Exchange owner',
    classification: `${kind}-module`, kind, slug: id,
    enabled: !['roborock','smartlife','apple-shortcuts','home-assistant'].includes(id),
    metadataMode: ['bishop-cluster','dustpan','github-control','dockyard','clinic'].includes(id) ? 'hybrid' : 'product',
    authMode: ['gitlab','n8n','portainer','home-assistant'].includes(id) ? 'oidc' : ['roborock','smartlife'].includes(id) ? 'api_key' : 'session_verify',
  }));
  const exchange = [...exchangeSurfaces, ...exchangeProducts];

  const bankConsoles = {
    'Bank & Accounts Console': ['bank-import','column-detection','source-folder','institution-profile','account-cassette','account-member','transaction-normalize','transaction-view','vendor-alias','ledger-chart','ledger-journal','receipt-record','receipt-intake','receipt-link','balance-reconcile','finance-workflow'],
    'Income Console': ['income-streams','deposits','work-logs','deals','pipeline','payroll','income-recon','income-tax-summary'],
    'Forecast & Analysis Console': ['cashflow','recurring','scenario','goals','accuracy','spending','financial-pulse'],
    'Tax Console': ['irc-reference','tax-document-intake','tax-line-classify','tax-evidence','daily-financial-report'],
    'Assets & Inventory Console': ['property-portfolio','property-search','property-liens','vehicle-registry','personal-property','maintenance','asset-inventory','document-catalog'],
    'Investments Console': ['crypto-holdings','crypto-transactions','defi','crypto-tax','trading-portfolio','options','tax-lots','investment-performance'],
    'Finance Operations Console': ['finance-calendar','family-entities','reports','capture','evaluation','storage-setup'],
  };
  const title = id => id.split('-').map(word => word === 'defi' ? 'DeFi' : word[0].toUpperCase() + word.slice(1)).join(' ');
  const bankthat = Object.entries(bankConsoles).flatMap(([consoleName, ids]) => ids.map(id => ({
    id: `bankthat-${id}`, name: title(id), purpose: `${title(id)} candidate responsibility`,
    source: `Bank Reader census · ${id}`, family: 'bankTHAT', console: consoleName,
    owner: 'marvelousempire/bank-reader', classification: 'reviewed private read-only evidence contract',
    provenance: 'bank-reader capability census · no account payload copied',
    critical: id === 'ledger-journal',
  })));

  const families = { exchange, bankthat };
  const grid = document.getElementById('stubthat-grid');
  const summary = document.getElementById('stubthat-summary');
  const inspector = document.getElementById('stubthat-inspector');
  const exchangeConsole = document.getElementById('exchange-console');
  const tabs = [...document.querySelectorAll('[data-stub-family]')];
  let exchangeFilter = 'all';
  let exchangeQuery = '';
  let actRoom = 'dashboard';
  const roomButtons = [...document.querySelectorAll('[data-act-room]')];
  const pipelineButtons = [...document.querySelectorAll('[data-pipeline-stage]')];
  const pipeline = {
    parseTHAT: ['Inventory parsed', 'Records source shape, dependencies, external calls, persistence, credentials, and write paths before admission.'],
    decantTHAT: ['Boundary applied', 'Classifies each capability as reuse, adapt, reference, or reject; broker and money-moving behavior is rejected.'],
    htmlTHAT: ['Semantic surface ready', 'Projects headings, controls, tables, receipts, and empty states with accessible native structure.'],
    cssTHAT: ['ACT v1 presentation ready', 'Uses the shared System, Light, and Dark semantic palette without importing donor identity.'],
    jsTHAT: ['Local behavior ready', 'Provides selection, filters, validation, hashing, and export without executing donor code.'],
    stubTHAT: ['Contract assembled', 'Publishes the reviewed read-only contract and provenance receipt while owner engines remain authoritative.'],
  };

  const layer = (name, text) => `<div><span>${name}</span><strong>${text}</strong></div>`;
  const sourceIntakeMarkup = `<form class="source-intake" id="source-intake">
    <label>Source type<select name="kind"><option value="repository">Repository</option><option value="url">URL</option><option value="file">File</option><option value="text">Pasted text</option></select></label>
    <label>License<input name="license" required placeholder="MIT, Apache-2.0, proprietary review…"></label>
    <label class="source-wide">Locator or pasted text<textarea name="locator" rows="3" required placeholder="Repository URL, page URL, or the text to refine"></textarea></label>
    <label>Immutable revision or hash<input name="revision" placeholder="Commit, version, or generated content hash"></label>
    <label>Local file<input name="file" type="file"></label>
    <label class="source-wide">Requested research outcome<input name="outcome" required placeholder="What should this source help Market Compass measure or interpret?"></label>
    <div class="source-intake-actions"><button type="submit" class="secondary">Create intake receipt</button><button type="button" class="secondary" data-source-export disabled>Export receipt</button></div>
    <pre class="source-intake-output" data-source-output>Complete the fields. The browser hashes local content; it never uploads or executes the donor.</pre>
  </form>`;

  async function sha256(bytes) {
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
  }

  function downloadJson(payload, name) {
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url; link.download = name; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
  }

  function bindSourceIntake() {
    const form = inspector.querySelector('#source-intake');
    if (!form) return;
    let receipt = null;
    const output = form.querySelector('[data-source-output]');
    const exportButton = form.querySelector('[data-source-export]');
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const fields = new FormData(form);
      const kind = String(fields.get('kind'));
      const file = fields.get('file');
      const locator = String(fields.get('locator')).trim();
      const fileBytes = file instanceof File && file.size ? await file.arrayBuffer() : null;
      const contentHash = await sha256(fileBytes || new TextEncoder().encode(locator));
      const revision = String(fields.get('revision')).trim() || `sha256:${contentHash}`;
      if ((kind === 'repository' || kind === 'url') && !String(fields.get('revision')).trim()) {
        output.textContent = 'Repository and URL intake requires an immutable commit, version, or content hash.';
        return;
      }
      receipt = {
        schema: 'market-source-refinery-intake.v1',
        source: { kind, locator: kind === 'file' ? file.name : locator, revision, license: String(fields.get('license')).trim(), retrieved_at: new Date().toISOString(), content_sha256: contentHash },
        requested_outcome: String(fields.get('outcome')).trim(),
        decisions: ['inventory pending', 'license review required', 'reuse/adapt/reference/reject required'],
        authority: { research_only: true, trade_execution: false, score_influence: false, money_movement: false, donor_execution: false },
        placement: ['Brown’s Barometers', 'Wuda', 'Omo or Prince comp card', 'intelTHAT', 'calculateTHAT', 'Market Exchange'],
        rejected: ['broker adapters', 'orders', 'credentials', 'account mutation', 'money movement', 'unsupported performance claims']
      };
      output.textContent = JSON.stringify(receipt, null, 2); exportButton.disabled = false;
    });
    exportButton.addEventListener('click', () => receipt && downloadJson(receipt, 'market-source-refinery-intake.json'));
  }

  function renderInspector(item, { reveal = true } = {}) {
    const productTabs = item.kind ? `<div class="exchange-inspector-tabs" role="tablist" aria-label="Product contract sections">${['General','UI','API & auth','SSO','Install'].map((name, index) => `<button type="button" role="tab" class="${index === 0 ? 'active' : ''}" aria-selected="${index === 0}" data-product-panel="${name}">${name}</button>`).join('')}</div><div class="exchange-product-panel" id="exchange-product-panel" role="tabpanel"></div>` : '';
    inspector.innerHTML = `
      <div class="stubthat-inspector-head"><div><p class="eyebrow">SELECTED MODULE CONTRACT</p><h3>${item.name}</h3></div><span class="stub-state">${item.family === 'bankTHAT' ? 'reviewed · private · read only' : item.slug === 'market-source-refinery' ? 'intake workflow ready' : 'owner-bound contract'}</span></div>
      <p>${item.purpose}. This module exposes reviewed local behavior and contract evidence only; it does not claim donor execution, credentials, money movement, or authority owned by another product.</p>
      <div class="stubthat-contract">
        ${layer('Owner', item.owner)}${layer('Console', item.console)}${layer('Source', item.source)}${layer('Classification', item.classification)}
        ${layer('htmlTHAT', 'semantic shell ready')}${layer('cssTHAT', 'ACT v1 admin presentation ready')}${layer('jsTHAT', 'local inspect/select behavior only')}${layer('Authority', 'read-only · no broker execution · no money movement')}
      </div>
      ${productTabs}
      ${item.slug === 'market-source-refinery' ? sourceIntakeMarkup : ''}
      ${item.critical ? '<p class="stub-warning"><b>Write hazard held:</b> the legacy Ledger empty-state auto-generate POST is excluded. An explicit, approved, repeat-safe adapter and receipt are required.</p>' : ''}`;
    if (item.kind) {
      const panel = inspector.querySelector('#exchange-product-panel');
      const drawPanel = name => {
        const content = {
          General: [['Product ID', item.slug], ['Type', item.kind], ['Metadata', item.metadataMode], ['State', item.enabled ? 'enabled in source catalog' : 'off / coming soon']],
          UI: [['Surface', item.console], ['Presentation', 'Market Compass read-only adapter'], ['Owner UI', 'not embedded']],
          'API & auth': [['Authentication', item.authMode], ['API base', 'held behind owner adapter'], ['Health', 'not probed by this stub']],
          SSO: [['SSO contract', item.authMode === 'oidc' ? 'owner OIDC required' : 'not declared'], ['Session', 'no credential copied']],
          Install: [['Installed state', item.enabled ? 'catalog-enabled; installation unverified' : 'not enabled'], ['Action', 'approval-gated; unavailable in stub']],
        }[name];
        panel.innerHTML = content.map(([label, value]) => `<div><span>${label}</span><strong>${value}</strong></div>`).join('');
      };
      inspector.querySelectorAll('[data-product-panel]').forEach(button => button.addEventListener('click', () => {
        inspector.querySelectorAll('[data-product-panel]').forEach(other => {
          const selected = other === button;
          other.classList.toggle('active', selected);
          other.setAttribute('aria-selected', String(selected));
        });
        drawPanel(button.dataset.productPanel);
      }));
      drawPanel('General');
    }
    bindSourceIntake();
    if (reveal) inspector.scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  }

  function filteredExchangeProducts() {
    return exchangeProducts.filter(item => (exchangeFilter === 'all' || item.kind === exchangeFilter || (exchangeFilter === 'enabled' && item.enabled) || (exchangeFilter === 'disabled' && !item.enabled)) && (!exchangeQuery || `${item.name} ${item.slug} ${item.purpose}`.toLowerCase().includes(exchangeQuery)));
  }

  function drawExchangeProducts() {
    const items = filteredExchangeProducts();
    grid.innerHTML = items.map(item => `<button type="button" class="stub-card exchange-product-card" data-stub-id="${item.id}"><span class="stub-family">${item.kind} · ${item.metadataMode}</span><strong>${item.name}</strong><small>${item.purpose}</small><span class="stub-layers"><i>${item.enabled ? 'ON' : 'OFF'}</i><i>${item.authMode}</i><i>READ ONLY</i></span><span class="stub-foot">Inspect product contract</span></button>`).join('') || '<p class="muted">No exchange tools match this search.</p>';
    grid.querySelectorAll('[data-stub-id]').forEach(button => button.addEventListener('click', () => {
      grid.querySelectorAll('.stub-card').forEach(card => card.classList.toggle('selected', card === button));
      renderInspector(exchangeProducts.find(item => item.id === button.dataset.stubId));
    }));
  }

  function renderExchangeConsole() {
    const enabled = exchangeProducts.filter(item => item.enabled).length;
    exchangeConsole.hidden = false;
    exchangeConsole.innerHTML = `<div class="exchange-dashboard">${[['Products',exchangeProducts.length],['Enabled',enabled],['Externals',exchangeProducts.filter(x=>x.kind==='external').length],['Connectors',exchangeProducts.filter(x=>x.kind==='connector').length]].map(([label,value])=>`<div><span>${label}</span><strong>${value}</strong></div>`).join('')}</div><div class="exchange-toolbar"><input type="search" id="exchange-search" placeholder="Search tools or module IDs…" aria-label="Search exchange tools"><div role="group" aria-label="Filter exchange tools">${['all','agent','external','connector','enabled','disabled'].map(name=>`<button type="button" data-exchange-filter="${name}" class="${name==='all'?'active':''}">${name}</button>`).join('')}</div></div><p class="trust-note">Catalog actions are inspect-only. Enable, save, install, API calls and SSO remain with their owners and require separate approval.</p>`;
    exchangeConsole.querySelector('#exchange-search').addEventListener('input', event => { exchangeQuery = event.target.value.trim().toLowerCase(); drawExchangeProducts(); });
    exchangeConsole.querySelectorAll('[data-exchange-filter]').forEach(button => button.addEventListener('click', () => {
      exchangeFilter = button.dataset.exchangeFilter;
      exchangeConsole.querySelectorAll('[data-exchange-filter]').forEach(other => other.classList.toggle('active', other === button));
      drawExchangeProducts();
    }));
    drawExchangeProducts();
  }

  function openActRoom(room) {
    actRoom = room;
    roomButtons.forEach(button => button.classList.toggle('active', button.dataset.actRoom === room));
    if (room === 'dashboard') { exchangeFilter = 'all'; exchangeQuery = ''; renderExchangeConsole(); }
    if (room === 'catalog' || room === 'products') { exchangeFilter = 'all'; exchangeQuery = ''; renderExchangeConsole(); exchangeConsole.querySelector('#exchange-search').focus(); }
    if (room === 'installed') { exchangeFilter = 'enabled'; exchangeQuery = ''; renderExchangeConsole(); exchangeConsole.querySelector('[data-exchange-filter="enabled"]').click(); }
    if (room === 'apis') { exchangeFilter = 'external'; exchangeQuery = ''; renderExchangeConsole(); exchangeConsole.querySelector('[data-exchange-filter="external"]').click(); }
    if (room === 'observatory') { exchangeFilter = 'all'; exchangeQuery = ''; renderExchangeConsole(); renderInspector(exchangeProducts[0]); inspector.querySelector('[data-product-panel="API & auth"]').click(); }
    exchangeConsole.scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  }

  function render(family) {
    const items = families[family];
    const consoleCount = new Set(items.map(item => item.console)).size;
    summary.innerHTML = `<b>${items.length} modules inventoried</b><span>${consoleCount} ${consoleCount === 1 ? 'console' : 'consoles'}</span><span>parseTHAT complete</span><span>decantTHAT boundaries applied</span><span>${family === 'bankthat' ? 'private evidence contracts reviewed' : 'owner authority preserved'}</span>`;
    if (family === 'exchange') {
      renderExchangeConsole();
    } else {
      exchangeConsole.hidden = true;
      grid.innerHTML = items.map(item => `<button type="button" class="stub-card${item.critical ? ' critical' : ''}" data-stub-id="${item.id}">
      <span class="stub-family">${item.console}</span><strong>${item.name}</strong><small>${item.purpose}</small>
      <span class="stub-layers"><i>HTML</i><i>CSS</i><i>JS</i><i>STUB</i></span>
      <span class="stub-foot">${item.critical ? 'write hazard held' : 'read-only contract'}</span>
      </button>`).join('');
      grid.querySelectorAll('[data-stub-id]').forEach(button => button.addEventListener('click', () => {
        grid.querySelectorAll('.stub-card').forEach(card => card.classList.toggle('selected', card === button));
        renderInspector(items.find(item => item.id === button.dataset.stubId));
      }));
    }
    tabs.forEach(tab => {
      const active = tab.dataset.stubFamily === family;
      tab.classList.toggle('active', active); tab.setAttribute('aria-selected', String(active));
    });
    renderInspector(family === 'exchange' ? exchangeProducts[0] : items[0], { reveal: false });
  }

  tabs.forEach(tab => tab.addEventListener('click', () => render(tab.dataset.stubFamily)));
  roomButtons.forEach(button => button.addEventListener('click', () => openActRoom(button.dataset.actRoom)));
  pipelineButtons.forEach(button => button.addEventListener('click', () => {
    const [state, detail] = pipeline[button.dataset.pipelineStage];
    pipelineButtons.forEach(other => other.classList.toggle('active', other === button));
    inspector.innerHTML = `<div class="stubthat-inspector-head"><div><p class="eyebrow">MARKET EXCHANGE PIPELINE</p><h3>${button.dataset.pipelineStage}</h3></div><span class="stub-state">${state}</span></div><p>${detail}</p><div class="stubthat-contract">${layer('Inputs', 'reviewed source material')}${layer('Output', 'provenance-bound read-only contract')}${layer('Authority', 'research only')}${layer('Refusal', 'orders · credentials · money movement')}</div>`;
    inspector.scrollIntoView({ block: 'nearest' });
  }));
  render('exchange');
})();
