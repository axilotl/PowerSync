## What's Changed

**Battery Health: Fleet API Fetch Now Always Live**
The Battery Health endpoint was skipping the Fleet API entirely whenever old WiFi-scan data existed in storage — meaning paired systems never saw updated BMS data unless the old scan was manually cleared. The endpoint now always queries Tesla's Fleet API directly for Powerwall systems (with a 1-hour cache to avoid hammering the API), ignoring any stale stored data. Pull-to-refresh in the app forces a fresh fetch. The "Last Updated" timestamp now reflects when the data was actually retrieved from Tesla.

**Powerwall Pairing: Gateway IP No Longer Required**
The pairing handshake is entirely cloud-based — Tesla's Fleet API handles key registration and the physical toggle confirms presence. The `pair/start` endpoint previously rejected requests missing a gateway IP, which was wrong. It now accepts pairing requests without one, and preserves any IP already configured in Gateway Connection rather than clearing it.

Update available via HACS
