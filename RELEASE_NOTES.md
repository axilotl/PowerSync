<!-- release: v2.12.615 -->

## What's Changed

**Smart EV charging can preserve the home battery**
Smart Schedule now supports a Preserve Home Battery setting so EV charging can run without intentionally discharging the home battery. The same control is available in per-departure day constraints, where it can override the default setting for a specific departure day.

**Consume Battery and Preserve Home Battery are mutually exclusive**
Smart Schedule now treats the home-battery consume floor and preserve mode as separate choices. Setting Consume Home Battery above 0 disables preserve mode for that scope, while enabling Preserve Home Battery sets the consume floor to Off so the optimizer receives a clear no-discharge intent.

**Tesla Preserve Charge holds current home battery SOC**
The automation Preserve Charge action now preserves the Tesla home battery by setting backup reserve from the current site battery SOC instead of only disabling grid export. Unsupported Tesla reserve values in the high-80s and 90s are mapped to valid Tesla reserve targets so the action can still hold the battery safely.

Update available via HACS
