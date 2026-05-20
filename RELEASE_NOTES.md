<!-- release: v2.12.442 -->

## What's Changed

**Smart Schedule solar starts honor the visible battery floor**
Smart Schedule solar-surplus windows now use the Smart Schedule "Min Battery to Start" value shown in the app instead of falling back to the separate Solar Surplus default. This fixes cases where the app showed a lower start floor, such as 45%, but the backend log still blocked charging until the battery reached 80%.

Update available via HACS
