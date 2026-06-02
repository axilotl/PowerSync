<!-- release: v2.12.543 -->

## What's Changed

**Flow Power Disable Idle mode**
Flow Power users now get a configuration-only **Disable idle mode** option in Smart Optimization. When enabled, PowerSync converts optimizer `idle` hold slots into `self_consumption` before the schedule is displayed or executed, so the home can keep using battery energy between charge and export windows instead of holding SOC for later.

**Provider-scoped optimizer handling**
The new setting is only shown for Flow Power configuration and is ignored outside Flow Power, preventing stale options from affecting other providers. The executor also has a fallback guard so any stale `idle` action is treated as `self_consumption` when Flow Power Disable Idle is active.

Update available via HACS
