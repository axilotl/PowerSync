<!-- release: v2.12.289 -->

## What's Changed

**Allow battery export across all providers**
PowerSync now permits battery-to-grid export whenever the active tariff has a positive sell price, regardless of electricity provider. This fixes provider-specific blocking that could leave Amber, AEMO VPP, GloBird, Octopus, NZ, or other tariff users in self-consumption even when the optimiser had a valid export opportunity.

**Make Profit Max provider-neutral**
Profit Max now changes the optimiser incentive for every provider instead of only Flow Power. It lowers the terminal SOC weight so the optimiser is more willing to use stored energy for profitable export, while normal mode can still export when the sell price makes that economical.

**Keep zero and negative export periods protected**
Battery export remains blocked when the sell price is zero, negative, missing, or malformed. Existing explicit export windows such as Flow Power Happy Hour, export boost, and Octopus Saving Sessions still layer on top of the generic positive-price rule.

Update available via HACS
