<!-- release: v2.12.450 -->

## What's Changed

**Fallback EV SoC sensor for generic chargers**
Generic charger setups can now configure a second EV battery SoC sensor. PowerSync reads the primary sensor first, then falls back to the second sensor when the primary value is unavailable, unknown, invalid, or outside the normal 0-100% range. This helps homes that alternate two vehicles on one charger without needing to reconfigure the integration each time.

**Consistent SoC fallback across charger views and automations**
The fallback is shared by Smart EV charging, price-level charging, schedule/status APIs, and the dashboard/mobile loadpoint feed, so PowerSync continues to show and control one generic EV loadpoint while using the first valid SoC source.

Update available via HACS
