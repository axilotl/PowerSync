<!-- release: v2.12.417 -->

## What's Changed

**Respect site export limits in Smart Optimization**
PowerSync now carries configured Sigenergy and AlphaESS export limits into the LP optimizer and export command path. Battery export plans, schedule API values, and runtime force-discharge commands are capped to the same grid export limit, avoiding schedules that ask the inverter to export more than the site is allowed to send.

**Clean up stale Tesla backup reserve restores**
Tesla Powerwall startup now self-heals stale persisted backup reserve values from older optimizer IDLE cycles. If PowerSync finds an old stored reserve higher than the live Tesla reserve, it adopts the live lower reserve and updates the stored value so the Powerwall does not keep returning to an unexpected level after restart.

**Reduce Powerwall local signaling noise**
Powerwall local setup no longer starts the Hermes signaling WebSocket automatically for every paired entry. The signed device-command path remains available, while installs using standard Fleet tokens avoid repeated Hermes missing-scope or token-exchange warnings in Home Assistant logs.

Update available via HACS
