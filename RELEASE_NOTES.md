<!-- release: v2.12.585 -->

## What's Changed

**Solar curtailment now runs independently of monitor-only mode**
Monitor-only mode still blocks Smart Optimization battery commands, but it no longer prevents the separate solar curtailment path from applying inverter export limits. GoodWe, Sungrow, and other curtailment handlers can now continue protecting against low-value export while the optimiser remains observation-only.

Update available via HACS
