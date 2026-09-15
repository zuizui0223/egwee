# Primary state-separation synthesis after ML020 admission

**Date:** 2026-09-15

## Primary denominator

Five independent primary programme/study clusters remain in the direct `hedges_g_direct` family:

1. ML001 *Serapias lingua*;
2. ML002 *Brosimum alicastrum*;
3. ML003 *Spondias purpurea*;
4. ML014 *Eucalyptus socialis*;
5. ML020 Aizen–Feinsinger replicated Chaco programme (*Atamisquea emarginata*, *Cercidium australe*, *Prosopis nigra* as dependent species subsystems).

ML020 contributes one independent cluster, never three.

## Cluster-level p-values

- ML001: `0.00354530`;
- ML002: `0.19911670`;
- ML003: `0.17406774`;
- ML014: `0.09831774`;
- ML020: `1.00000000`.

ML020's p-value is the internally Bonferroni-adjusted minimum of three species-specific covariance-aware I-F contrasts. Its high p-value is retained exactly; admission did not depend on significance.

## Full synthesis

Fisher combination of the five independent cluster p-values:

- statistic = `22.647716471332092`;
- df = `10`;
- p = `0.012124324105113144`;
- decision = `reject_primary_binary_layer_exchangeability` at alpha 0.05.

The statistic is numerically unchanged from the prior four-cluster corpus because `-2 log(1)=0`; the degrees of freedom increase from 8 to 10, so the combined p-value becomes less extreme.

## Leave-one-primary-cluster-out

- omit ML001: p = `0.18194352880824005` — **do not reject**;
- omit ML002: p = `0.012767937397516447` — reject;
- omit ML003: p = `0.014072144220032149` — reject;
- omit ML014: p = `0.0211619920139365` — reject;
- omit ML020: p = `0.0038472411522688897` — reject (the previous four-cluster canonical result).

## Robustness conclusion

The requested fifth same-effect-family independent-system check does **not** remove the Serapias dependency. After adding ML020, omission of ML001 changes the combined p-value from the previous `0.07777` to `0.18194`.

Therefore the scientifically correct conclusion is now stronger in a different sense:

> The current cross-system corpus rejects response-layer exchangeability overall, but that rejection is not robust to removal of the Serapias cluster, even after adding a fifth independently structured direct fragmentation programme.

This is an informative negative robustness result, not a reason to exclude ML020. A sixth-cluster search must not be triggered merely to recover significance.