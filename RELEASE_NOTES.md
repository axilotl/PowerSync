## What's Changed

**GoodWe: Battery Power Direction Fixed (Discharging Now Shows as Discharging)**
The battery power sensor was reporting the wrong sign — when the battery was discharging to cover home load, the dashboard showed it as charging and vice versa. The GoodWe library's `pbattery1` field uses positive=discharge (not positive=charge as previously assumed), so the negation that was applied has been removed.

Update available via HACS
