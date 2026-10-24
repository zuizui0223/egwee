# CFTQ0142 / Acer miyabei retrospective gradient recovery rule — 2026-09-24

## Status and limitation

Programme identity: `P2_CF01_ACER_MIYABEI_2014`.

Primary source: Nagamitsu et al. (2014), *The American Midland Naturalist* 172:303–316,
doi:10.1674/0003-0031-172.2.303.

This is a **retrospective external recovery, not an outcome-blind or prospective test**. The
published Table 1 values and the paper's qualitative conclusions were visible during source audit
before this rule was written. The purpose of this rule is therefore not to manufacture a
confirmatory claim, but to make the recovery deterministic and to prevent selective use of the
source table after inspection.

## Source table and independent unit

Table 1 reports 21 forest fragments with:

- forest ID;
- distance to nearest forest;
- number of adult trees;
- mean DBH;
- seed-sampling effort;
- dispersed seed density;
- viable seed proportion;
- mean seed kinship coefficient where at least two genotyped seed samples were available.

EGWEE independent unit = **forest fragment**.

The 82 target trees, 237 quadrats, individual seeds, seed pairs and microsatellite comparisons are
nested below forest and never increase fragmentation n.

## Locked exposure

Primary fragmentation exposure = **log distance to nearest forest** from Table 1.

Higher log distance = stronger spatial isolation.

Adult-tree number and rural/urban context are biologically important source predictors but are not
substituted for the primary isolation axis after the table has been inspected.

## Locked C endpoint

Primary C = **gene-flow support = negative mean seed kinship coefficient**.

The source explicitly states that lower kinship among dispersed seeds is expected under higher gene
flow because foreign pollen or seeds reduce relatedness. Therefore:

`C_support = - mean_kinship`.

This sign definition is biological and source-based: larger C_support means greater realised
gene-flow support.

Forests with `NA` kinship remain missing and are not imputed.

## Locked F endpoint

Table 1 contains two direct reproductive quantities, seed density and viable seed proportion.
Rather than selecting one of those two visible outcomes, EGWEE deterministically combines them into
one realised viable-propagule output:

`F_viable_seed_density = seed_density_per_m2 * viable_seed_proportion`.

This quantity is the estimated density of viable dispersed seeds per square metre on the same
forest-level source table. It is a deterministic transformation of two source-reported F
components; it is not a source-modelled response and must be labelled as an EGWEE derived endpoint.

The raw seed-density and viable-proportion correlations are retained as descriptive sensitivities
and are not allowed to replace the primary derived F because one is more significant.

## Common frame

The primary C-F gradient uses every forest with non-missing:

1. distance to nearest forest;
2. mean seed kinship coefficient;
3. seed density;
4. viable seed proportion.

No forest is dropped for effect direction. Under Table 1 this common frame is expected to contain
nine forests; the recovery script must assert the exact forest IDs from the transcribed source
table before calculating effects.

## Effect representation

This programme belongs to the **Fisher-z gradient/generalisation stream only**.

For C and F separately:

1. compute Pearson `r` against `log(distance_to_nearest_forest_m)`;
2. compute `z = atanh(r)`;
3. use marginal Fisher-z variance `1/(n_forest - 3)`;
4. negative z means lower biological support/function with greater forest isolation.

Do not convert this programme to the primary Hedges-g fragmented/reference denominator.

## C-F dependence

On the exact common forest frame:

1. fit C and F separately on intercept + log isolation;
2. retain forest-level residuals;
3. calculate their Pearson residual correlation `rho_CF`;
4. set `Cov(z_C,z_F) = rho_CF * sqrt(V_C * V_F)`;
5. require the 2x2 working covariance matrix to be positive definite.

Report the covariance-aware `C - F` contrast with Normal confidence interval and p-value as a
retrospective generalisation result.

## Sensitivities retained without rescue

For the same common forest set, also report:

- source seed density alone;
- source viable seed proportion alone.

These are descriptive endpoint-definition sensitivities. They cannot replace the primary viable
seed density in the programme registry or be selected by significance.

## Admission

Admit one `gradient_generalisation_multilayer_cluster` only if:

- the Table 1 transcription is complete and source-located;
- the nine-forest common frame is reproduced exactly from missingness;
- all marginal Fisher-z values and the working covariance are finite;
- the covariance matrix is positive definite;
- forest remains the independent unit.

The programme contributes **zero** to direct I-F or C-F Hedges-g coverage.

## No-rescue rules

Do not:

- use 82 target trees or 237 quadrats as fragmentation n;
- impute missing kinship values;
- switch the primary exposure from isolation to adult-tree number or urban/rural class because a
  result is stronger;
- select seed density or viable proportion as primary after seeing their individual results;
- treat the derived viable seed density as if it had been the source paper's original response;
- call this retrospective recovery a prospective confirmation;
- use the result as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `acer_miyabei_gradient_CF_covariance_aware_retrospective`;
- `acer_miyabei_table1_transcription_mismatch`;
- `acer_miyabei_common_frame_not_reproducible`;
- `acer_miyabei_covariance_not_positive_definite`.

All outcomes are retained.
