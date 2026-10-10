# SF06 probabilistic information versus binary sentinel accuracy — 2026-10-08

## Status and purpose

Post-exposure exploratory diagnostic, **not a preregistered endpoint**. Uses only the corrected, source-hash-gated public Supplementary Table S1 pair CSV. This is a stricter 54-pair constituent-consensus sensitivity to the existing 55-pair IVW-sign probability audit (SF06_LOPO_SIGN_PROBABILITY_VALUE_2026-10-07.md), **not an independent replication**. A one-pair difference is expected because the main topology excludes a mixed-consensus pair. Its purpose is to distinguish "no improvement in a 0/1 decision at one threshold" from the stronger and unjustified assertion "pollination sign contains no information".

## What the full 54-pair table actually says

The constituent-consensus habitat-fragmentation sign table contains:

| Pollination sign | Female fitness lower | Female fitness nonlower |
|---|---:|---:|
| lower | 35 | 9 |
| nonlower | 7 | 3 |

The prevalence-like fraction in **this selected literature subset**, not in nature, is 42/54 = 77.8% with F lower. The observed conditional fractions are:

- F lower given I lower: 35/44 = 79.5%;
- F lower given I nonlower: 7/10 = 70.0%.

The most accurate majority-class decision under either I state is therefore F lower. A deterministic sign lookup yields the same 12 errors as an all-F-lower baseline. **Zero classification gain is partly a threshold/class-imbalance fact; it does not imply zero conditional information.**

Using plug-in observed frequencies, the in-sample mutual information between the two sign states is **0.00543 bits per pair**, small but positive (0.00377 nats). The in-sample binary Brier score changes from 0.17284 for the unconditional baseline to 0.17146 using the conditional sign frequencies, a modest improvement.

This is a **plug-in sample estimate**, which is positively biased in sparse categorical tables even under true independence; it is not evidence of nonzero population mutual information. Its role is only to show that a zero change in 0/1 accuracy is not mathematically equivalent to identical conditional probabilities.

## Out-of-publication probability test

For each source publication in turn, exclude **all its pairs**, fit probabilities from the remaining pairs, and predict the omitted publication.

Baseline:
P(F lower) = (training F-lower count + alpha) / (training count + 2 alpha)

Pollination-sign model:
P(F lower | I sign) = (training sign-group F-lower count + alpha) / (training sign-group count + 2 alpha)

We report alpha=0.5 (Jeffreys smoothing), as well as sensitivity to alpha=1, 2, 4. Both models use the same smoothing. Neither model sees a held-out outcome. Lower Brier and log loss are better.

| Held-out set, alpha=0.5 | Brier without I | Brier with I sign | Log loss without I | Log loss with I sign |
|---|---:|---:|---:|---:|
| Full public-S1: 54 pairs, 32 publications | 0.17659 | 0.18118 | 0.54056 | 0.55121 |
| EGWEE-source-disjoint: 31 pairs, 23 publications | 0.18310 | 0.19462 | 0.55788 | 0.59589 |

The simple conditional-probability model worsens publication-held-out Brier score by **2.60%** in the full subset and **6.29%** in the source-disjoint subset (relative to their respective baselines). Log loss also worsens. Equal-total-publication evaluation agrees in direction.

## Whole-species held-out sensitivity

We separately hold out all rows for each plant species, which blocks across-publication re-use of a focal taxon.

| Held-out set, alpha=0.5 | Brier without I | Brier with I sign | Log loss without I | Log loss with I sign |
|---|---:|---:|---:|---:|
| Full public-S1: 54 pairs, 52 species | 0.17948 | 0.18592 | 0.54890 | 0.56477 |
| EGWEE-source-disjoint: 31 pairs, 29 species | 0.18687 | 0.19872 | 0.56857 | 0.60741 |

Again, the simple conditional sign model does not improve held-out probability scores.

## Smoothing sensitivity

For alpha = 0.5, 1, 2 and 4, all four publication-held-out comparisons (full/disjoint by Brier/log loss) favor the baseline, not the conditional sign rule. These are post hoc robustness choices, not data-adaptive winner selection.

## Scientific interpretation

The corrected continuous Hedges-d relationship can still be positive, while sign information adds a very small in-sample probability difference and does not transfer well to new publications or species under this simple model.

This yields a more precise statement than "correlation but zero information":

> **The sign of pollination response contains some sample-level information but, in this public-S1 subset, does not improve held-publication or held-species probability prediction under a simple explicitly specified conditional-sign model.**

This remains compatible with stronger discrimination at some severity thresholds (as the separate post hoc threshold sweep showed), with nonlinear predictors, and with pollination genuinely contributing to reproductive fitness.

## Critical caveats

- The outcome is a **point-sign label** from effect estimates, not a verified true physiological state. Only three pairs have both marginal signs 95%-resolved, and all three are concordant.
- Publication × species × land-use pairing is not guaranteed to be synchronized by site or year.
- Cross-validation scores are conditional on a selected literature subset (426 public physical rows; 74 paper-reported inputs unavailable), not a field prevalence sample.
- This audit is not evidence that all possible classifiers are useless or that the true conditional mutual information is zero.
- The older "zero incremental classification gain" remains true only for 0/1 accuracy at the fixed F<0 threshold, not for all notions of predictive information.
