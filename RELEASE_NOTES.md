## What's Changed

**Sigenergy force charge / force discharge fixed**
The hardware-extension path that re-issues Modbus charge/discharge commands every ~30 seconds while a force action is active was crashing with `'SigenergyEnergyCoordinator' object has no attribute 'client'`. It tried to spin up a brand-new Sigenergy controller with the wrong constructor arguments instead of reusing the one the coordinator already owns. Both call sites now use the coordinator's existing controller (matching how every other Sigenergy code path already works), so manual and optimizer-driven force charge/discharge actually run on Sigenergy systems instead of erroring out every poll.

Update available via HACS
