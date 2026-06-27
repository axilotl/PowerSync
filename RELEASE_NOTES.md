<!-- release: v2.12.725 -->

## What's Changed

**Tesla free-window charging with live solar**
Tesla Powerwall Smart Optimization now still starts planned force-charge windows when the current import tariff is free or negative, even if live solar is available. The previous live-solar safety guard could incorrectly leave GloBird ZeroHero systems in self-consumption during the 11:00-14:00 free-charge period.

The guard still avoids Tesla force charging during paid import when live solar surplus is available and the site cannot target a partial charge power, preserving the curtailment protection added for normal paid-price operation.

Update available via HACS
