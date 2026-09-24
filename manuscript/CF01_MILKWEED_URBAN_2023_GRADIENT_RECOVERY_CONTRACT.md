# CF01 common milkweed 2023 gradient recovery contract

## Programme identity

- programme: `P2_CF01_MILKWEED_URBAN_2023`
- target-pair queue record: `CFTQ0044`
- peer-reviewed article DOI: `10.1007/s11252-022-01278-9`
- preprint DOI: `10.1101/2022.03.11.483986`
- public analysis/data repository: `sbreitbart/observ_study_phenotype`
- source repository commit pinned for recovery: `83e56d790410a134fa099425459aefb6f2d07f12`
- repository/archive DOI declared by source README: `10.5281/zenodo.6985410`

This is a **retrospective external recovery**. Numerical source data are public and were inspected after the target-pair design screen. Endpoint and analysis rules below are therefore fixed before EGWEE effect calculation and cannot be changed because of the resulting sign, magnitude or p-value.

## Family

This programme belongs to the registered **Fisher-z gradient/generalisation** stream.

It does **not** increment the primary fragmented-versus-reference Hedges-g I-F denominator.

## Primary exposure

The source paper quantifies urbanization two ways and presents distance from Toronto's urban center as the main-text proxy, with UrbanizationScore as an alternative metric.

Primary EGWEE exposure:

`greater_urbanization = - City_dist_km`

so larger exposure values mean greater urbanization / greater urban landscape alteration.

`Urb_score` is retained as a source-defined sensitivity exposure only.

The green-corridor subtransect is a secondary landscape-configuration modifier, not substituted for the primary urbanization gradient after outcomes are examined.

## Independent unit and temporal frame

Primary independent unit = **milkweed population / patch (`Patch_ID`)**.

Pollinator visitation was measured in 2019. To maintain a contemporaneous paired I/F frame, the primary F endpoint is also restricted to **2019**.

Plants, flowers, inflorescences, follicles, pollinator observations and morphospecies are nested below population and never increase independent n.

## Primary I endpoint

Primary I = **population-level total pollinator abundance per surveyed plant in 2019**.

Reproduce the source code:

1. divide each morphospecies count (`MS_01`–`MS_42`) by `Plants_surveyed`;
2. sum the per-plant morphospecies counts to `total_indivs`.

The source analysis constructs `div_sum` from non-zero pollinator observations, so populations with zero recorded pollinators do not enter its abundance regression. The EGWEE **primary source-code-faithful** analysis preserves that behaviour.

A prespecified sensitivity restores valid surveyed populations with zero pollinator abundance.

## Primary F endpoint

Primary F = **fruit set, mean follicles per inflorescence**.

At plant level the source cleaning code defines:

`pods_per_ped = Total_Pods / Peduncles`.

For the independent-unit analysis, average `pods_per_ped` within each `Patch_ID` in 2019.

Only populations with a finite 2019 population mean enter the paired common frame.

## Gradient effect

For each endpoint on the same primary common populations:

- calculate Pearson `r(exposure, endpoint)`;
- transform `z = atanh(r)`;
- use `V(z) = 1/(n-3)`.

Positive values mean the biological endpoint increases with greater urbanization. Negative values mean it decreases with greater urbanization.

## I-F dependence

Fit separate endpoint-on-exposure linear regressions over the same population frame. Calculate the Pearson correlation `rho_IF` between the two residual vectors and use:

`Cov(z_I,z_F) = rho_IF * sqrt(V_I V_F)`.

The pair contrast is:

`Delta_IF = z_I - z_F`.

This covariance is a working paired-population proxy and is not interpreted as a fully identified sampling covariance from the original mixed models.

## Prespecified sensitivity

Repeat the identical population-level calculation while **retaining surveyed populations with zero pollinator abundance**. This diagnoses the consequence of the source-code filtering step.

The sensitivity cannot replace the primary source-code-faithful result because it yields a stronger or weaker contrast.

A second descriptive check may use source `Urb_score`, but it is not promoted to the primary exposure.

## Admission rule

Admit one gradient/generalisation programme only if:

- the public repository and pinned commit reproduce the endpoint construction;
- I and F share the same population-level primary exposure;
- population remains the independent unit;
- primary and zero-retaining sensitivity results are reproducible;
- no lower-level count is promoted to independent n;
- the programme remains outside the primary Hedges-g I-F denominator.
