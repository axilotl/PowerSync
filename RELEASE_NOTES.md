<!-- release: v2.12.369 -->

## What's Changed

**Smart Optimization configuration switch**
Home Assistant now exposes an `Enable Smart Optimization` switch in the device configuration section, alongside the existing PowerSync control toggles. Turning it off disables the built-in LP optimizer without wiping the saved Smart Optimization settings, and turning it back on reselects the PowerSync LP provider so the optimizer can start again after the integration reloads.

**Configuration-flow optimizer toggle**
The initial setup and options flow now include the same Smart Optimization enable/disable control. This keeps the HA configuration screens and the entity switch aligned, so users can pause the optimizer either from the integration options or directly from the device's Configuration section.

Update available via HACS
