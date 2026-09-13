# Protocol amendment — cross-family state-separation synthesis

**Date:** 2026-09-13

## Purpose

The current EGWEE evidence contains four independent covariance-aware multilayer fragmentation clusters but two different effect families: three binary Hedges-g clusters (ML001–ML003) and one standardized gradient-slope cluster (ML015). These effect sizes must not be pooled as though they shared one numerical scale.

This amendment defines a family-agnostic synthesis of the narrower hypothesis that biological layers are exchangeable manifestations of one fragmentation-response state.

## Cluster-level null

For each independent cluster, the null is that all admitted primary layer effects in that cluster are equal on that cluster's own effect scale.

For every unordered pair of admitted endpoints i,j:

- contrast: d_ij = e_i - e_j;
- variance: V(d_ij) = V_i + V_j - 2 Cov_ij;
- z_ij = d_ij / sqrt(V(d_ij));
- two-sided p_ij from the standard normal distribution.

All pairwise contrasts are retained. No pair is selected after seeing its magnitude.

Because endpoints within a cluster are dependent, the cluster-level p-value is the Bonferroni union bound:

`p_cluster = min(1, m * min(p_ij))`,

where m is the number of unordered endpoint pairs. This remains valid without assuming independence among pairwise contrasts and avoids inverting ML003's structurally singular four-endpoint covariance proxy.

## Cross-cluster synthesis

The four clusters are separate biological systems/studies and are treated as independent cluster-level evidence units. Their Bonferroni-corrected cluster p-values are combined with Fisher's method:

`X = -2 * sum(log(p_cluster))`, with `df = 2k`, k = 4.

This combines evidence against within-system layer exchangeability without pooling Hedges-g and gradient slopes.

## Fixed endpoint sets

- ML001 Serapias: C pollen immigration, F fruit set, G_adult H_O.
- ML002 Brosimum: C correlated-paternity support, F progeny total dry mass.
- ML003 Spondias: C correlated-paternity support, adult H_O, juvenile H_O, seed H_O.
- ML015 Eucalyptus wandoo: I pollen tubes, F seeds per fruit year 2, G_adult H_e.

Sensitivity metrics (F_IS, Sp), unreconstructed layers, and non-admitted candidate clusters are excluded.

## Interpretation

A small combined p-value rejects the claim that the admitted biological layers can generally be treated as numerically exchangeable responses to fragmentation. It does **not** establish one universal ordering of layers, one common effect magnitude, a causal operator sequence in nature, or that every cluster individually shows significant discordance.

The synthesis is explicitly retrospective. ML015 aggregate outcome values were visible during candidate discovery, and the four-cluster corpus was assembled before this formal synthesis was defined. The output is therefore an auditable formal summary of the current evidence, not a prospective validation.

## No-rescue rules

Do not:

- pool effect magnitudes across Hedges-g and gradient-slope families;
- drop ML002 or ML003 because their cluster-level result is weak;
- select only significant endpoint pairs;
- replace Bonferroni with a less conservative within-cluster multiplicity method after seeing results;
- invert the singular ML003 4x4 covariance matrix;
- add non-admitted systems to increase k;
- reinterpret a non-significant cluster-level p-value as evidence of exchangeability.
