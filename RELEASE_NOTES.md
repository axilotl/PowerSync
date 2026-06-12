<!-- release: v2.12.628 -->

## What's Changed

**Flow Power KWatch API validation**
PowerSync now validates Flow Power KWatch API keys with the same 60-minute dispatch window used by the live price fetch. This fixes valid API keys being rejected when KWatch returned no 5-minute dispatch records for the shorter validation request.

**Flow Power timestamp parsing**
KWatch `dispatch5mins` responses that return nested JSON strings with `Key`/`Value` records now keep the timestamp from `Key` instead of falling back to inferred times.

Update available via HACS
