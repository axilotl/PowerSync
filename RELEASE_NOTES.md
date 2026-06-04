<!-- release: v2.12.573 -->

## What's Changed

**Fix FoxESS force charge and discharge controls after reloads**
PowerSync now rediscovers FoxESS Modbus control entities if Home Assistant or foxess_modbus renames or recreates them during startup, and it clamps force charge/discharge power writes to the number entity's allowed range. This prevents force charge failures such as requesting 20 kW from an inverter entity that only accepts up to 15 kW.

**Improve free-import battery charging under a site import cap**
Smart Optimization now adjusts supported battery charge commands during free-import slots using live site-import headroom. This lets compatible batteries charge harder when solar and load leave room under the configured grid import cap, while backing off when live headroom drops.

**Resume EV charging when curtailment hides solar surplus**
Solar-surplus EV charging now performs a minimum-amp probe when the battery is full, solar is present, export is curtailed, and the EV is idle. This helps an EV start again in curtailed/full-battery conditions where the normal surplus calculation can otherwise see no available headroom.

**Fix EV battery display in the energy-flow card**
The energy-flow card no longer treats EV power or presence entities as EV battery percentage sources. EV battery percentage is now shown only when a real battery percentage entity is configured.

Update available via HACS
