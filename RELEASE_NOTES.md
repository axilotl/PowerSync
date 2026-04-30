## What's Changed

**Fix: Off-grid / Reconnect now work after pairing without a local gateway IP**
Users who completed Powerwall pairing through the mobile app but never set the gateway's local IP would get a "Powerwall local client unavailable" error when running the `powerwall_go_off_grid` or `powerwall_reconnect_grid` services, despite their entry showing as paired. The cause was a bail-early guard in the client builder: it required a local IP even though both off-grid actions actually run through Fleet API `device_command` with a signed routable_message — a path that needs the paired RSA key, gateway DIN, Fleet API token, and energy site ID, but no LAN host at all. The builder now constructs a cloud-only client (with a 127.0.0.1 placeholder host) when no IP is configured, as long as the paired key and DIN are present. Off-grid and reconnect work immediately; LAN-only features fail fast with a clear log line so users know to set the gateway IP if they want them.

**Local-only features still need the gateway IP**
For clarity: the local fast snapshot poll (per-Powerwall sensors, system island state, alerts) and the local-write paths (backup-mode curtailment, operation-mode override, grid-charging toggle) are genuine LAN calls and still require `CONF_POWERWALL_LOCAL_IP`. Set the IP via the mobile app's Battery Setup → Gateway Connection screen if you want those features. The integration logs an informational line at startup when paired-without-IP so the state is visible.

**Docstring correction on go_off_grid**
The docstring claimed local TEDAPI v1r was the primary path with cloud as a fallback. The implementation has been cloud-only for some time — local TEDAPI returns success for the same setIslandModeRequest but doesn't actually operate the contactor (verified empirically on both PW2 and PW3). The docstring now accurately describes the cloud-signed `device_command` flow that the code has always been using.

Update available via HACS
