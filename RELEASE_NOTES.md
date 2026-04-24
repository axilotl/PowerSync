## What's Changed

**Sungrow SH: Fix Battery Power Sign on Affected Firmware**
On some SH-series firmware versions, register 13022 (the S16 battery power register) reports an unsigned value, making charge and discharge indistinguishable — both read as positive watts. The `get_battery_data` path now applies the same fix already in place for the main polling path: it reads the authoritative S32 signed register at 5214–5215 and uses that value instead. This corrects `sensor.power_sync_battery_power` on affected units so the optimizer can correctly account for battery charge/discharge direction.

*Update available via HACS*
