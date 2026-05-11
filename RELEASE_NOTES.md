<!-- release: v2.12.384 -->

## What's Changed

**Improve Tesla Hermes signaling diagnostics for stale scopes**
PowerSync now detects Tesla's `Unauthorized missing scopes` response during the Hermes JWT exchange and stops retrying that token path instead of falling through to the raw WebSocket token fallback. The log now includes the token scopes Tesla granted, making stale authorization issues visible without implying that normal Fleet API telemetry is broken.

**Remove misleading vehicle-scope guidance from Hermes failures**
Hermes signaling failures now describe the provider re-authorization problem in energy-system terms and no longer suggest adding vehicle support or installing extra vehicle-focused integrations.

Update available via HACS
