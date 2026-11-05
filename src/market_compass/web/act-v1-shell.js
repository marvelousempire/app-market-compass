(() => {
  const root = document.documentElement;
  const body = document.body;
  const links = [...document.querySelectorAll('[data-act-shell-room]')];
  const targets = links.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  const roomLabel = document.querySelector('#act-current-room');
  const roomHelp = document.querySelector('#act-room-help');
  const dialog = document.querySelector('#act-command-dialog');
  const dialogSearch = document.querySelector('#act-command-search');
  const dialogResults = document.querySelector('#act-command-results');
  const recovery = document.querySelector('#act-layout-recovery');
  const roomDescriptions = {
    overview: 'Top-line runtime, controls, Actors, and research status.', runtime: 'Commissioned source, host, safety mode, and runtime receipts.', actors: 'Omo, Prince, Wuda, and Brown’s governed Actor spaces.', exchange: 'Read-only Market Exchange and bankTHAT contract inventory.', desk: 'Market analysis, price memory, momentum, and evidence.', intel: 'Independent local research and proof-health receipts.', route: 'Price path, bus stops, invalidation, and confluence.', timeframes: '4H, daily, and weekly alignment.', evidence: 'Score contributions and historical calibration.', catalysts: 'Recent human-factor and market-news evidence.'
  };

  const safeStore = { get(key) { try { return localStorage.getItem(key); } catch { return null; } }, set(key, value) { try { localStorage.setItem(key, value); } catch {} } };
  const selectRoom = (id) => {
    links.forEach((link) => {
      const active = link.dataset.actShellRoom === id;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
    });
    const active = links.find((link) => link.dataset.actShellRoom === id);
    if (active && roomLabel) roomLabel.textContent = active.querySelector('b')?.textContent || id;
    if (roomHelp) roomHelp.textContent = roomDescriptions[id] || '';
  };

  document.querySelectorAll('.act-nav-group-toggle').forEach((button) => button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') !== 'false';
    button.setAttribute('aria-expanded', String(!expanded));
    const group = button.closest('[data-nav-group]')?.dataset.navGroup;
    if (group) safeStore.set(`act-v1-group-${group}`, expanded ? 'collapsed' : 'open');
  }));
  document.querySelectorAll('[data-nav-group]').forEach((group) => {
    if (safeStore.get(`act-v1-group-${group.dataset.navGroup}`) === 'collapsed') group.querySelector('.act-nav-group-toggle')?.setAttribute('aria-expanded', 'false');
  });

  const setColor = (color) => {
    root.dataset.actColor = color;
    safeStore.set('act-v1-color', color);
    document.querySelectorAll('[data-act-color]').forEach((button) => button.setAttribute('aria-checked', String(button.dataset.actColor === color)));
  };
  const setLayout = (layout) => {
    body.dataset.actLayout = layout;
    safeStore.set('act-v1-layout', layout);
    document.querySelectorAll('[data-act-layout]').forEach((button) => {
      const selected = button.dataset.actLayout === layout;
      button.setAttribute(button.getAttribute('role') === 'radio' ? 'aria-checked' : 'aria-pressed', String(selected));
    });
    recovery?.classList.toggle('hidden', layout === 'control-room');
    if (recovery) recovery.textContent = layout === 'focus' ? '▣ Open rails' : '▣ Open right rail';
  };
  document.querySelectorAll('[data-act-color]').forEach((button) => button.addEventListener('click', () => setColor(button.dataset.actColor)));
  document.querySelectorAll('[data-act-layout]').forEach((button) => button.addEventListener('click', () => setLayout(button.dataset.actLayout)));
  setColor(safeStore.get('act-v1-color') || 'system');
  setLayout(safeStore.get('act-v1-layout') || 'control-room');

  const collapse = document.querySelector('#act-rail-collapse');
  const setCompact = (compact) => {
    body.classList.toggle('act-shell-compact', compact);
    safeStore.set('act-v1-compact', compact ? '1' : '0');
    collapse?.setAttribute('aria-label', compact ? 'Expand sidebar' : 'Collapse sidebar');
  };
  collapse?.addEventListener('click', () => setCompact(!body.classList.contains('act-shell-compact')));
  setCompact(safeStore.get('act-v1-compact') === '1');
  recovery?.addEventListener('click', () => setLayout('control-room'));

  const commandRooms = links.map((link) => ({ id: link.dataset.actShellRoom, href: link.getAttribute('href'), icon: link.querySelector('span')?.textContent || '•', label: link.querySelector('b')?.textContent || link.dataset.actShellRoom }));
  const renderCommands = (query = '') => {
    if (!dialogResults) return;
    const needle = query.trim().toLowerCase();
    dialogResults.innerHTML = commandRooms.filter((item) => !needle || `${item.label} ${roomDescriptions[item.id] || ''}`.toLowerCase().includes(needle)).map((item) => `<a href="${item.href}" data-command-room="${item.id}"><span aria-hidden="true">${item.icon}</span>${item.label}</a>`).join('');
    dialogResults.querySelectorAll('[data-command-room]').forEach((link) => link.addEventListener('click', () => { selectRoom(link.dataset.commandRoom); dialog?.close(); }));
  };
  const openDialog = () => { renderCommands(); dialog?.showModal(); setTimeout(() => dialogSearch?.focus(), 0); };
  document.querySelectorAll('[data-act-command="menu"],[data-act-command="search"],[data-act-command="settings"]').forEach((button) => button.addEventListener('click', openDialog));
  document.querySelectorAll('[data-act-dialog-close]').forEach((button) => button.addEventListener('click', () => dialog?.close()));
  dialogSearch?.addEventListener('input', () => renderCommands(dialogSearch.value));
  window.addEventListener('keydown', (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); openDialog(); } });

  document.querySelectorAll('[data-act-command="receipts"]').forEach((button) => button.addEventListener('click', () => document.querySelector('[data-operator-action="receipts"]')?.click()));
  document.querySelectorAll('[data-act-symbol]').forEach((button) => button.addEventListener('click', () => { const input = document.querySelector('#symbol'); if (!input) return; input.value = button.dataset.actSymbol; input.dispatchEvent(new Event('change', { bubbles: true })); document.querySelector('#analyze')?.click(); }));
  links.forEach((link) => link.addEventListener('click', () => selectRoom(link.dataset.actShellRoom)));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => { const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]; if (visible) { const link = links.find((item) => item.getAttribute('href') === `#${visible.target.id}`); if (link) selectRoom(link.dataset.actShellRoom); } }, { rootMargin: '-15% 0px -70%', threshold: [0, .2, .6] });
    targets.forEach((target) => observer.observe(target));
  }
})();
