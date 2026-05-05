<!-- release: v2.12.299 -->

## What's Changed

**Correct Powerwall pack roles for PW3 and PW2 sites**
PowerSync now separates physical Powerwall DINs from BMS module serials when reading Tesla BMS telemetry. PW3 stacks are labelled from the actual leader/follower batteryBlocks, expansion modules remain expansions, and PW2 systems stay as ordinary Powerwall 1/2/3/4 units instead of being mislabelled as PW3 followers or expansions. Serial attributes now expose both the physical Powerwall serial and the BMS module serial when Tesla reports them differently.

**Reconcile stale follower and expansion SOC readings from Tesla aggregate totals**
Serial-less or stale near-empty PW3 follower/expansion BMS rows can now be corrected from Tesla's aggregate remaining-energy total when the pack capacities match. This fixes cases where one pack showed around 1 percent while the rest of the site was near the real system SOC.

**Block grid charging during Flow Power export windows**
The LP optimiser now marks Flow Power Happy Hour export intervals as battery-charge-blocked slots. That prevents the optimiser from buying energy during an export-only window, including the free-import force-charge shortcut and the greedy fallback path.

Update available via HACS
