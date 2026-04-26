## What's Changed

**SAJ H2: restore_normal now exits passive charge mode correctly**
`restore_normal` was only turning off `passive_discharge_control`, which is a no-op when the inverter is in passive *charge* mode (charge switch ON). stanus74 never received the turn-off signal, so AppMode stayed at 3 (passive) instead of restoring to self-consumption. Fixed by turning off both passive switches — whichever one is currently ON will trigger stanus74 to write `passive_enable=0` and restore the previously-captured AppMode.

**SAJ H2: Solar power now reads from CT clamp sensor on AC-coupled systems**
For AC-coupled installs (no DC PV strings connected to the SAJ), the inverter's `pvPower` register always reads zero. PowerSync was mapping solar to `pvPower` first and never reaching the `CT_PVPowerWatt` fallback, so solar showed 0 W even while the CT clamp was measuring generation. Fixed by trying `CT_PVPowerWatt` first; `pvPower` remains as fallback for DC-coupled installs.

Update available via HACS
