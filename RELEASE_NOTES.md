<!-- release: v2.12.379 -->

## What's Changed

**OCPP opportunity charging uses the detected charger entity**
PowerSync now resolves the actual HACS OCPP charger prefix before starting price-level or opportunity charging. This fixes systems where the charger is discovered as an entity such as `switch.charger_charge_control`, but the automation path fell back to `switch.ocpp_charger_charge_control` and failed to restart after a stop.

**Cleaner OCPP session ownership**
Price-level OCPP sessions now use the same detected loadpoint identity as the mobile/manual controls, avoiding repeated failed start attempts when a charger is plugged in, in `Finishing`, or ready for a cheap-price charging window.

Update available via HACS
