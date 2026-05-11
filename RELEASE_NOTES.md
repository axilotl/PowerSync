<!-- release: v2.12.388 -->

## What's Changed

**Re-engage NeoVolt stacks after cutoff handover**
PowerSync now detects the NeoVolt edge case where one stack reaches its discharge cutoff, the site starts importing, and the higher-SOC stack still reports Normal but does not actually take over the house load. The balancer now briefly reasserts Normal on the higher-SOC stack, matching the manual Idle then Normal toggle that restored discharge during testing.

**Improve Hermes signaling token selection**
PowerSync now uses the corrected local Powerwall signaling token path so Hermes signaling setup does not pick the wrong token source.

Update available via HACS
