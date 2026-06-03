<!-- release: v2.12.565 -->

## What's Changed

**Home Assistant logging settings are respected again**
PowerSync no longer forces the integration and its submodules to DEBUG logging at import time. That means your Home Assistant `logger:` configuration can quiet PowerSync normally, reducing noisy logs and avoiding unnecessary debug formatting work on busy systems.

**Repeated settings syncs no longer churn the optimiser cache**
When the mobile app or Home Assistant re-sends the same optimiser settings, PowerSync now treats unchanged profit-max, spread-export, and spread-import values as no-ops. This avoids unnecessary config writes, dispatcher updates, and load-estimator cache invalidations that could trigger expensive history refits without any real setting change.

**Large forecast arrays are excluded from recorder history**
LP optimiser, Solcast, and Amber forecast sensors still expose their live forecast attributes, but Home Assistant's recorder is now told not to persist the large regenerated prediction arrays. Scalar sensor states remain recorded while the database avoids oversized forecast blobs and repeated recorder warnings.

Update available via HACS
