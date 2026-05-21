<!-- release: v2.12.452 -->

## What's Changed

**Fix optimizer reserve recovery after starting below the floor**
Smart Optimization now treats the configured optimizer reserve as the recovery target when a battery starts below that floor. The planner can still build a feasible recovery schedule, but once the battery can physically reach the configured reserve it no longer plans later export or discharge back through that user-set threshold.

**Fix Sigenergy planning while export curtailment is active**
Sigenergy systems that are temporarily curtailed now avoid treating the live 0 kW curtailment limit as the site's future export cap. This prevents Amber/AEMO export windows from making the LP optimizer infeasible and falling back to a conservative greedy schedule while curtailment is active.

Update available via HACS
