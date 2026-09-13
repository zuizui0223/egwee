# ML006 / PS016 Primula 2025 cluster-recovery contract

## Goal

Test whether Bohm et al. (2025), Biological Conservation 305:111044, DOI `10.1016/j.biocon.2025.111044`, can support one synchronized `G_adult / I_interaction / F_reproductive_function` cluster under a single source-defined landscape exposure.

## Locked common exposure

Primary exposure = percentage forest cover within a 1000 m radius around each focal population.

This scale is fixed before opening supplementary population values because:

- forest cover was measured prospectively at 250, 500, 750 and 1000 m around all 33 populations;
- the published F analysis for seed number per fruit specifically uses quadratic forest cover at 1000 m and population size;
- the pollinator candidate set explicitly includes quadratic forest cover at 1000 m as well as 750 m; 1000 m is therefore source-defined and not invented post hoc;
- choosing 750 m because it has the best I AIC would break the same-exposure rule with F.

Do not switch to 750 m, population size, habitat type, geographic region, or pollinator abundance as the cluster-defining exposure after outcomes are opened.

## Common population frame

Primary overlap = the 15 populations in which pollinator abundance was surveyed.

All three primary layer summaries must be recoverable for these same 15 population identities. The 33-population G/F dataset may be retained as context or sensitivity only; it cannot be combined with the 15-population I effect as if all 33 had I observations.

## Locked endpoints

- `G_adult`: nucleotide diversity `Pi` at population level. `PP` is retained only as a prespecified sensitivity and cannot replace Pi if its result is stronger.
- `I_interaction`: source pollinator abundance per 30-min survey at population level.
- `F_reproductive_function`: source seed number per fruit at population level.

## Locked response geometry

The paper prospectively expected forest effects to be positive or unimodal and fits quadratic forest-cover effects for F and I. To keep the biological exposure and response geometry identical across layers, primary reanalysis uses the same second-order exposure basis for each layer on the 15-population overlap:

`Y ~ forest1000_z + forest1000_z^2`

where `forest1000_z` is forest cover centered and scaled using the 15-population overlap only.

For each layer retain the ordered coefficient vector `(beta_linear, beta_quadratic)` and its 2x2 coefficient covariance. Do not collapse the quadratic response to a simple Pearson correlation or Fisher-z effect.

The cross-layer object is therefore a multivariate coefficient block, not a scalar grand mean. A layer is admissible only if both coefficients and their sampling covariance are estimable under the locked frame.

## Source opening order

1. inspect Elsevier supplementary package existence and format;
2. inspect supplementary headings/table schemas without selecting results;
3. determine whether exact identities and population-level forest1000, Pi, pollinator abundance, and seed number per fruit are jointly recoverable for the same 15 populations;
4. only if step 3 passes, materialize the fixed 15-population table and fit all three locked quadratic models in one run;
5. reconstruct cross-layer dependence from paired population-level estimating contributions or a transparent bootstrap if source granularity permits it.

## No-rescue rules

Do not:

- use PP as primary after seeing Pi;
- use forest750 because I fits better there;
- define G by population size while defining I/F by forest cover;
- treat individual plants, flowers, fruits, SNPs, visits, or loci as independent fragmentation replicates;
- infer unreported population values from fitted curves or figures;
- digitize figures to manufacture the common population table if exact supplementary values are absent;
- treat absence of a published G~forest model as a biological zero;
- set within-cluster covariance to zero by convenience;
- join another Primula study or campaign to fill a missing layer.

## Terminal outcomes

- `ML006_admitted_G_I_F_common_forest1000_quadratic`;
- `common_population_values_not_recoverable`;
- `common_exposure_values_not_recoverable`;
- `quadratic_effect_uncertainty_not_reconstructable`;
- `cross_layer_covariance_not_reconstructable`;
- `source_access_blocked`.

All outcomes are acceptable.
