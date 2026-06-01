<!-- release: v2.12.523 -->

## What's Changed

**Open-Meteo solar forecasts are detected more reliably**
PowerSync now recognizes Open-Meteo Solar Forecast sensors by their `watts` forecast attributes as well as by the default entity names. This helps systems where Home Assistant has renamed the forecast entities or users have customized the entity IDs, preventing the optimizer from falling back to a zero-solar schedule when valid Open-Meteo forecast data is available.

**Sigenergy tariff uploads use the numeric station ID**
Sigenergy tariff sync now resolves configured station identifiers to the numeric tariff `stationId` expected by the cloud endpoint, and rejects alphanumeric system IDs before uploading. Station selection also prefers the numeric ID when it is available, avoiding generic Sigenergy cloud failures during tariff updates.

Update available via HACS
