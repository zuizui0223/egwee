# ML016 / PS021 white spruce 2006 cluster-recovery contract

**Locked:** 2026-09-15 before stand-level reproductive-success values are opened.

## Goal

Test whether the paired 2006 white-spruce studies by O'Connell, Mosseler and Rajora can supply a fifth independent primary fragmented-versus-reference multilayer cluster without changing the frozen EGWEE effect-unit or effect-family rules.

The programme consists of:

- O'Connell et al. (2006), *Impacts of forest fragmentation on the reproductive success of white spruce (Picea glauca)*, Canadian Journal of Botany 84:956–965, DOI `10.1139/b06-051`;
- O'Connell et al. (2006), *Impacts of forest fragmentation on the mating system and genetic diversity of white spruce (Picea glauca) at the landscape level*, Heredity 97:418–426, DOI `10.1038/sj.hdy.6800886`.

Both papers use the same northern-Ontario agricultural landscape, the same 23 sampled white-spruce stands, the same August–September 1994 cone collection and the same 104 maternal trees. The reproductive paper supplies seed-production outcomes; the Heredity paper supplies stand-level mating-system estimates.

## Discovery-stage disclosure

This recovery is **not** described as a fully outcome-blind preregistration. During candidate screening, the source-defined stand-size classes and some stand-level `t_m` values from the Heredity Table 1 became visible, and the published direction that filled seeds per cone increase with stand size was already known.

However, before the stand-level reproductive-success vector is opened, this contract fixes:

- the primary binary contrast;
- the independent unit;
- the two primary endpoints;
- the effect orientation and variance convention;
- the within-cluster covariance rule;
- all no-rescue and terminal rules.

No endpoint or contrast may be changed after the reproductive stand values are inspected.

## Source-defined fragmentation contrast

The source divides the 23 stands into three stand-size classes differing by an order of magnitude:

- **small:** `1 <= N < 10` reproductive trees;
- **medium:** `10 <= N < 100`;
- **large:** `N >= 100`.

The primary direct contrast is prospectively fixed as:

- fragmented = **small stands**;
- reference = **large stands**.

Medium stands are excluded from the primary Hedges-g contrast and retained only as source context / sensitivity information. They cannot be added or removed after seeing endpoint values.

This uses a source-defined binary extreme-class comparison rather than constructing a post-hoc threshold.

## Independent-unit firewall

Primary independent unit = **stand**.

Expected source counts are 11 small stands, 6 medium stands and 6 large stands. Trees, cones, seeds, embryos, megagametophytes, loci and repeated measurements are nested below stand and can never increase fragmentation `n`.

The primary effects are admissible only if each selected endpoint is recoverable as one value per stand on the same small-plus-large stand frame. Tree-level means cannot be treated as independent fragmentation replicates merely because the source sampled multiple trees per medium/large stand.

## Locked biological endpoints

### G_mating — stand multilocus outcrossing rate `t_m`

Primary mating-support endpoint = stand-level multilocus outcrossing rate `t_m` from Heredity Table 1.

Orientation is direct: higher `t_m` = greater outcrossing / mating support. Primary effect is fragmented-minus-reference Hedges g, so a negative value indicates lower mating support in small stands.

Do not switch after opening values to `t_s`, `t_m-t_s`, family selfing, primary selfing, correlated paternity, pollen-pool differentiation, genetic diversity or another mating/genetic metric.

### F — stand mean filled seeds per cone

Primary reproductive-function endpoint = stand-level mean number of **filled seeds per cone** from the reproductive-success study.

Higher filled-seed production = greater reproductive function. Primary effect is fragmented-minus-reference Hedges g, so a negative value indicates poorer seed production in small stands.

Do not switch after opening values to total seeds, empty-seed proportion, germination, seedling growth, ten-year growth, seed efficiency or another reproductive metric.

## Effect representation

For each endpoint, calculate Hedges g using the stand-level values in the small and large classes and the repository's canonical direct-contrast convention equivalent to `metafor::escalc(measure="SMD", vtype="LS")`:

- fragmented group = small stands;
- reference group = large stands;
- `n` = number of stands, never number of trees/seeds;
- effect orientation fixed as support/function, with higher endpoint values already meaning better biological support.

Both endpoints must be finite and have effect-unit-valid small/large stand vectors before ML016 can be admitted.

## Within-cluster dependence

The mating and reproductive effects arise from the same sampled stands and cannot be treated as independent.

If exact stand-level `t_m` and filled-seed values are both available on the same small-plus-large stand frame:

1. center each endpoint within the source-defined small/large groups;
2. calculate the Pearson correlation between the two centered stand-level residual vectors;
3. use that correlation as the transparent sampling-covariance proxy;
4. set `V_GF = r_GF * sqrt(v_G * v_F)`;
5. require the resulting 2x2 working covariance matrix to be finite and positive definite.

Covariance may not be set to zero merely because exact sampling covariance is unavailable. No ridge is added solely to obtain invertibility.

## Admission rule

ML016 becomes an `admissible_multilayer_cluster` only if all of the following hold:

1. the two papers are confirmed to use the same 1994 stand programme;
2. exact stand identities/classifications are recoverable;
3. exact stand-level `t_m` is recoverable for all admitted small/large stands;
4. exact stand-level filled seeds per cone is recoverable for the same admitted stand frame;
5. both Hedges-g effects pass the stand-level effect-unit contract;
6. the 2x2 dependence proxy is reconstructable and positive definite.

Significance, direction and whether the new cluster changes the cross-system Fisher decision are **not** admission criteria.

## No-rescue rules

Do not:

- digitize a figure to manufacture the stand-level filled-seed vector;
- use the published nonlinear regression equation to generate predicted filled-seed values and call them observations;
- replace filled seeds with an easier reproductive endpoint after source inspection;
- replace `t_m` with a mating metric that happens to show a stronger stand-size response;
- treat 102/104 maternal trees as fragmentation replicates;
- combine medium stands with small or large after seeing effects;
- use stand size itself as a response;
- code source nonsignificance as effect zero;
- select or reject ML016 because it improves or weakens leave-one-cluster-out significance.

## Terminal outcomes

- `ML016_admitted_Gmating_F_covariance_aware`;
- `reproductive_stand_vector_not_reconstructable`;
- `mating_stand_vector_not_reconstructable`;
- `same_stand_frame_not_reconstructable`;
- `stand_level_covariance_not_reconstructable`;
- `stand_level_covariance_not_positive_definite`;
- `source_programme_identity_not_confirmed`.

All terminal outcomes are retained. If public text exposes only a fitted relationship, class summary, figure or tree-level observations without exact stand-level F values, recovery stops rather than manufacturing a fifth primary cluster.
