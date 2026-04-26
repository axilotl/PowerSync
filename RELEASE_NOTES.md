## What's Changed

**SAJ H2: Fix live power sensors reading 0.0**
The PowerSync bridge for SAJ H2 / HS2 systems was discovering entities from the `saj_h2_modbus` integration but never successfully mapping any of them. The `saj_h2_modbus` integration registers entities with camelCase unique_id keys (`batteryPower`, `Bat1SOC`, `totalgridPower`, `pvPower`, `TotalLoadPower`, `directionBattery`) but the PowerSync bridge was searching for snake_case suffixes (`battery_power`, `battery_1_soc`, `total_grid_power`) — none of which matched. As a result, all power sensors (battery level, battery power, grid power, solar power, home load) showed 0.0 on both the dashboard and mobile app. All key mappings are now corrected.

**TariffScheduleSensor: Fix TOU rate display not refreshing at midnight**
The schedule sensor caches static data (rate schedule, buy/sell price lists) and only rebuilds it when the tariff `last_sync` timestamp changes. This caused TOU tariffs that have different weekday vs. weekend rates to show stale day-of-week data until the next tariff update — typically up to 5 minutes after midnight. The cache now also invalidates when the weekday changes, so the correct rates are shown immediately after midnight rollover.

**TariffScheduleSensor: Performance — halve redundant work per state write**
Previously, the 48-slot schedule list and buy/sell price dictionaries were rebuilt from scratch on every state write (once per minute from the periodic timer, plus once per tariff update). The schedule data itself only changes every ~5 minutes. These computations are now cached and only rebuilt when `last_sync` changes, reducing per-write overhead. The current-price calculation was also being called twice per write cycle; it now runs once and the result is reused.

Update available via HACS
