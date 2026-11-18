# CFTQ0272 / Coffea Sulawesi forest-distance I-F recovery contract — 2026-09-25

## Programme

Programme identity: `P2_CF01_COFFEA_SULAWESI_2003`.

Primary source: Klein, Steffan-Dewenter & Tscharntke (2003), *Journal of Applied Ecology*
40:837–845, doi:10.1046/j.1365-2664.2003.00847.x.

This is a **retrospective external recovery**. Published response directions were visible before this
contract was written. The contract therefore fixes one deterministic recovery rather than claiming
outcome-blind confirmation.

## Independent unit

Independent unit = **agroforestry system/site**.

The source uses 15 coffee agroforestry systems. Three focal coffee plants per system and all
within-plant flower observations are nested below site and never increase landscape n.

## Locked exposure

Primary landscape exposure = **distance to nearest old-growth rainforest / forest margin**.

Higher distance = stronger isolation from natural forest.

The source also measures light intensity, coffee blossom cover, non-coffee blossom cover and
flowering-plant richness. These remain local covariates/moderators and cannot replace forest distance
after response values are opened.

No thresholding of distance is allowed.

## Locked I endpoint

Primary I = **total coffee flower-visiting bee abundance / visitation under the standardized source
observation effort**, aggregated to one value per agroforestry system.

The broad all-bee endpoint is chosen to avoid post hoc selection between social and solitary bee
guilds. Guild-specific abundance/species-richness responses are retained only as sensitivities or
mechanistic descriptors.

## Locked F endpoint

Primary F = **open-pollinated coffee fruit set** at site level.

Bagged flowers and manually cross-pollinated flowers are pollination-efficiency controls. They do not
replace the natural open F endpoint.

## Common frame

Use only sites with:

1. forest distance;
2. primary total-bee I;
3. open fruit-set F.

Missing sites are not imputed. The exact common site count is determined mechanically before
correlations are calculated.

## Effect representation

This programme belongs to the Fisher-z gradient/generalisation stream.

For I and F separately:

1. calculate Pearson `r` against distance to forest;
2. calculate `z = atanh(r)`;
3. use variance `1/(n_site - 3)`;
4. negative z means lower interaction/function with greater forest isolation.

Do not convert distance to a binary near/far contrast.

## I-F dependence

On the common site frame:

1. regress I and F separately on forest distance;
2. retain site-level residuals;
3. calculate `rho_IF`;
4. set `Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F)`;
5. require a positive-definite working covariance block.

If valid marginals are recoverable but paired site values are not, do not set covariance to zero;
retain the programme under the already-frozen cluster-robust fallback only if the cross-system
analysis supports that representation.

## Admission

Admit one gradient/generalisation programme only if the authoritative public/source material exposes:

- the 15 site identities or an unambiguous common subset;
- forest distance per site;
- total-bee visitation/abundance per site;
- open fruit set per site;
- a valid common-site frame with at least four sites.

## No rescue

Do not:

- choose social bees because distance to forest is strongest for that guild;
- choose solitary bees because another local variable is stronger;
- replace forest distance with shade or blossom cover after inspecting outcomes;
- count three coffee plants/site as independent landscape units;
- back-transform selected stepwise-model coefficients into a new effect family without a separate
  frozen conversion rule;
- treat this programme as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `coffea_gradient_IF_covariance_aware`;
- `coffea_site_level_distance_not_recoverable`;
- `coffea_site_level_total_bee_I_not_recoverable`;
- `coffea_site_level_open_fruit_set_not_recoverable`;
- `coffea_common_site_frame_insufficient`;
- `coffea_covariance_not_positive_definite`.

All outcomes are retained.
