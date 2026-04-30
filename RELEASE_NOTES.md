## What's Changed

**SAJ now always returns to Self-Use after a force charge or force discharge**
`restore_normal()` previously relied on stanus74's `_deactivate_passive_mode()` to put the inverter back into whatever AppMode it was in before passive mode was engaged. For users running on Time of Use (AppMode=1) or Backup (AppMode=2), that meant a force charge/discharge would silently return the inverter to its original schedule-driven mode — which often disagrees with what the optimizer wants next. Restore now explicitly writes `AppMode=0` (Self-Use) at the end of the sequence, after the passive switches are disengaged, so the inverter is always in a self-consumption posture when PowerSync hands control back. Users who actually want TOU or Backup as their resting state can re-select it manually; the integration treats Self-Use as the canonical "no-override" mode.

Update available via HACS
