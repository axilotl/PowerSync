<!-- release: v2.12.709 -->

## What's Changed

**Prevent Tesla force charge from curtailing live solar**
PowerSync now blocks optimizer-triggered Tesla force charge while meaningful live solar production is present. Tesla force charging is implemented through a TOU handoff and cannot reliably target a partial charge rate, so on AC-coupled systems it can cause the Powerwall to import at full charge power while solar output drops to zero. The optimizer now yields to self-consumption during those daytime conditions instead of extending or starting the force-charge window.

Update available via HACS
