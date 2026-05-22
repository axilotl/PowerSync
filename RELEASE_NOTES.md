<!-- release: v2.12.457 -->

## What's Changed

**Sungrow forced export reliability**
Sungrow SH force-discharge now clears a stale enabled 0 W export limit before switching the inverter into forced discharge. This fixes cases where PowerSync selected an export window and wrote forced discharge successfully, but the inverter only served local load and would not export to grid. The Sungrow settings API also now accepts settings POST requests on the documented settings endpoint.

**Sigenergy control and tariff hardening**
Sigenergy tariff upload now retries transient API failures such as rate limiting and temporary server errors, including support for Retry-After delays. Sigenergy force-discharge automation also preserves the requested export-limit state instead of restoring it immediately, and scheduled Sigenergy EV charging now uses the Sigenergy charger loadpoint even when stale Tesla charger metadata exists in stored vehicle settings.

**Reserve and startup fixes**
Tesla startup reserve handling now ignores polluted zero reserve values so a stale or transient 0% reading does not replace the configured optimizer floor or persisted user reserve. This keeps the no-discharge reserve behavior stable after restarts.

**Powerwall Local startup warning fix**
Powerwall Local now warms the shared insecure SSL context before creating the signed TEDAPI client, avoiding Home Assistant blocking-call warnings for paired entries that do not yet have a LAN IP.

Update available via HACS
