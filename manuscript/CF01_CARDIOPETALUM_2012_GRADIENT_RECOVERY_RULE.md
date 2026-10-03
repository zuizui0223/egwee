# CFTQ0166 / Cardiopetalum retrospective gradient recovery rule — 2026-09-24

## Status and limitation

Programme identity: `P2_CF01_CARDIOPETALUM_2012`.

Primary source: Elias et al. (2012), *Journal of Tropical Ecology* 28:317–320,
doi:10.1017/S0266467412000120.

This is a **retrospective external recovery, not an outcome-blind test**. The source Table 1 values
and published directional results were visible during the audit before this rule was written.
The purpose is to make the recovery deterministic and prevent endpoint/exposure selection after
inspection.

## Independent unit

Table 1 reports **10 independent cerrado forest fragments** (F1–F10), spanning 2.16–929 ha.

EGWEE independent unit = **forest fragment**.

Marked plants, flowers, beetles, 30×30 m density plots, fruits and seeds are nested below fragment
and never increase fragmentation n.

## Locked primary exposure

Primary fragmentation severity = **negative natural log fragment area (ha)**:

`fragmentation_severity = -log(fragment_area_ha)`.

Higher values therefore mean smaller fragments / stronger habitat-area fragmentation.

Distance to the nearest fragment is retained as a source-defined **isolation sensitivity** only.
It cannot replace area as the primary exposure after the visible source results are inspected.

## Locked I endpoint

Primary I = **pollinator abundance per flower (ABP)** from Table 1.

The source defines this as total beetles found inside collected flower chambers divided by the
number of flowers collected within each fragment.

Use the Table-1 fragment mean only. Plants and flowers are not independent fragmentation units.

## Locked F endpoint

Primary F = **fruit set per flower (F)** from Table 1.

Fruit set is selected deterministically because it is the first direct reproductive-output endpoint
reported in the source table and is complete for all 10 fragments.

Two alternate source reproductive endpoints are retained as endpoint-definition sensitivities:

- follicles set per flower (FO), n=10;
- seed set per flower (S), n=9 because F10 is source-missing.

Neither sensitivity may replace primary fruit set because it gives a stronger result.

## Gradient effect representation

This programme belongs only to the Fisher-z gradient/generalisation stream.

For I and primary F separately:

1. calculate Pearson r against `-log(fragment_area_ha)`;
2. calculate Fisher z = atanh(r);
3. use variance `1/(10-3)`;
4. negative z means lower interaction/function in smaller fragments.

For the seed-set sensitivity use its source-complete n=9 frame and variance `1/(9-3)`.

The nearest-fragment-distance sensitivity is evaluated on all 10 fragments using
`log(distance_m)` as stronger isolation.

## I-F dependence

On all 10 fragments:

1. regress I and primary F separately on `-log(fragment_area_ha)`;
2. calculate residual Pearson `rho_IF`;
3. set `Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F)`;
4. require the 2×2 working covariance matrix to be positive definite;
5. report the covariance-aware `I - F` contrast.

The covariance is a reconstructed working dependence proxy, not an exact analytic sampling
covariance.

## Admission

Admit one `gradient_generalisation_multilayer_cluster_retrospective` only if:

- the 10 Table-1 fragment rows reproduce exactly;
- fragment is retained as n;
- I and fruit-set F are finite for all 10 fragments;
- the working covariance matrix is positive definite;
- source-missing seed set in F10 remains missing.

This programme contributes **zero** primary direct Hedges-g I-F programmes.

## No-rescue rules

Do not:

- use marked plants or flowers as fragmentation n;
- select fragment isolation instead of area because it gives a preferred result;
- select follicle set or seed set as primary F after seeing their correlations;
- impute F10 seed set;
- convert the continuous fragment-area series into arbitrary small/large bins for the primary result;
- call this retrospective recovery prospective confirmation;
- use this result as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `cardiopetalum_gradient_IF_covariance_aware_retrospective`;
- `cardiopetalum_table1_transcription_mismatch`;
- `cardiopetalum_covariance_not_positive_definite`.

All outcomes are retained.
