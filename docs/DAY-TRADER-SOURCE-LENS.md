# Day Trader source lens

Market Compass refines selected research concepts from
[`marvelousempire/day-trader-skill`](https://github.com/marvelousempire/day-trader-skill)
at immutable revision `3d0f4ef6986f4984b7c6bd46f7ff4f87744c3abd` (MIT,
Copyright (c) 2026 Jake Schincariol).

This is a clean-room, research-only adaptation. It does not execute or vendor
the upstream modules. The first MicroSlices detect five daily chart conditions
and RSI crossings at 35, 50, and 65. Brown's Barometers owns measurements;
Wuda owns notable threshold events. Market Exchange owns the source contract,
and Compass Desk displays the result.

The default daily feed cannot prove an intraday opening-range event, so that
slice is held. Existing Market Compass Historical Analogs and Backtest remain
the scenario tools, explicitly not predictions. SEC/news techniques remain
reference candidates for intelTHAT rather than duplicate fetchers.

The upstream broker, order ticket, account credentials, money movement,
account-mutating budget path, and execution-like alerts are rejected. The API
receipt always declares `trade_execution: false`, `money_movement: false`,
`score_influence: false`, and `research_only: true`.

Read it at `GET /api/research-lenses/day-trader/{symbol}` or through the Day
Trader Research Lens panel. A chart setup is not a recommendation.
