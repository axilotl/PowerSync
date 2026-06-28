<!-- release: v2.12.732 -->

## What's Changed

**Fix Flow Power v2 import price calculation**
PowerSync now applies Flow Power v2 PEA pricing without subtracting the average daily network tariff after the active tariff has already been applied. This aligns the PowerSync Flow Power price sensor and optimiser tariff schedule with Flow Power's account import PEA/current import price, instead of underpricing import by the daily average tariff amount.

Update available via HACS
