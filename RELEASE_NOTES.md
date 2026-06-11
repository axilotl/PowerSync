<!-- release: v2.12.620 -->

## What's Changed

**Flow Power KWatch forecasts keep their time slots**
Flow Power KWatch pricing now preserves forecast interval timing before the prices reach the dashboard, Smart Optimization, tariff sync, or any battery-specific control path. This fixes KWatch forecasts collapsing into one slot, which could make price charts look flat or mostly empty and cause optimizer plans to fall back to simple self-consumption behavior.

**KWatch response parsing handles more API shapes**
PowerSync now accepts KWatch price fields with uppercase or underscore-separated names and can safely infer sequential interval times if a response omits explicit timestamps. This makes the Flow Power API pricing path more resilient for all supported battery systems using KWatch as the price source.

Update available via HACS
