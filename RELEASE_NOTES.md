<!-- release: v2.12.425 -->

## What's Changed

**Fixed Tesla force export staying in Self Powered**
Tesla Powerwall force charge and force discharge now always re-issue TOU/autonomous mode before uploading the temporary force tariff. This prevents cases where the force tariff is written successfully but a Powerwall 3 remains in Self Powered mode and does not export until TOU is selected manually in the Tesla app.

**Fixed saved tariff price calculation errors**
PowerSync now calculates the active TOU period before reading buy and sell rates from a saved Tesla tariff. This fixes the `current_period` error that could spam Home Assistant logs while a force tariff was active and PowerSync was falling back to the saved real tariff for pricing.

Update available via HACS
