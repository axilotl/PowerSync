<!-- release: v2.12.294 -->

## What's Changed

**Sigenergy optimizer hardware extension fallback**
Optimizer-issued force charge and force discharge extensions now keep using Sigenergy Modbus directly even when Home Assistant has not attached the coordinator controller. This prevents the hardware extension path from falling back into the full manual force handler and removes the noisy `_extend_hardware: no coordinator found` warning from HA logs.

Update available via HACS
