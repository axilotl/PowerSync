<!-- release: v2.12.626 -->

## What's Changed

**Sigenergy force discharge now writes the discharge command limit**
PowerSync now explicitly sends the Sigenergy ESS max discharge command used by Remote EMS discharge modes before applying the active power target and grid export ceiling. This fixes force discharge sessions that entered DISCHARGE_ESS mode successfully but only covered household load instead of exporting.

Update available via HACS
