## What's Changed

**Tesla Powerwall — gateway IP prompt at setup**
The initial setup flow now prompts for the Powerwall gateway's local IP after the Tesla Energy Site selection. The field is optional — leave blank to run cloud-only — but a hint explains that providing it unlocks per-Powerwall snapshot data, automated curtailment, and faster operation-mode / grid-charging toggles. Existing users aren't prompted again; they can still add the IP later via the mobile app's Battery Setup → Gateway Connection screen.

**New diagnostic: `binary_sensor.power_sync_powerwall_local_ip_missing`**
Surfaces the "paired-without-IP" state as a HA entity. Returns `on` when the integration completed cloud-side pairing but no local gateway IP is configured, `off` otherwise. Drives the new mobile-app banner and gives anyone running the integration headlessly a way to detect the same condition from automations or dashboards. Available on every Tesla install — no capability probe required.

Update available via HACS
