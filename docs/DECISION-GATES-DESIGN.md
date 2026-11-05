# Decision Gates and calculateTHAT — design contract

Status: designed for research-only use. This contract does not authorize trading.

## Decision sequence

1. **Observe** — bind the requested symbol, data age, market session and evidence receipt.
2. **Calculate** — calculateTHAT evaluates named arithmetic and threshold checks without changing the Market Compass score.
3. **Challenge** — the counter-case, invalidation, catalyst risk and Actor psychology rules must be visible.
4. **Gate** — hard stops outrank positive triggers. Missing evidence never becomes a pass.
5. **Approve** — an external approval owner must record the exact symbol, setup, expiry and allowed action.
6. **Execute** — unavailable in this app. A future broker owner must independently revalidate the receipt.

## State machine

| State | Meaning | Permitted action |
| --- | --- | --- |
| `DO_NOT_GO` | One or more hard stops failed. | Research and repair only. |
| `REVIEW_ONLY` | No hard stop failed, but readiness or approval is incomplete. | Human review only. |
| `APPROVAL_READY` | Evidence gates pass; external approval is still absent. | Request approval; no order. |
| `APPROVED_NOT_EXECUTABLE` | Reserved for a valid external approval receipt. | Hand off to a separately governed execution owner. |

Market Compass never returns `EXECUTE`.

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
| Approval receipt | Exact, current external approval | Authority gate |

These are presentation defaults, not personalized financial advice. Preferences may be proposed in an Actor's comp card, but changes require an explicit versioned rule receipt.

## Trigger vocabulary

- `notable`: a threshold crossing worth showing, such as RSI crossing 35, 50 or 65.
- `watch`: supporting evidence exists but one or more readiness gates are incomplete.
- `setup_ready`: every non-authority gate passes.
- `invalidate`: price crosses the route invalidation or a hard stop appears.
- `approval_expired`: an approval receipt is missing, mismatched or stale.

Triggers are observations. They are not orders.

## Micro-slice ownership

- `observe-contract` owns input identity and freshness.
- `trigger-contract` owns notable/watch/setup/invalidate events.
- `calculate-contract` owns transparent arithmetic.
- `psychology-contract` owns Actor-specific preferences and restraint rules.
- `approval-contract` owns approval receipt shape and expiry.
- `execution-boundary` owns the permanent no-broker boundary in Market Compass.

Each slice has one reason to change and may be independently replaced without granting authority to another slice.
