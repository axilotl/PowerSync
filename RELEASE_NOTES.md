<!-- release: v2.12.419 -->

## What's Changed

**Fix NeoVolt stack parking behavior**
PowerSync now parks higher-SOC NeoVolt stacks with `No Battery Charge` before falling back to `Idle (No Dispatch)`. This avoids the previous behavior where a parked stack could stop dispatching to the house, causing the site to import from grid while balancing another lower-SOC stack.

**Expose NeoVolt surplus balancing in optimization settings**
NeoVolt users now see the independent stack surplus-balancing selector in the optimization options, directly below the Smart Optimization toggle. The selector remains independent from Smart Optimization itself, making it clear that NeoVolt stack balancing can be controlled separately from the LP optimizer.

Update available via HACS
