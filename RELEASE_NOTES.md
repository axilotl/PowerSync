## What's Changed

**Fix: consecutive force-mode automations no longer undo each other via stale expiry timers (#22, thanks @rpcai!)**
When two force-mode automations ran back-to-back — e.g. `force_discharge` at 3kW followed by `force_discharge` at 6kW, or `force_charge → force_discharge` — the second command's hardware writes could be silently wiped out moments later by the first command's cleanup timer. The root cause was an asyncio race where `cancel_expiry_timer()` was only called *after* awaits in the handler, so a callback that was already on the event loop's ready queue would run anyway during the new command's Modbus/API write window.

The fix adds two complementary guards, both executed synchronously **before the first `await`** in each service handler (which asyncio guarantees cannot be interrupted by callbacks):

1. A new `_cancel_all_force_timers()` helper that cancels both the discharge and charge expiry timers at the start of `handle_force_discharge`, `handle_force_charge`, and `handle_restore_normal`. Because it runs to completion before any `await`, no already-scheduled callback can slip through.

2. A command generation counter that advances on every service invocation. Each of the 12 `auto_restore_*` callbacks (Sigenergy / FoxESS / GoodWe / Sungrow / Tesla × discharge + charge, plus the two persisted-state restores) captures the generation at scheduling time and silently skips execution if the counter has since advanced. This is the defence-in-depth layer that catches any timer that somehow slips through the cancel.

Full credit to **@rpcai** who diagnosed this on a FoxESS H3-Smart running consecutive `force_discharge` commands and contributed the fix in PR #22.

**Fix: mutual exclusion between force_discharge and force_charge state flags**
Related to the above: `handle_force_charge` has always cleared `force_discharge_state["active"]` in each battery-specific branch when transitioning from discharge to charge mode. The opposite direction (`force_charge → force_discharge`) was missing the symmetric clear, so `force_charge_state["active"]` would stay `True` even after force_discharge took over, confusing downstream checks (optimizer mode evaluation, tariff endpoint, automation triggers, mode-change notifications). `handle_force_discharge` now clears any active `force_charge_state` at the entry chokepoint — simpler than scattering the clear across all five battery branches, and guaranteed to fire on every invocation.

Update available via HACS
