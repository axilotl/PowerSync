## What's Changed

**Generic EV Charger: Better diagnostics for misconfigured switch entity**
Instead of a cryptic HA validation error when the configured switch entity is missing or malformed, PowerSync now checks upfront: the entity_id must contain a domain (e.g. `switch.charger_charge`), and the entity must exist in Home Assistant. The exact configured value is now logged at DEBUG level on every start attempt to make misconfiguration easy to spot.

Update available via HACS
