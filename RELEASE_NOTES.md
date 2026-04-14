## What's Changed

**Enphase DPEL: send relay_config default for gateways with relay controls**
2.12.39 fixed `installed_capacity` and the read-modify-write merge, but uncovered yet another required field: `relay_config`. Envoy firmware on gateways that have ANY relay control configured in Enlighten Manager (even if the relays are physically inert) demands a `relay_config` value on every DPEL POST — but the matching GET `/ivp/ss/dpel` doesn't return it, so we couldn't echo it back from the base settings. Result: every DPEL write was rejected 400 "missing/incorrect relay_config" and curtailment fell through to the no-op fallback.

PowerSync now sends `relay_config: false` (a "no active relay" sentinel) by default in every DPEL payload. Gateways without relay configuration ignore it. Gateways with relay configuration should accept the disabled value since the relays in question are typically just storage/backup transfer relays not used for production limiting. If your gateway still rejects it, you can disable the relay controls in Enlighten Manager as a workaround.

This is the third in a sequence of fixes triaged from real installs over the past day — Enphase's API requires more "echo-back" of fields than the documented DPEL surface suggests.

Update available via HACS
