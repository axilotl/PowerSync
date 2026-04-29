## What's Changed

**Telemetry sensors now actually refresh at 2 seconds when paired**
Battery power, grid power, solar power, home load, battery level, and grid status sensors now read directly from the local coordinator's snapshot when paired, and subscribe to its 2s update tick instead of the cloud Tesla coordinator's 30-60s cadence. Previous release said this happened — the underlying poll was running but the sensor entities still drew from the cloud coordinator, so the user-visible refresh stayed slow. Now they update on every local poll.

**Powerwall controls moved from Configuration to Controls**
Backup Reserve, Operation Mode, Grid Export Rule, Force Charge / Force Discharge (and their Duration / Power inputs) were incorrectly tagged as Configuration entities, hiding them in the device card's collapsed Configuration section. They're now in the main Controls area where they belong, alongside Grid Charging and Off-Grid which were already there. Away Mode, Monitoring Mode, Profit Maximisation Mode, and the Pair / Unpair Powerwall Gateway buttons stay in Configuration — those are setup-shaped controls.

Update available via HACS
