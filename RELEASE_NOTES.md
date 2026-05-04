<!-- release: v2.12.284 -->

## What's Changed

**Fix PowerSync sensor startup on Home Assistant**
This release fixes a startup crash in the PowerSync sensor platform caused by legacy Powerwall pack registry identifiers with an unexpected shape. When the cleanup step failed, Home Assistant aborted the whole sensor platform, leaving live energy, price, battery, daily energy, EV, firmware, and TOU schedule sensors unavailable even though the underlying coordinators were still fetching data.

**Keep legacy cleanup from taking sensors down**
Powerwall pack registry cleanup now tolerates older identifier formats and is isolated so cleanup failures cannot prevent the core PowerSync sensors from registering during Home Assistant startup.

Update available via HACS
