# Protocol amendment — estimand-scale sensitivity — 2026-09-27

> **SUPERSEDED FOR MAIN lnRR COVARIANCE RECONSTRUCTION (2026-09-29).** This file is retained as provenance for the earlier carried-correlation sensitivity. The authoritative submission-facing scale audit reconstructs lnRR covariance directly from aligned raw independent units by multivariate delta method. See `manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md` and `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-29_EFFECT_SCALE.md`.

## Trigger

After the ecology-first manuscript had been assembled, an audit showed that the headline inference based on equality of Hedges-g responses is sensitive to the effect-size scale.

The motivating example is ML001 *Serapias lingua*. On the primary Hedges-g scale, absolute magnitudes rank G > C > F. On an oriented log-response-ratio scale derived from the same group summaries, they rank C > F > G. The C–F contrast that appears strongly separated in standardized-magnitude space is not resolved on lnRR (working rho-proxy p ≈ 0.605).

This amendment is written **after** those data were observed. It is a mandatory sensitivity audit, not a new preregistered primary analysis.

## Historical primary estimand

The original primary direct stream remains Hedges g with endpoint-specific pooled-SD standardization, source-supported covariance proxies and cluster-level Bonferroni/Fisher synthesis.

That historical analysis is retained for reproducibility. It may no longer be interpreted as a scale-invariant biological statement that response layers differ in fragmentation severity.

## Added sensitivity estimand

For primary direct endpoints with positive group means, compute the oriented log response ratio:

`lnRR = orientation_multiplier × log(mean_fragmented / mean_reference)`

Negative values retain the existing support orientation: stronger fragmentation corresponds to lower biological support/function.

Delta-method marginal variance:

`V(lnRR) = SD_f^2 / (n_f mean_f^2) + SD_r^2 / (n_r mean_r^2)`.

Because exact cross-endpoint sampling covariance on the lnRR scale is not known, report three dependence regimes rather than selecting one:

1. `rho_proxy`: carry the existing dimensionless group-centred endpoint correlation proxy onto lnRR marginal variances;
2. `zero_cov`: working independence sensitivity;
3. `cauchy_maxvar`: pairwise Cauchy–Schwarz maximum contrast variance, used as a covariance-free non-certification boundary.

ML020 raw means/SD are reconstructed from the committed four-site Appendix-I table rather than back-calculated from g.

## Scale-independent directional audit

Also record only the sign of every oriented primary direct effect.

This is descriptive. The 17 effects are not independent Bernoulli trials and no 17-effect sign test is permitted.

## Decision rule for manuscript claims

A claim about **relative layer severity, separation, bottleneck position or leave-one-cluster robustness** is not called scale-robust unless its qualitative interpretation survives both the historical g analysis and the lnRR sensitivity without relying on one convenient dependence regime.

If g and lnRR give materially different endpoint ordering or different leave-one-cluster conclusions, the manuscript must state that the inference is estimand-scale dependent.

Sign consistency may support a weaker statement about common direction of deterioration, but cannot by itself establish equality or separation of magnitudes.

## Immediate consequence

The existing statements that:

- the primary direct rejection is specifically Serapias-dependent;
- Serapias provides a resolved upstream movement/connectivity bottleneck relative to fruit set;
- the complete process–function census establishes a scale-stable variable bottleneck position;

must be re-audited before submission.

## Submission gate

Journal of Ecology submission is reopened. The manuscript is **not submission-ready** until:

1. the Hedges-g / lnRR comparison is reported in Methods, Results and Limitations;
2. the scale-sensitive headline is removed or explicitly qualified;
3. the primary figure/claim ceiling no longer implies scale-invariant layer separation;
4. exploratory life-cycle attenuation/lag hypotheses are clearly separated from confirmatory results.

## Canonical implementation

- `evidence/meta_extraction/estimand_scale_sensitivity_v1.csv`
- `scripts/check_estimand_scale_sensitivity.py`
