<!-- release: v2.12.394 -->

## What's Changed

**Add a Profit Max target SOC**
Smart Optimization now lets Profit Max target a configurable battery SOC before the export window instead of always aiming for 100%. The setting is available in setup/options, accepts either ratio or percentage values internally, and keeps the existing 100% default for current installs.

**Mark unavailable Hermes signaling as degraded**
Tesla Hermes signaling token rejections are now treated as an unavailable signaling state instead of a Home Assistant error. Normal Fleet API telemetry and tariff sync can continue while the private Hermes channel is unavailable, and diagnostics now expose the unavailable reason without repeated reconnect noise.

Update available via HACS
