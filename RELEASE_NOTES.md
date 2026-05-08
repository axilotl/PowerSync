<!-- release: v2.12.343 -->

## What's Changed

**Dashboard dependency detection guard**
PowerSync now has regression coverage for the startup race where the dashboard checks HACS frontend resources before `button-card` has registered as a custom element. This protects the existing dashed URL fallback for `/hacsfiles/button-card/button-card.js`, so future dashboard updates do not reintroduce false "button-card not detected" warnings for correctly installed HACS users.

Update available via HACS
