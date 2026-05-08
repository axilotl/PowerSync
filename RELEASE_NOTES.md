<!-- release: v2.12.346 -->

## What's Changed

**GoodWe EMS force-charge now prefers solar before grid**
GoodWe entity-mode force charge now uses the `charge_battery` EMS mode when the GoodWe Home Assistant integration exposes it. This asks the inverter to charge the battery at the requested power while prioritising PV first and using grid import only for the shortfall, which avoids unnecessary solar curtailment during cheap or free grid windows.

**GoodWe exports now target battery discharge directly**
GoodWe entity-mode force discharge now prefers `discharge_battery`, so export actions target battery discharge power directly instead of relying on meter export control. Older GoodWe HA setups that do not expose the newer EMS modes still fall back to the previous `buy_power` and `sell_power` behaviour.

Update available via HACS
