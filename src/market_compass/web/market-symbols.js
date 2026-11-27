// Market Compass is a public Web symbol reader of the accepted ACT V5 catalog.
// Native Apple targets use the catalog's SF Symbol names; Web uses its outlines.
const rooms = {
  overview: 'home', runtime: 'health', settings: 'settings', actors: 'actor',
  exchange: 'work', 'player-exchange': 'family', 'player-profile': 'profile',
  'player-market': 'studio', measurement: 'fields', desk: 'desktop',
  options: 'shape', 'intel-app': 'brain', intel: 'proof', gates: 'officer',
  channel: 'source', route: 'pathways', timeframes: 'calendar',
  evidence: 'proof', catalysts: 'heartbeat',
};
const views = {
  cockpit: 'home', pack: 'work', macro: 'world-map', rss: 'source',
  edgar: 'rules', receipts: 'proof',
};
const commands = {settings: 'settings', search: 'search', receipts: 'proof', menu: 'menu'};
const operator = {plan: 'queue', status: 'health', launch: 'play', open: 'link', receipts: 'proof', stop: 'close'};
const layouts = {'control-room': 'grid', focus: 'selection-on', 'wide-canvas': 'screen'};
const footer = {overview: 'home', actors: 'actor', exchange: 'work', desk: 'desktop'};
const hrefs = {
  '#market-overview': 'home', '#actor-spaces': 'actor', '#market-exchange': 'work',
  '#market-workspace': 'desktop', '/handbook': 'rules',
};

function bind(target, role) {
  if (target && role) target.dataset.mcSymbolRole = role;
}

function assignRoles(root) {
  root.querySelectorAll('[data-act-shell-room], [data-command-room]').forEach(node =>
    bind(node, rooms[node.dataset.actShellRoom || node.dataset.commandRoom]));
  root.querySelectorAll('[data-intel-view]').forEach(node => bind(node, views[node.dataset.intelView]));
  root.querySelectorAll('[data-operator-action]').forEach(node => bind(node, operator[node.dataset.operatorAction]));
  root.querySelectorAll('[data-act-command]').forEach(node => bind(node, commands[node.dataset.actCommand]));
  root.querySelectorAll('.act-shell-footer [data-act-footer-room]').forEach(node => bind(node, footer[node.dataset.actFooterRoom]));
  root.querySelectorAll('.act-shell-footer [data-act-layout], #act-layout-recovery').forEach(node =>
    bind(node, layouts[node.dataset.actLayout] || 'grid'));
  root.querySelectorAll('.act-mobile-tabs a, .act-shell-nav a:not([data-act-shell-room]), .act-shell-footer a:not([data-act-footer-room])').forEach(node =>
    bind(node, hrefs[node.getAttribute('href')]));
  root.querySelectorAll('.act-nav-group-toggle i').forEach(node => bind(node, 'next'));
  bind(root.querySelector('#act-rail-collapse'), 'previous');
  bind(root.querySelector('#watch-current'), 'tag');
  bind(root.querySelector('#player-profile-back'), 'return');
  bind(root.querySelector('#player-market-close'), 'close');
  bind(root.querySelector('.app-rail a[href="/"]'), 'return');
  root.querySelectorAll('[data-act-dialog-close]').forEach(node => bind(node, 'close'));
}

function iconSlot(target) {
  if (target.matches('span, i')) return target;
  const existing = target.querySelector(':scope > .mc-symbol');
  if (existing) return existing;
  const child = target.querySelector(':scope > [aria-hidden="true"]') ||
    (target.matches('[data-intel-view]') ? target.querySelector(':scope > span') : null);
  if (child) return child;
  const text = [...target.childNodes].find(node => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
  if (!text) return null;
  const match = text.textContent.match(/^(\s*)(?:•••|[^\p{L}\p{N}\s])\s*/u);
  const slot = document.createElement('span');
  slot.setAttribute('aria-hidden', 'true');
  target.insertBefore(slot, text);
  if (match) text.textContent = text.textContent.slice(match[0].length);
  return slot;
}

function render(root, catalog, revision) {
  assignRoles(root);
  root.querySelectorAll('[data-mc-symbol-role]').forEach(target => {
    const role = target.dataset.mcSymbolRole;
    if (target.dataset.mcSymbolRevision === revision && target.querySelector('svg[data-act5-symbol]')) return;
    if (!Object.hasOwn(catalog.SYMBOL_ROLES, role)) {
      target.dataset.mcSymbolState = 'unavailable';
      return;
    }
    const slot = iconSlot(target);
    if (!slot) return;
    slot.classList.add('mc-symbol');
    slot.setAttribute('aria-hidden', 'true');
    slot.innerHTML = catalog.symbolMarkup(role);
    target.dataset.mcSymbolRevision = revision;
    delete target.dataset.mcSymbolState;
  });
}

async function start() {
  try {
    const response = await fetch('/api/ui-symbols/manifest', {cache: 'no-store'});
    if (!response.ok) throw new Error('Shared symbol manifest unavailable');
    const {revision} = await response.json();
    if (!/^[a-f0-9]{40}$/.test(revision)) throw new Error('Invalid shared symbol revision');
    const catalog = await import(`/api/ui-symbols/r/${revision}/symbols.mjs`);
    if (catalog.SYMBOL_CORE_REVISION !== revision || typeof catalog.symbolMarkup !== 'function')
      throw new Error('Shared symbol cohort changed');
    render(document, catalog, revision);
    document.documentElement.dataset.mcSymbolRevision = revision;
    let scheduled = false;
    new MutationObserver(() => {
      if (scheduled) return;
      scheduled = true;
      queueMicrotask(() => { scheduled = false; render(document, catalog, revision); });
    }).observe(document.body, {childList: true, subtree: true});
  } catch (error) {
    document.documentElement.dataset.mcSymbolState = 'unavailable';
    const status = document.createElement('span');
    status.className = 'mc-symbol-status';
    status.setAttribute('role', 'status');
    status.textContent = 'Shared symbols unavailable; original control icons remain.';
    document.body.append(status);
    console.warn('Market Compass symbols:', error);
  }
}

start();
