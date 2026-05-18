<!-- release: v2.12.422 -->

## What's Changed

**GoodWe control mode selection**
GoodWe setup now has an explicit EMS control method selector for Direct IP control versus Home Assistant entity control. The flow no longer relies on the presence of an entity prefix to imply mode, and Direct IP mode ignores the GoodWe EMS prefix while legacy entity-mode configs continue to load correctly.

**Sungrow Modbus telemetry alignment**
PowerSync now follows the current mkaiser Sungrow SHx Modbus mapping more closely for key runtime telemetry. Battery power, battery current, grid meter power, grid frequency, BMS charge/discharge current limits, backup reserve, and export-limit state now use the preferred register addresses and scaling where available, with fallbacks retained for older firmware.

**More stable Sungrow/WiNet polling**
Sungrow Modbus requests are now serialized and paced with a small connect/request delay to reduce WiNet-S/S2 dropped-frame behaviour. Runtime telemetry reads also no longer perform a no-op write probe against current-limit registers, avoiding unnecessary Modbus writes on systems where those registers are read-only or fragile.

**Powerwall local timeout handling**
Powerwall local TEDAPI calls now convert connection timeouts into the same unreachable-gateway error path used for other local gateway failures, so local polling and dispatch fallbacks can recover cleanly instead of leaking a raw timeout.

Update available via HACS
