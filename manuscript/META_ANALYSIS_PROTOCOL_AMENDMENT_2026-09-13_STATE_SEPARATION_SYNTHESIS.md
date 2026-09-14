# Protocol amendment — primary state-separation synthesis and separate gradient generalisation

**Date:** 2026-09-13; extended 2026-09-15 after prospectively locked ML014 recovery

## Purpose

This amendment defines the formal state-separation synthesis while preserving the effect-family boundary frozen in `META_ANALYSIS_PROTOCOL_2026-09-11.md`.

The primary meta-analysis contains direct fragmented-versus-reference contrasts represented as Hedges g. Continuous fragmentation gradients are a separate Fisher-z generalisation stream. They are not pooled or combined as though they were members of one primary effect family.

An earlier implementation incorrectly treated ML015 *Eucalyptus wandoo* as a primary cluster using standardized gradient slopes. That implementation remains superseded. ML015 has no unfragmented/reference group and remains a separate Fisher-z gradient-generalisation cluster.

ML014 *Eucalyptus socialis* was subsequently recovered under `EUCALYPTUS_SOCIALIS_2012_ML014_RECOVERY_CONTRACT.md`, which fixed its Monarto contrast, independent family unit, `G_mating=r_p` representation, F growth endpoint and covariance rule before public numeric outcome rows were opened. ML014 therefore extends the already-fixed primary Hedges-g synthesis without changing the synthesis rule after seeing its effect values.

## Primary cluster-level null

The primary formal synthesis is restricted to independently admitted binary/contrast clusters:

- ML001 *Serapias lingua*;
- ML002 *Brosimum alicastrum*;
- ML003 *Spondias purpurea*;
- ML014 *Eucalyptus socialis*.

For each cluster, the null is that all admitted primary layer effects in that cluster are equal on that cluster's own Hedges-g scale.

For every unordered pair of admitted endpoints i,j:

- `d_ij = e_i - e_j`;
- `V(d_ij) = V_i + V_j - 2 Cov_ij`;
- `z_ij = d_ij / sqrt(V(d_ij))`;
- two-sided `p_ij` from the standard normal distribution.

All pairwise contrasts are retained. No pair is selected after seeing its magnitude.

Because endpoints within a cluster are dependent, the cluster-level p-value is the Bonferroni union bound:

`p_cluster = min(1, m * min(p_ij))`,

where m is the number of unordered endpoint pairs. This does not require independence among pairwise contrasts and avoids inverting ML003's structurally singular four-endpoint covariance proxy.

## Primary cross-cluster synthesis

The four primary clusters are separate biological systems/studies. Their Bonferroni-corrected cluster p-values are combined with Fisher's method:

`X = -2 * sum(log(p_cluster))`, with `df = 2k`, `k = 4`.

The same fixed rule is also recomputed after omitting each primary cluster once. This leave-one-primary-cluster-out diagnostic is a claim ceiling, not a selection rule: no cluster is removed from the canonical result because its omission weakens or strengthens the combined p-value.

## Fixed primary endpoint sets

- ML001 Serapias: C pollen immigration, F fruit set, G_adult H_O.
- ML002 Brosimum: C correlated-paternity support, F progeny total dry mass.
- ML003 Spondias: C correlated-paternity support, adult H_O, juvenile H_O, seed H_O.
- ML014 Eucalyptus socialis: G_mating correlated-paternity support (`-r_p`) and family mean progeny growth F, on the same prospectively locked Monarto family frame.

Sensitivity metrics (`F_IS`, `Sp`), unreconstructed layers, Yookamurra context from PS020, and non-admitted candidate clusters are excluded.

## ML015 gradient generalisation

ML015 *Eucalyptus wandoo* is analysed separately using the already-frozen `fisher_z_gradient` stream. Its three effects are I pollen tubes, F seeds per fruit year 2, and G_adult `H_e`.

The same pairwise contrast and Bonferroni cluster procedure is applied within ML015 on its Fisher-z scale using its gradient covariance proxy. ML015 is **not** included in the primary Fisher combination and its p-value is never combined with the primary Hedges-g cluster p-values.

## Interpretation

A small primary combined p-value rejects exchangeability across the currently admitted primary binary/contrast systems. Leave-one-cluster-out results must be reported alongside that result whenever any omission crosses the decision threshold.

A small ML015 gradient p-value independently shows state separation in a continuous-gradient natural system. Concordance between tiers strengthens generalisation but does not convert the gradient study into a primary replicate.

Neither tier establishes one universal ordering of C, I, F or G, one common effect magnitude, a causal operator sequence in nature, or that every cluster individually shows significant discordance.

## Retrospective/prospective boundary

The overall meta-analytic corpus and the synthesis rule are retrospective. ML014 is a prospective **cluster recovery within that fixed method**: its exposure, endpoints, effect unit and dependence rule were locked before its public numeric rows were opened. This does not convert the whole meta-analysis into prospective validation.

## No-rescue rules

Do not:

- add ML015 to the primary Hedges-g denominator;
- combine Hedges-g and Fisher-z cluster p-values into one Fisher statistic;
- substitute standardized OLS slopes as a third effect family;
- drop a weak primary cluster after seeing its p-value;
- select only significant endpoint pairs;
- change the ML014 endpoint from `r_p` to `k_n` or its F endpoint from family growth after value access;
- include Yookamurra in ML014's primary Monarto contrast;
- replace Bonferroni with a less conservative within-cluster method after seeing results;
- invert the singular ML003 4x4 covariance matrix;
- add non-admitted systems merely to increase k;
- reinterpret a non-significant cluster-level p-value as evidence of exchangeability.
