(()=>{
  const byId=id=>document.getElementById(id);
  const human=window.MarketCompassHuman;
  let current=null, pending=null, serial=0, activeView='articles', chosenPublishers=null;
  const publisherKey=symbol=>`market-compass-channel-publishers-v1:${symbol}`;
  const savedPublishers=symbol=>{try{const value=JSON.parse(localStorage.getItem(publisherKey(symbol)));return Array.isArray(value)?new Set(value.filter(item=>typeof item==='string')):null;}catch{return null;}};
  const savePublishers=()=>{if(!current)return;try{if(chosenPublishers)localStorage.setItem(publisherKey(current.symbol),JSON.stringify([...chosenPublishers]));else localStorage.removeItem(publisherKey(current.symbol));}catch{}};
  const text=(tag,value,className)=>{const node=document.createElement(tag);node.textContent=value;if(className)node.className=className;return node;};
  const selectedSymbol=()=>String(byId('symbol')?.value||'BB').trim().toUpperCase();
  const view=name=>{
    activeView=name;
    document.querySelectorAll('[data-channel-panel]').forEach(panel=>{panel.hidden=panel.dataset.channelPanel!==name;});
    document.querySelectorAll('[data-act-submenu-target^="channel-view:"]').forEach(button=>button.setAttribute('aria-current',String(button.dataset.actSubmenuTarget===`channel-view:${name}`)));
  };
  const renderArticles=data=>{
    const list=byId('asset-channel-articles');list.replaceChildren();
    const visible=data.items.filter(item=>!chosenPublishers||chosenPublishers.has(item.publisher));
    byId('asset-channel-status').textContent=`${visible.length} of ${data.items.length} linked items shown · ${data.source} · checked ${human.date(data.retrieved_at)}`;
    if(!visible.length){list.append(text('p',data.items.length?'No articles match the selected publishers. Change Sources and publishers to see them.':`No ticker-linked articles are available from ${data.source} right now. Try Refresh channel later.`,'asset-channel-empty'));return;}
    for(const item of visible){
      const card=document.createElement('article');card.className='asset-channel-item';
      const label=text('span',item.kind==='video'?'Video':'Article','asset-channel-kind');
      const link=document.createElement('a');link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=item.title;
      card.append(label,link,text('p',`${item.publisher} · ${human.date(item.published)}`));list.append(card);
    }
  };
  const renderSources=data=>{
    const sources=byId('asset-channel-sources');sources.replaceChildren();
    const news=text('article','','asset-channel-source');news.append(text('strong','Yahoo Finance search'),text('p',`${data.items.length} exact ticker-linked items · checked ${human.date(data.retrieved_at)}`));sources.append(news);
    const sec=text('article','','asset-channel-source');sec.append(text('strong','SEC EDGAR filings'),text('p',data.filings?.state==='observed'?`${data.filings.metrics?.filingCount||0} company filings available`:'Unavailable in this installation; SEC access is not configured.'));sources.append(sec);
    const counts=new Map();data.items.forEach(item=>counts.set(item.publisher,(counts.get(item.publisher)||0)+1));
    const filters=byId('asset-channel-publishers');filters.replaceChildren();
    byId('market-settings-symbol').textContent=`Selected asset: ${data.symbol}`;
    filters.append(text('h4','Show articles from'));
    const all=document.createElement('button');all.type='button';all.className='secondary';all.textContent='Show all publishers';all.addEventListener('click',()=>{chosenPublishers=null;savePublishers();renderSources(data);renderArticles(data);});filters.append(all);
    for(const [publisher,count] of [...counts].sort((a,b)=>a[0].localeCompare(b[0]))){
      const label=document.createElement('label');const input=document.createElement('input');input.type='checkbox';input.checked=!chosenPublishers||chosenPublishers.has(publisher);
      input.addEventListener('change',()=>{if(!chosenPublishers)chosenPublishers=new Set(counts.keys());if(input.checked)chosenPublishers.add(publisher);else chosenPublishers.delete(publisher);savePublishers();renderArticles(data);});
      label.append(input,text('span',`${publisher} · ${count}`));filters.append(label);
    }
  };
  const renderFilings=data=>{
    const list=byId('asset-channel-filings');list.replaceChildren();const filing=data.filings||{};
    if(filing.state!=='observed'){
      const reason=filing.reason?.includes('fair-access contact')?'SEC filings are unavailable until the app owner configures SEC access.':(filing.reason||'SEC filings are unavailable for this asset right now.');
      list.append(text('p',reason,'asset-channel-empty'));return;
    }
    const rows=filing.inputs?.filings||[];
    if(!rows.length){list.append(text('p','No matching recent SEC filings were returned.','asset-channel-empty'));return;}
    const source=(filing.source_urls||[]).find(url=>url.startsWith('https://data.sec.gov/submissions/'));
    for(const row of rows){const card=document.createElement('article');card.className='asset-channel-item';card.append(text('strong',row.form),text('p',`Filed ${human.date(row.filed)}`));if(source){const link=document.createElement('a');link.href=source;link.target='_blank';link.rel='noopener noreferrer';link.textContent='Open SEC company submissions';card.append(link);}list.append(card);}
  };
  const load=async(symbol=selectedSymbol())=>{
    if(!/^[A-Z0-9.^-]{1,16}$/.test(symbol)){byId('asset-channel-status').textContent='Choose a valid asset symbol.';return;}
    const request=++serial;pending?.abort();pending=new AbortController();
    byId('asset-channel-status').textContent=`Loading ${symbol} articles and filings…`;
    byId('asset-channel-current').textContent=`Selected asset: ${symbol}`;
    try{
      const response=await fetch(`/api/asset-channel/${encodeURIComponent(symbol)}`,{signal:pending.signal,credentials:'same-origin'});
      const data=await response.json();if(!response.ok)throw new Error(data.detail||'The channel could not load.');
      if(request!==serial)return;if(current?.symbol!==data.symbol)chosenPublishers=savedPublishers(data.symbol);current=data;
      byId('asset-channel-title').textContent=`${data.company} · ${data.symbol}`;
      byId('asset-channel-description').textContent=`Ticker-linked coverage for ${data.symbol}, with source links and publication times.`;
      document.querySelectorAll('[data-channel-symbol]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.channelSymbol===data.symbol)));
      renderArticles(data);renderFilings(data);renderSources(data);
    }catch(error){if(error.name==='AbortError'||request!==serial)return;current=null;byId('asset-channel-status').textContent=`${symbol} channel unavailable. ${error.message}`;byId('asset-channel-articles').replaceChildren(text('p','No items could be verified. Try Refresh channel.','asset-channel-empty'));byId('asset-channel-filings').replaceChildren(text('p','Filings could not be checked.','asset-channel-empty'));}
  };
  document.addEventListener('DOMContentLoaded',()=>{
    view('articles');
    byId('asset-channel-refresh')?.addEventListener('click',()=>load());
    document.querySelectorAll('[data-channel-symbol]').forEach(button=>button.addEventListener('click',()=>{
      const symbol=button.dataset.channelSymbol;
      byId('symbol').value=symbol;
      window.dispatchEvent(new CustomEvent('marketcompasschannelanalyze',{detail:{symbol}}));
      load(symbol);
    }));
    window.addEventListener('marketcompassreport',event=>{const symbol=event.detail?.symbol;if(symbol&&symbol!==current?.symbol)load(symbol);});
    window.addEventListener('marketcompasschannelview',event=>view(event.detail?.view||'articles'));
    byId('asset-channel-play')?.addEventListener('click',()=>{
      const status=byId('asset-channel-audio-status');
      if(!('speechSynthesis' in window)){status.textContent='Spoken headlines are unavailable in this browser.';return;}
      speechSynthesis.cancel();
      const heard=(current?.items||[]).filter(item=>!chosenPublishers||chosenPublishers.has(item.publisher));
      if(!heard.length){status.textContent='No selected headlines are available to read.';return;}
      const script=heard.slice(0,10).map(item=>`${item.title}. From ${item.publisher}.`).join(' ');
      const speech=new SpeechSynthesisUtterance(`${current.company} headlines. ${script}`);
      speech.onend=()=>{status.textContent='Finished reading headlines.';};
      speech.onerror=()=>{status.textContent='Headline reading stopped.';};
      speechSynthesis.speak(speech);status.textContent=`Reading ${Math.min(10,heard.length)} headlines.`;
    });
    byId('asset-channel-stop')?.addEventListener('click',()=>{window.speechSynthesis?.cancel();byId('asset-channel-audio-status').textContent='Headline reading stopped.';});
    load();
  });
})();
