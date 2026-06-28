<!-- release: v2.12.729 -->

## What's Changed

**Refresh Flow Power KWatch optimiser prices**
PowerSync now treats Flow Power KWatch as a dynamic optimiser price source, so KWatch price updates trigger the same plan refresh path as Amber and AEMO pricing. This prevents Smart Optimization from continuing to plan from an older Flow Power tariff schedule after the KWatch forecast has moved, which could show charge windows based on stale effective prices.

Update available via HACS
