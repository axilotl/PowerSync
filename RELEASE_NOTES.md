<!-- release: v2.12.489 -->

## What's Changed

**Tesla tariff restores now wait for readback**
PowerSync now confirms Tesla has actually exposed the uploaded TOU tariff in `site_info` before treating a tariff sync or restore as successful. This reduces the chance of a short stale-tariff window after force discharge where the Gateway can briefly behave against the wrong price schedule.

**Powerwall handoff stays in self-consumption**
Optimizer-owned Tesla restores now keep the Powerwall in self-consumption and leave grid charging unchanged while the restored tariff is handed back. Grid charging is only explicitly re-enabled when the next optimizer action is force charge, avoiding unexpected imports immediately after an export window ends.

Update available via HACS
