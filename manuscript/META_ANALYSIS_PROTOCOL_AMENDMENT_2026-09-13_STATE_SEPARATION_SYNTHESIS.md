# Protocol amendment — primary state-separation synthesis and separate gradient generalisation

**Date:** 2026-09-13

## Purpose

This amendment defines the formal state-separation synthesis while preserving the effect-family boundary frozen in `META_ANALYSIS_PROTOCOL_2026-09-11.md`.

The primary meta-analysis contains direct fragmented-versus-reference contrasts represented as Hedges g. Continuous fragmentation gradients are a separate Fisher-z generalisation stream. They are not pooled or combined as though they were members of one primary effect family.

An earlier implementation of this amendment incorrectly treated ML015 *Eucalyptus wandoo* as a fourth primary cluster using standardized gradient slopes. That implementation is superseded here. ML015 has no unfragmented/reference group and its composite fragmentation PC is an EGWEE response-free construct from source descriptors, so it remains a separate Fisher-z gradient-generalisation cluster.

## Primary cluster-level null

The primary formal synthesis is restricted to the independently admitted binary/contrast clusters:

- ML001 *Serapias lingua*;
- ML002 *Brosimum alicastrum*;
- ML003 *Spondias purpurea*.

For each cluster, the null is that all admitted primary layer effects in that cluster are equal on that cluster's own Hedges-g scale.

For every unordered pair of admitted endpoints i,j:

- contrast: `d_ij = e_i - e_j`;
- variance: `V(d_ij) = V_i + V_j - 2 Cov_ij`;
- `z_ij = d_ij / sqrt(V(d_ij))`;
- two-sided `p_ij` from the standard normal distribution.

All pairwise contrasts are retained. No pair is selected after seeing its magnitude.

Because endpoints within a cluster are dependent, the cluster-level p-value is the Bonferroni union bound:

`p_cluster = min(1, m * min(p_ij))`,

where m is the number of unordered endpoint pairs. This does not require independence among pairwise contrasts and avoids inverting ML003's structurally singular four-endpoint covariance proxy.

## Primary cross-cluster synthesis

The three primary clusters are independent biological systems/studies. Their Bonferroni-corrected cluster p-values are combined with Fisher's method:

`X = -2 * sum(log(p_cluster))`, with `df = 2k`, `k = 3`.

This is a retrospective formal summary of evidence against primary-layer exchangeability. It does not pool endpoint effect magnitudes across studies.

## Fixed primary endpoint sets

- ML001 Serapias: C pollen immigration, F fruit set, G_adult H_O.
- ML002 Brosimum: C correlated-paternity support, F progeny total dry mass.
- ML003 Spondias: C correlated-paternity support, adult H_O, juvenile H_O, seed H_O.

Sensitivity metrics (`F_IS`, `Sp`), unreconstructed layers, and non-admitted candidate clusters are excluded.

## ML015 gradient generalisation

ML015 *Eucalyptus wandoo* is analysed separately using the already-frozen `fisher_z_gradient` effect stream.

Its three gradient effects are:

- I: pollen tubes at the base of the style;
- F: seeds per fruit, year 2;
- G_adult: adult `H_e`.

The same pairwise contrast and Bonferroni cluster procedure may be applied within ML015 on its Fisher-z scale using its gradient covariance proxy. This yields a system-level diagnostic of state separation under a continuous fragmentation gradient.

ML015 is **not** included in the primary Fisher combination, and its p-value is never combined with the primary Hedges-g cluster p-values. It contributes generalisation evidence only.

## Interpretation

A small primary combined p-value rejects the claim that the currently admitted primary binary/contrast layers can generally be treated as exchangeable fragmentation responses across ML001–ML003.

A small ML015 gradient p-value independently shows state separation in a continuous-gradient natural system. Concordance between those two tiers strengthens interpretation but does not convert the gradient study into a primary binary/contrast replicate.

Neither tier establishes one universal ordering of C, I, F or G, one common effect magnitude, a causal operator sequence in nature, or that every cluster individually shows significant discordance.

## Retrospective status

Both the primary corpus and ML015 source tables were assembled before this corrected formal synthesis was frozen. The outputs are auditable retrospective summaries, not prospective validation.

## No-rescue rules

Do not:

- add ML015 to the primary Hedges-g denominator;
- combine Hedges-g and Fisher-z cluster p-values into one Fisher statistic;
- substitute standardized OLS slopes as a third effect family;
- drop ML002 or ML003 because their cluster-level results are weak;
- select only significant endpoint pairs;
- replace Bonferroni with a less conservative within-cluster multiplicity method after seeing results;
- invert the singular ML003 4x4 covariance matrix;
- add non-admitted systems merely to increase k;
- reinterpret a non-significant cluster-level p-value as evidence of exchangeability.
