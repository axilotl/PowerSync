<!-- release: v2.12.522 -->

## What's Changed

**GoodWe export-limit restore no longer trips the inverter library encoder**
PowerSync now keeps GoodWe export-limit writes inside the register range accepted by the GoodWe library. Restoring normal export after curtailment uses the inverter's maximum unsigned 16-bit limit instead of an out-of-range value, avoiding repeated `GoodWe restore() failed: int too big to convert` log errors.

**Dashboard history charts now preserve state changes instead of drawing artificial slopes**
PowerSync history charts now render recorder state history as held-state steps by default and prefer `last_updated` timestamps for fallback points. This avoids perfect diagonal lines across sparse Home Assistant history samples, especially on the 24-hour energy chart when grid or price values jump between tariff periods.

Update available via HACS
