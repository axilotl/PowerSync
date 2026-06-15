<!-- release: v2.12.653 -->

## What's Changed

**GoodWe LP charging now preserves available solar**
GoodWe EMS entity control now prefers the solar-first Charge PV mode when PowerSync asks the inverter to charge. This lets the LP charge target act as the allowed grid contribution while still allowing available PV to charge the battery, instead of limiting total battery charge power and exporting excess solar. Systems that do not expose Charge PV fall back to the previous Charge Battery command.

Update available via HACS
