<!-- release: v2.12.402 -->

## What's Changed

**Prefer external Solcast integration data**
PowerSync now treats an installed Solcast Solar integration as the source of truth when it is available, even if old built-in Solcast API credentials are still saved. This prevents duplicate direct API polling and keeps the weather/Solcast settings endpoint reporting the external integration source.

**Cleared built-in Solcast credentials stay cleared**
Deleting the built-in Solcast API key or resource IDs now removes stale legacy config-entry data as well as options, so reloads no longer repopulate those fields when users only want to use the external Solcast integration.

Update available via HACS
