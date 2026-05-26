<!-- release: v2.12.475 -->

## What's Changed

**Fix PW3 Battery Health pack counts**
PowerSync now ignores extra null PW3 BMS placeholder rows when calculating Battery Health. Sites with one leader and two follower Powerwalls should no longer see a phantom third follower or have the real follower capacity split across too many packs.

**Use scanned BMS capacity for Tesla aggregate sensors**
When Tesla live status omits total pack energy, the aggregate Battery Pack Capacity and calculated Battery Energy Left sensors now prefer the latest Battery Health BMS capacity before falling back to the static battery-count estimate.

Update available via HACS
