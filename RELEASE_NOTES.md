<!-- release: v2.12.484 -->

## What's Changed

**Correct Flow Power network tariff boundaries**
Flow Power network tariff lookups now use the dispatch interval end expected by the tariff library when evaluating the current wall-clock window. This prevents the network tariff sensor from showing the previous time-of-use rate for the first five minutes after a tariff change, including Essential Energy BLNRSS2 Sun Soaker windows.

**Keep Flow Power PEA pricing aligned**
The same interval-boundary handling now feeds Flow Power PEA network tariff calculations, so optimizer pricing and the live network tariff sensor stay aligned at tariff transitions. A regression test covers the boundary conversion to keep the tariff lookup from drifting back to the delayed behavior.

Update available via HACS
