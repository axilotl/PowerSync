<!-- release: v2.12.521 -->

## What's Changed

**Powerwall pairing now falls back cleanly when local LAN access is blocked**
PowerSync can now complete the Powerwall RSA pairing flow through Tesla/Fleet even when Home Assistant cannot reach the gateway directly on the local network, such as HA running inside a Proxmox VM or across a multicast/VLAN boundary. The app status endpoints now report whether the system is cloud-paired, local-only features are available, pending, unavailable, or need repair, so users are not left stuck at the gateway step when cloud pairing succeeded.

**Local gateway polling no longer treats cloud-only placeholders as real gateways**
Cloud-only paired installs now skip loopback gateway polling and avoid reporting stale local snapshots as currently available. Battery health and BMS reads also skip placeholder gateway hosts and fall back to the Fleet relay path, reducing noisy local gateway failures while still preserving direct LAN reads when a real gateway IP is configured.

Update available via HACS
