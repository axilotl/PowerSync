<!-- release: v2.12.625 -->

## What's Changed

**Clarify Flow Power KWatch fallback logging**
PowerSync now waits for the Flow Power portal fallback result before warning about KWatch account-summary failures. If KWatch returns `api_status_500` but the saved portal session restores successfully, Home Assistant logs now show that PowerSync is using the fallback instead of surfacing a misleading unresolved warning.

Update available via HACS
