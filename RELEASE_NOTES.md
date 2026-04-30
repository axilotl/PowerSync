## What's Changed

**Fix: Tesla Powerwall extended sensors stuck at "Unknown"**
The five new Powerwall sensors introduced in v2.12.236 — Battery Pack Capacity, Battery Energy Left, Backup Time Remaining, Grid Services Active, and Grid Services Power — read their values from the wrong Tesla API payload. `total_pack_energy` and `energy_left` live in `live_status`, not `site_info`, so the coordinator was looking for fields that aren't there and falling through to None for every sensor (which Home Assistant displays as "Unknown"). The coordinator now reads both fields directly from `live_status` where Tesla actually returns them.

When `total_pack_energy` is missing entirely (older firmware), the coordinator falls back to `battery_count × 13.5 kWh` derived from `site_info.components.battery_count` so single- and multi-Powerwall sites still report a sensible nameplate capacity. `Battery Energy Left` similarly falls back to `pack_capacity × SOC%` when Tesla omits the direct `energy_left` value. `Backup Time Remaining` then derives from whichever pair landed and updates whenever home load changes.

`Grid Services Power` now defaults to 0 W instead of `None` when the site has no active VPP dispatch — much more useful for graphs and history than `Unknown`. The Grid Services Active binary sensor was already working correctly: it shows "Not running" when no grid services are dispatching, which is the expected state for the vast majority of sites.

Update available via HACS
