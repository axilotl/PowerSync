<!-- release: v2.12.336 -->

## What's Changed

**Fix FoxESS optimizer force charge commands**
FoxESS systems no longer fail optimizer-issued force charge commands with a `min_timeout_seconds` error. This restores the Flow Power pre-export charging path where the optimizer plans a full battery target before a profitable export window and then needs to keep extending the hardware charge command until the window arrives.

**Fix FoxESS manual force charge fallback**
Manual FoxESS force charge calls now use the same timeout plumbing, so the mobile app and Home Assistant force charge controls no longer trip over the missing timeout argument when PowerSync calculates the inverter's charge power from the configured FoxESS current limit.

Update available via HACS
