# Preregistration — Toronto residual urban-context replication

## Purpose

N2 identified `U_TORONTO_2025` as the only audited system whose public metadata explicitly co-locate upstream urban context, direct visitation with effort, focal floral support, realised reproduction and a stable garden/species key in one reusable table. This analysis is a new independent within-system residual-context replication. It does not rescue the stopped urban–island comparison and does not count four phytometer species as four independent systems.

The question is:

> After conditioning on a prospectively fixed partial pollination-process state, do urban cover and green-space edge density retain reproducible held-out predictive information for realised seed production across gardens?

The target is residual context information, not a signed urbanization effect.

## Locked source

- Source dataset: Sookhan, Onuferko & MacIvor 2025, Dryad `10.5061/dryad.b8gtht7r4`.
- File: `data.csv`.
- Ecological holdout unit: `site_id` (community garden).
- Source design: four phytometer species deployed across ten gardens; `P. hirsutus` occurs at eight gardens, the other species at ten.

Public README/schema information may be used before outcome access. Published effect directions, fitted coefficients and p-values are not model-selection inputs.

## Frozen variable mapping

### Proximal partial state

`I_visit = number_of_visits / survey_effort`

This is the only direct interaction-intensity coordinate. `qD_0` and `qD_2` are not substituted into the primary state after seeing outcomes.

Local focal support:

- `floral_units_array` = mean floral units in the deployed phytometer array.

Local floral-community support is matched to deployment phenology before outcome access:

- `PEHI` (`Penstemon hirsutus`, deployed 19 Jun–9 Jul) -> `floral_richness_1` (27–30 Jun survey);
- `DECA` (`Desmodium canadense`, deployed 15 Aug–8 Sep) -> `floral_richness_2` (20 Aug–9 Sep survey);
- `LOSI` (`Lobelia siphilitica`, deployed 23 Aug–9 Sep) -> `floral_richness_2`;
- `SYNO` (`Symphyotrichum novae-angliae`, deployed 18 Sep–7 Oct) -> `floral_richness_3` (7 Oct survey).

Call this row-wise variable `garden_richness_matched`.

### Upstream context

- `urban_cover` = percent urban land cover within 500 m;
- `ugs_edge_density` = urban-green-space edge density within 500 m.

These are tested only after the partial process state is fixed.

### Primary realised-function endpoint

`number_seed`, total seeds pooled across measured fruits.

`fruit_sample_size` is the exposure/denominator. The primary likelihood is Poisson with log link and `log(fruit_sample_size)` as an offset, matching the source response semantics. If any row has `fruit_sample_size <= 0`, that row is ineligible for the primary endpoint for a source-defined denominator reason, not an outcome-direction reason.

Secondary endpoints may be reported descriptively after the primary analysis, but they do not redefine the decision:

- `mass_seed_mg`;
- `mass_per_seed_ug`.

No favourable endpoint is promoted after outcome access.

## Frozen models

Species identity is retained as a fixed categorical baseline term because the four phytometers differ in morphology, phenology and breeding biology and are repeatedly measured across gardens.

Primary nested comparison:

`M0: number_seed ~ species_phytometer + I_visit + floral_units_array + garden_richness_matched + offset(log(fruit_sample_size))`

`M1: number_seed ~ species_phytometer + I_visit + floral_units_array + garden_richness_matched + urban_cover + ugs_edge_density + offset(log(fruit_sample_size))`

No `urban_cover × species` or `edge_density × species` interaction is opened in the primary test. Adding interactions after seeing the outcome is prohibited. The purpose is transferable residual context, not reproduction of source-paper species-specific significance tests.

All continuous predictors are standardized from the training fold only. The offset is never standardized.

If Poisson fitting fails numerically in a held-out fold, the analysis stops and records `primary_model_not_identifiable`; it does not switch likelihood after viewing performance. Overdispersion alone is not a post-hoc licence to change the primary model. A negative-binomial sensitivity may be designed only as a separately declared future analysis after the primary decision is frozen.

## Validation

Validation is leave-one-garden-out (LOGO): all rows for one `site_id` are held out together.

The inferential/validation unit is the garden. Species rows sharing a garden are never counted as independent systems or independent origin replicates.

For each held-out garden, fit `M0` and `M1` on all other gardens and score the held-out seed counts with the Poisson log predictive density under the fitted exposure offset.

Primary comparison statistic:

`delta_NLL = NLL(M1) - NLL(M0)` summed across all held-out rows.

- `delta_NLL < 0` means adding upstream urban context improves held-out prediction;
- `delta_NLL >= 0` means no held-out gain is demonstrated.

Also report garden-level paired `delta_NLL` values and their bootstrap 95% interval by resampling gardens. The bootstrap unit is the garden, not rows or species.

Decision labels:

- `residual_urban_context_information_detected` only if total `delta_NLL < 0` and the 95% garden-bootstrap interval is entirely below zero;
- `no_detected_residual_urban_context_information` otherwise;
- `primary_model_not_identifiable` if the preregistered primary model cannot be fit/evaluated across the declared folds.

This is not an equivalence test. Failure to detect gain does not prove urban context is biologically irrelevant.

## Response firewall and stop rules

Before this preregistration is committed, do not inspect values of `number_seed`, `mass_seed_mg`, `mass_per_seed_ug`, fitted outcome models, correlations with reproduction, or published coefficient direction for the purpose of choosing models.

After outcome access, do not:

1. change `I_visit` to `qD_0`, `qD_2`, richness or another predictor because it performs better;
2. drop one phytometer species because its direction is inconvenient;
3. choose a different floral-richness survey after seeing outcomes;
4. add context-by-species interactions to rescue a residual-context result;
5. change the holdout unit from garden to row/species;
6. change the primary endpoint from `number_seed` because another endpoint is favourable;
7. interpret a non-significant or non-improving result as equivalence or biological absence;
8. use this one urban system as evidence for urban–island convergence.

## Claim ceiling

A positive result would show only that, in this independent Toronto garden system, the measured urban landscape context contains reproducible predictive information beyond the declared partial pollination-process state.

A negative result would show only that this residual information was not detected under the declared representation and held-out design.

Either outcome contributes one additional independent empirical case to the measurement-order rule:

`proximal state adequacy -> representation preservation -> residual upstream context`.
