## What's Changed

**Flow Power: Fix battery undercharging before Happy Hour windows**
On Flow Power tariffs, the LP optimizer was capping battery charge at roughly the current SOC rather than targeting full charge ahead of the 45c/kWh Happy Hour export windows. The root cause was "confidence decay" — a mechanism that reduces speculative Amber spot prices at long lookahead distances — being applied to Flow Power's fixed contractual rates. At 18–24 hours ahead, the 45c Happy Hour export was being decayed to ~5c and the 36c import to ~28c, making overnight grid charging appear unprofitable. The optimizer now skips confidence decay for Flow Power, correctly treating Happy Hour rates as fixed prices and charging the battery fully in preparation.

**Flow Power: Fix LP export forecast and cost tracking on HA dashboard**
The same decay issue caused the LP forecast chart to show no planned exports (since it didn't value them), and caused the predicted daily savings to be understated. Both are resolved by the same fix — the optimizer now plans Happy Hour exports as intended, and the cost projection reflects the correct 45c export price.

Update available via HACS
