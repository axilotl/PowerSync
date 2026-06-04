<!-- release: v2.12.578 -->

## What's Changed

**Harden GoodWe TCP polling against stale LAN Kit responses**
PowerSync now closes and recreates its GoodWe Modbus TCP connection after each read or write request. This keeps the existing request lock and lower-round-trip telemetry block reads, while preventing delayed or duplicate LAN Kit frames from being reused by the next pymodbus transaction.

**Keep GoodWe telemetry coverage aligned with the new connection lifecycle**
GoodWe Modbus tests now verify that telemetry block reads still decode the same values, reads and writes remain serialized, and each TCP client is closed after use so stale socket data cannot contaminate the next request.

Update available via HACS
