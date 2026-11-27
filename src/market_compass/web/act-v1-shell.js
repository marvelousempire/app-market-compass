(() => {
  const root = document.documentElement;
  const body = document.body;
  const links = [...document.querySelectorAll('[data-act-shell-room]')];
  const targets = links.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  const roomLabel = document.querySelector('#act-current-room');
  const roomHelp = document.querySelector('#act-room-help');
  const roomSubmenu = document.querySelector('#act-room-submenu');
  const dialog = document.querySelector('#act-command-dialog');
  const dialogSearch = document.querySelector('#act-command-search');
  const dialogResults = document.querySelector('#act-command-results');
  const recovery = document.querySelector('#act-layout-recovery');
  const roomDescriptions = {
    overview: 'Top-line runtime, controls, Actors, and research status.', runtime: 'Commissioned source, host, safety mode, and runtime receipts.', settings: 'Market prices, reviewed imports, publisher choices, and appearance.', actors: 'Omo, Prince, Wuda, and Brown’s governed Actor spaces.', exchange: 'Read-only Market Exchange and bankTHAT contract inventory.', 'player-exchange': 'Find players and open their individual records.', 'player-profile': 'One selected Player with intelligence, news, history, evidence, and your view.', 'player-market': 'Ticker-linked market charts, levels, options research, reports, and evidence.', measurement: 'Choose any subject and evaluate its measurements with a named method, using a transparent hypothetical index.', desk: 'Market analysis, price memory, momentum, and evidence.', options: 'Theoretical options, virtual positions, Alpaca context, and SEC filings.', 'intel-app': 'Four source-bound research rooms for the selected desk symbol.', intel: 'Independent local research and proof-health receipts.', gates: 'Transparent go, watch, do-not-go, and invalidation research signals.', channel: 'Ticker-linked articles, publisher links, filings, and spoken headlines.', route: 'Price path, bus stops, invalidation, and confluence.', timeframes: '4H, daily, and weekly alignment.', evidence: 'Score contributions and historical calibration.', catalysts: 'Recent human-factor and market-news evidence.'
  };
  const roomSubmenus = {
    overview: [['Runtime status', '#operator-deck'], ['Player controls', '.control-bar'], ['Actor Studio', '#actor-spaces'], ['Market Exchange', '#market-exchange']],
    settings: [['Market prices', '#market-data-settings'], ['Upload files', '#market-settings-upload'], ['Publisher choices', '#market-settings-publishers'], ['Appearance', '#market-settings-appearance']],
    runtime: [['Preview controls', '#operator-deck'], ['Player controls', '.control-bar'], ['Watchlist', '.watch-row']],
    actors: [['Omo', 'cassette:omo'], ['Prince', 'cassette:prince'], ['Wuda', 'cassette:wuda'], ['Brown’s Barometers', 'cassette:browns-barometers']],
    exchange: [['Dashboard', 'exchange:dashboard'], ['Catalog', 'exchange:catalog'], ['All products', 'exchange:products'], ['Installed', 'exchange:installed'], ['APIs & MCPs', 'exchange:apis'], ['API Observatory', 'exchange:observatory']],
    'player-exchange': [['All Players', 'player-filter:all'], ['Watched', 'player-filter:watched'], ['Studied', 'player-filter:studied'], ['No analysis', 'player-filter:unread'], ['Journaled', 'player-filter:journaled'], ['Market desk', '#player-market-studio']],
    'player-profile': [['Overview', 'player-profile:overview'], ['Intelligence', 'player-profile:intelligence'], ['Player News', 'player-profile:news'], ['Price history', 'player-profile:history'], ['Evidence & receipts', 'player-profile:proof'], ['My view', 'player-profile:view'], ['Market Studio', '#player-market-studio']],
    'player-market': [['Market pulse', 'player-market:pulse'], ['Chart room', 'player-market:chart'], ['Training translation', 'player-market:translation'], ['Levels & signals', 'player-market:levels'], ['Matchup splits', 'player-market:splits'], ['Option chain', 'player-market:options'], ['Futures board', 'player-market:futures'], ['Market reports', 'player-market:reports'], ['Market evidence', 'player-market:evidence'], ['My market desk', 'player-market:desk'], ['Method & safety', 'player-market:method']],
    measurement: [['Subject schedules', '#hcck-profiles'], ['Measure and simulate', '#universal-simulator'], ['Original market desk', '#market-workspace']],
    options: [['Option chain', 'options-view:chain', [['Expiration','expiry'],['Calls and puts','types'],['Strike prices','strikes']]], ['Trade builder', 'options-view:builder', [['Action','action'],['Risk','risk'],['Virtual order','order']]], ['Returns', 'options-view:returns', [['Price and time','scenario'],['Volatility','volatility'],['Chart','chart']]], ['Strategies', 'options-view:strategies', [['Legs','legs'],['Risk','risk'],['Chart','chart']]], ['Alpaca data', 'options-view:alpaca', [['Quote','quote'],['Refresh','refresh']]], ['SEC filings', 'options-view:edgar', [['Filings','filings']]], ['Positions', 'options-view:positions', [['Open positions','open']]], ['Journal', 'options-view:journal', [['Entries','entries']]]],
    'intel-app': [['Cockpit', 'intel-view:cockpit'], ['Market Pack', 'intel-view:pack'], ['Macro Conditions', 'intel-view:macro'], ['News Intelligence', 'intel-view:rss'], ['SEC Monitor', 'intel-view:edgar'], ['Run History', 'intel-view:receipts']],
    desk: [['Intelligence overview', '.intelligence-overview'], ['Day Trader lens', '#day-trader-lens'], ['Price route', '#route-panel'], ['Timeframes', '#timeframe-panel'], ['Evidence', '#evidence-panel'], ['Catalysts', '#catalyst-panel']],
    intel: [['Day Trader lens', '#day-trader-lens'], ['Local receipts', '#intelthat-panel'], ['Historical analogs', '#history-panel'], ['Forecast', '#forecast-panel'], ['Evidence board', '#evidence-board']],
    gates: [['Decision gates', '#decision-gates'], ['calculateTHAT', '#calculate-that-formula'], ['Refresh signal', 'click:#calculate-that-run']],
    channel: [['Articles and videos', 'channel-view:articles'], ['SEC filings', 'channel-view:filings'], ['Sources and publishers', 'channel-view:sources'], ['Listen to headlines', 'channel-view:listen']],
    route: [['Bus Stop route', '#route-panel'], ['Nephew analyst', '.analyst-panel'], ['Timeframe alignment', '#timeframe-panel']],
    timeframes: [['4H / 1D / 1W', '#timeframe-panel'], ['Price workbench', '.chart-memory'], ['Evidence contributions', '#evidence-panel']],
    evidence: [['Contributions', '#contributions'], ['Historical calibration', '#calibration'], ['Bull and bear cases', '.contrast'], ['Evidence board', '#evidence-board']],
    catalysts: [['Catalyst timeline', '#catalyst-panel'], ['Decision gates', '#decision-gates'], ['intelTHAT receipts', '#intelthat-panel']]
  };
  const roomLanding = {overview:'#operator-deck',runtime:'#operator-deck',settings:'#market-data-settings',actors:'#actor-spaces',exchange:'#market-exchange','player-exchange':'#player-exchange','player-profile':'#player-profile','player-market':'#player-market-studio',measurement:'#measurement-studio',desk:'.intelligence-overview',options:'#options-lab','intel-app':'#intelthat-app',intel:'#intelthat-panel',gates:'#decision-gates',channel:'#asset-channel',route:'#route-panel',timeframes:'#timeframe-panel',evidence:'#evidence-panel',catalysts:'#catalyst-panel'};
  const main = document.querySelector('main.shell');
  let focusedSelector = roomLanding.overview;
  const focusCanvas = selector => {
    if (!main || !selector) return;
    focusedSelector = selector;
    const found = document.querySelector(selector);
    if (!found || !main.contains(found)) return;
    const target = found.closest('section,article') || found;
    main.querySelectorAll('.act-room-hidden').forEach(node => node.classList.remove('act-room-hidden'));
    let node = target;
    while (node && node !== main) {
      for (const sibling of node.parentElement?.children || []) {
        if (sibling !== node && sibling !== document.querySelector('.control-bar') && sibling !== document.querySelector('#error') && sibling !== document.querySelector('#identity-strip')) sibling.classList.add('act-room-hidden');
      }
      node = node.parentElement;
    }
    body.classList.add('act-room-mode');
    main.scrollTop = 0;
    window.scrollTo(0, 0);
    window.dispatchEvent(new Event('resize'));
  };

  const safeStore = { get(key) { try { return localStorage.getItem(key); } catch { return null; } }, set(key, value) { try { localStorage.setItem(key, value); } catch {} } };
  const selectRoom = (id) => {
    body.dataset.actRoom = id;
    const activeLink = links.find(link => link.dataset.actShellRoom === id);
    const title = activeLink?.querySelector('b')?.textContent;
    const heading = document.querySelector('.app-header h1');
    const eyebrow = document.querySelector('.app-header .eyebrow');
    const subtitle = document.querySelector('.app-header .subhead');
    if (heading && title) heading.textContent = title;
    if (eyebrow) eyebrow.textContent = `MARKET COMPASS / ${title || 'OVERVIEW'}`.toUpperCase();
    if (subtitle) subtitle.textContent = roomDescriptions[id] || '';
    links.forEach((link) => {
      const active = link.dataset.actShellRoom === id;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
    });
    const active = links.find((link) => link.dataset.actShellRoom === id);
    if (active && roomLabel) roomLabel.textContent = active.querySelector('b')?.textContent || id;
    if (roomHelp) roomHelp.textContent = roomDescriptions[id] || '';
    if (roomSubmenu) {
      roomSubmenu.replaceChildren(...(roomSubmenus[id] || []).flatMap(([label, target, children]) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.actSubmenuTarget = target;
        button.innerHTML = `<span>${label}</span><i aria-hidden="true">→</i>`;
        if (!children) return [button];
        button.setAttribute('aria-expanded', 'false');
        const childGroup = document.createElement('div');
        childGroup.className = 'act-room-submenu-children';
        childGroup.hidden = true;
        childGroup.setAttribute('aria-label', `${label} sections`);
        childGroup.append(...children.map(([childLabel, focus]) => {
          const child = document.createElement('button');
          child.type = 'button';
          child.dataset.actSubmenuTarget = `options-detail:${target.slice(13)}:${focus}`;
          child.textContent = childLabel;
          return child;
        }));
        return [button, childGroup];
      }));
    }
  };

  const revealTarget = (selector) => {
    const target = document.querySelector(selector);
    if (target?.closest('.research-only')) document.querySelector('.view-btn[data-view="research"]')?.click();
    return target;
  };
  const scrollTarget = (target) => {
    if (!target) return;
    const scroll = () => requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
    if (target.getClientRects().length) scroll();
    else window.addEventListener('marketcompassreport', scroll, { once: true });
  };

  roomSubmenu?.addEventListener('click', (event) => {
    const button = event.target.closest('[data-act-submenu-target]');
    if (!button) return;
    const target = button.dataset.actSubmenuTarget;
    roomSubmenu.querySelectorAll('button').forEach(item => item.removeAttribute('aria-current'));
    button.setAttribute('aria-current', 'true');
    if (target.startsWith('intel-view:')) {
      window.dispatchEvent(new CustomEvent('marketcompassintelview', { detail: { view: target.slice(11) } }));
      focusCanvas('#intelthat-app');
    } else if (target.startsWith('options-view:')) {
      window.dispatchEvent(new CustomEvent('marketcompassoptionsview', { detail: { view: target.slice(13) } }));
      focusCanvas('#options-lab');
    } else if (target.startsWith('options-detail:')) {
      const [, view, focus] = target.split(':');
      window.dispatchEvent(new CustomEvent('marketcompassoptionsview', { detail: { view, focus } }));
      focusCanvas('#options-lab');
    } else if (target.startsWith('player-filter:')) {
      window.dispatchEvent(new CustomEvent('marketcompassplayerfilter', {detail:{filter:target.slice(14)}}));
      focusCanvas('#player-exchange');
    } else if (target.startsWith('player-profile:')) {
      window.dispatchEvent(new CustomEvent('marketcompassprofileview', {detail:{view:target.slice(15)}}));
      focusCanvas('#player-profile');
    } else if (target.startsWith('player-market:')) {
      window.dispatchEvent(new CustomEvent('marketcompassmarketview', {detail:{view:target.slice(14)}}));
      focusCanvas('#player-market-studio');
    } else if (target.startsWith('channel-view:')) {
      window.dispatchEvent(new CustomEvent('marketcompasschannelview', {detail:{view:target.slice(13)}}));
      focusCanvas('#asset-channel');
    } else if (target.startsWith('cassette:')) {
      document.querySelector(`[data-cassette="${target.slice(9)}"]`)?.click();
      focusCanvas('#actor-spaces');
    } else if (target.startsWith('exchange:')) {
      document.querySelector(`[data-act-room="${target.slice(9)}"]`)?.click();
      focusCanvas('#market-exchange');
    } else if (target.startsWith('click:')) {
      document.querySelector(target.slice(6))?.click();
    } else {
      const node = revealTarget(target);
      if (node) focusCanvas(target);
    }
  });
  window.addEventListener('message', event => {
    if (body.dataset.actRoom !== 'options' || event.origin !== location.origin || event.source !== document.querySelector('#options-lab-frame')?.contentWindow || event.data?.type !== 'market-compass-options-view') return;
    const view = event.data.view;
    roomSubmenu?.querySelectorAll('.act-room-submenu-children').forEach(group => { group.hidden = true; });
    roomSubmenu?.querySelectorAll('button[data-act-submenu-target^="options-view:"]').forEach(button => {
      const active = button.dataset.actSubmenuTarget === `options-view:${view}`;
      button.setAttribute('aria-expanded', String(active));
      if (active) button.setAttribute('aria-current', 'true'); else button.removeAttribute('aria-current');
      if (active && button.nextElementSibling?.classList.contains('act-room-submenu-children')) button.nextElementSibling.hidden = false;
    });
  });
  window.addEventListener('message', event => {
    if (body.dataset.actRoom !== 'intel-app' || event.origin !== location.origin || event.source !== document.querySelector('#intelthat-app-frame')?.contentWindow || event.data?.type !== 'market-compass-intel-view') return;
    roomSubmenu?.querySelectorAll('button').forEach(item => {
      if (item.dataset.actSubmenuTarget === `intel-view:${event.data.view}`) item.setAttribute('aria-current', 'true');
      else item.removeAttribute('aria-current');
    });
  });

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
    window.dispatchEvent(new CustomEvent('actappearancechange', { detail: { color } }));
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
    const subRooms = needle ? commandRooms : commandRooms.filter(item => item.id === body.dataset.actRoom);
    const subLinks = subRooms.flatMap(item => (roomSubmenus[item.id] || []).filter(([label]) => !needle || `${item.label} ${label}`.toLowerCase().includes(needle)).map(([label,target]) => `<a href="${item.href}" data-command-sub-room="${item.id}" data-command-sub-target="${target}"><span aria-hidden="true">↳</span>${label}</a>`));
    const roomLinks = commandRooms.filter((item) => !needle || `${item.label} ${roomDescriptions[item.id] || ''}`.toLowerCase().includes(needle)).map((item) => `<a href="${item.href}" data-command-room="${item.id}"><span aria-hidden="true">${item.icon}</span>${item.label}</a>`);
    dialogResults.innerHTML = [...subLinks,...roomLinks].join('');
    dialogResults.querySelectorAll('[data-command-room]').forEach((link) => link.addEventListener('click', event => { event.preventDefault(); history.replaceState(null,'',link.getAttribute('href')); selectRoom(link.dataset.commandRoom); focusCanvas(roomLanding[link.dataset.commandRoom]); dialog?.close(); }));
    dialogResults.querySelectorAll('[data-command-sub-room]').forEach(link => link.addEventListener('click', event => {
      event.preventDefault();
      const room = link.dataset.commandSubRoom;
      history.replaceState(null,'',link.getAttribute('href'));
      selectRoom(room);
      focusCanvas(roomLanding[room]);
      [...roomSubmenu.querySelectorAll('button')].find(button => button.dataset.actSubmenuTarget === link.dataset.commandSubTarget)?.click();
      dialog?.close();
    }));
  };
  const openDialog = () => { renderCommands(); dialog?.showModal(); setTimeout(() => dialogSearch?.focus(), 0); };
  document.querySelectorAll('[data-act-command="menu"],[data-act-command="search"]').forEach((button) => button.addEventListener('click', openDialog));
  document.querySelectorAll('[data-act-command="settings"]').forEach((button) => button.addEventListener('click', () => {history.replaceState(null,'','#market-settings');selectRoom('settings');focusCanvas(roomLanding.settings);}));
  document.querySelectorAll('[data-act-alpaca-entry]').forEach((link) => link.addEventListener('click', (event) => {
    event.preventDefault();
    history.replaceState(null, '', '#market-settings');
    selectRoom('settings');
    focusCanvas('#market-data-settings');
    roomSubmenu?.querySelector('[data-act-submenu-target="#market-data-settings"]')?.setAttribute('aria-current', 'true');
  }));
  document.querySelectorAll('[data-act-dialog-close]').forEach((button) => button.addEventListener('click', () => dialog?.close()));
  dialogSearch?.addEventListener('input', () => renderCommands(dialogSearch.value));
  window.addEventListener('keydown', (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); openDialog(); } });

  document.querySelectorAll('[data-act-command="receipts"]').forEach((button) => button.addEventListener('click', () => document.querySelector('[data-operator-action="receipts"]')?.click()));
  document.querySelectorAll('[data-act-symbol]').forEach((button) => button.addEventListener('click', () => { const input = document.querySelector('#symbol'); if (!input) return; input.value = button.dataset.actSymbol; input.dispatchEvent(new Event('change', { bubbles: true })); document.querySelector('#analyze')?.click(); }));
  links.forEach((link) => link.addEventListener('click', (event) => {
    const selector = link.getAttribute('href');
    const target = selector && revealTarget(selector);
    selectRoom(link.dataset.actShellRoom);
    if (!target) return;
    event.preventDefault();
    history.replaceState(null, '', selector);
    focusCanvas(roomLanding[link.dataset.actShellRoom] || selector);
  }));
  const initialLink = links.find(link => link.getAttribute('href') === location.hash);
  const initialRoom = initialLink?.dataset.actShellRoom || 'overview';
  selectRoom(initialRoom);
  focusCanvas(roomLanding[initialRoom]);
  window.addEventListener('marketcompassreport', () => focusCanvas(focusedSelector));
  window.addEventListener('marketcompassanalysiscomplete', () => {
    history.replaceState(null, '', '#market-workspace');
    selectRoom('desk');
    focusCanvas(roomLanding.desk);
  });
  window.addEventListener('hashchange', () => {
    const link = links.find(item => item.getAttribute('href') === location.hash);
    if (link) {selectRoom(link.dataset.actShellRoom); focusCanvas(roomLanding[link.dataset.actShellRoom]);}
  });
  document.querySelector('.options-link')?.addEventListener('click', event => {event.preventDefault(); history.replaceState(null, '', '#options-lab'); selectRoom('options'); focusCanvas('#options-lab');});
})();
