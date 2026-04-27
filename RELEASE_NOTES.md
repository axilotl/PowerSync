## What's Changed

**Fix: Solar surplus EV charging now respects vehicle location**
When a vehicle left home without disconnecting the charger (or when the device tracker updated to `not_home` while the surplus timer was counting down), the solar surplus mode would still fire a remote charge command via the Tesla/Tessie integration — starting or continuing charging wherever the car happened to be. The surplus mode now checks vehicle location before making any charging decision: if the car is not home, the surplus timers are reset and no charge command is sent. If charging was already underway when the car left, the session is stopped cleanly.

**Fix: SAJ H2 force charge/discharge now uses correct power levels**
Force charge and force discharge previously wrote a hardcoded value of 1100 (110% of rated capacity) to the SAJ H2 passive power registers, ignoring the actual power requested by the LP optimizer. Power is now correctly converted from watts to SAJ's 0–1000 scale against the inverter's reported rated capacity. Additionally, the `passive_enable` number entity write has been removed from the charge, discharge, and idle paths — writing that register directly bypasses the AppMode management in the switch entity, leaving the inverter in a mixed state (passive register set but AppMode still TOU) that can cause erratic behaviour and protection trips. The switch-based path is now used exclusively.

Update available via HACS
