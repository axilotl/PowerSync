<!-- release: v2.12.285 -->

## What's Changed

**Protect Octopus batteries from profit-mode export drains**
PowerSync now treats battery-to-grid export as an explicit event or configured window, not a blanket permission from Profit Maximisation Mode. Octopus users can still export from the battery during joined Saving Sessions, but ordinary cheap-import versus fixed-export arbitrage will no longer empty the battery ahead of poor solar days.

**Keep provider-specific export windows working**
Flow Power Profit Maximisation remains scoped to Happy Hour export slots, configured export boost windows still allow battery export only inside the configured time and threshold, and Octopus free electricity events remain charge-only. The optimizer also blocks impossible grid-import-to-export passthrough in the LP model.

Update available via HACS
