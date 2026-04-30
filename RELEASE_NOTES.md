## What's Changed

**Powerwall local snapshot now uses RSA-signed direct LAN reads**
The integration no longer logs into the gateway's Bearer REST API for live polling. Snapshots — battery percentage, meter readings (solar/battery/grid/load), grid status, operation mode, backup reserve, alerts, per-pack data — are now fetched via a single RSA-signed `DeviceControllerQuery` to `/tedapi/v1r` plus a `config.json` read, both signed with the RSA key established during pairing. This eliminates the customer-password requirement entirely, removes the 401-spam failure mode when credentials drift, and parallelises into a single round-trip instead of the previous login + four sequential REST calls. PW2 and PW3 follow the same RSA-signed code path.

**Customer password removed from setup**
The "Powerwall customer password" field has been removed from initial setup, options, and the mobile-app gateway endpoint. The integration uses RSA signing exclusively for both snapshot reads and control commands, so no password is ever needed. Existing config entries with a stored password are unaffected — the value is simply ignored. Older app builds that still send `customer_password` to `/api/power_sync/powerwall/set_gateway_ip` continue to work; the field is silently dropped.

**Legacy unsigned PW2 client retired**
Removed the `_UnsignedRESTClient` fallback path that some early PW2 installs used before RSA pairing was supported on PW2 firmware. Both generations now require completed cloud pairing (RSA private key + DIN in entry data); the integration refuses to construct a local client without them. Any install that hadn't completed pairing was already getting Bearer 401 spam and broken snapshots — re-pair from the integration options to restore local features.

Update available via HACS
