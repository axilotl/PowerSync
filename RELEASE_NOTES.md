## What's Changed

**Restores integration loading after 2.12.229**
2.12.229 shipped an `actions.py` module that imported a `solar_surplus_config` helper module which wasn't included in the release. Home Assistant booted the integration successfully, but the first invocation of any feature that touched `actions.py` (push notifications, EV start/stop, dynamic surplus charging) crashed with `ModuleNotFoundError`. This release ships the missing helper plus the rest of the refactor so all of those code paths work again.

**SAJ H2 force discharge no longer refuses on healthy systems**
Fixed a false-positive guard that blocked manual force discharge on SAJ H2 / HS2 inverters even when the battery was clearly running. The pre-flight engagement check required both `inverter_working_mode == 2` AND R-phase inverter voltage ≥ 50V; on some stanus74 firmware revisions the R-phase voltage register reads 0V even while the inverter is on-grid and exporting (working mode 2, battery flowing, SOC well above the floor). The voltage signal alone was treated as a hard refusal and force discharge silently no-op'd. `working_mode` is now the authoritative engagement signal — `2` means engaged regardless of what RInvVolt reports — and the voltage check is only consulted as a fallback when working_mode is unavailable on older firmwares. The genuine low-SOC lockout state (working_mode 4) is still caught and refused with the same clear error as before.

**EV charging now stops even when PowerSync didn't start it**
Fixed a bug where Teslas that auto-started charging on plug-in (the default Tesla firmware behaviour) would keep drawing power indefinitely. PowerSync only tracked stop logic against its own internal "did I start this?" flag — so when conditions said charging should stop (price, SoC, schedule), nothing happened. The planner now probes the vehicle's actual charging state via Teslemetry BT, Tesla Fleet, or BLE entities and sends the stop command whenever the car is drawing power, regardless of who initiated it. This also fixes the reload scenario where the in-memory "is charging" flag was wiped while the car kept charging. (This fix was first published in 2.12.229 but couldn't run because of the import bug above.)

**Solar-surplus config consolidation**
The home-battery SOC threshold for solar EV charging now lives in a single shared helper (`solar_surplus_config.py`) used by the API view, the automation executor, the planner, and the price recommendation endpoint. Previous code carried the default in five places, which let the legacy `home_battery_minimum` field and the newer `min_battery_soc` field drift apart on saves/reads and quietly fall back to a hard-coded 80% when the app sent the new field name. They're now kept in sync on every read and write, percentages are clamped to 0–100, and the price-recommendation surplus calculation uses the user's actual configured buffer instead of an inline `0.5kW` default.

**Better diagnostics when hermes signaling auth fails**
When the local Powerwall signaling channel can't get a hermes JWT, the warning log now includes the parsed error code, the access token's actual scopes, and up to 400 characters of Tesla's response detail (previously truncated at 200, hiding the most useful diagnostic — `token_scopes`). Makes it possible to tell at a glance whether a 412 from Tesla is a missing-scope issue on your token or a Tesla-side change.

Update available via HACS
