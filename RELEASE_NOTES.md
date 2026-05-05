<!-- release: v2.12.296 -->

## What's Changed

**Tesla self-consumption is re-applied after restart drift**
When the optimizer plan is `self_consumption`, PowerSync now verifies the live Tesla operation mode before skipping a repeated command. If the Powerwall is still in `autonomous` after a Home Assistant restart or Tesla mode drift, the optimizer re-applies self-consumption instead of leaving Tesla's TOU logic to keep exporting.

Update available via HACS
