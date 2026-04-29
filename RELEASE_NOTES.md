## What's Changed

**Fix: AEMO dispatch trigger pinned QLD/VIC/SA/TAS users to NSW1 (introduced in v2.12.215)**
The NEM region resolver added in v2.12.215 had its second step pick up `CONF_FLOW_POWER_STATE`, which defaults to `"NSW1"` for *every* config entry in this codebase — not just Flow Power ones. So any Amber or Localvolts user without an explicit `CONF_AEMO_REGION` (i.e. anyone who hadn't configured AEMO spike protection) silently got pinned to NSW1 before the Tesla site-timezone or Amber network-field paths even ran. A Powerwall in Brisbane was therefore subscribing to NSW1 dispatch prices instead of QLD1 — wrong tariff numbers, wrong arbitrage decisions. The resolver now tries the Tesla site `installation_time_zone` first (strongest signal — comes from Tesla's commissioning data), then Amber's network field, then `CONF_AEMO_REGION`, and only consults `CONF_FLOW_POWER_STATE` for Flow Power entries. Affected users will see a `Auto-detected NEM region QLD1 from Tesla site timezone (Australia/Brisbane)` log line on next HA restart confirming the correct region.

Update available via HACS
