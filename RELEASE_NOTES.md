## What's Changed

**Refactor: unified Tesla vehicle discovery across the mobile API view and automation planner (issue #23 finding D)**
Before this release there were two parallel Tesla vehicle discovery systems: `EVVehiclesView.get()` in the HTTP view layer scanned the device registry manually for Fleet API vehicles and then ran its own BLE discovery via `_get_tesla_ble_vehicle()`, while `discover_all_tesla_vehicles()` in the automation charging planner did a second, independent scan of the same device registry with a second BLE fallback path. Any future extension — new Tesla integration, BLE/Teslemetry/Tessie enhancement, capability probe — had to land in both places, and it was very easy for the two to drift out of sync (the BLE discovery path already had because PR #24 added it to only one of them).

This release collapses both paths into a single source of truth:

- `discover_all_tesla_vehicles()` now returns a richer dict per vehicle including the `device` registry entry, `source` (`fleet_api` / `tesla_ble`), and `ble_prefix`. Backward compatible — existing callers that only read `vin` / `name` / `device_id` see no change.
- `EVVehiclesView.get()` now calls `discover_all_tesla_vehicles()` for its Fleet API section instead of doing its own device-registry scan. The previous ~60-line duplicated scan loop (the 8th occurrence of the same pattern) is gone, and the view simply iterates discovery results and enriches each with current entity state for the mobile app.
- The BLE section of `EVVehiclesView.get()` is unchanged — it still uses `_get_tesla_ble_vehicle()` to produce rich state dicts — but now the discovery and the state enrichment are clearly separated.

Net effect: any future Tesla integration support (or BLE enhancement) added to `discover_all_tesla_vehicles()` automatically appears in both the automation planner and the mobile app vehicle list without a parallel edit. No behavior changes for existing users.

**Refactor stats:** `__init__.py` loses ~45 lines of duplicated scan-loop boilerplate; `ev_charging_planner.py` adds ~8 lines of dict enrichment to expose `device` / `source` / `ble_prefix` to the view.

Update available via HACS
