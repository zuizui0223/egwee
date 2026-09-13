# ML015 / Eucalyptus wandoo 2018 gradient-recovery contract

## Goal and protocol tier

Recover the multilayer fragmentation-gradient geometry in Llorens et al. (2018), *Frontiers in Ecology and Evolution* 6:39, DOI `10.3389/fevo.2018.00039`, without promoting a continuous-gradient study into the frozen primary fragmented-versus-reference Hedges-g denominator.

The source sampled 19 populations across a highly fragmented agricultural landscape and measured three fragmentation descriptors: population size, isolation and shape/edge dominance. It does not supply an unfragmented/reference group. Under `META_ANALYSIS_PROTOCOL_2026-09-11.md`, continuous gradients belong to the separate Fisher-z generalisation stream, not the primary Hedges-g stream.

ML015 therefore cannot become the fourth primary Hedges-g cluster. It may contribute a three-layer gradient generalisation/sensitivity cluster if the quantitative and dependence gates below pass.

## Discovery-stage disclosure

This candidate was identified by reading the public article tables. Aggregate response values and qualitative directions were visible before this recovery contract was written. ML015 is not described as an outcome-blind preregistration.

The composite severity axis is nevertheless constructed from exposure variables only. It is an EGWEE analysis construct from source-defined fragmentation descriptors, not a scalar exposure defined by the source. For that additional reason it is retained in the separate gradient-generalisation tier rather than used to enlarge the primary confirmatory denominator.

## Independent-unit frame

Independent unit = population. Maternal plants, fruits, pollen tubes, loci, alleles and progeny remain nested below population.

The paired multilayer frame is the intersection of populations with all three locked response layers. Missing populations are excluded only by that complete-case rule.

## Locked fragmentation-gradient axis

Construct one response-free severity PC from the 19-population Table 1 exposure matrix:

1. `smallness = -log10(population_size)`;
2. `isolation = sqrt(source_isolation)`;
3. `edge = log10(population_shape)`.

Standardize all three across all 19 populations with sample SD (`ddof=1`), perform ordinary PCA on their covariance matrix, choose PC1, and orient its sign so the sum of loadings on the three severity-oriented variables is positive. Standardize the resulting PC1 scores across all 19 populations. The PCA is never recomputed on the response-complete subset.

Do not substitute population size alone, isolation alone, shape alone, soil EC/salinity, PLS or another response-optimized axis after outcomes are inspected.

## Locked biological layers

Common-frame endpoints are:

- `I_pollination`: mean pollen tubes at the base of the style, Table 6;
- `F_reproductive_function`: mean seeds per fruit in year 2, Table 6;
- `G_adult`: unbiased expected heterozygosity `H_e`, Table 7.

Endpoint identities are not changed after effect calculation.

## Frozen effect representation

The repository effect schema already fixes continuous gradients to `fisher_z_gradient`. For each endpoint on the same complete-case population frame:

1. calculate Pearson `r` between fixed fragmentation severity and the endpoint;
2. calculate `z = atanh(r)`;
3. use the canonical Fisher-z marginal sampling variance `1/(n-3)`;
4. retain the existing orientation: larger severity = stronger fragmentation, so negative z means lower biological support/function with fragmentation and positive z means an increase.

Do not use standardized OLS slopes as a new effect stream and do not convert these Fisher-z effects to Hedges g.

## Within-cluster dependence

The three effects share the same populations. Follow the pre-existing covariance hierarchy rather than treating them as independent:

1. fit an intercept plus the fixed severity score separately to each raw endpoint on the common population frame;
2. retain the three population-level residual vectors;
3. calculate their 3x3 residual-correlation matrix `R`;
4. combine it with the audited marginal Fisher-z variances using `V_ij = R_ij * sqrt(v_i*v_j)`;
5. require finite diagonals and a positive-definite working `V` matrix.

This is an approximate reconstructed covariance proxy, not an exact sampling covariance. It is labelled accordingly. Covariance is never set to zero and no numerical ridge is added solely to obtain invertibility.

## Admission labels

If the Fisher-z effects and covariance are valid, ML015 is labelled `gradient_generalisation_multilayer_cluster`. This means:

- the three `fisher_z_admissible` effects can be used in the separately analysed gradient/generalisation stream;
- ML015 does **not** increment `admissible_primary_layers` or `n_admissible_primary_effects` in the primary Hedges-g denominator;
- the primary confirmatory denominator remains the independently admitted binary/contrast clusters.

## No-rescue rules

Do not select a single fragmentation variable based on response direction, change endpoints, drop complete-case populations, treat source nonsignificance as zero, use lower-level observations as population n, mix Fisher z with Hedges g in one pooled effect scale, or relabel this discovery-exposed composite gradient as an outcome-blind primary contrast.

## Terminal outcomes

- `ML015_gradient_generalisation_I_F_Gadult_covariance_aware`;
- `common_population_frame_insufficient`;
- `fragmentation_pc_not_identifiable`;
- `gradient_covariance_not_positive_definite`;
- `published_population_values_incomplete`.

All outcomes are retained.
