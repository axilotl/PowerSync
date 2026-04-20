## What's Changed

**Fixed crash when fetching OCPP charger status**
The integration crashed with a `NameError` when the mobile app requested EV charger data and an OCPP charger was detected. The `CONF_OCPP_ENABLED` constant was referenced in the OCPP charger detection handler but never imported, causing every charger status request to fail with a 500 error. This is now fixed.

**Corrected Sigenergy Modbus register addresses for ESS rated power, capacity, and SOH**
Four Sigenergy plant-level input registers had incorrect addresses sourced from an older/incorrect protocol version, causing Modbus `ILLEGAL_DATA_ADDRESS` errors on every poll. The ESS rated charge power (30079→30550), rated discharge power (30081→30552), rated energy capacity (30083→30548), and State of Health (30087→30602) registers have been corrected to match Sigenergy Modbus Protocol v1.7+. The charge/discharge power errors were visible as recurring Modbus debug errors; the capacity and SOH registers were silently returning nothing, meaning the battery spec auto-detection and health sensor were not reading any data.

*Update available via HACS*
