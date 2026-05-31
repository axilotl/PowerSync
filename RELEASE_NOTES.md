<!-- release: v2.12.518 -->

## What's Changed

**Solar surplus charging now respects a full EV battery**
PowerSync now checks the target vehicle SoC before starting an app-managed solar surplus charging session. If Home Assistant reports the EV at 100%, the solar surplus session is not opened and no charging command is issued.

**Existing solar surplus sessions stop when the EV is full**
If a solar surplus dynamic session is already active and the EV reaches full charge, PowerSync now stops and releases that session instead of continuing to own the charger and adjust amps.

Update available via HACS
