## What's Changed

**Tesla tariff sync now fires on every 5-min Amber tick**
Removed the 0.5c/kWh price-delta dead-band that was silently skipping tariff pushes to Tesla when Amber prices drifted slowly. Real-world impact: when prices hovered within ±0.5c of the last synced value, the Tesla app could go 30-50 minutes without a price refresh even though new 5-min intervals were arriving. TOU sync now POSTs to Tesla on every AEMO dispatch event, so the Powerwall and Tesla app reflect the current Amber interval price reliably.

**Happy Hour export stays active down to the reserve floor (Modbus batteries)**
Fixed a regression where Sigenergy, Sungrow, FoxESS, GoodWe, AlphaESS, ESY Sunhome, Solax, and SAJ systems would stop responding to discharge commands in the last 15-30 minutes of Happy Hour, reverting to load-following self-consumption with usable SOC still above the configured reserve. The executor's "near-floor" safety guard was Tesla-specific (Tesla's force_discharge sets the soft backup_reserve to 0%, so it can drain itself empty if SOC data is stale). Modbus batteries don't share that risk — their inverter BMS enforces the minimum SOC at the DOD register level — so the guard now only applies to Tesla. Recovers the tail end of Happy Hour revenue (~$1-2/day at $0.45/kWh export bonus) for affected users. No behaviour change for Tesla.

**Charge window no longer drifts into the Happy Hour boundary (Flow Power + profit_max)**
Fixed the planned charge window "marching right" with each 5-min LP re-run, so charging would complete at the exact moment Happy Hour started — leaving zero slack for Modbus write latency, BMS taper above 90%, AEMO predispatch jitter, or dropped control packets. Two changes: the LP's grid-import tie-breaker now prefers earlier slots when there's a binding SOC-by-time deadline (was preferring later, which let the cheap window repaint later as forecasts refreshed), and the pre-window deadline is pulled 15 minutes earlier before being passed to the LP. Result: charging completes with a 15-minute buffer before HH start, both runs still hit 99.5% SOC. Costs ~$0.02/day in slightly pricier earlier slots, but eliminates the failure mode where the system was still importing as Happy Hour began. Only fires for `profit_max=true` + `provider=flow_power`; all other combinations unchanged.

Update available via HACS
