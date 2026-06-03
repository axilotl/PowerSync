<!-- release: v2.12.546 -->

## What's Changed

**Profit Max home-load protection**
Profit Max can still lower the optimiser reserve when Auto-Apply decides the forecast allows it, but forced export now keeps a separate home-load bridge floor. This leaves enough battery to cover forecast household load until the next charge period or solar surplus instead of selling that energy first.

**Clearer optimizer power charts**
The Smart Optimization chart now compresses the power axis on the Home Assistant dashboard so large charge and export windows no longer flatten normal home load. This makes household consumption, battery charge, export, and EV activity easier to compare in the same graph.

Update available via HACS
