<!-- release: v2.12.526 -->

## What's Changed

**FoxESS H3 Smart DC curtailment now verifies the inverter accepted the command**
PowerSync now routes direct FoxESS Modbus curtailment through the same verified remote-control path used by force modes. This gives H3 Smart systems the required enable delay and readback checks instead of reporting curtailment as successful after an unverified register write.

**FoxESS curtailment is kept active through long negative feed-in periods**
While export earnings remain below the curtailment threshold, PowerSync now re-applies the FoxESS remote-control command before the inverter's remote timeout expires. This prevents curtailment from silently lapsing during extended negative-price windows.

Update available via HACS
