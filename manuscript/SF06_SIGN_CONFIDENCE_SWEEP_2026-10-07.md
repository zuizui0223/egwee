# SF06 marginal sign-confidence sweep — 2026-10-07

## Status

Post-exposure uncertainty robustness audit. The primary external topology remains the pre-exposure constituent-sign point-estimate rule. This sweep does not replace it.

## Question

The corrected external many-to-many topology is based on point signs, while only three pairs have both two-sided 95% marginal intervals excluding zero.

Rather than compare only those two extremes, we retain pairs whose two endpoints each support their estimated sign with at least a chosen marginal normal-approximation probability q.

For an endpoint with estimate d and standard error SE, sign confidence is Phi(|d|/SE).

## Full habitat-fragmentation subset

| minimum marginal sign confidence q | retained pairs | I−F− | I−F+ | I+F− | I+F+ | minimum mismatches |
|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 55 | 36 | 9 | 7 | 3 | 12 |
| 0.60 | 37 | 27 | 3 | 4 | 3 | 6 |
| 0.70 | 30 | 24 | 2 | 2 | 2 | 4 |
| 0.80 | 18 | 15 | 1 | 1 | 1 | 2 |
| 0.90 | 10 | 9 | 1 | 0 | 0 | 1 |
| **0.95** | **6** | **5** | **1** | 0 | 0 | **1** |
| 0.975 | 4 | 4 | 0 | 0 | 0 | 0 |

Thus one many-to-many mismatch remains even when both endpoint signs have at least 95% marginal support.

At q=0.975, approximately corresponding to requiring each endpoint's two-sided 95% interval to exclude zero under the normal approximation, only four pairs remain and the mismatch disappears. This agrees with the stricter resolved-sign sensitivity.

## Source-publication-disjoint subset

| q | retained pairs | I−F− | I−F+ | I+F− | I+F+ | minimum mismatches |
|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 32 | 21 | 6 | 4 | 1 | 7 |
| 0.60 | 21 | 15 | 3 | 2 | 1 | 4 |
| 0.70 | 16 | 12 | 2 | 1 | 1 | 3 |
| 0.80 | 12 | 10 | 1 | 0 | 1 | 1 |
| 0.90 | 7 | 6 | 1 | 0 | 0 | 1 |
| **0.95** | **6** | **5** | **1** | 0 | 0 | **1** |
| 0.975 | 4 | 4 | 0 | 0 | 0 | 0 |

The high-confidence mismatch therefore does not depend on a publication already present in the frozen EGWEE map.

## Interpretation

This produces a useful uncertainty boundary.

The external many-to-many result is stronger than a raw sign census of completely unresolved effects: discordance persists after increasingly stringent marginal sign-confidence filtering, including q=0.95.

But the evidence is not strong enough to claim a population of individually two-sided-95%-resolved sign reversals. At the q≈0.975 boundary, the retained set becomes small and concordant.

The appropriate hierarchy is therefore:

1. robust point-estimate topology with publication/species/source-disjoint persistence;
2. one high marginal-sign-confidence mismatch surviving to q=0.95;
3. no externally generalized mismatch among the very small set with both two-sided 95% signs resolved.

## Claim ceiling

Allowed:

- external non-identifiability is not solely driven by completely uncertain endpoint signs;
- one source-disjoint mismatch persists when both endpoint signs have at least 95% marginal directional support.

Not allowed:

- q=0.95 is equivalent to a two-sided 95% confidence interval excluding zero;
- the sweep is preregistered;
- the single high-confidence mismatch establishes prevalence;
- the external source contains multiple individually two-sided-95%-resolved reversals.
