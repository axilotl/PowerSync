<!-- release: v2.12.362 -->

## What's Changed

**Safari energy-flow flicker fix**
The built-in energy-flow house scene now keeps its background image outside the animated SVG layer and preloads scene changes before applying them. This avoids Safari/WebKit repaint flicker during live Home Assistant state updates while preserving the existing animated flow paths and dynamic scene switching.

**Frontend regression coverage**
Added focused coverage for the Safari-safe rendering path and a local stress harness for rapid dashboard updates and background swaps, so future changes are less likely to reintroduce the same flicker.

Update available via HACS
