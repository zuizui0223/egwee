# Protocol amendment — conservative unknown-covariance fallback

**Frozen:** 2026-09-15, before opening numeric effects for any new candidate evaluated under this fallback.

## Purpose

The fifth-cluster search is intended to test whether the primary state-separation conclusion survives omission of `ML001 Serapias`, not to minimise the full-corpus p-value. Several otherwise eligible direct Hedges-g studies report effect-unit-valid marginal effects and variances for two biological layers on the same fragmentation comparison but do not publish the cross-layer sampling covariance.

The existing protocol already permits a conservative dependence fallback when within-study covariance cannot be reconstructed. This amendment makes that fallback executable without assuming independence.

## Scope

This fallback may be used only when all of the following are true:

1. both endpoints belong to the already-frozen `hedges_g_direct` primary effect family;
2. both endpoints use the same source-defined fragmented-versus-reference exposure;
3. the independent fragmentation unit is valid for each marginal Hedges g and its sampling variance;
4. the two endpoint samples refer to the same study/species/system and materially aligned exposure-unit frame;
5. no lower-level flowers, fruits, seeds, progeny, loci, repeated observations, or individuals are promoted to fragmentation replication;
6. the endpoint identities and layer mapping were fixed before their numeric effect sizes were opened.

The fallback does **not** rescue studies lacking an effect-unit-valid marginal Hedges g or sampling variance. It also does not permit conversion of gradients, correlations, odds ratios, or model coefficients into the primary family merely to fill the fifth-cluster slot.

## Conservative variance bound

For two oriented Hedges-g estimates `g1` and `g2` with sampling variances `v1` and `v2`, the state-separation contrast is

`d = g1 - g2`.

The exact contrast variance is

`Var(d) = v1 + v2 - 2 Cov(g1,g2)`.

When the covariance is unknown, Cauchy-Schwarz gives

`Cov(g1,g2) >= -sqrt(v1 v2)`.

Therefore the largest admissible contrast variance is

`V_max = v1 + v2 + 2 sqrt(v1 v2) = (sqrt(v1) + sqrt(v2))^2`.

The conservative test uses

`z_worst = d / sqrt(V_max)`

and the usual two-sided Normal p-value. Because `V_max` is the maximum variance compatible with the two marginal variances, this produces the smallest absolute z and largest two-sided p over all correlations `rho in [-1,1]`. It is therefore deliberately hostile to claiming state separation.

## More than two endpoints

If a future admitted cluster has more than two marginal effects but no full covariance matrix, apply the same worst-case variance bound separately to each prespecified pair. Then apply the already-frozen within-cluster Bonferroni rule to those conservative pairwise p-values.

No claim is made that setting every pairwise correlation to -1 defines one globally valid covariance matrix. The construction is a pairwise upper bound used only to obtain a conservative p-value for each contrast.

## Interpretation

A cluster may enter the primary synthesis under this fallback only if its marginal effects themselves pass all primary admission gates. Its cluster p-value is labelled `unknown_covariance_worst_case` and remains distinct from clusters with reconstructed covariance.

If the fifth cluster causes the `omit ML001` Fisher combination to reject at 0.05 even under this worst-case dependence bound, that is evidence that the conclusion does not require the Serapias cluster. If it does not, the result is recorded as a negative robustness test.

Candidate selection, endpoint selection, and admission are never based on whether the resulting cluster p-value crosses the threshold.