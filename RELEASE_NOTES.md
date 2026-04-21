## What's Changed

**Amber Multi-Site Selection**
Users with multiple Amber NMIs/sites can now select which site PowerSync uses during initial setup. Previously, the config flow auto-selected the first active site without asking — meaning users with a closed old site and an active new site (or genuinely multiple properties) had no way to choose the correct one. A site picker step now appears when multiple sites are found on the account; single-site accounts are still auto-selected silently. Tesla + Amber users were already handled correctly via the combined site selection step.

Update available via HACS
