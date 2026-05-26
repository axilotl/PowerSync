<!-- release: v2.12.483 -->

## What's Changed

**Restore Sigenergy force-charge timers**
Scheduled PowerSync force-charge and force-discharge actions now run through the same Home Assistant service path as manual controls. This preserves the requested duration, restore timer, and persisted force-mode state across Home Assistant restarts, so a timed Sigenergy force charge does not continue indefinitely after the integration reloads.

**Correct Flow Power PEA TWAP handling**
Flow Power import pricing now uses the raw wholesale TWAP for PEA calculations instead of feeding the portal account TWAP back into the formula. Portal BPEA and GST values are still used when available, while portal TWAP remains exposed as an account metric, bringing PowerSync's current import price back in line with Flow Power.

Update available via HACS
