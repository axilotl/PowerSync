<!-- release: v2.12.699 -->

## What's Changed

**Tesla EV start targeting**
Scheduled and coordinated EV starts now resolve a default Tesla start to the single home plugged-in Tesla before sending the start command. This fixes multi-Tesla setups where the first Tesla is home but unplugged and a later Tesla is plugged in, which could cause scheduled or solar-surplus starts to fail.

Update available via HACS
