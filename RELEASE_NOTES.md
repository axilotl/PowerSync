## What's Changed

**Octopus Energy now works without the internal coordinator data path**
UK users on the BottlecapDave Octopus Energy integration sometimes had no prices feeding the LP because the optimizer's internal data path expects a specific cached structure that isn't always populated (fresh installs, older versions, race conditions during startup). The price coordinator now falls back to reading the documented public entities (`sensor.octopus_energy_electricity_*_current_rate` and `event.octopus_energy_electricity_*_current_day_rates`) when the internal data is missing, with both import-only and import+export tariffs handled. If only an import tariff is present, a synthetic 4.1p SEG export rate is generated so the LP still has a complete forecast to work with.

**Multi-vehicle Tesla households: Wall Connector power attaches to the right car**
Tesla's Wall Connector telemetry stays awake even when vehicles are asleep, so PowerSync uses it for connection and power detection — but it was unconditionally attached to the first vehicle in the list, which was wrong for households with multiple Teslas. The matcher now reads the WC's reported VIN (when available) and finds the matching vehicle exactly; when no VIN is reported, it only attaches power if exactly one vehicle is charging or connected, otherwise leaves it ambiguous rather than guessing wrong. Same logic now drives both the integration-internal status read and the EV widget endpoint.

**EV power values normalized across W and kW units**
Different Tesla integrations and Wall Connector firmwares report charging power in different units — some in watts (`7400`), some in kilowatts (`7.4`). The previous code did a raw `float(state.state)` which treated `7400` as `7400 kW`, producing nonsense readings on dashboards and breaking solar-surplus calculations. A new normalizer reads the entity's `unit_of_measurement` attribute when available and falls back to a magnitude heuristic (`>100 = watts`), so charging power is always reported correctly in kW.

**Coordinated charging modes can take over from each other cleanly**
Price-level recovery, scheduled charging, and the EV mode coordinator can now displace an existing solar-surplus session when you actually want one of them to take over (e.g. cheap-rate window opens, scheduled charging time arrives). Previously the start request was silently blocked because the existing solar-surplus owner held the loadpoint. Manual sessions still always block automatic takeovers — manual is sacred. New `can_take_over_ev_ownership` helper centralizes the rules and is fully unit-tested.

**Tesla solar-surplus respects the 5 A hardware minimum**
Tesla refuses to charge below 5 A, so when solar-surplus had a configured minimum lower than that the stop-delay hysteresis would never trigger correctly and the LP would issue impossible amp commands. Solar-surplus and dynamic-start now treat 5 A as the effective floor for Tesla regardless of what's configured.

**Dashboard PV-string card now works for more inverters**
The "FoxESS Sensors" dashboard card has been renamed and generalized to "PV String Details" and now auto-detects PV1/PV2 power, voltage, and current from any inverter that exposes them — including FoxESS, GoodWe (`ppv1/ppv2`), Solax (`vpv1/ipv1`), and any integration whose entity IDs end in `_pv1_power`, `_pv1_voltage`, `_pv1_current`, etc. The card only appears when at least one PV string entity is actually present, so no empty cards on hybrid setups without separate string telemetry.

**Default-loadpoint dashboard merges with observed vehicle**
If the dynamic state has a `_default` loadpoint (no specific vehicle ID resolved yet) and exactly one Tesla is charging or connected on the system, the dashboard now merges them so you see the real vehicle name and a stable loadpoint ID instead of "EV" / "_default". Reduces duplicate cards and gives the energy chart something stable to anchor to across restarts.

Update available via HACS
