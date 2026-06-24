<!-- release: v2.12.710 -->

## What's Changed

**GoodWe export targets now include forecast home load**
When Smart Optimization plans a GoodWe export window, PowerSync now sends the planned battery discharge target to the GoodWe EMS control path instead of sending only the net grid export target. This keeps GoodWe `sell_power` export windows aligned with the optimizer plan when the plan needs enough battery output to cover forecast home load and still export the requested amount to the grid.

Update available via HACS
