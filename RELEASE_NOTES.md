<!-- release: v2.12.517 -->

## What's Changed

**Price-level EV charging now respects a full vehicle battery**
PowerSync now stops price-level charging from starting when a paired vehicle reports 100% state of charge. This prevents cheap-price opportunity charging from waking a connected Tesla or charger session just because the import price drops below the opportunity threshold while the car is already full.

Update available via HACS
