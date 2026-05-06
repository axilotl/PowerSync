<!-- release: v2.12.301 -->

## What's Changed

**Sigenergy discharge keeps solar online**
Force discharge now uses Sigenergy's PV-first Remote EMS discharge mode instead of ESS-first. This avoids the plant shutting down solar production while the battery is exporting, so daytime manual or optimizer-driven discharge can keep using active PV generation.

**Sigenergy optimizer avoids peak grid charging**
The optimizer now blocks Sigenergy grid-charge commands when the current import price is too high to recover through later import avoidance or export value. This prevents reserve-recovery charge slots from pulling expensive grid energy during peak price periods while still allowing genuinely cheap grid charging.

Update available via HACS
