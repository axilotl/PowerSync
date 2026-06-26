<!-- release: v2.12.721 -->

## What's Changed

**Fix Tesla force discharge/export dispatch**
Tesla force discharge now uploads a tariff with a real export incentive instead of setting the temporary buy and sell prices to the same high value. This fixes a case where Powerwall systems could accept the force discharge command but remain idle, leaving the house supplied from the grid instead of exporting from the battery.

Update available via HACS
