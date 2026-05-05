<!-- release: v2.12.287 -->

## What's Changed

**Restore off-peak charging when batteries are low**
PowerSync now allows the optimizer to grid-charge during cheap periods even when there is no solar surplus. A previous export-arbitrage guard accidentally made no-solar charging impossible in some LP solves, which could leave a depleted Powerwall sitting in self-consumption instead of recovering during off-peak rates.

**Stop fighting manual Tesla TOU recovery**
When the optimizer's current action is self-consumption, PowerSync no longer treats Tesla `autonomous` mode as drift that must be overwritten. This prevents the optimizer from forcing a user-initiated TOU/manual recovery back to self-powered while a low battery is being rescued.

**Charge immediately at the reserve floor**
If the optimizer chooses charge while battery SOC is at or below the configured reserve, PowerSync now bypasses charge hysteresis and issues the charge command immediately instead of waiting for another confirmation cycle.

Update available via HACS
