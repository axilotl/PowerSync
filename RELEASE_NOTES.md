<!-- release: v2.12.552 -->

## What's Changed

**FoxESS curtailment now survives optimizer self-consumption handoffs**
PowerSync now keeps an active FoxESS curtailment command in place when the optimizer moves through self-consumption, instead of clearing the inverter's remote-control state and leaving the curtailment cache stale. This improves H3 Smart zero-export behavior when export earnings stay below the curtailment threshold.

**FoxESS curtailment is re-applied when live export proves it is not holding**
If PowerSync believes a FoxESS inverter is curtailed but live grid telemetry still shows sustained export, it now reissues the curtailment command immediately rather than waiting for the normal remote-control timeout window. Manual restores also clear the FoxESS curtailment cache so future checks start from the real inverter state.

Update available via HACS
