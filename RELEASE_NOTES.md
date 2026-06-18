<!-- release: v2.12.673 -->

## What's Changed

**Restore Sungrow discharge limits after failed force discharge**
PowerSync now restores the previous Sungrow discharge limit if a force-discharge command fails after temporarily lowering the inverter limit to the requested manual power. This prevents a failed low-power force-discharge attempt, such as 500 W, from leaving the battery capped and causing unexpected grid import when house loads rise.

**Clear failed Sungrow force-discharge state**
If Sungrow force-discharge does not stick, PowerSync now clears the visible force-discharge switch/countdown state instead of leaving Home Assistant showing an active manual discharge while the inverter has already returned to normal mode.

**Clamp manual force power to optimiser maximums**
Manual force-charge and force-discharge requests now respect the configured optimiser maximum charge/discharge power. Explicit low-power requests remain allowed, but requests above the configured maximum are capped before they reach the inverter.

Update available via HACS
