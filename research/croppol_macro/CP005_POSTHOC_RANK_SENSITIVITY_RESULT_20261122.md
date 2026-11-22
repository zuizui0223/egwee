# CP005 — Post-outcome algorithmic sensitivity of exploratory CropPol yield-rank source transfer

**22 Nov 2026.** CP004 frozen primary source-heldout result was negative: `Δ=M1−M0=−0.03795027` pairwise yield-rank concordance, 201 original fields, 12 original homogeneous blocks, 10 provisional source components. This CP005 analysis was intentionally designed **AFTER seeing that result** and is **not a preregistered independent ecological study or a second confirmatory test**. It preserves source cohort, endpoint, original source grouping, within-block rank transformation, source-equal weighting and leave-one-source-out assignment. [Post-result sensitivity freeze](CP005_POSTHOC_PENALTY_SENSITIVITY_FREEZE_20261122.md) preceded examination of any alternative penalty results.

## Results from the original pinned author CSV

[Successful live original-source GitHub Actions run 45009831579](https://github.com/zuizui0223/egwee/actions/runs/45009831579), [source-safe derivative](CP005_SAFE_POSTHOC_SENSITIVITY_RECEIPT_20261122.json). A separate fixed-penalty implementation reproduced the **exact original lambda 0.10 M0 and M1 concordances**, to tolerance <1e−10, without changing CP004.

| Fixed ridge penalty, all 201 fields | Source-equal M0 | Source-equal M1 | Added visits Δ | New 4,000-source bootstrap interval | Source gains/losses |
|---|---:|---:|---:|---:|---:|
| 0.01 | 52.40% | 49.29% | **−3.11 pp** | [−6.54,+0.32] pp | 4 / 6 |
| **0.10 original primary** | **52.40%** | **48.60%** | **−3.80 pp** | **[−6.95,−0.65] pp** | **3 / 7** |
| 1.00 | 52.40% | 48.05% | **−4.35 pp** | [−7.87,−0.91] pp | 3 / 7 |

These **new post-outcome source-bootstrap intervals use seed 20261123**, not the original CP004 CI seed 20261122. The original CP004 primary reported **[−6.90,−0.81] pp** and remains **unaltered**; CI differences reflect bootstrap Monte Carlo sample draws, not source change.

Holding the originally trained `lambda=0.10` source-heldout models fixed, delete **one** of the ten scored source components from the *evaluation mean* at a time. All **10/10** remaining-nine source-average increments are negative, range **−4.58 to −2.83 pp**. This is a jackknife of evaluation sources only, **not** ten independent new source withholding trials, and does not refit models or artificially create extra regions.

Decision: **`PENALTY_AND_JACKKNIFE_SIGN_STABLE_NEGATIVE`** as an algorithmic sensitivity statement only. The penalty 0.01 source-bootstrap interval overlaps zero: **it is NOT true that all penalties independently show statistically resolved degradation**. The pairwise heldout prediction of source-specific yield ranks does not improve when total observed visitation rank is added to a field-area-only source-transferred benchmark under these three fixed penalizations.

## Scientific interpretation ceiling

Even stable sign across penalties **cannot** establish absence of pollinator benefits or a mechanism for low yield. This field-size-only benchmark lacks the stronger field-context covariates, flower availability, plant reproductive resources, management, crop/soil, crop-specific pollinator effectiveness, and survey-effort calibration that might enable sound out-of-source prediction. Its original source graph contains only **provisional** independent campaigns; 201 fields and 1,758 pairwise comparisons are nested in 10 source components, not 1,758 independent ecological experiments. The source outcomes are heterogeneous direct-output and harvested-mass families scored as **within-homogeneous-block ranks only**, not pooled absolute yield.

The original authors and earlier CropPol literature already established visitor–yield associations and substantial heterogeneity. The present exploratory negative source-transfer finding motivates **documented independent context predictors and cross-study harmonized phenology/floral resource variables** rather than another search over unregistered model scales, endpoints or crop subsets. The CP003 taxon sampling table cannot supply standing flower density or plant density.

No original raw source rows, study/field identifiers, visit magnitudes, source-specific errors, genotypes, inferred donor identity or copyrighted content redistributed. Keep PR94 draft, no theoretical `egwe` or empirical `egwee` main merge. Original CP004 frozen analysis and CI remain authoritative.
