<!-- release: v2.12.392 -->

## What's Changed

**Detect OCPP current-limit rejections correctly**
PowerSync now asks the HACS OCPP integration for the real current-limit result before falling back to its optimistic number entity. When a charger rejects smart-charging/current-limit commands, PowerSync now treats that as unsupported for the session instead of logging a false success and repeatedly trying amp changes that the charge point has refused.

Update available via HACS
