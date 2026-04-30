## What's Changed

**Dashboard: Cleaner price gauges**
The dynamic dashboard's Import and Export price gauges have been redesigned. The previous Home Assistant gauge cards displayed prices in `$/kWh` with awkward decimals (e.g. `0.245`); the new gauges render as compact custom SVG dials showing cents directly (e.g. `24.5 c/kWh`), which matches how most Australian retailers quote prices and is far easier to read at a glance. Color thresholds are tuned for the cents scale: green when prices are favourable, yellow as they climb toward typical rates, and red during peaks or expensive export windows.

The Export gauge label has also been renamed from "Export Earnings" to "Export Price" — both the gauge tile and the price-history chart series — to match the language used in the rest of the integration and avoid confusion with the daily earnings sensor (which is a separate, dollar-denominated value).

Update available via HACS
