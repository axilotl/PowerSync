<!-- release: v2.12.532 -->

## What's Changed

**Tesla local backup reserve calibration**
PowerSync now converts backup reserve values correctly when writing through the paired local Powerwall gateway path. The Tesla gateway stores backup reserve including the hidden 5% low-SOE reserve, while the Tesla app and PowerSync controls show the user-facing value, so a 5% setting now writes the calibrated local value and should remain 5% in the Tesla app instead of appearing as 0%.

**Consistent local reserve readback**
Local Powerwall reserve readbacks now use the same offset in the other direction, keeping PowerSync controls, local gateway state, and Tesla app percentages aligned for paired Powerwall installs.

Update available via HACS
