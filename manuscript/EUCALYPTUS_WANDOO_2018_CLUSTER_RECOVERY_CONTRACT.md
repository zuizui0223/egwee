# ML015 / Eucalyptus wandoo 2018 cluster-recovery contract

## Goal

Attempt a fourth independent covariance-aware multilayer cluster from Llorens et al. (2018), *Frontiers in Ecology and Evolution* 6:39, DOI `10.3389/fevo.2018.00039`.

The source sampled 19 populations across a highly fragmented agricultural landscape and measured three source-defined fragmentation variables: population size, population isolation, and population shape/edge dominance. Pollination/reproduction were measured for a subset, and adult genetic diversity for all 19 populations.

## Discovery-stage disclosure

This candidate was identified by reading the public article tables. Aggregate source values and the qualitative directions of several source relationships were therefore visible before this ML015 recovery contract was written. ML015 is **not** described as an outcome-blind preregistration.

To prevent outcome-driven predictor selection despite that discovery exposure, the primary landscape axis is generated solely from the three source fragmentation variables, using all 19 populations and no biological response values. No single fragmentation variable is selected because it gives the strongest response.

## Independent-unit frame

Primary independent unit = population. Maternal plants, fruits, pollen tubes, loci, alleles and progeny are nested observations and cannot become fragmentation replicates.

The co-primary common frame is the intersection of populations with all three locked response layers below. Missing response populations are excluded only by that complete-case rule; no population is dropped because its direction is inconvenient.

## Locked fragmentation exposure

Construct an outcome-independent fragmentation-severity PC from the 19-population Table 1 exposure matrix.

Source-compatible transforms and orientations:

1. `smallness = -log10(population_size)`; smaller populations indicate greater fragmentation severity.
2. `isolation = sqrt(source_isolation)`; source isolation is `1 / percentage remnant vegetation within 3 km`, so larger is more isolated.
3. `edge = log10(population_shape)`; larger shape values indicate greater edge dominance/linearity.

Standardize the three transformed variables across all 19 populations with sample SD (`ddof=1`). Perform ordinary PCA on the 3x3 covariance matrix. Primary severity = PC1 score. Fix PC1 sign so the sum of its loadings on the three severity-oriented variables is positive. Standardize the final PC1 score across all 19 populations with sample SD.

The PCA is never recomputed on the response-complete subset and is never rotated or replaced after response values are joined.

## Locked biological layers

Common-frame endpoints:

- `I_pollination`: mean number of pollen tubes at the base of the style, Table 6. Higher values mean greater pollen receipt.
- `F_reproductive_function`: mean number of seeds per fruit in year 2 (`y2`), Table 6. Year 2 is locked because it shares the same Table 6 population frame with the pollen-tube endpoint and the source reports no significant overall year difference in mean seeds per fruit.
- `G_adult`: unbiased expected heterozygosity `H_e`, Table 7. Higher values mean greater standing adult genetic diversity.

For comparability across scales, each endpoint is standardized once within the locked common complete-case population frame using its observed mean and sample SD. Do not restandardize inside bootstrap samples.

Primary per-layer estimand = OLS slope of standardized endpoint on the fixed standardized fragmentation PC1. With severity increasing toward stronger fragmentation, negative slope means deterioration; positive slope means improvement/increase under fragmentation.

## Dependence and uncertainty

The three layer effects share the same populations. Preserve this dependence with a paired population bootstrap:

- resample the common-frame populations jointly with replacement;
- 10,000 draws;
- RNG seed `20260913`;
- fixed PC1 scores and fixed endpoint standardizations from the observed data;
- refit the three OLS slopes in every draw;
- store the full 3x3 bootstrap covariance matrix and percentile 95% intervals.

The cluster is admissible only if all three effects are finite and the estimated covariance matrix is positive definite. Significance is **not** required for cluster admission.

## No-rescue rules

Do not:

- choose population size, isolation or shape alone after observing outcomes;
- use soil EC/salinity as the primary fragmentation exposure;
- replace the exposure PC with a response-optimized PLS/canonical axis;
- switch I to flower number or a mating-system endpoint after observing results;
- switch F to fruit number, fruit:flower ratio, year 1 seed set or progeny performance after observing results;
- switch G from `H_e` to `P_L`, allelic richness or `F_IS` after observing results;
- use maternal-plant or locus counts as landscape n;
- omit a complete-case population because it weakens a layer effect;
- treat source nonsignificance as effect=0;
- set within-cluster covariance to zero.

## Terminal outcomes

- `ML015_admitted_I_F_Gadult_covariance_aware`;
- `common_population_frame_insufficient`;
- `fragmentation_pc_not_identifiable`;
- `covariance_not_positive_definite`;
- `published_population_values_incomplete`.

All outcomes are retained.
