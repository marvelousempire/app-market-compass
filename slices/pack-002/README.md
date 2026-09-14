# Pack #2 — Relative Strength Desk + Market Tape

This is the opening ask of the session: take Market Compass and the RSI Hunter
XRP asset desk (https://rsihunter.com/asset/xrp) and add glanceable analysis
without replacing the 8001 evidence sequence or the scoring model.

Not an XRP-only calculator. Any asset with a close series plus BTC and ETH
benches can sit on this desk.

## Slices
- 10 RSI zones
- 11 Relative strength vs BTC / ETH
- 12 Market tape
- 13 ATH drawdown
- 14 SMA stack
- 15 Supply metrics
- 16 Desk receipt

## Run
```bash
python3 slices/pack-002/main.py
python3 slices/pack-002/tests/test_pack_002.py
```
