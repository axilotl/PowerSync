<!-- release: v2.12.541 -->

## What's Changed

**Profit Max respects the manual optimizer reserve**
When Auto-apply optimizer reserve is enabled, Profit Max now keeps forced export/discharge above the saved manual Minimum discharge level. Forecast auto-reserve can still raise the software floor when needed, but it will not lower Profit Max force-export below the user's manual optimizer reserve.

**Forced export stops before crossing the floor**
PowerSync now blocks or cancels optimizer force-export when current SOC is at the applicable reserve floor, or when the planned export action would project SOC at or below that floor. In those cases it returns the inverter to self-consumption instead of relying on the hardware backup reserve to stop the battery later.

Update available via HACS
