## What's Changed

**Optimizer entities renamed and clarified**
The "Optimizer Next Action" sensor was confusing because it skips ahead to the next *change* of action — when the optimizer is in self-consumption mode for the next 17 hours, the sensor reports "charge" with tomorrow morning's timestamp, which reads like the battery is about to charge in a few minutes when it isn't. The sensor has been renamed to **Next Scheduled Change** and gains two new attributes that give the missing context: `current_action` (what the battery is doing right now) and `current_until` (when that current action segment is scheduled to end). Together these answer "what's happening now, when does it end, and what's next" inside a single entity card.

The "Optimizer Current Action" sensor has been renamed to **Current Action** and now exposes a `until` attribute showing when the active action segment ends. Same data the new Next Scheduled Change sensor uses, surfaced on the current-state side too.

Existing automations and dashboards that reference these entities by `entity_id` (e.g. `sensor.power_sync_optimization_status`, `sensor.power_sync_optimization_next_action`) continue to work — only the friendly display labels and a couple of attribute fields changed; underlying state values, unique_ids, and event firing are unchanged. The dynamic dashboard and mobile app pick up the new labels automatically.

Update available via HACS
