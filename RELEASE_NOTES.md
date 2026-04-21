## What's Changed

**Battery Health API: Full BMS Telemetry for All Brands**
The Battery Health endpoint previously only returned a single SOH percentage for non-Tesla systems. It now returns a rich `bms` block with whatever each brand exposes over Modbus — temperature, voltage, current, SoC, min/max SoC limits, and max charge/discharge power (fields vary by brand). The app can now display detailed battery health data for Sungrow, Sigenergy, GoodWe, AlphaESS, and FoxESS, not just Tesla.

**Battery Health API: Unified Response Shape Across Brands**
Tesla and non-Tesla responses now share a consistent structure: a `brand` field identifies the system, and a `bms` object holds normalised telemetry under the same key names. Tesla responses also gain `rated_capacity_kwh` and `current_capacity_kwh` in the `bms` block alongside the existing health percentage.

**Battery Health API: Cloud RSA Source Support**
The POST handler now accepts and stores extended metadata from a richer data source: `source` (distinguishes mobile TEDAPI vs cloud RSA), `gateway_din`, `energy_site_id`, `site_name`, and `raw_vitals`. These are passed through in the GET response so the app knows how the data was collected.

Update available via HACS
