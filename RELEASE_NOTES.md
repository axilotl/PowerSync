<!-- release: v2.12.724 -->

## What's Changed

**Apply Tesla force discharge reserve last**
Tesla force discharge now uploads the force-discharge tariff before writing the backup reserve, then writes the reserve as the final apply step. If the reserve was already at 0%, PowerSync briefly nudges it before returning it to 0% so Tesla receives a real state change after the tariff update.

Update available via HACS
