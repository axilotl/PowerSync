<!-- release: v2.12.575 -->

## What's Changed

**Reduce GoodWe TCP polling round trips**
PowerSync now reads GoodWe TCP telemetry in a handful of Modbus register blocks instead of many rapid single-register requests. This reduces the chance that GoodWe LAN/TCP gateways return delayed or duplicate responses into the next request, which can show up as pymodbus transaction ID mismatch and `Cancel send, because not connected` errors.

**Keep GoodWe telemetry decoding covered**
GoodWe Modbus tests now verify the block-read plan and decoded telemetry values, so future changes preserve the lower-request polling path.

Update available via HACS
