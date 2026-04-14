## What's Changed

**Optimizer: 20-min LP lookahead prevents force-charge cancel during slot-shuffle**

ItsVRK reported on Discord that his Powerwall didn't grid-charge during the 11-18c midday dip before the 40-60c evening peak, landing at only 44% SOC at 3:43pm. His log showed the LP *did* choose CHARGE three times (12:20, 12:35, 13:06) but the first two were canceled within 6 and 11 minutes — 17 minutes of lost charging during the cheapest window of the day.

Root cause is LP degeneracy, not a bad LP decision. In flat-price windows the LP's optimal plan has multiple equivalent-cost solutions differing only in WHICH specific 5-min slot to charge in. HiGHS (the LP solver) picks a different slot each recompute, so `action[t=0]` flips between "charge" and "self_consumption" every few cycles while the LP still plans to charge at t=1 or t=2 — all within the currently-uploaded Tesla tariff, so canceling + later re-uploading is pure waste. Combined with the asymmetric commit hysteresis (2 cycles to start, 1 cycle to cancel), each flip tore down ~10 minutes of real charging.

PowerSync now checks a 20-min lookahead over the LP's own schedule before canceling a force charge. If the LP still plans the same force action within any of the next 4 intervals, the force mode is extended instead of canceled. Real price regime changes still flow through: within 1-2 LP cycles all 4 lookahead slots flip to SC/EXPORT and the cancel fires as before.

Verified against ItsVRK's 2026-04-14 log:
- Cancel at 12:26 (9 min gap to re-commit) → SAVED by lookahead
- Cancel at 12:46 (19 min gap to re-commit) → SAVED by lookahead
- Cancel at 15:02 (no re-commit, 2+ hrs SC after) → correctly cancels

Projected SOC impact on that day: ~44.9% → ~57% by 3:45pm, ~$0.41 evening peak cost avoided for his site on that single day. Scaled across any user with flat cheap-window days and Powerwall/Sigenergy/Sungrow/FoxESS/GoodWe force-charge behavior, the effect compounds.

Orthogonal to the existing spike-handling layers (confidence decay, Spike Protection, AEMO Spike Manager) — those still process real price events and flip the LP's full schedule; the lookahead only blocks cancels when the LP's own near-term plan still wants the force action.

Update available via HACS
