## What's Changed

**Enphase load-following curtailment now actually engages**
A regression on certain Envoy firmware (notably AU/NZ region) caused PowerSync's solar curtailment to log "Successfully curtailed" while the Enphase kept producing at full output. The cause: the gateway requires an `installed_capacity` field in the DPEL payload that we weren't sending. Without it the Envoy returned 400, we fell back to a payload variant the gateway accepts but never enforces, and you'd see your inverter happily exporting through "negative pricing" curtailment cycles.

PowerSync now resolves your installed PV capacity automatically (from the gateway's microinverter list) and includes it in the DPEL request. If the no-op fallback ever fires for any reason, you'll now see a clear `WARNING` in the log explaining the gateway accepted the call but isn't enforcing the limit, instead of a misleading success message.

**No action required** — the next curtailment cycle after updating will use the corrected payload. Look for `Discovered installed_capacity` or `Computed installed_capacity from N microinverters` in your logs to confirm.

Update available via HACS
