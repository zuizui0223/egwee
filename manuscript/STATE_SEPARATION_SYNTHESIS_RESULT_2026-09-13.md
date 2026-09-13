# EGWEE formal state-separation synthesis — corrected result

**Date:** 2026-09-13

## Terminal result

`reject_primary_binary_layer_exchangeability_with_separate_gradient_support`

The corrected synthesis preserves the frozen effect-family boundary:

- primary formal inference uses the three independently admitted fragmented-versus-reference Hedges-g clusters, ML001–ML003;
- ML015 *Eucalyptus wandoo* is retained separately as a Fisher-z gradient generalisation cluster;
- ML015 is not counted as a fourth primary cluster and is not included in the primary Fisher combination.

## Primary cluster-level tests

| cluster | system | admitted primary layers | Bonferroni cluster p | interpretation |
|---|---|---|---:|---|
| ML001 | *Serapias lingua* | C / F / G_adult | 0.00354530 | clear within-system non-exchangeability |
| ML002 | *Brosimum alicastrum* | C / F | 0.19911670 | no individual-cluster rejection |
| ML003 | *Spondias purpurea* | C / G_adult / G_juvenile / G_seed | 0.17406774 | no individual-cluster rejection after six-pair correction |

The strongest ML001 contrast remains F fruit set versus G_adult H_O: difference = 21.51837567 Hedges-g units, SE = 6.63482966, z = 3.24324, two-sided p = 0.00118177.

## Primary cross-cluster synthesis

Fisher combination of the **three primary binary/contrast cluster** p-values gives approximately:

- Fisher statistic: **18.0086**
- df: **6**
- combined p: **0.00621**

The canonical executable recomputes these values directly from the effect and covariance files on every run.

Therefore the currently admitted primary binary/contrast corpus rejects the layer-exchangeability null at the formal synthesis level.

## Separate ML015 gradient generalisation

ML015 is analysed only on the frozen Fisher-z gradient scale:

- I pollen tubes: `z = +0.69029123`;
- F seeds per fruit y2: `z = -0.87593080`;
- G_adult H_e: `z = -0.41117288`.

The strongest within-ML015 contrast is I versus F:

- difference = `1.56622203` Fisher-z units;
- SE = `0.46979298`;
- z = `3.33386`;
- two-sided p = `0.00085651`.

Bonferroni correction across the three ML015 endpoint pairs gives `p_cluster = 0.00256953`.

This is strong independent gradient/generalisation evidence for state separation: along the response-free composite fragmentation gradient, pollen quantity increases while realised seed production declines. It is **not** combined with the primary Hedges-g cluster p-values.

## What this means

The supported primary statement is:

> across the three currently admitted replicated fragmented-versus-reference systems, biological response layers cannot generally be treated as exchangeable manifestations of one scalar fragmentation response.

ML015 separately shows that the same qualitative state-separation problem extends to a continuous-gradient natural system.

This is stronger than noting heterogeneous effect sizes, because each primary cluster compares multiple layers within one system while preserving dependence. It is narrower than the superseded four-cluster claim because the gradient study is no longer promoted into the primary denominator.

## What this does not mean

- It does not establish a universal ordering of C, I, F or G.
- It does not imply that every primary cluster individually rejects exchangeability.
- It does not pool Hedges g with Fisher z.
- It does not combine the ML015 gradient p-value with the primary Fisher statistic.
- It does not validate EGWE's finite-model operator ordering or strongest-refuge predictor in nature.
- It is not a prospective validation.

## Correction note

A superseded implementation treated ML015 standardized OLS slopes as a fourth primary cluster and reported a four-cluster Fisher p-value of `0.0005347329`. That result is not canonical because the frozen protocol assigns continuous gradients to the separate Fisher-z stream. The present three-primary-cluster synthesis and separate ML015 gradient diagnostic replace that implementation.

## Audit trail

Method boundary is fixed in `META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_STATE_SEPARATION_SYNTHESIS.md`.

Canonical executable is `scripts/synthesize_state_separation.py`.

`EUCALYPTUS_WANDOO_2018_CLUSTER_RECOVERY_RESULT.md` and the ML015 gradient checker independently enforce that ML015 contributes zero primary Hedges-g effects.
