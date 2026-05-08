<!-- release: v2.12.348 -->

## What's Changed

**Amber WebSocket callback executor cleanup**
Amber live-price WebSocket updates now reuse a client-owned notification executor instead of creating a new thread pool for every callback. This prevents idle `WS-Notify` executor threads from accumulating over time while preserving the non-blocking callback path for live sensors and solar curtailment checks.

Update available via HACS
