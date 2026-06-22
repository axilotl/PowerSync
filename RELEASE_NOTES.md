<!-- release: v2.12.686 -->

## What's Changed

**Tesla force-charge retry fix**
PowerSync now keeps Tesla force-charge and force-discharge operation-mode retries running when the Tesla API returns a rate-limit or temporary server error. Previously, that retry branch could fail with `name '_parse_retry_after' is not defined`, leaving the force operation incomplete instead of retrying the Tesla request.

Update available via HACS
