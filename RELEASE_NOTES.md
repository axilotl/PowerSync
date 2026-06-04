<!-- release: v2.12.577 -->

## What's Changed

**Add Flow Power No Idle Mode switch**
Flow Power users can now toggle No Idle Mode directly from PowerSync's Configuration controls. When enabled, Smart Optimization replaces idle hold actions with self-consumption for Flow Power plans, making the existing no-idle behavior configurable without reopening the integration options flow.

**Keep optimizer settings in sync**
The No Idle Mode setting now updates through the same live optimizer settings path as Profit Maximisation and spread import/export controls. Changes made from the switch, options flow, or optimization settings API persist to the config entry and stay aligned with the running optimizer.

Update available via HACS
