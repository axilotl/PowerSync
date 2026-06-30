<!-- release: v2.12.739 -->

## What's Changed

**Optimizer charge window power display**
Active optimizer charge and export windows now report the command power PowerSync actually sent to the inverter, while preserving the original scheduled power as `planned_power_w`. This fixes cases where the dashboard showed a 10 kW planned charge window even though live import/headroom limits correctly reduced the active force-charge command to a lower value.

Update available via HACS
