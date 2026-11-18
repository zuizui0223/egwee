# SF06 nested publication-deletion audit: external predictive influence (2026-10-10)

**Status:** post hoc robustness check of previously inspected literature-derived public-S1 signs. This is empirical EGWEE; no new effect, meta-analysis study, species or prospectively registered test is added. This note does not replace the 16-programme frozen map or the independent Q→E→F prospective design.

## New question

Previous publication-LOO validation reported that a one-variable pollination-sign probability model predicted female-fitness decline *worse* than a context-only baseline. But publication-LOO alone is not an influence check: one publication might still determine the comparison between two competing rules.

The nested check now **deletes each entire source publication from the eligible dataset**, then **re-runs publication-LOO from scratch** within the remaining publications. Both the baseline rate and conditional-sign rates are refitted using only each inner training fold. No held-out female-fitness label is used for fitting.

The outcome remains a **point-sign indicator** from public meta-analytic effects. It is not verified field impairment. Main filter: habitat-fragmentation pairs with both constituent-consensus signs known; 54 pairs from 32 publications. A pre-existing source-publication exclusion yields 31 pairs from 23 publications, independent of the frozen EGWEE I–F evidence map by publication (but not a random sampling frame).

The score is `delta = loss(I-sign conditional model) - loss(context-only baseline)`; positive values indicate **worse** transfer to a held publication after measuring I sign. Lower Brier and log loss are better. The primary descriptive smoothing is Jeffreys alpha=0.5; alpha=1,2,4 are shown jointly to prevent a single post hoc winner.

## New findings

| Subset / Jeffreys alpha=0.5 | Original publication-LOO Brier delta | Full-dataset publication-deletion range | Positive / negative deletions |
|---|---:|---:|---:|
| Full 54-pair, 32-publication public-S1 | +0.004593 | +0.003983 to +0.009440 | 32 / 0 |
| Source-publication-disjoint 31-pair, 23-publication subset | +0.011511 | **-0.003288** to +0.019634 | **22 / 1** |

The corresponding log-loss direction is the same: 32/32 positive after deletion in the full set; 22/23 positive and one negative in the disjoint set.

The unique sign-changing deletion removes **Hauber et al. (2022), *Trichodiadema strumosum***. This publication contributes one `I nonlower / F nonlower` point-sign pair to the 31-pair subset, with `d_I=+0.647`, `d_F=+1.448`. The refitted 30-pair source-disjoint comparison becomes:

| Smoothing alpha | Brier delta without Hauber | Log-loss delta without Hauber | Interpretation |
|---|---:|---:|---|
| 0.5 | **-0.003288** | **-0.014514** | conditional sign better by both scores |
| 1.0 | **-0.000109** | **-0.002624** | tiny row-weighted improvement; equal-publication Brier remains worse |
| 2.0 | +0.005253 | +0.012071 | conditional sign worse |
| 4.0 | +0.011429 | +0.025888 | conditional sign worse |

At alpha=2 and alpha=4, **all 23** single-publication-deleted disjoint comparisons still favor the context-only baseline for both scores. The conclusion is therefore dependent on **the smoothing specification and a single source publication** in the disjoint set. It would be incorrect to describe the disjoint predictive failure as publication-deletion-invariant. The full-set failure *is* one-deletion direction-stable under all four smoothings examined.

## Biological interpretation and significance boundary

This does **not** refute the primary existence result: multiple source-confirmed fragmentation systems show apparently retained pollination/interactions and poorer reproduction; the most strongly resolved quantitative anchors remain *Eucalyptus wandoo*, *Cardiopetalum calophyllum*, and Kakamega *Acanthopale pubescens*. Nor does it establish a beneficial pollination sign predictor after Hauber removal: both model selection and sensitivity checks are post exposure, the labels are uncertain, and the data are sparse.

The unexpected lesson is conditional: **a process indicator can be associated with function on average, yet its incremental diagnostic value can be fragile to which ecological programmes are represented, the predictive loss, and regularization.** The contrast is a statement about the current *literature subset and model*, not a universal law of pollination ecology.

In the paper, retain the weaker phrasing: 'In the corrected public-S1 literature subset, a simple sign-only model did not improve held-publication probability prediction in the complete and source-disjoint sets; the latter result is not invariant to single-publication deletion under weak smoothing.' Avoid a universal 'no predictive information' claim, a newly confirmed mechanism, or a prevalence/causal statement.

## Next biological discrimination

The scientific question that can actually advance is **when observed interaction quantity becomes diagnostically useful versus misleading**. Distinguish within the same independent fragment/reference landscape and reproductive season:

- interaction count or pollen-tube **quantity** (`Q`);
- pollinator identity and realised compatible/outcross donor **quality** (`E`);
- viable seed production and subsequent recruitment **function** (`F` and `R`);
- seed/flower resources, alternative self/wind routes, seed dispersal and detection;
- sampling opportunity and matching of maternal/offspring cohorts.

Predeclare a baseline risk model and a staged Q-only, Q+E, Q+E+resource/seed-dispersal comparison before outcomes; evaluate on entirely held-out independent landscapes, not seeds/plants as units. Improvement must be quantified using proper probability scores and, ideally, randomly assigned stage-specific interventions on a whole-patch recruit denominator. Source-publication-disjoint literature comparisons cannot substitute for such synchronized natural measurements.

## Reproduce

`python scripts/check_sf06_publication_delete_predictive_influence.py`

This reads only `evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv` and checks the source rows, nested refitting, exact effect-score references, and sensitivity against changes. No external source downloads or frozen denominator mutations are performed. The historical sign-topology and existing publication-LOO probability checks remain independently callable.

**Causal/novelty ceiling:** This audit is a necessary robustness qualification of the exploratory sentinel analysis; it is *not* independent biological replication and not a journal-ready ecological discovery by itself.
