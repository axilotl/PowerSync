<!-- release: v2.12.361 -->

## What's Changed

**Tesla/Teslemetry EV detection no longer blocks sensor setup**
PowerSync now tolerates Home Assistant device identifiers that include extra metadata fields when scanning Tesla and Teslemetry vehicles. This prevents the sensor platform from failing with `too many values to unpack` and keeps PowerSync entities available on systems where a vehicle identifier has more than the standard two values.

Update available via HACS
