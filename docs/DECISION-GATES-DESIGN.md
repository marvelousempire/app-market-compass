# Decision Gates and calculateTHAT — design contract

Status: active research-signal contract. Market Compass permanently excludes trading and order execution.

## Decision sequence

1. **Observe** — bind the requested symbol, data age, market session and evidence receipt.
2. **Calculate** — calculateTHAT evaluates named arithmetic and threshold checks, reads the Market Compass evidence score, and emits an active signal without mutating the score.
3. **Challenge** — the counter-case, invalidation, catalyst risk and Actor psychology rules must be visible.
4. **Gate** — hard stops outrank positive triggers. Missing evidence never becomes a pass.
5. **Point** — publish the Go, Watch, Do Not Go, Invalidated, or notable research signal with its evidence and counter-case.
6. **Decide elsewhere** — the human decides and acts outside Market Compass. Broker connectivity and execution are permanently excluded.

## State machine

| State | Meaning | Permitted action |
| --- | --- | --- |
| `DO_NOT_GO_SIGNAL` | One or more hard stops failed. | Active warning: research and repair only. |
| `WATCH_SIGNAL` | No hard stop failed, but one or more readiness gates remain incomplete. | Active watch signal with named holds. |
| `GO_SIGNAL` | Every research gate passes. | Active go signal for human consideration. |

Market Compass never returns `EXECUTE`, and signals do not require a trade-approval receipt.

## Default gates

| Gate | Pass condition | Failure class |
| --- | --- | --- |
| Asset reality | Foundation state is `acceptable` | Hard stop |
| Confidence | At least 65% | Hard stop |
| Evidence edge | At least 10 points between bull and bear evidence | Readiness |
| Timeframe agreement | At least 67% across available timeframes | Readiness |
| Route | Direction is known and invalidation exists | Hard stop |
| Reward/risk | At least 2.0 | Readiness |
| Evidence gaps | No declared missing inputs | Hard stop |

These are presentation defaults, not personalized financial advice. Preferences may be proposed in an Actor's comp card, but changes require an explicit versioned rule receipt.

## Trigger vocabulary

- `notable`: a threshold crossing worth showing, such as RSI crossing 35, 50 or 65.
- `watch_signal`: supporting evidence exists but one or more readiness gates are incomplete.
- `go_signal`: every research gate passes.
- `do_not_go_signal`: a hard stop or invalidation is present.
- `invalidate`: price crosses the route invalidation or a hard stop appears.
Signals are active research outputs. They are not orders.

## Micro-slice ownership

- `observe-contract` owns input identity and freshness.
- `trigger-contract` owns notable/watch/setup/invalidate events.
- `calculate-contract` owns transparent arithmetic.
- `psychology-contract` owns Actor-specific preferences and restraint rules.
- `approval-contract` records that approval is irrelevant to signal generation and belongs only to any action outside Market Compass.
- `execution-boundary` owns Market Compass's permanent no-broker boundary.

Each slice has one reason to change and may be independently replaced without granting authority to another slice.
