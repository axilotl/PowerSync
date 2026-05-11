<!-- release: v2.12.378 -->

## What's Changed

**FoxESS H3-Pro and H3-Smart minimum SOC writes use the writable register**
PowerSync now writes the FoxESS minimum SOC setting to register `46611` for H3-Pro and H3-Smart systems instead of the read-only backup cut-off register `46609`. This restores the min SOC control path on affected FoxESS firmware while leaving the existing H1, H3, and KH register maps unchanged.

Update available via HACS
