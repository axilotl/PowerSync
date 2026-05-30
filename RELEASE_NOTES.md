<!-- release: v2.12.513 -->

## What's Changed

**Faster Home Assistant startup for Tesla Powerwall installs**
PowerSync now preserves Tesla capability probe results during startup instead of losing them when setup replaces the integration's stored entry data. Capability-gated Tesla entities also use a shorter bounded wait, preventing the 120-second Home Assistant "wrapping up" delay reported by Tesla Powerwall users when capability data was not published in time.

**Amber WebSocket startup fallback**
Amber WebSocket startup is now wrapped in a timeout. If the WebSocket path is slow or unreachable during Home Assistant startup, PowerSync falls back to REST pricing instead of letting setup block indefinitely.

**Dashboard history chart completeness**
The dashboard history chart now requests full update history and prefers `last_updated` timestamps when plotting points. This keeps short-lived sensor updates visible in the chart instead of relying only on significant state changes.

**Test suite reliability**
Powerwall local and SolarEdge regression tests now isolate their Home Assistant stubs more tightly, keeping the full Python 3.12 test suite deterministic.

Update available via HACS
