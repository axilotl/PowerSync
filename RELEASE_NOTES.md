<!-- release: v2.12.320 -->

## What's Changed

**Globird and Tesla setup guidance**
PowerSync now makes the Tesla + Globird setup requirement explicit in the Home Assistant setup flow. Tesla Powerwall users are prompted to set the correct Globird/TOU tariff in Tesla before continuing, then restart Home Assistant or reload PowerSync after tariff changes so the scheduler refreshes its cached tariff baseline.

**Globird tariff scheduler safety**
The Globird options copy now separates Tesla-sourced tariffs from PowerSync custom tariffs, reducing the chance that stale or missing Tesla tariff data causes the LP optimizer, EV planning, or `sensor.power_sync_tariff_schedule` to use the wrong peak/off-peak periods.

Update available via HACS
