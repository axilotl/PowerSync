<!-- release: v2.12.405 -->

## What's Changed

**FoxESS Cloud API can now run as a full battery backend**
FoxESS setup now supports a cloud-only path alongside Modbus TCP and RS485. Cloud-only entries validate a FoxESS Open API key, auto-select the inverter serial when the account has one device, avoid Tesla credential setup, and create FoxESS energy/control entities through a dedicated cloud coordinator.

**FoxESS cloud controls now match the Modbus feature surface**
PowerSync can route FoxESS force charge, force discharge, restore normal, backup reserve, work-mode restore, current limits, idle/backup hold, tariff scheduling, and export curtailment through the cloud backend. Scheduler V3 is used for temporary force/idle actions and tariff schedules, with previous scheduler state saved and restored after temporary actions.

**FoxESS Open API endpoints updated**
The FoxESS client now uses the newer realtime query shape, Scheduler V3 payloads, settings endpoints, battery SOC endpoints, and includes datalogger Modbus passthrough support for future parity gaps. Cloud polling is conservative to respect FoxESS API limits.

Update available via HACS
