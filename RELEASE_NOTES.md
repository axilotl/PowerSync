<!-- release: v2.12.695 -->

## What's Changed

**Fixed Sigenergy tariff sync during startup**
PowerSync now handles the Sigenergy tariff-sync region lookup when it runs before the integration's per-entry cache has been created during Home Assistant startup. This prevents the setup-time KeyError seen in Sigenergy tariff uploads while keeping the existing Amber NEM region detection and caching behavior once setup has completed.

Update available via HACS
