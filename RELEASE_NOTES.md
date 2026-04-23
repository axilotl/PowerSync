## What's Changed

**False "Automation Action Failed" alerts suppressed for non-Tesla systems**
Automations containing `set_grid_export` were firing a push notification failure alert on any non-Tesla battery system, even when the rest of the automation ran correctly. This happened because `set_grid_export` is Tesla-only and was returning a failure signal instead of silently skipping. It now skips without alerting, so automations shared across different battery brands no longer generate spurious failure notifications.

**Solax battery setup fixed for Gen4/Gen5/Gen6 inverters**
Newer wills106 installations expose the SOC floor as `selfuse_discharge_min_soc` rather than the legacy `battery_minimum_capacity` entity, causing the connection validation step to fail with a missing entity error. PowerSync now tries both naming conventions automatically, so Gen4/Gen5/Gen6 hardware connects without any manual workaround.

**Expanded weather conditions (sunny / partly cloudy / cloudy / rainy / snowy / stormy)**
Weather classification was previously coarse — rain, snow, and storms all mapped to "cloudy", and fog mapped to "partly sunny". Six distinct conditions are now supported, so automations can trigger meaningfully on precipitation and severe weather rather than just light levels. Weather-based automation trigger comparisons have been updated to match the expanded scale.

**New scene backgrounds for rain, snow, storm, and cloudy conditions**
The energy flow card now has scene artwork for all six weather states across day/night/charging/idle combinations — previously only clear and rain scenes existed. A battery direction arrow component (`battery-direction-arrow`) has also been added as a positionable flow element for scene layouts.

Update available via HACS
