<!-- release: v2.12.731 -->

## What's Changed

**Monitoring mode now releases Tesla control**
Turning monitoring mode on now actively asks PowerSync to restore Tesla to normal operation instead of only doing that for Sigenergy systems. This prevents a Powerwall from staying in a stale PowerSync force-charge or TOU state when monitoring mode is enabled after force state has already been cleared or lost.

**Force charge keeps grid charging enabled**
Tesla Powerwall force-charge now re-enables grid charging after the PW3 charge-kick mode bounce. This keeps force charge in the intended state: Time-Based Control, backup reserve raised to 100%, the PowerSync force-charge tariff active, and grid charging allowed.

**Safer restart cleanup while monitoring**
If Home Assistant restarts while a force mode is persisted and monitoring mode is enabled, PowerSync now restores the saved Tesla state instead of dropping the persisted timer and leaving the hardware in the force mode.

Update available via HACS
