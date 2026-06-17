<!-- release: v2.12.662 -->

## What's Changed

**Scheduled charging with multiple Teslas**
Scheduled charging now handles multi-Tesla homes more safely when no single VIN is selected by a legacy charging path. The location check now prefers any Tesla that is actually at home before falling back to an away vehicle, while exact VIN checks still stay VIN-specific. This prevents an away Tesla from blocking or stopping scheduled charging for another Tesla that is plugged in at home.

**Dashboard tooltip transparency**
Dashboard chart tooltips now use explicit transparent RGB backgrounds instead of theme `color-mix()` blending. This avoids Home Assistant themes or WebViews resolving the tooltip surface as fully opaque after a hard refresh.

**GoodWe EMS mode guidance**
GoodWe documentation now matches the current EMS control behavior: force charge prefers `charge_pv`, falls back to `charge_battery` where needed, and keeps PV contributing first while grid power supplies the shortfall.

Update available via HACS
