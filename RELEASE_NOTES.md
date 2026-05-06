<!-- release: v2.12.306 -->

## What's Changed

**Refreshed PowerSync Home Assistant dashboard**
The built-in PowerSync dashboard now uses a native responsive chart system for price, energy, TOU, LP forecast, and planned battery power charts instead of the older mixed graph approach. The dashboard keeps Home Assistant theme colors and card styling, adds clearer legends and zero-line handling, and adapts more cleanly across desktop, tablet landscape, tablet portrait, and narrow mobile layouts.

**Battery power forecast chart**
The LP optimizer now exposes planned battery charge and discharge power as dashboard data, allowing the dashboard to show upcoming battery actions directly as a 48-hour Battery Power forecast. Charging is shown below zero and discharging above zero so the plan is easier to interpret than text-only action summaries.

**Sigenergy tariff upload consistency**
Sigenergy tariff sync now builds its cloud upload from PowerSync's canonical tariff conversion before falling back to the raw interval converter. This keeps the uploaded schedule aligned with the same import tariff view used elsewhere in PowerSync, while preserving the display fix that mirrors the final import schedule into Sigenergy sell-price payloads to avoid the app showing feed-in prices as a second tariff.

**Local dashboard test helper**
Added a local `scripts/open_ha_dashboard.py` helper for developers who keep Home Assistant URL, dashboard URL, and a long-lived token in an ignored `.env` file. It can validate API access without printing credentials and open the persistent PowerSync dashboard for visual checks.

Update available via HACS
