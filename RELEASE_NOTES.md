<!-- release: v2.12.473 -->

## What's Changed

**Improve Tesla solar-surplus amp control**
Solar-surplus EV charging now handles stale Tesla charge-current entity limits more gracefully. When Home Assistant still shows an old maximum but rejects the requested amperage as out of range, PowerSync falls back to the entity's accepted maximum and keeps the dynamic charging state aligned with the amperage that was actually applied.

**Use saved solar-surplus settings in status APIs**
Solar-surplus status, EV widget, loadpoint status, and price recommendation endpoints now read the same stored solar-surplus configuration used by the automation runtime instead of hard-coded defaults. Dashboard and app-facing surplus values should now reflect the configured calculation mode, household buffer, and battery minimum consistently.

**Expand FoxESS PV and Modbus compatibility**
FoxESS now exposes PV1-PV6 power sensors, shows up to six PV strings on the dashboard, and uses the PV string sum when the reported total solar value omits a string. Direct FoxESS Modbus startup also guards against Nathan Marlor foxess_modbus' vendored pymodbus modules leaking into PowerSync's direct Modbus imports.

**Fix SAJ H2 grid and daily-energy mapping**
The SAJ H2 bridge now prefers the net grid-load power sensor for grid import/export, avoids treating total grid power as a net-grid signal, and recognizes the current SAJ Modbus daily solar, feed-in, and sell-energy keys. This should fix dashboards where solar was corrected but grid import/export still stayed empty.

Update available via HACS
