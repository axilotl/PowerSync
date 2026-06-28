<!-- release: v2.12.730 -->

## What's Changed

**Optimizer schedule boundary execution**
Planned battery actions now apply from the cached optimizer schedule as soon as a tariff interval boundary is reached, before the next optimization solve performs forecast and API work. This prevents force-charge windows from starting late when the solve itself is delayed by several minutes.

**Tesla free/negative import charging reliability**
Tesla Powerwall force-charge plans in free or negative import windows should now switch the battery settings at the planned start time instead of waiting for the next completed optimizer run.

Update available via HACS
