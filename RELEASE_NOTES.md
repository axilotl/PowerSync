<!-- release: v2.12.466 -->

## What's Changed

**GloBird Zerohero export scheduling**
PowerSync Smart Optimization now recognizes battery energy filled from an earlier cheap or free import window when deciding whether a later feed-in window should export. This fixes schedules such as GloBird Zerohero where the battery charged during the 11:00-14:00 free period but stayed in self-consumption during the 18:00-21:00 positive export period, even though battery export was allowed.

**Optimizer regression coverage**
Added a focused optimizer regression for the Zerohero free-import to positive-FIT schedule shape, using Sigenergy-style battery limits, so future scheduler changes preserve the expected charge-then-export plan.

Update available via HACS
