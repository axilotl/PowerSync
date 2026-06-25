<!-- release: v2.12.713 -->

## What's Changed

**FoxESS KH grid import sign correction**
PowerSync now normalizes FoxESS KH direct Modbus grid power so forced grid charging is treated as grid import instead of export. This fixes KH/K-series installs where the inverter reports grid import as a negative register value during Backup/force-charge mode, which could show the grid flow in the wrong direction and inflate daily export totals while the battery is actually charging from the grid.

Update available via HACS
