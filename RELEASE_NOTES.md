## What's Changed

**Fix Sigenergy NEM region detection for non-NSW Amber users**
The auto-detection of the NEM region from Amber's network field was calling `GET /sites/{site_id}` — an endpoint Amber doesn't expose. When the Amber site ID was already stored in config, the function would silently fail and fall back to defaulting timezone to Sydney. Sigenergy users on Energex/Ergon (QLD), AusNet/CitiPower (VIC), SA Power Networks, or TasNetworks were all silently being treated as NSW1, causing the 30-min Sigenergy timeRange slots to drift against their real local time. The function now reads the existing `GET /sites` list and finds the user's site by ID, which is the actual API Amber supports.

Update available via HACS
