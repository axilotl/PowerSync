<!-- release: v2.12.733 -->

## What's Changed

**Fix FoxESS force discharge being cancelled by curtailment restore**
PowerSync now keeps FoxESS remote-control ownership with an active force charge or force discharge command instead of letting the solar curtailment restore path disable remote control during the session. This prevents scheduled FoxESS export windows from starting correctly and then dropping back to idle when a stale curtailment marker is restored a minute later.

Update available via HACS
