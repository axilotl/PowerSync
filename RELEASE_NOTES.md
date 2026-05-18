<!-- release: v2.12.423 -->

## What's Changed

**Retired duplicate Sungrow secondary setup**
PowerSync no longer exposes or initializes the old second Sungrow inverter path. Existing installs that still have retired secondary Sungrow fields saved will have those keys cleaned when the Sungrow connection settings are saved, preventing the same WiNet endpoint from being polled and commanded twice.

**Cleaner Sungrow connection settings**
The Sungrow configuration screens now only ask for the active hybrid inverter Modbus endpoint. Grid-only PV inverters should remain configured through AC inverter/curtailment settings instead of the battery Modbus section.

Update available via HACS
