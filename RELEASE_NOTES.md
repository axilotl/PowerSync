<!-- release: v2.12.642 -->

## What's Changed

**Solcast forecast detection for renamed sensors**
PowerSync now scans Solcast sensor entities for usable `detailedForecast` attributes when the forecast sensors do not use the default entity IDs. This lets Smart Optimization consume the timestamped Solcast forecast already present in Home Assistant instead of falling back to price-only scheduling.

Update available via HACS
