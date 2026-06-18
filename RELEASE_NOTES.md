<!-- release: v2.12.672 -->

## What's Changed

**Preserve Sungrow optimiser force windows**
PowerSync now prevents an expired manual Sungrow force-charge or force-discharge timer from restoring the inverter to normal mode when the optimiser still has an active charge, discharge, or export window. This keeps Sungrow hardware in the optimiser-requested forced mode instead of briefly dropping back to self-consumption until the next optimisation interval re-applies the command.

**Clear expired manual timer state safely**
When a manual Sungrow timer expires inside an optimiser-owned force window, PowerSync now clears the manual switch/countdown state without changing the inverter hardware state. Manual Stop/Restore still restores normal operation immediately, while optimiser-controlled windows continue uninterrupted.

Update available via HACS
