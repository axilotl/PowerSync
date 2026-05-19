<!-- release: v2.12.435 -->

## What's Changed

**Stabilized Sungrow Modbus control**
Sungrow SH systems now serialize Modbus polling and control commands through the coordinator, preventing normal refreshes from overlapping force charge, force discharge, IDLE, backup reserve, and export-limit writes. This avoids WiNet/Modbus connection churn where the inverter could briefly stop responding during optimizer control transitions.

**Added native Sungrow export curtailment**
Solar curtailment on Sungrow battery systems now uses the Sungrow export-limit path instead of falling through to the Tesla API path. PowerSync can apply a load-following export limit when feed-in pricing is unattractive, restore the limit when export is allowed again, and keep the configured Sungrow AC inverter path active.

**Improved Sungrow inverter configuration**
Sungrow AC inverter configuration now supports both SG string inverters and SH hybrid models, including same-endpoint SH configurations used for export-limit curtailment. Saving the inverter config enables runtime polling/curtailment, and the conflict check only blocks true duplicate SG/string inverter endpoints.

Update available via HACS
