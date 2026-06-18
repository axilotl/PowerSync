<!-- release: v2.12.674 -->

## What's Changed

**Restore Sungrow self-consumption discharge limit to inverter max**
PowerSync now restores Sungrow self-consumption to the highest known normal inverter discharge limit after temporary force-discharge or no-discharge control. This prevents a low manual target, such as 500 W, or a lower optimiser cap from becoming the ongoing self-consumption discharge limit.

**Protect low-power manual tests**
Manual low-power force discharge remains supported, but cleanup now resolves the normal restore target from the inverter's known charge/discharge limits instead of simply reusing the lower live cap seen before the command.

Update available via HACS
