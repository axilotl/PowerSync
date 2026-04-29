## What's Changed

**Fix: AEMO new-dispatch listener crashing on first fire (introduced in v2.12.215)**
The dispatch listener registered in v2.12.215 was a bare lambda that called `hass.async_create_task` directly. Home Assistant invokes dispatcher listeners on whichever thread originally called `async_dispatcher_send`, and HA's frame-safety machinery can re-enter that same listener from a `SyncWorker` thread. `hass.async_create_task` is not thread-safe, so each new AEMO dispatch was raising `RuntimeError: Detected that custom integration 'power_sync' calls hass.async_create_task from a thread other than the event loop` instead of running the tariff sync. The HACS-shipped fix from v2.12.215 was therefore inert: dispatch events were emitted, but the handler never executed and Tesla still received no tariff POSTs. The listener now uses `hass.loop.call_soon_threadsafe` to hop back onto the event loop before scheduling the coroutine, matching the pattern the WebSocket callback already uses. No config or behavior change for users — just makes the v2.12.215 fix actually work.

Update available via HACS
