<!-- release: v2.12.687 -->

## What's Changed

**Fix Smart Optimization infeasible solves with capped solar export**
Smart Optimization now models solar curtailment inside the LP solver. This prevents false `LP solver status: Infeasible` fallbacks when forecast solar exceeds household load, battery charging is intentionally blocked for an export window, and the site has a grid export cap. PowerSync can now keep producing an optimized schedule instead of falling back to self-consumption hold in those capped-surplus cases.

Update available via HACS
