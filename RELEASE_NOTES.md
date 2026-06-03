<!-- release: v2.12.547 -->

## What's Changed

**Sungrow curtailment status accuracy**
PowerSync no longer lets the native Sungrow hybrid export-limit state make a separate AC-coupled Sungrow inverter appear curtailed when its own Modbus readback says it is running normally. This fixes the misleading app/dashboard status where the inverter could show as curtailed even though the AC inverter power limit was back at 100%.

**Solar surplus EV headroom uses live curtailment data**
EV solar-surplus calculations now receive the actual coordinator-reported curtailment state instead of inheriting stale cached Sungrow command state. This keeps full-battery solar-surplus ramping behavior available when real curtailment is active, without confusing it with a stale display flag.

Update available via HACS
