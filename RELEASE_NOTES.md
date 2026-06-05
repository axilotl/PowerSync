<!-- release: v2.12.591 -->

## What's Changed

**Tesla app TOU tariffs are read from the v2 API payload**
PowerSync now checks Tesla's newer `tariff_content_v2` field when loading the Powerwall tariff schedule, then falls back to the older `tariff_content` field. This fixes cases where a TOU plan configured in the Tesla app could be present on the Tesla side but still fail to appear in PowerSync after a Home Assistant restart or reload.

Update available via HACS
