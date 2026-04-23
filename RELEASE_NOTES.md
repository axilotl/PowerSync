## What's Changed

**Solax battery setup fixed for Gen4/Gen5/Gen6 inverters**
Newer wills106 installations expose the SOC floor as `selfuse_discharge_min_soc` rather than the legacy `battery_minimum_capacity` entity, which caused setup to fail at the connection validation step with a missing entity error. PowerSync now tries both naming conventions, so Gen4/Gen5/Gen6 hardware connects without requiring any manual workaround.

**Expanded weather conditions (sunny / partly cloudy / cloudy / rainy / snowy / stormy)**
Weather classification was previously coarse — rain, snow, and storms all mapped to "cloudy", and fog mapped to "partly sunny". This is now split into six distinct conditions so automations can trigger meaningfully on precipitation and severe weather, not just light levels. The comparison scale for weather-based automation triggers has been updated accordingly.

**New scene backgrounds for rain, snow, storm, and cloudy conditions**
The energy flow card background system now has artwork for all six weather states across day/night/charging/idle combinations — previously only clear and rain scenes existed. The scene layout data has also been extracted into a separate generated module, keeping the card JS lean and the scene definitions easy to update.

**Battery direction arrow added to energy flow card**
A charge/discharge direction indicator is now available as a positionable flow component (`battery-direction-arrow`), giving scene layouts a way to surface battery flow direction visually without relying solely on the power label sign.

Update available via HACS
