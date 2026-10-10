# CFTQ0065 / BDFFP seed-rain C-F recovery contract — 2026-09-24

## Audit status

Programme identity: `P2_CF01_BDFFP_SEED_RAIN_2020`.

Sources:

- Hooper & Ashton (2020), *Ecological Applications* 30:e02093, doi:10.1002/eap.2093;
- public Dryad dataset doi:10.5061/dryad.612jm640h.

This is a **retrospective external recovery**. The article abstract and source-reported qualitative direction were visible before this contract was committed. No outcome-blind discovery claim is made. The rules below are fixed before EGWEE opens or calculates plot-level effect values.

## Study geometry

The source uses eleven 1-ha sampling plots:

- three plots in three distinct 1-ha fragments;
- two plots in 10-ha fragments;
- two plots in 100-ha fragments;
- four continuous-forest control plots.

The source explicitly treats the design as replicated with respect to fragment size at the **plot level**.

Each plot contains eight seed traps sampled repeatedly over two years. Trap, census, seed, species and functional-trait rows are nested below plot and never increase fragmentation n.

## Primary fragmentation contrast

The primary EGWEE direct contrast is fixed as:

- **fragmented:** every source plot located in an isolated 1-ha, 10-ha or 100-ha forest fragment;
- **reference:** every source continuous-forest control plot.

Expected independent-unit counts are therefore `n_fragmented=7` and `n_reference=4`, subject only to verifying the public table contains all eleven source plots.

No fragment-size class is selected or removed because of its response.

The ordered 1/10/100-ha size structure is retained for a secondary generalisation check only. It does not replace the primary direct contrast after results are calculated.

## Locked response layers

### C — seed movement/connectivity

Primary C is **plot-level density of dispersed tree seeds**, pooled across the eight traps and the full source census window.

This maps to `C_movement_connectivity` because the source explicitly classifies these seeds as having been dispersed before capture.

### F — reproductive function

Primary F is **plot-level density of undispersed tree seeds**, on the same plot and census frame.

This maps to `F_reproductive_function` as realised local seed production.

The primary pair uses the broadest common all-tree scope for both layers. A non-pioneer-only matched pair may be retained as a prespecified sensitivity **only if the public files provide the same taxonomic filter for both dispersed and undispersed seed densities without outcome-dependent reconstruction**.

Species richness, functional diversity, functional composition and individual trait classes are not substituted for the primary density endpoints.

## Plot aggregation

Use the public source's plot-level density table if it already contains one row per plot and endpoint.

If only trap-level values are present:

1. reproduce the source rule of summing the complete two-year census within trap;
2. aggregate the eight traps to the source 1-ha plot;
3. construct one C value and one F value per plot;
4. stop if the eleven source plots cannot be reconstructed unambiguously.

Do not use 88 seed traps as fragmentation replicates.

## Effect-size contract

For C and F separately:

1. form the seven fragmented plot values and four continuous-control plot values;
2. calculate Hedges `g` for `fragmented - continuous`;
3. use the canonical EGWEE large-sample Hedges-g variance;
4. retain the raw direction and orient negative values as lower movement/reproductive function under fragmentation.

The primary calculation uses source-scale plot density. A log1p density analysis may be reported as a sensitivity, but it cannot replace the primary result because of significance or effect size.

## C-F dependence

C and F share the same eleven plots.

Reconstruct the working covariance exactly as in the existing direct paired-unit contracts:

1. group-center C and F separately within fragmented and reference conditions;
2. calculate Pearson `rho_CF` across the eleven group-centered paired plot observations;
3. set `cov(g_C,g_F) = rho_CF * sqrt(v_C * v_F)`;
4. require the 2x2 working covariance matrix to be positive definite;
5. require `Var(g_C - g_F) > 0`.

The covariance is labelled a reconstructed working proxy rather than an exact analytic sampling covariance.

## Admission gate

Promote this programme to the direct C-F family only if:

1. all eleven source plots are recoverable;
2. dispersed and undispersed density endpoints are available on the same plot frame;
3. plot is retained as the independent fragmentation unit;
4. both marginal Hedges-g effects and their working covariance are reproducible;
5. the C/F endpoint mapping above is applied without post-result substitution.

Admission is based on effect-unit validity, not direction or significance.

If admitted, this programme contributes **one** independent C-F programme. It never counts fragment-size classes, plots, traps or seed categories as separate programmes.

## No-rescue rules

Do not:

- choose only the fragment size with the largest response;
- exclude one fragment-size class after seeing outcomes;
- treat seed traps as independent fragmentation units;
- switch density to richness or functional diversity because it gives a stronger contrast;
- use a taxonomic/trait subset unless it is the prespecified matched non-pioneer sensitivity;
- reinterpret dispersed-seed density as pollination interaction;
- use the published fold-change as the EGWEE effect when plot-level data are recoverable;
- convert the primary direct pair into the gradient stream to rescue a failed direct contrast.

## Terminal outcomes

- `bdffp_direct_CF_covariance_aware`;
- `bdffp_plot_frame_incomplete`;
- `bdffp_common_CF_density_frame_not_reconstructable`;
- `bdffp_C_endpoint_not_movement_identifiable`;
- `bdffp_F_endpoint_not_local_production_identifiable`;
- `bdffp_covariance_not_positive_definite`.

All outcomes are retained.
