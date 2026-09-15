# ML016 / PS021 robustness interpretation gate

This gate is fixed before ML016 effect sizes are recovered.

## Existing non-Serapias diagnostic

Using the currently canonical cluster-level p-values for ML002, ML003 and ML014, omission of ML001 Serapias gives Fisher `p = 0.07777` and therefore does not reject primary binary-layer exchangeability.

## Fifth-cluster interpretation

If ML016 passes the independently locked admission contract, add its cluster-level state-separation p-value to the same Fisher combination and recompute all leave-one-primary-cluster-out diagnostics.

The key confirmatory question is binary and prospective:

> Does the primary rejection survive omission of ML001 after adding one independent same-effect-family cluster?

Do not rank candidate fifth clusters by the p-value they would contribute and do not reopen a failed candidate merely because another candidate would make the Fisher p-value smaller.

For transparency only, with ML002/ML003/ML014 held fixed, a new cluster-level p-value of approximately 0.126 would place the four-cluster `omit ML001` Fisher combination at the conventional 0.05 boundary. This numerical boundary is **not an eligibility rule** and must not be used for candidate or endpoint selection.

If ML016 is admissible but the omit-ML001 combination remains >=0.05, record that as failure of leave-Serapias-out robustness. If ML016 is inadmissible, do not calculate a hypothetical contribution from lower-level or mismatched effects.
