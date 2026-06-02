<!-- release: v2.12.536 -->

## What's Changed

**Auto-apply optimizer reserve**
Smart Optimization can now automatically apply the optimizer reserve recommended by the forecast. The new opt-in switch adjusts only PowerSync's software optimizer floor, clamps it above the configured hardware backup reserve, and re-solves once so the live schedule reflects the applied floor.

**Manual reserve restore**
PowerSync now saves the user's manual optimizer reserve separately from the live auto-applied reserve. Turning the new switch off restores the saved manual optimizer reserve, and both the auto state and manual restore value survive Home Assistant restarts.

**Home Assistant and mobile controls**
The setting is available in the Home Assistant config flow, as a config switch, through the optimization API, and in the mobile app's Optimiser Options section. Recommendation metadata now reports the suggested optimizer reserve explicitly, plus the manual and applied reserve values when available.

Update available via HACS
