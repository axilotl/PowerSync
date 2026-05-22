<!-- release: v2.12.458 -->

## What's Changed

**Flow Power optimizer now uses v2 PEA pricing**
Smart Optimization now values Flow Power import prices with the current v2 Price Efficiency Adjustment formula, matching the tariff and price sensor surfaces. The optimizer now factors GST-adjusted spot price, network tariff, GST-adjusted TWAP, average daily tariff, and BPEA into its charge and discharge decisions instead of relying on the legacy v1 PEA calculation.

**Flow Power TWAP override applied consistently**
The optimizer now honors the Flow Power TWAP override before falling back to the dynamic TWAP tracker, so manual pricing overrides, displayed prices, generated tariffs, and LP decisions stay aligned.

Update available via HACS
