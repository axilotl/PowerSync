<!-- release: v2.12.677 -->

## What's Changed

**GoodWe force export releases zero-export curtailment**
GoodWe systems now avoid restoring a saved 0W export limit when PowerSync is about to force discharge for an export opportunity. This prevents negative-price curtailment state from blocking Happy Hour or optimizer-driven export commands on systems where the saved GoodWe export limiter state was itself zero export.

Update available via HACS
