<!-- release: v2.12.504 -->

## What's Changed

**Honor Monitoring Mode for GoodWe controls**
PowerSync now blocks force charge, force discharge, restore normal, and self-consumption service writes while Monitoring Mode is enabled. This keeps GoodWe EMS and direct-control commands from changing inverter settings when users are observing plans only, including when Smart Optimization is toggled or a control service is called while monitoring.

Update available via HACS
