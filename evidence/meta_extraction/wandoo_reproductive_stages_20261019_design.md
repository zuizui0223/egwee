# Wandoo reproductive-stage comparison: fixed analysis design

Design recorded: 2026-10-19 02:28:35 UTC, before fitting the conditional stage models or computing their leave-one-population-out predictions.

Source baseline: EGWEE PR 52 head `5a6754d2ca4053d8ecce54f57c28e965ea015fec`; Llorens et al. (2018), doi:10.3389/fevo.2018.00039, Tables 1 and 6.

This is a retrospective analysis. The source paper, its qualitative conclusions, and the existing EGWEE PC1 result were already known. A same-11-population comparison of PC1 against negative log10 population size was also calculated before this design. None of those observations make the present design an outcome-blind preregistration.

## Fixed question and frames

Does adding population size or soil salinity to pollen-tube quantity give different information about fruit production, fruit establishment, and seed filling?

Primary frame: the same 11 populations `J,K,F,C,E,G,B,I,A,H,D` for all three synchronous year-2 responses: fruits per branch, source mean fruit:flower ratio, and seeds per fruit. Interaction I is year-2 mean pollen tubes at the base of the style. The independent unit is population; maternal plants, flowers, and quadrats are nested measurements.

Required sensitivity: the source-native 12-population frame `J,L,K,F,C,E,G,B,I,A,H,D` for the two fruit responses. Population L produced no fruit. Its fruit values remain zero; its seeds per fruit remain undefined, never zero-imputed. This sensitivity is not an additional independent replication.

## Fixed models, transformations, and estimation

For every eligible frame and response, fit all three unweighted OLS models with an intercept:

1. `F ~ I`
2. `F ~ I + log10(population_size)`
3. `F ~ I + log10(EC_mS_per_m)`

All response and I values stay on their published raw mean scales. Log10 size and log10 EC are the only transformed quantities. No outcome-driven variable selection, interactions, threshold searches, added P model, or response transformations. Soil P and all other Table 1 quantities are retained for provenance, not tested as extra predictors here. Report every specified model.

Report coefficients, classical OLS standard errors and t intervals, R2, residual degrees of freedom, the added-variable partial R2 and unadjusted p. Apply Holm correction jointly to the six primary added-variable tests (three responses times two additions); native-12 p values are descriptive sensitivities. The analysis estimates conditional associations and does not identify causal mediation or an environmental mechanism.

## Supplementary prediction check

For each fixed model, leave one entire population out, refit on the others, and predict the held-out published population mean. Report raw RMSE and the fractional MSE improvement relative to I only within each endpoint/frame; do not compare raw RMSE between different endpoints. Save all held-out predictions and errors. No tuning or model selection uses held-out outcomes. These overlapping LOO folds are an internal small-sample sensitivity, not independent validation.

Record full-fit leverage and the population with the greatest leverage. For interpretability, report whether unbounded OLS predictions leave an endpoint's physical range; do not clip them after seeing the outcomes.

## Non-synchronous years and provenance

Restore all Table 6 values, including means, SE, source N, y1/y2/y3 labels, and missing entries. Pollen tubes were measured only in y2. Seeds per fruit y1 and fruits per branch y3 may receive descriptive correlations with log size and log EC and same-endpoint across-year correlations, but they are not fitted as synchronous I-F replications. Do not manufacture total seed output by multiplying published marginal means.

Restore all Table 1 environmental values for all 19 populations, retaining units, the source Table 1 isolation and shape definitions, and the published source. Save exact source-table text and provenance. Cross-check the CSV against the source-table text, the original PDF tables, and overlapping existing EGWEE values before interpretation. Preserve source N as reported; it is not a guarantee of identical year-specific effective N.

## Mathematical verification and claim boundary

Verify fitted coefficients, uncertainty, and predictions against an independent OLS implementation. Verify direct LOO refits against the analytical PRESS identity and check row-order invariance, frame membership, no zero imputation, and the existing PC1 estimates on the recovered overlap.

The original paper already reported soil-salinity associations with fruit production and population-size associations with year-2 seed filling. Reproducing those marginal associations is not a new mechanism. The additional contribution being tested is the comparison of information beyond the same I measure across distinct reproductive stages on a common population frame. A stage-specific pattern, if found, remains retrospective and single-system; significance in one stage and non-significance in another is not by itself a formal between-stage effect-difference test.
