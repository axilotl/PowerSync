<!-- release: v2.12.428 -->

## What's Changed

**Fixed Octopus Intelligent Go charging when export is positive**
PowerSync now treats BottlecapDave Octopus Energy rates correctly for low-SOC overnight charging on Intelligent Go. A positive Outgoing export rate no longer turns the whole cheap import window into a charge-blocked export window; the optimiser can still force charge at 6.9p when that energy is needed for later self-consumption.

**Preserved export safety guards**
The optimiser still blocks pure grid-import-to-export passthrough and still respects explicit charge blocks for export windows such as Flow Power Happy Hour. This keeps profitable export controls intact without preventing low-rate battery top-ups.

Update available via HACS
