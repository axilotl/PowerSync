<!-- release: v2.12.350 -->

## What's Changed

**GoodWe ESA export discharge restored**
PowerSync now uses the GoodWe EMS `sell_power` mode first when forcing discharge through the GoodWe Home Assistant EMS entities. This restores grid export behavior on GoodWe ESA systems where `discharge_battery` only supplied household load instead of exporting.

**Solar-first charging preserved**
GoodWe force charge continues to prefer `charge_battery`, so available solar remains the priority source for battery charging. `buy_power` is still kept as a compatibility fallback for installations that expose the older EMS option.

Update available via HACS
