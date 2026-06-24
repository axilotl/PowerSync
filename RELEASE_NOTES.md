<!-- release: v2.12.708 -->

## What's Changed

**FoxESS direct Modbus PV2 power register**
PowerSync now reads PV2 power from the correct FoxESS H1/KH/H3 register when using direct Modbus. The previous mapping used the PV2 voltage register as PV2 power, which could make the live solar value and PowerSync daily solar accumulator look much higher than the inverter or FoxCloud daily generation values.

**FoxESS solar total stability**
Daily solar totals derived from direct Modbus live power should no longer climb from a constant voltage-as-power reading on affected FoxESS systems. Existing inflated same-day totals may remain until the next daily reset, but new live PV readings should use the corrected power source after updating and restarting Home Assistant.

Update available via HACS
