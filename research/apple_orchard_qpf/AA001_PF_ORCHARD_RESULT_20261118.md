# AA001 — 2023 apple natural-open germinated pollen predicts fruit set modestly in one source; regional instability

**2026-11-18. Status: source-exact, prospectively frozen *for this narrower stage* before examining P–F coefficients, but chosen after original three-stage QPF coverage STOP. One original study. Not a general pollination mechanism, not a third directly measured same-flower Q→P→F programme.**

## Source and independent ecological unit

Riva et al. 2026, *Science of the Total Environment*, DOI [10.1016/j.scitotenv.2026.181767](https://doi.org/10.1016/j.scitotenv.2026.181767); original Zenodo [10.5281/zenodo.19403906](https://doi.org/10.5281/zenodo.19403906). Original file SHA256 pinned and all 4 sources verified by [CI 44290503422](https://github.com/zuizui0223/egwee/actions/runs/44290503422), see `AA001_SOURCE_AND_GRAIN_RESULT_20261118.md`.

The main, prospectively defined original Q+P+F matched 2023 orchard test failed **11/12** required orchard keys, and remains **not executed**. Do not quote the following P–F result as confirmation of that three-stage hypothesis.

After this original strictly source-only QPF coverage result and **before inspecting P–F effects**, `AA001_PF_CONTEXT_PREDICTION_FREEZE_20261118.md` fixed a **different, narrower** original biological question: on the same orchard+plot, compare 2023 **O (naturally open)** pollen germination measured from **excised stigmas** with final fruit success measured on other flowers in those same source orchard plot/treatment conditions. No actual visitor Q in this model, no plot or style pseudo-independent replicate, no inflorescence joining across destructive assays, no hand-pollen treatment contrasts selected by outcome.

Admission was source-locked to >=12 valid 2023 orchard P/F O aggregates, >=3 original regions, >=2 orchards in every region and common source plot O measurements. The executed source supports:

| Original source coverage | Recomputed result |
|---|---:|
| P source 2023 O plot keys | **79** |
| F source 2023 O plot keys | **140** |
| Exact same-orchard+plot O P and F keys | **76** |
| **Independent original orchard prediction units** | **18** |
| **Original region groups** | **5** (smallest has 3 orchards) |
| Source germinated-pollen style rows contributing | **347** |

The P and F are **on different source flowers**, so even matched plot/site-year does not identify individual pollen-to-fruit fate, compatible conspecific pollen, paternity, wind exposure or a causal post-pollination mechanism.

## Model frozen *before* the P–F coefficient

One orchard is one prediction observation. P is the mean of valid style germinated pollen grains in original 2023 O matched plots. F is the aggregate natural-open final success / (success + failure) in the corresponding source F orchard plots, transformed to smoothed `log[(final_successes+0.5)/(final_failures+0.5)]`. The original source temperature is a common orchard long-term climate proxy. Each fold removes **the entire original source Region** (all its orchard observations).

M0 = orchard temperature. M1 = M0 + log1p(mean germinated pollen P). Both unpenalized-intercept **ridge λ=1**, with both predictors and final-fruit target standardized **on training orchards only** inside each fold. Scoring is held-out orchard mean squared error on that training-only target scale. No model tuning, outcome unit switching, or thinning of source orchids after observing effects.

**Registered conditional positive rule:** pooled orchard-equal M0−M1 gain >0 **and at least 3 original region folds improve**. This is a pragmatic *one-study predictive signal gate*, NOT a p-value or evidence of region-general causality.

| Original region fold (anonymized) | Orchards | M0 MSE | M1 MSE | Gain M0−M1 |
|---|---:|---:|---:|---:|
| 1 | 4 | 0.324391 | **0.061273** | **+0.263118** |
| 2 | 3 | 0.456075 | **0.110464** | **+0.345611** |
| 3 | 5 | 2.324161 | **1.939391** | **+0.384769** |
| 4 | 3 | **0.060444** | 0.429593 | −0.369148 |
| 5 | 3 | **0.223254** | 0.680844 | −0.457590 |
| **Orchard-equal pooled** | **18** | **0.840982** | **0.755819** | **+0.085163** |

- **Result:** prespecified `ONE_STUDY_BOUNDED_POLLEN_CONTEXT_PREDICTIVE_INCREMENT`, 3/5 held-out source regions positive.
- Reduction in heldout MSE relative to temperature-only = `0.08516/0.84098` = approximately **10.1%** on the *training-z logit final fruit* scale, not 10.1% higher actual yield or seed set.
- Equal-original-region mean gain, less sensitive to orchard numbers: **+0.033352**; two source regions deteriorate.
- Original-source runner verified all four source raw SHA digests and frozen source keys; [successful original source CI 44291631662](https://github.com/zuizui0223/egwee/actions/runs/44291631662), derivative artifact 14422500591. No source biological rows or orchard IDs redistributed.

## Explicit post-outcome influence qualification — NOT another confirmation

After opening these five fold scores, we recomputed **only the arithmetic mean of already-fitted held-out fold errors** with each complete source scoring region deleted. **The models were not refit and no original observation was deselected for the primary result.**

The resulting orchard-weighted aggregate score ranges from **−0.03007 to +0.19371**, and is **negative when the five-orchard positive fold (region index 3) is excluded**. Equal-region mean likewise ranges from **−0.05450 to +0.15609**, changing sign when deleting any of the three positive-gain scoring regions.

Thus the modest positive headline is **not leave-one-region aggregation robust**. This is an important predictability warning: the M1 advantage is sensitive to a few regional orchard cohorts and does not support universal climate-independent P→F conversion. The original 3/5 and +0.085 point summary remain valid as the *frozen one-source result*, not evidence of external ecological generality.

## Ecological information gained, prior art and ceiling

**Supported within this programme:** Germinated pollen quantity under natural-open treatment can carry additional context about orchard-level final fruit outcomes beyond site long-term mean temperature, but the magnitude and direction of predictive increment are markedly heterogeneous among held-out regions. This is an original-source observation-cohort prediction, **not a new discovered biological response to temperature**.

**Previously established by the original article:** pollinator exclusion reduces germinated pollen and fruit set; fruit set and apple weight show climate/treatment associations. These are Riva et al.'s biological findings, not EGWEE's new confirmation. Some alternative mechanism such as wind contribution or cultivar/management is not identified by the present model.

**Not supported:** that adding germinated pollen predicts fruit set *for every region*, a third complete same-flower Q→P→F system, mechanistic transfer/compatibility, causal pollen limitation or pollen source provenance, per-visit effectiveness, actual pollination exposure Q at these F flowers, genetic mating quality, downstream seed recruitment, or any fragmentation-specific ecology. Only one original apple research programme is represented, and a 5-region CV does not quantify population-level certainty.

### Research direction

This is a useful **bounded positive exception** to the repeated failure of visit-quantity or pollen covariates to add holdout functional prediction in previous egwee QPF original sources, but source grains differ and results cannot be meta-combined as equivalent biological estimands. It suggests an explicit *cross-programme prediction* to test **environment- and region-dependent translation of successful pollen germination into final fruit function**, with independent original orchard and natural-flora studies where common maternal cohort and direct pollen donor identity are actually verified.

No original source tables, orchard labels, gene sequences, field fruit counts or per-flower measurements uploaded; only scripts and aggregate source/validation records. Original frozen EGWEE 5-cluster effect-size analysis, QPF001/004, CropPol, EuPPollNet and theoretical egwe unchanged.
