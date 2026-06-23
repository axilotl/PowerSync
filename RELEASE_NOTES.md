<!-- release: v2.12.693 -->

## What's Changed

**Fixed GoodWe setup after Smart Optimization options**
Initial setup could fail with an unexpected error after entering GoodWe connection settings because the Smart Optimization setup step wrote Charge by Time compatibility values to an undefined local variable. The setup flow now stores those values on the integration options being built, allowing fresh GoodWe + Amber installs to continue normally.

Update available via HACS
