## What's Changed

**SAJ H2: Fixed coordinator crash preventing house scene and energy data from loading**
The SAJ H2 coordinator was calling `EnergyAccumulator.totals()` which doesn't exist — the method is named `as_dict()`. This crash happened on every first update, causing the coordinator to be set to `None` on startup. The knock-on effect: all live power values (solar, home, battery, grid) showed as `--` in the house scene, and energy summary data was unavailable. This is fixed; the coordinator now starts and populates data correctly.

**SAJ H2 and Solax: Energy Summary now populated in the app**
Even after the crash fix, the Energy Summary screen in the app would show zeros because there was no calendar history handler for SAJ H2 or Solax — those systems were silently falling through to the Tesla-only code path and returning an error. Both systems now have their own handler that reads today's accumulated generation, import, export, and consumption from the energy accumulator and returns it correctly. (Note: energy summary is today's running total only — historical day/week/month data requires Tesla.)

Update available via HACS
