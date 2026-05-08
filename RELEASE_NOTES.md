<!-- release: v2.12.337 -->

## What's Changed

**Stabilise the full test suite**
PowerSync's unit-test harness now isolates module-level Home Assistant and PowerSync stubs between tests. This prevents stale `power_sync.const` or placeholder `aiohttp` modules from leaking into unrelated tests, keeping the full suite reliable for future releases.

Update available via HACS
