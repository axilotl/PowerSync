## What's Changed

**Flow Power Import Price: Portal TWAP Now Used for Accurate Pricing**
The `Flow Power Import Price` sensor was not using the TWAP from your Flow Power portal account data, even when the portal connection was active. It fell back to the hardcoded 8 c/kWh default instead. The sensor now uses the same TWAP priority order as the tariff schedule (override → portal → local tracker → fallback), so the live price sensor matches what's used for the LP optimizer and cost tracking.

**Flow Power Import Price: Diagnostic Attributes Added**
The sensor's attributes now include `tariff_code`, `network`, and an improved `twap_source` field (showing `portal`, `override`, `dynamic`, or `fallback`) to make it easy to verify which inputs are driving the calculated price — useful when comparing against the standalone Flow Power HA integration.

Update available via HACS
