<!-- release: v2.12.529 -->

## What's Changed

**AEMO NEMWEB dispatch backoff**
PowerSync now backs off briefly when NEMWEB dispatch file requests fail transiently, such as intermittent 403 responses around dispatch publish time. During the backoff window it reuses the latest parsed dispatch data when available, or falls back to AEMO's JSON summary endpoint, reducing repeated warnings during active 1-second polling.

Update available via HACS
