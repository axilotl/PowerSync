<!-- release: v2.12.492 -->

## What's Changed

**PowerSync pricing sensors avoid `unknown` during Home Assistant startup**
Pricing and daily cost sensors now restore their last valid numeric state while Home Assistant and the PowerSync coordinators are still warming up. This prevents startup template errors in dashboards that read sensors such as current import price, daily import cost, export earnings, and month-to-date average cost per kWh.

Update available via HACS
