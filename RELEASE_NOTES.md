<!-- release: v2.12.524 -->

## What's Changed

**Smart Schedule now respects per-vehicle charge-current limits in the optimizer**
PowerSync now reads EV charger current limits from both the app's current `min_charge_amps` / `max_charge_amps` fields and the older `min_amps` / `max_amps` storage keys. This prevents the LP optimizer and schedule preview from falling back to a 30-32A default when a vehicle is configured for a lower limit such as 15A.

**Solar surplus and scheduled EV starts share the same charger-limit compatibility**
Solar surplus starts, schedule previews, price-level starts, and Auto Schedule settings now all accept the same charger limit aliases. This keeps the physical charger settings shown in the app aligned with the backend commands and the optimizer's planned EV load.

Update available via HACS
