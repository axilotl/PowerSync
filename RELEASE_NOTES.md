## What's Changed

**TOU pricing fixed for Home Assistant Container / Supervised installs**
The Import/Export price sensors and TOU schedule were reading the container's system clock instead of Home Assistant's configured timezone. On stock HA Container and Supervised installs (where the container TZ defaults to UTC), this meant the integration thought it was UTC time even though HA itself was set correctly — picking the wrong tariff period and showing wildly wrong rates. A SA user on GloBird ZeroHero saw 0.0c displayed at 11pm because the integration was reading 12:30 UTC and matching the midday SUPER_OFF_PEAK window. HAOS users were unaffected because HAOS sets the container TZ from the configured zone. Tariff lookup, current period detection, and the schedule sensor's `current_hour`/`current_minute` attributes now all use HA's timezone.

**Sigenergy 30-minute price slot lookup uses HA timezone**
Two separate code paths that match the current 30-minute Amber/Sigenergy price slot (`PERIOD_HH_MM` keys) were also reading the wrong hour, so Sigenergy users were getting the previous or next half-hour's price applied to their actions. Fixed in both the legacy action path and the EV planner's price fallback.

**Custom and saved-tariff (US/CA) lookups respect HA timezone**
Tesla customers using saved utility tariffs or custom-built tariffs were hitting the same issue — the season/period/day-of-week lookup ran on the container clock. This affected Tesla TOU users outside Australia where the time offset can flip the entire day-of-week classification.

**EV charging planner schedules on local time**
Smart Schedule mode evaluated `weekday` from the container clock, so per-day rules (weekday vs weekend amperage, time-critical priority, consume-battery levels, time-window checks) could fire on the wrong day near local midnight. The planner now reads weekday and time-of-day from HA's timezone everywhere it makes scheduling decisions.

**Daily curtailment cap rolls over at local midnight**
The Powerwall local-curtailment fallback's daily-duration cap was resetting at UTC midnight instead of local midnight, meaning the "X seconds per day" budget could exhaust mid-afternoon for users far from UTC. Now resets correctly when the user's local date changes.

**Inverter night-mode fallback uses local hour**
When the `sun.sun` entity is missing, the integration falls back to a 6pm–6am hour-based check to decide whether the inverter is sleeping. That fallback now reads the local hour, so the heuristic actually corresponds to night where the user lives.

Update available via HACS
