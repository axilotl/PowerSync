## What's Changed

**Pair the Powerwall gateway from inside HA — no app required**
Two new buttons under the Battery device's Configuration section: **Pair Powerwall Gateway** kicks off the same RSA key registration flow the PowerSync mobile app uses, and **Unpair Powerwall Gateway** clears the stored key and reverts commands to cloud. When you press Pair, a persistent notification walks you through the DC isolator toggle: "Toggle OFF, wait 10s, then ON" with the remaining window in seconds, and updates again on success/timeout/failure. Closes the gap for users who never installed the app or want to re-pair without leaving HA.

Update available via HACS
