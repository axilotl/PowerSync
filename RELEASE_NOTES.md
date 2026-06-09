<!-- release: v2.12.616 -->

## What's Changed

**Optimizer schedule times stay aligned with tariff windows**
Smart Optimization now builds displayed battery action times from the same timestamp slots used for the price forecast. This prevents zero-cost GloBird ZeroHero charge windows from appearing shifted by one or more 5-minute intervals when optimization crosses an interval boundary.

**Regression coverage for shifted free-charge windows**
Added coverage for a forecast starting at 8:00 while the optimizer clock has moved to 8:15, ensuring the planned 11:00-14:00 free import window still appears exactly as 11:00-14:00.

Update available via HACS
