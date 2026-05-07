<!-- release: v2.12.328 -->

## What's Changed

**Clear Tesla grid-mode controls**
Tesla Powerwall local control now exposes separate On-Grid and Off-Grid switches in Home Assistant instead of relying on the Off-Grid switch being off to mean reconnected. The two switches are mutually exclusive and the dashboard shows both modes, making it obvious how to reconnect after intentionally islanding the system.

**Stable off-grid transition feedback**
When a Powerwall off-grid or reconnect command is accepted, PowerSync now keeps the requested grid mode visible while the gateway transitions, so the switch no longer appears to bounce back immediately before fresh gateway state arrives.

Update available via HACS
