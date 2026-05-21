<!-- release: v2.12.456 -->

## What's Changed

**Optimizer reserve now separates self-use from forced discharge**
PowerSync now treats the Smart Optimisation reserve as the software floor for forced export and optimiser-owned force discharge, while allowing normal self-consumption to continue down to the battery's hardware reserve. This prevents batteries that sit just under the optimiser reserve from being force-charged purely to recover the software floor when they can still serve home load naturally.

**Forced export stops at the optimiser floor**
The LP planner, greedy fallback, and active force-discharge extension path now all block or cancel optimiser-owned export/discharge once SOC is at or below the Smart Optimisation reserve, even when export pricing is attractive. This keeps the optimiser floor meaningful for export behavior across battery systems.

**Economic charging still works**
Cheap or free import periods, including Amber-style dynamic pricing, can still trigger force charging when the tariff makes it worthwhile. The change only stops reserve-recovery charging and forced export below the optimiser floor.

Update available via HACS
