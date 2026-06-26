<!-- release: v2.12.723 -->

## What's Changed

**Restore safe Tesla force discharge pricing**
Force discharge now sets both the import and export rates to $99/kWh during the forced discharge window. This restores the previous behavior that discourages Powerwall firmware from treating the force window as a cheap grid-import opportunity while still advertising a high export price.

Update available via HACS
