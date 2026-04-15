## What's Changed

**Fix FoxESS H3-Pro / H3-Smart force-charge being stifled by concurrent house load (e.g. EV charging)**
Reported by JoelyMoley: on a FoxESS H3-Pro, force-charging the home battery while
the EV was drawing 11 kW topped out at 4-5 kW to the battery instead of the
expected ~15 kW. Stopping the EV immediately restored full 15 kW charge rate.

Root cause: force_charge/force_discharge on H3-Pro/H3-Smart was enabling remote
control with bitfield 0x0009 ("grid meter target") instead of 0x0001 ("AC output
target"). In grid-target mode the power setpoint controls what the grid meter
reads, so the inverter apportions `battery_charge = setpoint − house_load + PV`.
With an EV pulling 11 kW, a 15 kW setpoint left only ~4 kW for the battery.

Switched all FoxESS families (H1, H3, KH, H3-Pro, H3-Smart) to AC-output target.
The setpoint now commands battery power directly and is independent of whatever
the house/EV is drawing — force-charge hits the configured power regardless of
concurrent load, matching H1/H3/KH behaviour that's been in production for
months. Register addresses, widths and scaling differ between families but the
0x0001 enable semantics are shared, so no per-family branching is needed.

Update available via HACS
