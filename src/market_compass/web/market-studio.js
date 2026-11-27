(() => {
  const studio = document.querySelector('#player-market-studio');
  const exchange = document.querySelector('#player-exchange');
  const profile = document.querySelector('#player-profile');
  if (!studio || !exchange || !profile) return;

  const $ = (selector, root = document) => root.querySelector(selector);
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const number = (value, digits = 2) => value != null && value !== '' && Number.isFinite(Number(value))
    ? Number(value).toLocaleString(undefined, {minimumFractionDigits: digits, maximumFractionDigits: digits}) : '—';
  const money = value => value != null && value !== '' && Number.isFinite(Number(value)) ? `$${number(value)}` : '—';
  const percent = value => value != null && value !== '' && Number.isFinite(Number(value)) ? `${number(Number(value) * 100, 1)}%` : '—';
  const dateLabel = value => { const date = new Date(value); return Number.isNaN(date.getTime()) ? 'Date unavailable' : date.toLocaleString(); };
  const readablePrices = value => String(value || '').replace(/asset reality/gi,'Player reality').replace(/\bnear\s+([0-9]+(?:\.[0-9]+)?)(?![%\d])/gi, (_, amount) => `near ${money(amount)}`);
  const fact = (label, value, detail = '') => `<article class="player-market-fact"><span>${escape(label)}</span><strong>${escape(value)}</strong>${detail ? `<small>${escape(detail)}</small>` : ''}</article>`;
  const roomLink = (label, hash) => `<a class="player-market-action" href="${hash}">${escape(label)} →</a>`;
  const rooms = [
    ['pulse','Market pulse'], ['chart','Chart room'], ['translation','Training translation'],
    ['levels','Levels & signals'], ['splits','Matchup splits'], ['options','Option chain'],
    ['futures','Futures board'], ['reports','Market reports'], ['evidence','Market evidence'],
    ['desk','My market desk'], ['method','Method & safety']
  ];
  const groups = [['all','All Players'], ['watched','Watched'], ['studied','Studied'], ['unread','No analysis'], ['journaled','Journaled']];
  let report = null;
  let selectedSymbol = null;
  let profileRoom = 'overview';
  let room = 'pulse';
  let charts = [];
  let studies = {ema:true, bands:true, fib:true, volume:true, rsi:true, macd:true};
  let searchMatches = [];
  let searchTimer = 0;
  let searchSerial = 0;
  const names = new Map();
  const getStorage = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key) || 'null') ?? fallback; } catch { return fallback; } };
  const setStorage = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} };
  const catalogKey = 'market-compass-player-exchange-v1';
  const catalogState = {...{filter:'all',sort:'recent',direction:'desc',size:'thin'}, ...getStorage(catalogKey,{})};
  const noteKey = symbol => `market-compass-thesis-v1:${symbol}`;
  const savedNote = symbol => getStorage(noteKey(symbol), null);
  const snapshots = () => getStorage('market-compass-snapshots-v1', []);
  const watched = () => {
    const saved = getStorage('market-compass-watchlist-v1', []);
    const symbols = ['BB','AAPL','QQQ','SPCX', ...(Array.isArray(saved) ? saved : [])];
    return [...new Set(symbols.map(value => String(value).trim().toUpperCase()).filter(Boolean))];
  };
  const studyFor = symbol => report?.symbol === symbol ? {price:report.price,confidence:report.confidence,at:report.as_of}
    : snapshots().find(item => item.symbol === symbol) || null;
  const players = () => {
    const watchedSet = new Set(watched());
    const symbols = [...new Set([...watchedSet, ...searchMatches.map(item => item.symbol)])];
    return symbols.map(symbol => {
      const found = searchMatches.find(item => item.symbol === symbol) || names.get(symbol) || {};
      const study = studyFor(symbol);
      return {symbol, name:found.name || (report?.symbol === symbol ? report.data_meta?.longName : '') || symbol,
        type:found.type || (report?.symbol === symbol ? report.data_meta?.instrumentType : '') || 'Market player',
        exchange:found.exchange || (report?.symbol === symbol ? report.data_meta?.exchangeName : '') || '',
        watched:watchedSet.has(symbol), study, note:savedNote(symbol)};
    });
  };
  const groupFor = player => player.note?.text ? 'journaled' : player.study ? 'studied' : player.watched ? 'watched' : 'new';
  const currentPlayers = () => {
    const filter = catalogState.filter;
    const list = players().filter(player => filter === 'all' ||
      (filter === 'watched' && player.watched) ||
      (filter === 'studied' && !!player.study) ||
      (filter === 'unread' && !player.study) ||
      (filter === 'journaled' && !!player.note?.text));
    const sort = catalogState.sort;
    const direction = catalogState.direction === 'asc' ? 1 : -1;
    list.sort((a,b) => {
      if (sort === 'recent') return direction * ((new Date(a.study?.at || 0)).getTime() - (new Date(b.study?.at || 0)).getTime()) || a.symbol.localeCompare(b.symbol);
      if (sort === 'price') return direction * ((Number(a.study?.price) || 0) - (Number(b.study?.price) || 0)) || a.symbol.localeCompare(b.symbol);
      return direction * String(a[sort] || '').localeCompare(String(b[sort] || ''));
    });
    return list;
  };
  function renderExchange() {
    const all = players(), shown = currentPlayers(), counts = {
      all:all.length, watched:all.filter(x=>x.watched).length, studied:all.filter(x=>x.study).length,
      unread:all.filter(x=>!x.study).length, journaled:all.filter(x=>x.note?.text).length
    };
    $('#player-exchange-summary').innerHTML = [
      ['Catalog',counts.all], ['Watched',counts.watched], ['Studied',counts.studied],
      ['Research coverage',counts.all ? `${Math.round(counts.studied/counts.all*100)}%` : '—']
    ].map(([label,value])=>`<div><strong>${escape(value)}</strong><small>${escape(label)}</small></div>`).join('');
    $('#player-exchange-filters').innerHTML = groups.map(([key,label]) =>
      `<button type="button" data-player-filter="${key}" ${catalogState.filter === key ? 'aria-current="page"' : ''}><b>${label}</b><strong>${counts[key]}</strong></button>`).join('');
    const stages = [['new','New'],['watched','Watching'],['studied','Studied'],['journaled','Journaled']];
    const stageCounts = Object.fromEntries(stages.map(([key])=>[key,all.filter(x=>groupFor(x)===key).length]));
    const ceiling = Math.max(...Object.values(stageCounts),1);
    $('#player-exchange-bars').innerHTML = stages.map(([key,label]) => `<div class="player-exchange-bar"><div class="player-exchange-bar-track"><i class="${key}" style="height:${Math.max(4,stageCounts[key]/ceiling*100)}%"></i></div><span>${label}</span><strong>${stageCounts[key]}</strong></div>`).join('');
    const search = $('#player-exchange-search').value.trim();
    $('#player-exchange-status').textContent = `${shown.length} players in this view${search ? ' · search results included' : ' · your watched catalog'}.`;
    const grid = $('#player-exchange-grid'); grid.dataset.size = catalogState.size;
    grid.innerHTML = shown.map(player => {
      const last = player.study;
      const status = player.note?.text ? 'Journaled' : last ? 'Studied' : player.watched ? 'Watching' : 'New';
      return `<button type="button" class="player-exchange-card" data-player-symbol="${escape(player.symbol)}" aria-label="Open ${escape(player.symbol)} Player record"><span class="player-exchange-card-mark">${escape(player.symbol.slice(0,2))}</span><span class="player-exchange-card-body"><strong>${escape(player.symbol)}</strong><span>${escape(player.name)}</span><small>${escape(player.type)}${player.exchange ? ` · ${escape(player.exchange)}` : ''}</small></span><span class="player-exchange-card-end"><b>${last ? money(last.price) : '—'}</b><small>${status}${last?.at ? ` · ${escape(dateLabel(last.at))}` : ''}</small></span></button>`;
    }).join('') || '<p class="player-exchange-empty">No players in this group. Search a ticker or choose another group.</p>';
    exchange.querySelectorAll('[data-exchange-sort]').forEach(button => button.classList.toggle('active',button.dataset.exchangeSort===catalogState.sort));
    exchange.querySelectorAll('[data-exchange-size]').forEach(button => button.classList.toggle('active',button.dataset.exchangeSize===catalogState.size));
    $('#player-exchange-direction').textContent = catalogState.direction === 'desc' ? 'Newest first' : 'Oldest first';
  }
  const saveCatalog = () => { setStorage(catalogKey,catalogState); renderExchange(); };
  exchange.addEventListener('click', event => {
    const filter = event.target.closest('[data-player-filter]');
    const sort = event.target.closest('[data-exchange-sort]');
    const size = event.target.closest('[data-exchange-size]');
    const card = event.target.closest('[data-player-symbol]');
    if (filter) { catalogState.filter=filter.dataset.playerFilter; saveCatalog(); }
    else if (sort) { catalogState.sort=sort.dataset.exchangeSort; saveCatalog(); }
    else if (size) { catalogState.size=size.dataset.exchangeSize; saveCatalog(); }
    else if (event.target.closest('#player-exchange-direction')) { catalogState.direction=catalogState.direction==='desc'?'asc':'desc'; saveCatalog(); }
    else if (card) {
      const symbol=card.dataset.playerSymbol;
      selectedSymbol=symbol;
      profileRoom='overview';
      renderProfile();
      $('a[data-act-shell-room="player-profile"]')?.click();
      $('#symbol').value=symbol;
      window.dispatchEvent(new CustomEvent('marketcompasschannelanalyze',{detail:{symbol}}));
    }
  });
  window.addEventListener('marketcompassplayerfilter',event => { if (groups.some(([key])=>key===event.detail.filter)) {catalogState.filter=event.detail.filter;saveCatalog();} });
  $('#player-exchange-search').addEventListener('input',event => {
    clearTimeout(searchTimer);
    const query=event.target.value.trim();
    if (!query) { searchMatches=[]; renderExchange(); return; }
    const serial=++searchSerial;
    searchTimer=setTimeout(async()=>{
      $('#player-exchange-status').textContent='Finding players…';
      try {
        const response=await fetch(`/api/symbols?q=${encodeURIComponent(query)}&limit=20`);
        if (!response.ok) throw Error('Search unavailable');
        const rows=await response.json();
        if (serial!==searchSerial) return;
        searchMatches=Array.isArray(rows)?rows.filter(row=>row.symbol):[];
        searchMatches.forEach(row=>names.set(row.symbol,row));
        renderExchange();
      } catch {
        if (serial===searchSerial) { searchMatches=[];renderExchange();$('#player-exchange-status').textContent='Player search is unavailable right now.'; }
      }
    },250);
  });
  // Resolve only the watched cards visible in this browser. The search owner remains the source for names.
  watched().forEach(async symbol => {
    try { const response=await fetch(`/api/symbols?q=${encodeURIComponent(symbol)}&limit=8`);
      if (!response.ok) return;
      const rows=await response.json(); const exact=rows.find(row=>row.symbol===symbol);
      if (exact) { names.set(symbol,exact); renderExchange(); }
    } catch {}
  });

  const profileRooms = [['overview','Overview'],['intelligence','Intelligence'],['news','Player News'],['history','Price history'],['proof','Evidence & receipts'],['view','My view']];
  const profileAction = (label, target) => `<button type="button" class="player-profile-action" data-profile-action="${target}">${escape(label)} →</button>`;
  function renderProfile() {
    const symbol=selectedSymbol || report?.symbol;
    const player=players().find(item=>item.symbol===symbol) || {symbol,name:symbol,type:'Player'};
    const current=report?.symbol===symbol ? report : null;
    const saved=snapshots().filter(item=>item.symbol===symbol).slice(0,12);
    $('#player-profile-title').textContent=symbol ? `${player.name || symbol} · ${symbol}` : 'Choose a Player';
    $('#player-profile-description').textContent=symbol ? `${player.type || 'Player'}${player.exchange ? ` · ${player.exchange}` : ''} · Individual market record` : 'Open a ticker from the Player Exchange to see its individual record.';
    $('#player-profile-price').textContent=current ? money(current.price) : player.study ? money(player.study.price) : '—';
    $('#player-profile-date').textContent=current ? `As of ${dateLabel(current.as_of)}` : player.study?.at ? `Last studied ${dateLabel(player.study.at)}` : 'No market reading yet';
    $('.player-profile-tabs',profile).innerHTML=profileRooms.map(([key,label])=>`<button type="button" data-profile-room="${key}" ${key===profileRoom ? 'aria-current="page"' : ''}>${label}</button>`).join('');
    const lead=`<div class="player-profile-section-head"><p class="eyebrow">${escape(profileRooms.find(([key])=>key===profileRoom)?.[1] || 'PLAYER RECORD')}</p><h3>${escape(symbol || 'Choose a Player')}</h3><p>Source dates and missing evidence stay visible. Market Compass does not change the source record.</p></div>`;
    const empty='<p class="player-profile-empty">Select a Player and wait for its dated market analysis.</p>';
    let content=empty;
    if (symbol && profileRoom==='overview') content=`<div class="player-profile-facts">${fact('Current price',current?money(current.price):player.study?money(player.study.price):'—')}${fact('Market state',current?.action||'Not studied')}${fact('Research confidence',current?percent(current.confidence):'—')}${fact('Source',current?.data_meta?.provider||'Not loaded')}</div><div class="player-profile-story"><h4>The Player at a glance</h4><p>${escape(readablePrices(current?.summary || 'A current market reading has not loaded yet. Price and evidence will appear when the selected ticker responds.'))}</p></div>${profileAction('Open Player Market Studio','studio')}`;
    if (symbol && profileRoom==='intelligence') content=current ? `<div class="player-profile-facts">${fact('Bull evidence',current.bull_evidence??'—')}${fact('Bear evidence',current.bear_evidence??'—')}${fact('Trend',current.layers?.trend?.state||'Unknown')}${fact('Momentum',current.layers?.momentum?.state||'Unknown')}</div><div class="player-profile-story"><h4>What would change this view?</h4><p>${escape(current.invalidation?.summary||current.invalidation||'Open Decision Gates for the current invalidation and risk levels.')}</p></div>${profileAction('Open Decision Gates','gates')}` : empty;
    if (symbol && profileRoom==='news') content=`<div class="player-profile-story"><h4>The living record of ${escape(player.name||symbol)}</h4><p>News, SEC filings, and publication times belong to this selected ticker. Open Player News to check the current source feed.</p></div>${profileAction('Open Player News','news')}`;
    if (symbol && profileRoom==='history') {const tape=current?.timeframes?.['1d']?.chart||current?.chart||{};const bars=(tape.date||[]).slice(-12).map((date,i,dates)=>{const n=(tape.date||[]).length-dates.length+i;return `<article><b>${escape(dateLabel(date))}</b><span>Close ${money(tape.close?.[n])} · Volume ${number(tape.volume?.[n],0)}</span></article>`;}).reverse();content=`<div class="player-profile-story"><h4>Dated price tape</h4><p>Recent market closes for ${escape(symbol)}. Saved research snapshots are listed separately. Neither is a broker transaction.</p></div><div class="player-profile-ledger">${bars.join('')||'<p>No dated price bars available.</p>'}</div><div class="player-profile-story"><h4>Saved studies</h4><p>${saved.length} browser-local snapshots</p></div><div class="player-profile-ledger">${saved.map(item=>`<article><b>${escape(dateLabel(item.at||item.saved_at))}</b><span>${money(item.price)} · Bull ${escape(item.bull??'—')} / Bear ${escape(item.bear??'—')}</span></article>`).join('')||'<p>No saved studies for this Player yet.</p>'}</div>${profileAction('Open chart room','chart')}`;}
    if (symbol && profileRoom==='proof') content=current ? `<div class="player-profile-facts">${fact('Evidence items',current.contributions?.length??0)}${fact('Dated catalysts',current.catalysts?.length??0)}${fact('Retrieved',dateLabel(current.data_meta?.retrieved_at))}${fact('Provider',current.data_meta?.provider||'Unknown')}</div><div class="player-profile-ledger">${(current.contributions||[]).slice(0,8).map(item=>`<article><b>${escape(item.label||'Evidence')}</b><span>${number(item.evidence_points,1)} points · ${percent(item.confidence)} confidence</span></article>`).join('')||'<p>No contribution receipts in this reading.</p>'}</div>${profileAction('Open market evidence','evidence')}` : empty;
    if (symbol && profileRoom==='view') content=`<div class="player-profile-story"><h4>Your private view</h4><p>${escape(savedNote(symbol)?.text || 'No local thesis saved for this Player yet.')}</p><small>${savedNote(symbol)?.at ? `Saved ${escape(dateLabel(savedNote(symbol).at))}` : 'Stored in this browser when you save a thesis.'}</small></div>${profileAction('Open my market desk','desk')}`;
    $('#player-profile-content').innerHTML=lead+content;
  }
  profile.addEventListener('click',event=>{
    const roomButton=event.target.closest('[data-profile-room]');
    if(roomButton){profileRoom=roomButton.dataset.profileRoom;renderProfile();return;}
    if(event.target.closest('#player-profile-back')){$('a[data-act-shell-room="player-exchange"]')?.click();return;}
    const action=event.target.closest('[data-profile-action]')?.dataset.profileAction;
    if(!action)return;
    if(['studio','chart','evidence','desk'].includes(action)){$('a[data-act-shell-room="player-market"]')?.click();window.dispatchEvent(new CustomEvent('marketcompassmarketview',{detail:{view:action==='studio'?'pulse':action}}));}
    else if(action==='news')$('a[data-act-shell-room="channel"]')?.click();
    else if(action==='gates')$('a[data-act-shell-room="gates"]')?.click();
  });
  window.addEventListener('marketcompassprofileview',event=>{profileRoom=event.detail.view;renderProfile();});

  const series = () => report?.timeframes?.['1d']?.chart || report?.chart || {};
  const header = () => {
    const symbol=report?.symbol || 'Player';
    $('#player-market-topline').textContent=`${symbol} · Market Studio`;
    $('#player-market-title').textContent=report ? `${symbol} market desk` : 'Player market desk';
    $('#player-market-context').textContent=report ? 'Three separate evidence books. One player. Every move opens back to dated market proof.' : 'Choose a player to load its market evidence.';
    $('#player-market-symbol').textContent=symbol;
    $('#player-market-price').textContent=report ? money(report.price) : '—';
    $('#player-market-date').textContent=report ? `As of ${dateLabel(report.as_of)}` : 'Waiting for data';
    $('#player-market-books').innerHTML=report ? [
      ['Price tape',money(report.price),'Dated market close','chart'],
      ['Bull case',report.bull_evidence??'—','Evidence for the upside','splits'],
      ['Bear case',report.bear_evidence??'—','Evidence against the upside','splits']
    ].map(([label,value,detail,view])=>`<button type="button" data-book-room="${view}" class="player-market-book"><span>${escape(label)}<strong>${escape(value)}</strong></span><small>${escape(detail)}</small></button>`).join('') : '';
  };
  const clearCharts = () => { charts.forEach(chart => {try{chart.remove()}catch{}});charts=[]; };
  const chartOptions = height => ({height,layout:{background:{color:'#09090b'},textColor:'#d4d4d8'},
    grid:{vertLines:{color:'#242428'},horzLines:{color:'#242428'}},
    rightPriceScale:{borderColor:'#404045'},timeScale:{borderColor:'#404045',timeVisible:true}});
  const seriesPoints = (data,key) => (data.date||[]).map((dt,i)=>({time:Math.floor(new Date(dt).getTime()/1000),value:Number(data[key]?.[i])})).filter(x=>Number.isFinite(x.time)&&Number.isFinite(x.value));
  function paintCharts() {
    const data=series(), dates=data.date||[], target=$('#player-market-chart');
    if (!target) return;
    if (!dates.length) { target.innerHTML='<p>No dated candles are available for this player.</p>';return; }
    if (!window.LightweightCharts) {target.innerHTML='<p>The chart library is unavailable. The dated levels remain available in Levels & signals.</p>';return;}
    const price=LightweightCharts.createChart(target,chartOptions(Math.min(430,Math.max(300,innerHeight-480))));
    charts.push(price);
    const candles=price.addCandlestickSeries({upColor:'#f6c64f',downColor:'#d45656',borderVisible:false,wickUpColor:'#f6c64f',wickDownColor:'#d45656'});
    candles.setData(dates.map((dt,i)=>({time:Math.floor(new Date(dt).getTime()/1000),open:+data.open?.[i],high:+data.high?.[i],low:+data.low?.[i],close:+data.close?.[i]})).filter(x=>[x.time,x.open,x.high,x.low,x.close].every(Number.isFinite)));
    if (studies.ema) for (const [key,color] of [['ema13','#f8e5a2'],['ema27','#88aaff']]) {
      const line=price.addLineSeries({color,lineWidth:2,lastValueVisible:false,priceLineVisible:false});line.setData(seriesPoints(data,key));
    }
    if (studies.bands) for (const side of [1,-1]) {
      const line=price.addLineSeries({color:'#998aaf',lineWidth:1,lineStyle:2,lastValueVisible:false,priceLineVisible:false});
      line.setData(dates.map((dt,i)=>{const window=(data.close||[]).slice(Math.max(0,i-19),i+1).map(Number).filter(Number.isFinite);if(window.length<20)return null;const mean=window.reduce((a,b)=>a+b,0)/window.length;const variance=window.reduce((a,b)=>a+(b-mean)**2,0)/window.length;return {time:Math.floor(new Date(dt).getTime()/1000),value:mean+side*2*Math.sqrt(variance)};}).filter(Boolean));
    }
    if (studies.fib) Object.entries(report.route?.fibonacci||{}).forEach(([name,value])=>{if(Number.isFinite(+value))candles.createPriceLine({price:+value,color:'#bfa260',lineStyle:2,axisLabelVisible:true,title:`Fib ${name}`});});
    price.timeScale().fitContent();
    const subchart=(id,height,draw)=>{const element=$(id);if(!element)return;const chart=LightweightCharts.createChart(element,chartOptions(height));charts.push(chart);draw(chart);chart.timeScale().fitContent();};
    if (studies.volume) subchart('#player-market-volume',95,chart=>{const volume=chart.addHistogramSeries({priceFormat:{type:'volume'},priceScaleId:''});volume.setData(dates.map((dt,i)=>({time:Math.floor(new Date(dt).getTime()/1000),value:+data.volume?.[i],color:+data.close?.[i]>=+data.open?.[i]?'#f6c64f88':'#d4565688'})).filter(x=>Number.isFinite(x.value)));});
    if (studies.rsi) subchart('#player-market-rsi',150,chart=>{const line=chart.addLineSeries({color:'#f6c64f',lineWidth:2});line.setData(seriesPoints(data,'rsi14'));for(const level of [30,50,70])line.createPriceLine({price:level,color:'#6d6d75',lineStyle:2,axisLabelVisible:true,title:String(level)});});
    if (studies.macd) subchart('#player-market-macd',150,chart=>{const hist=chart.addHistogramSeries();hist.setData(dates.map((dt,i)=>({time:Math.floor(new Date(dt).getTime()/1000),value:+data.hist?.[i],color:+data.hist?.[i]>=0?'#f6c64f88':'#d4565688'})).filter(x=>Number.isFinite(x.value)));for(const [key,color] of [['macd','#8eb7ff'],['signal','#f6c64f']]){const line=chart.addLineSeries({color,lineWidth:2});line.setData(seriesPoints(data,key));}});
  }
  const pulse = () => {
    const trend=report.layers?.trend||{},momentum=report.layers?.momentum||{},barCount=series().date?.length||0;
    return `<div class="player-market-panel-head"><p class="eyebrow">MARKET COMMAND CENTER</p><h3>Player market pulse</h3><p>Read the three books, check source health, then open the study behind the move.</p></div><div class="player-market-grid">${fact('Dated closes',barCount)}${fact('Trend',trend.state||'Unknown')}${fact('Momentum',momentum.state||'Unknown')}${fact('Research confidence',percent(report.confidence))}${fact('Current price',money(report.price))}${fact('As of',dateLabel(report.as_of))}</div><div class="player-market-launches">${roomLink('Audit evidence','#evidence-panel')}${roomLink('Read levels','#route-panel')}${roomLink('Open player news','#asset-channel')}</div>`;
  };
  const chartRoom = () => {
    const data=series(),momentum=report.layers?.momentum?.metrics||{};
    return `<div class="player-market-panel-head chart-head"><p class="eyebrow">PLAYER MARKET STUDIO · PRICE TAPE</p><h3>Candles and indicator desk</h3><p>Candles use dated market bars. Prices, highs, lows, and volume come from the selected source; overlays are calculations for study.</p><span class="player-market-bar-count">${(data.date||[]).length} bars</span></div><div class="player-market-study-label"><b>Study tabs · ${Object.values(studies).filter(Boolean).length} on</b><small>CANDLES STAY ON · TOGGLE RSI · MACD · OVERLAYS</small></div><fieldset class="player-market-studies"><legend class="sr-only">Chart studies</legend>${[['ema','EMA · 13 / 27','Recent trend'],['bands','Range bands','Recent spread'],['fib','Fibonacci','Observed levels'],['volume','Volume','Bar size'],['rsi','RSI · 14','Momentum'],['macd','MACD','Move change']].map(([key,label,detail])=>`<label><input type="checkbox" data-study="${key}" ${studies[key]?'checked':''}><span><b>${label}</b><small>${detail}</small></span></label>`).join('')}</fieldset><div class="player-market-readouts">${fact('Settled close',money(report.price))}${fact('EMA · 13 bars',money(data.ema13?.at(-1)))}${fact('RSI · 14',number(momentum.rsi14,1))}${fact('Bar volume',number(data.volume?.at(-1),0))}</div><div class="player-market-graph"><div id="player-market-chart" role="img" aria-label="Dated player market candles"></div>${studies.volume?'<p class="player-market-chart-caption">VOLUME · DATED MARKET BARS</p><div id="player-market-volume" aria-label="Dated trading volume"></div>':''}</div>${studies.rsi?'<div class="player-market-substudy"><p class="eyebrow">MOMENTUM PANEL · RSI STUDY</p><h4>Weight, support, and resistance</h4><p>RSI reads recent upward and downward price movement. It does not promise the next move.</p><div id="player-market-rsi" aria-label="RSI chart"></div></div>':''}${studies.macd?'<div class="player-market-substudy"><p class="eyebrow">MACD STUDY</p><h4>Trend and momentum change</h4><div id="player-market-macd" aria-label="MACD chart"></div></div>':''}<div class="player-market-guide"><h4>Chart guide</h4><p><b>Candles</b> show dated open, high, low, and close. <b>EMA</b> weighs recent closes. <b>Bands and Fibonacci</b> are study guides. <b>Volume</b> is market trading activity, never money in your account.</p></div>`;
  };
  const translation = () => `<div class="player-market-panel-head"><p class="eyebrow">SIGNALS VS OUTCOMES</p><h3>Training translation</h3><p>Here, “training” is the earlier price and research record. A useful translation into future returns requires dated out-of-sample proof.</p></div><div class="player-market-split"><article><h4>Observed record</h4>${fact('Dated bars',series().date?.length||0)}${fact('Trend',report.layers?.trend?.state||'Unknown')}${fact('Momentum',report.layers?.momentum?.state||'Unknown')}</article><article><h4>Forward proof</h4>${fact('Historical analogs',report.calibration?.sample_size??'—')}${fact('Forecast state',report.forecast?.state||'Unknown')}<p>No future price is treated as observed.</p></article></div>${roomLink('Inspect historical evidence','#evidence-panel')}`;
  const levels = () => {
    const route=report.route||{}, memory=report.layers?.memory?.metrics||{};
    return `<div class="player-market-panel-head"><p class="eyebrow">RANGE · SUPPORT · RESISTANCE</p><h3>Levels & signals</h3><p>Observed route levels and tested price memory. Study markers are not orders.</p></div><div class="player-market-grid">${fact('Current',money(report.price))}${fact('Next upside',money(route.next_bus_stops?.[0]))}${fact('Next downside',money(route.downside_stops?.[0]))}${fact('Invalidation',money(route.invalidation))}${fact('Reward / risk',number(route.reward_risk))}${fact('Direction',route.direction||'Unknown')}</div><div class="player-market-split"><article><h4>Support</h4>${(memory.supports||[]).slice(0,4).map(x=>fact('Tested level',money(x.price),`${x.touches||0} tests`)).join('')||'<p>No tested support returned.</p>'}</article><article><h4>Resistance</h4>${(memory.resistances||[]).slice(0,4).map(x=>fact('Tested level',money(x.price),`${x.touches||0} tests`)).join('')||'<p>No tested resistance returned.</p>'}</article></div>${roomLink('Open full price route','#route-panel')}`;
  };
  const splits = () => `<div class="player-market-panel-head"><p class="eyebrow">TWO SIDES OF THE TAPE</p><h3>Matchup splits</h3><p>Compare the strongest upside case with the fair challenge from the same report.</p></div><div class="player-market-split"><article><h4>Bull talk · the case for</h4>${Object.values(report.layers||{}).flatMap(layer=>layer.evidence||[]).slice(0,6).map(x=>`<p>${escape(x.text)}</p>`).join('')||'<p>No bullish case recorded.</p>'}</article><article><h4>Bear talk · the fair challenge</h4>${Object.values(report.layers||{}).flatMap(layer=>layer.counter_evidence||[]).slice(0,6).map(x=>`<p>${escape(x.text)}</p>`).join('')||'<p>No bearish case recorded.</p>'}</article></div>`;
  const options = () => `<div class="player-market-panel-head"><p class="eyebrow">PLAYER MARKET STUDIO · OPTIONS</p><h3>Option chain</h3><p>Open the existing Options Lab for ${escape(report.symbol)} contracts and theoretical strategy studies. Its market-data status remains separate from this price tape.</p></div>${roomLink('Open Options Lab','#options-lab')}<p class="player-market-limit">No contract or premium is invented in this room. Options Lab states which feeds are available.</p>`;
  const futures = () => `<div class="player-market-panel-head"><p class="eyebrow">PLAYER MARKET STUDIO · FUTURES</p><h3>Futures board</h3><p>A futures board needs verified contract, exchange, expiry, and dated price data.</p></div>${fact('Selected player',report.symbol)}${fact('Contract board','Unavailable','No verified chain feed connected')}<p class="player-market-limit">A ticker identified as a future can still have a price chart; that does not supply a complete contracts board.</p>`;
  const reports = () => `<div class="player-market-panel-head"><p class="eyebrow">THE NEWS WIRE</p><h3>Market reports</h3><p>${escape(readablePrices(report.summary||'No current report summary.'))}</p></div><div class="player-market-reports">${(report.catalysts||[]).slice(0,8).map(item=>`<article><small>${escape(item.publisher||'Source')} · ${escape(dateLabel(item.published))}</small><h4>${escape(item.title)}</h4></article>`).join('')||'<p>No dated market reports in this analysis.</p>'}</div>${roomLink('Open full Player News','#asset-channel')}`;
  const evidence = () => `<div class="player-market-panel-head"><p class="eyebrow">MARKET EVIDENCE</p><h3>Audit the tape</h3><p>Contribution scores retain confidence and independence discounts.</p></div><div class="player-market-evidence">${(report.contributions||[]).map(x=>`<article><b>${escape(x.label)}</b><strong>${number(x.evidence_points,1)}</strong><small>Confidence ${percent(x.confidence)} · Independence ${percent(x.independence)}</small></article>`).join('')||'<p>No contribution details available.</p>'}</div>${fact('Source',report.data_meta?.provider||'Unknown')}${fact('Retrieved',dateLabel(report.data_meta?.retrieved_at))}${roomLink('Open full evidence','#evidence-panel')}`;
  const desk = () => {const saved=savedNote(report.symbol);return `<div class="player-market-panel-head"><p class="eyebrow">MY MARKET DESK</p><h3>Keep a thesis</h3><p>This note stays in this browser. Broker positions are not connected here.</p></div><label class="player-market-note-label">Thesis for ${escape(report.symbol)}<textarea id="player-market-thesis" rows="5" placeholder="What would change your view of this player?">${escape(saved?.text||'')}</textarea></label><button type="button" class="player-market-save" id="player-market-save">Save note</button><p id="player-market-note-status" role="status">${saved?.at ? `Saved ${escape(dateLabel(saved.at))}` : 'No note saved yet.'}</p>`;};
  const method = () => `<div class="player-market-panel-head"><p class="eyebrow">METHOD & SAFETY</p><h3>How this market desk works</h3><p>Every ticker is a Player, Member, and Subject in this platform motif. Its market facts retain their named source and date.</p></div><div class="player-market-grid">${fact('Price tape','Dated source bars','Open, high, low, close, and volume')}${fact('Research score','Evidence balance','Not a probability or trade signal')}${fact('Study tools','Read only','No order execution or score write')}${fact('Local work','Browser storage','Watchlists and notes stay here')}</div>`;
  const views = {pulse,chart:chartRoom,translation,levels,splits,options,futures,reports,evidence,desk,method};
  function showRoom(next) {
    if (!views[next]) return;
    room=next;studio.dataset.view=room;clearCharts();
    studio.querySelectorAll('[data-market-room]').forEach(button => {const active=button.dataset.marketRoom===room;button.classList.toggle('active',active);button.setAttribute('aria-current',active?'page':'false');});
    $('#player-market-room').innerHTML=report ? views[room]() : '<p>Choose a Player in the Exchange, then open the market desk.</p>';
    if (report && room==='chart') paintCharts();
  }
  $('.player-market-tabs',studio).innerHTML=rooms.map(([key,label])=>`<button type="button" data-market-room="${key}">${label}</button>`).join('');
  studio.addEventListener('click', event => {
    const tab=event.target.closest('[data-market-room]');const book=event.target.closest('[data-book-room]');
    if (tab) showRoom(tab.dataset.marketRoom);
    else if (book) showRoom(book.dataset.bookRoom);
    else if (event.target.closest('#player-market-close')) $('a[data-act-shell-room="player-exchange"]')?.click();
    else if (event.target.closest('#player-market-save') && report) {
      const text=$('#player-market-thesis').value.trim();
      try { localStorage.setItem(noteKey(report.symbol),JSON.stringify({symbol:report.symbol,text,at:new Date().toISOString()}));$('#player-market-note-status').textContent=`Saved ${dateLabel(new Date())} in this browser.`;renderExchange(); }
      catch {$('#player-market-note-status').textContent='This browser could not save the note.';}
    }
  });
  studio.addEventListener('change',event=>{const key=event.target.dataset.study;if(key){studies[key]=event.target.checked;showRoom('chart');}});
  window.addEventListener('marketcompassreport',event=>{report=event.detail.report;selectedSymbol=report.symbol;header();showRoom(room);renderExchange();renderProfile();});
  window.addEventListener('marketcompassmarketview',event=>showRoom(event.detail.view));
  header();showRoom('pulse');renderExchange();renderProfile();
})();
