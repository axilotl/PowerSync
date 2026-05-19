<!-- release: v2.12.434 -->

## What's Changed

**Use GoodWe EMS entities for TCP / LAN Kit-20 control**
PowerSync now automatically routes GoodWe TCP / LAN Kit-20 force charge and discharge commands through the detected GoodWe Experimental EMS entities, even if the existing configuration was left on Direct IP control. This avoids the GoodWe TCP path that can read telemetry but does not reliably command the inverter.

**Clarify GoodWe control setup**
The GoodWe setup text and wiki now make the control split explicit: Direct IP requires UDP 8899, while TCP / LAN Kit-20 systems should use the EMS entity pair exposed by the Home Assistant GoodWe integration.

Update available via HACS
