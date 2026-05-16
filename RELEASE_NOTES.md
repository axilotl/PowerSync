<!-- release: v2.12.415 -->

## What's Changed

**FoxESS Cloud API signature fix**
PowerSync now signs FoxESS Cloud Open API requests with the literal `\r\n` separator that FoxESS expects. This fixes `40256 illegal signature` failures for FoxESS Cloud API keys from Personal Center > API Management, including device discovery, live data reads, scheduler sync, and cloud control calls.

**Regression coverage for FoxESS auth**
Added a focused test that locks the FoxESS signature format to the proven literal separator, so future cleanup does not accidentally revert the signer back to real CRLF bytes.

Update available via HACS
