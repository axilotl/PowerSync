## What's Changed

**GoodWe EMS Mode: Force Charge/Discharge Now Uses Rated Power by Default**
When force charge or force discharge was triggered from the dashboard or mobile app (no specific watt target), the EMS power limit register was left unchanged — meaning the inverter might discharge at 0W or whatever it was last set to. The integration now defaults to the inverter's rated power when no specific target is given, matching the same behaviour as the direct UDP control path.

Update available via HACS
