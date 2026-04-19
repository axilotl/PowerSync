## What's Changed

**Tesla API token handling — skip polls when token is unavailable**
When the tesla_fleet integration briefly returns no token during a refresh cycle, PowerSync was silently falling back to the stale startup token and making API calls that would fail or return stale data. Now, if the token getter returns nothing, the poll (or spike/saving-session action) is skipped entirely and retried on the next cycle. This prevents error storms during Tesla token rotation.

**Enphase DPEL curtailment — try relay_config=True for AU gateways**
Some Australian Enphase IQ Gateways reject all DPEL export limit payloads with `relay_config=False` (even when no physical relay is wired), causing load-following curtailment to silently fail. PowerSync now also tries `relay_config=True` variants throughout the payload sequence, giving these gateways a better chance of accepting the curtailment command.

**EV charging — fix ghost sessions persisting after vehicle departs**
EV charging sessions that received no energy readings for 30+ minutes (e.g. because the vehicle disconnected or BLE contact was lost) were left open indefinitely and could confuse the charging planner. A background cleanup now auto-closes these stale sessions every 5 minutes.

**EV energy flow card — fix stale BLE presence detection**
BLE sensor entities hold their last-known state when a vehicle leaves Bluetooth range, which caused the energy flow card to show an EV as present long after it had left. The card now ignores binary/sensor entities that haven't updated in 15 minutes.

**EV energy flow card — clean up BLE vehicle display names**
Vehicle labels sourced from BLE entities were showing raw internal prefixes like `ble_phoenix` or `Tesla BLE (ble_slater)` instead of readable names. Labels are now stripped of prefix noise and properly capitalised.

**Sigenergy force charge/discharge — use existing Modbus connection**
Force charge and discharge commands were creating a brand-new Sigenergy controller (and opening a new Modbus connection) instead of reusing the coordinator's existing connection. This caused connection conflicts. The commands now use the coordinator's live controller instance directly, and the conflicting active-power-target register write (which fought against the export limit approach) has been removed.

*Update available via HACS*
