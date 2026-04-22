## What's Changed

**Solax: fix manual mode entity mapping**
PowerSync now uses the upstream `manual_mode_select` entity names exposed by `wills106/homeassistant-solax-modbus`, with optional support for `manual_mode_control` where that entity exists. This fixes Solax setups that were failing because PowerSync was looking for a non-existent `manual_mode` entity and the wrong stop label.

**Flow Power: fix current price sensor wiring**
Flow Power retail prices are now published under the standard `Current Import Price` and `Current Export Price` sensors used by the mobile app and default dashboard. This fixes cases where backend pricing and cost tracking were correct internally, but the UI still showed near-zero current rates from the generic tariff path.

Update available via HACS
