<!-- release: v2.12.528 -->

## What's Changed

**Sigenergy station ID handling**
Sigenergy tariff sync now keeps the configured station identifier and the numeric tariff API `stationId` separate. This preserves alphanumeric system/station IDs for the rest of the integration while still sending the numeric tariff ID required by the Sigenergy cloud tariff-save endpoint.

**Sigenergy station selection**
The station picker now prefers the non-numeric system identifier when Sigenergy exposes both IDs, and caches the numeric tariff ID only for tariff uploads. Manual station ID changes clear the cached tariff ID so the next sync resolves the correct value again.

Update available via HACS
