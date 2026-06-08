<!-- release: v2.12.608 -->

## What's Changed

**Dashboard chart stability**
Generic PowerSync dashboard charts now skip redraws when Home Assistant sends unrelated state updates. This keeps active graph tooltips and legend show/hide selections steady while still refreshing when the chart's own data, configuration, hidden-series state, size, or scheduled time bucket changes.

Update available via HACS
