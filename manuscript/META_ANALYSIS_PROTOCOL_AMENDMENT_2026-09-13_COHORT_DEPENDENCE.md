# Protocol amendment — cohort endpoints and low-rank within-cluster dependence

**Locked:** 2026-09-13, before any cross-system use of the newly recovered Spondias cohort endpoints.

This amendment extends the multilayer-cluster contract after Appendix B of `PS001` exposed multiple genetic developmental stages on only five independent sites. It does not change any effect orientation or fragmentation contrast.

## 1. Genetic representation rule

The pre-existing `PS003 Serapias` convention is generalized:

- `H_O` is the primary genetic-support representation when site/population-level values are available;
- `F_IS` is an alternate sensitivity representation and cannot be counted as another independent genetic layer;
- spatial genetic structure metrics such as `Sp` remain valid structural sensitivity endpoints when they answer a distinct within-layer question, but they do not replace canonical `H_O` merely because their effect direction is more convenient.

This rule is applied to `PS001 Spondias` after Appendix B supplied site-specific adult, juvenile and seed `H_O`/`F_IS` values.

## 2. Developmental cohorts are dependent outcomes, not extra clusters

Adult, seed and juvenile genetic observations measured in the same study/species/fragmentation contrast remain inside one multilayer cluster. Seed and juvenile endpoints may both be retained because they represent distinct developmental stages, but they do not increase the number of independent systems.

For `PS001`, the primary genetic endpoints are therefore:

- `G_adult`: adult `H_O`;
- `G_offspring`: juvenile `H_O`;
- `G_offspring`: seed `H_O`.

Their corresponding `F_IS` rows are sensitivity representations. Adult `Sp` is retained as structural sensitivity.

## 3. Low-rank covariance rule

For a binary fragmentation contrast with `n` paired independent units split across `g` exposure groups, group-centering leaves at most `n-g` residual degrees of freedom. If the number of co-retained endpoints `p` exceeds that residual dimension, the empirical outcome-correlation proxy is structurally rank-deficient.

In that case:

1. do **not** force the full proxy covariance matrix to be positive definite;
2. do **not** add an arbitrary ridge solely to make the matrix invertible;
3. retain the auditable pairwise correlations/covariances;
4. use only prespecified lower-dimensional contrasts whose covariance sub-block is nonsingular, or use the cluster-robust fallback at the cross-system stage;
5. label the stored covariance as `proxy_pairwise_low_rank` and record the rank limitation explicitly.

This is a dependence limitation, not evidence that the biological endpoints are independent.

## 4. Spondias application

`PS001` has five paired sites and two habitat groups, so within-habitat residual dimension is `5 - 2 = 3`. The four co-primary outcomes `C`, adult `H_O`, juvenile `H_O`, and seed `H_O` therefore yield a 4x4 proxy matrix with rank at most 3.

The repository stores all pairwise covariance terms but does not invert the 4x4 proxy. Adult-versus-juvenile and adult-versus-seed `H_O` contrasts are evaluated from their 2x2 covariance components.

## 5. Claim boundary

The Appendix B recovery supports site-level genetic effects without using individual sample size as fragmentation replication. It does not by itself establish a cohort lag.

A cohort-lag claim requires the covariance-aware offspring-minus-adult contrast to be distinguishable from zero, or independent systems showing the same ordered geometry. Point-estimate ordering alone remains descriptive.

## 6. Firewall

No endpoint is promoted because its direction fits the existing theory. Admission requires the same source-defined fragmentation contrast and site-level independent-unit frame. Missing I/F site values remain missing rather than being reconstructed from significance tests, plant counts or lower-level denominators.
