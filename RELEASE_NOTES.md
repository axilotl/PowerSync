<!-- release: v2.12.468 -->

## What's Changed

**Sungrow tariff fallback for curtailment**
Sungrow curtailment can now use the configured tariff schedule when no live feed-in price coordinator is available. This stops non-Amber Sungrow systems from repeatedly logging that no feed-in price exists when a TOU tariff is already configured.

**Continuous free-period force charging**
Smart Optimization now smooths free or negative import-price windows into a continuous target-charge schedule for systems that support target charge power, including Sungrow. This prevents the optimizer from stop-starting force charge between adjacent free-period slots while leaving paid-price behavior unchanged unless spread import is explicitly enabled.

**Cleaner non-Tesla startup and energy recorder behavior**
Tesla tariff startup fetches are now skipped unless a Tesla site and token path are configured, avoiding misleading Tesla tariff warnings on non-Tesla systems. The daily load sensor also now uses a `total` state class so Home Assistant recorder accepts small downward corrections in calculated daily load.

Update available via HACS
