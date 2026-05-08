<!-- release: v2.12.333 -->

## What's Changed

**NeoVolt SOC-aware force charging**
Optimizer and manual force-charge commands now respect independent-stack SOC balance. When one stack is well ahead, PowerSync force-charges the lower-SOC stack and parks the higher-SOC stack instead of splitting the charge request equally.

**Balanced restore behavior**
When the force-charge window ends, PowerSync restores any temporarily parked higher-SOC stack to its previous normal mode.

Update available via HACS
