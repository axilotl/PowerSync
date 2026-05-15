<!-- release: v2.12.407 -->

## What's Changed

**Solar surplus EV charging now respects the battery reserve**
Solar surplus charging now withholds the configured parallel battery charge reserve before calculating EV amps. This prevents systems such as Sigenergy from treating home battery charging power as EV-available surplus and ramping the car to max while the battery reserve and household buffer should still be protected.

**Sigenergy tariff sync allows optional device IDs**
Sigenergy cloud tariff sync no longer requires an optional device ID before uploading tariff schedules. Sites with valid station credentials can continue syncing Amber and other tariff data for app visibility even when the device identifier is not present.

Update available via HACS
