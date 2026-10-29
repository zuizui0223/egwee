# SF06 conditional female-fitness offset audit — 2026-10-07

## Status

Post-exposure interpretation of the corrected preregistered regression. This note does not change the primary model and does not treat the intercept as a causal direct effect.

## Primary Hedges-d model

For the 49 habitat-fragmentation pairs with unambiguous SC/SI metadata:

`d_F = alpha + beta d_I + gamma SC`

Corrected estimates:

- alpha = **-0.4135**, 95% CI **[-0.7180, -0.1089]**, p = **0.00779**;
- beta_pollination = **+0.1904**, 95% CI **[+0.0565, +0.3243]**, p = **0.00531**;
- gamma_SC = +0.0639, unresolved.

Thus the fitted relationship has two simultaneous features:

1. female-fitness response becomes less negative as the pollination response becomes less negative / more positive;
2. at `d_I=0`, the fitted female-fitness response remains negative.

Predicted female-fitness effect at zero pollination effect:

- SI: **d_F=-0.413**;
- SC: **d_F=-0.350**.

## Observed pollination range

Across the 49 SC/SI fragmentation pairs:

- d_I range = **[-2.224, +2.034]**;
- median d_I = **-0.480**;
- 95th percentile ≈ +0.842.

On the fitted linear model, the pollination effect required to move predicted female fitness to zero is:

- SI: d_I ≈ **+2.17**;
- SC: d_I ≈ **+1.84**.

The SI threshold lies above the observed maximum. Only one SC pair exceeds its fitted threshold.

These threshold calculations are descriptive extrapolations of the fitted Hedges-d relationship, not biological intervention targets.

## Ecological interpretation

The negative conditional offset is compatible with the branching-pathway view:

fragmentation can affect female fitness through routes that are not summarized by the measured pollination response, including plant condition, mating provenance, post-pollination viability, reproductive assurance and later life-cycle interactions.

The same model still has a positive pollination slope, so this is **not** evidence that pollination is irrelevant. It is evidence that a one-dimensional pollination response is not a complete statistical state variable for female-fitness response on this representation.

## Important boundary

Hedges d standardizes different endpoints by their own dispersions. Therefore the intercept is **estimand-specific** and must not be interpreted as a scale-free causal “direct fragmentation effect”.

The source-publication-disjoint subset retains a negative intercept direction (about -0.47) but with wider uncertainty (p≈0.085), so external independence supports direction more strongly than precise magnitude.

## Claim ceiling

Allowed:

- on the source Hedges-d representation, a positive pollination–fitness slope coexists with a negative conditional female-fitness offset;
- this is consistent with multiple fragmentation pathways contributing to reproductive response.

Not allowed:

- the intercept is a causal direct effect of fragmentation;
- -0.413 is a scale-general biological deficit;
- all non-pollination pathways have been identified or measured.
