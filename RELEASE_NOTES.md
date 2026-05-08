<!-- release: v2.12.330 -->

## What's Changed

**NeoVolt independent-stack solar balancing**
PowerSync now coordinates multi-host Neovolt / Bytewatt systems that do not have parallel/BMS coordination. When one stack is parked in `No Battery Charge` or `Idle (No Dispatch)`, PowerSync can use measured export headroom to briefly force-charge that spare stack from otherwise-exported solar, then restore its previous anti-fighting mode when surplus disappears.

**Battery-to-battery charge protection**
The NeoVolt balancer will not start if another stack is discharging, and it stops immediately if that happens while balancing. This prevents one battery from being drained to charge the other while still allowing surplus solar to top up the idle stack.

Update available via HACS
