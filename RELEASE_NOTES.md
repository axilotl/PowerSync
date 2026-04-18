## What's Changed

**Tesla Fleet API token no longer causes false reauth after ~12 hours**
When PowerSync is configured to use the Tesla Fleet HA integration as its token source, a brief window during the Fleet integration's own OAuth refresh cycle could cause PowerSync's token getter to return nothing. Previously this silently fell back to the access token from when HA last started — which expires after several hours and triggered a full reauth flow, breaking the power flow display in the mobile app until credentials were re-entered. PowerSync now skips the affected poll cycle and retries on the next interval instead of using a stale credential.

*Update available via HACS*
