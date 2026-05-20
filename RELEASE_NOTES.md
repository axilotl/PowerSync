<!-- release: v2.12.446 -->

## What's Changed

**Smart Optimization LP solver timeout raised**
Extends the built-in HiGHS LP solver time limit for full 48-hour, 5-minute optimization plans. Larger sites could hit the previous 10-second cap and fall back to the greedy scheduler even though the LP would solve successfully a few seconds later, reducing forecast quality and apparent savings. The optimizer now gives these larger plans more time while preserving the existing greedy fallback if the solver still cannot finish.

Update available via HACS
