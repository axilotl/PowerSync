<!-- release: v2.12.678 -->

## What's Changed

**Flow Power API site lookup compatibility**
PowerSync now sends the empty JSON body expected by Flow Power's `GetResidentialSites` endpoint when validating a KWatch API key and loading linked residential sites. This avoids the Flow Power API rejecting the site lookup when the endpoint is called without a body, while keeping the existing site, tariff, and price normalization behaviour unchanged.

Update available via HACS
