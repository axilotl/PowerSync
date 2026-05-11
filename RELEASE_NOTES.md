<!-- release: v2.12.377 -->

## What's Changed

**Tesla hardware backup reserve stays separate from the optimizer floor**
PowerSync no longer lets Tesla IDLE or self-consumption control paths push the Powerwall hardware backup reserve up to the optimizer minimum discharge level. This prevents installs with a low hardware reserve and a higher optimizer floor from seeing the Tesla app reserve jump back to the optimizer value after Home Assistant restarts or optimizer cycles.

**Tesla IDLE now holds at the current battery SOC**
When the optimizer needs a Tesla Powerwall to pause discharge, it now sets the temporary hold point to the current SOC instead of the optimizer floor. This avoids asking the Powerwall to charge from the grid just to reach a software scheduling floor.

Update available via HACS
