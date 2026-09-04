# E1 preregistration — Honshu–Izu ecological state residual-origin test

## Status and source lock

This is a **prospective analysis declaration written before inspecting the downloaded Figshare archive schema or refitting the data**. The source is fixed to Hiraiwa & Ushimaru (2024), Figshare item/version `10.6084/m9.figshare.25025000.v1` (`article_id=25025000`, version 1).

The purpose is to test the empirical counterpart of the state-sufficiency hypothesis at the **ecological partial-state layer**. It does not test genetics, pollen/seed connectivity, reproductive assurance or full urban–island convergence.

## Question

> After conditioning on the measured functional interaction state, does mainland/island origin or distance from the mainland still improve prediction of realised pollination function?

The test is not whether geography has a significant coefficient in isolation. Geography is already known to predict several upstream network properties. The question is whether it retains **out-of-sample predictive information after the functional state is supplied**.

## Observation structure

The published design contains eight sites surveyed in five seasons (40 site-season networks). Pollination success was measured as pollen receipt on stigmas for focal plant species and standardized within species. Site and survey identities were used as repeated/random structure in the source analysis.

The analysis must preserve site and season identities. Rows from the same site are never treated as independent held-out units.

## Candidate ecological state

The candidate E1 state is fixed prospectively as the smallest set directly motivated by the published results:

- community-level trait matching;
- pollinator functional diversity `FD_Q`;
- pollinator functional evenness `FEve`;
- season/survey identity;
- focal-plant identity / taxonomic structure where present in the archived pollination-success table.

Pollinator species richness is retained only as a **coarse-state comparator**, not as part of the primary sufficient-state candidate, because the published analysis did not support it as a direct predictor of trait matching or community-level pollination function.

No new network metric is selected after viewing the residual-origin result.

## Primary response

Primary response: the archived standardized pollen-receipt / pollination-success outcome used in the published functional analysis.

If the archive contains both species-level and community-level response tables, the **species-level standardized pollen-receipt table is primary** because it retains the largest number of direct function observations and the original analysis structure. A community-level aggregation may be reported secondarily but cannot replace the primary result after outcomes are seen.

## Model sequence

The exact archived column names will be mapped after discovery, but the semantic model sequence is fixed now.

### E1-C0 — coarse ecological model

`pollination_function ~ pollinator_species_richness + season + focal_plant_structure`

Purpose: benchmark the habitat/species-count description.

### E1-C1 — candidate functional-state model

`pollination_function ~ trait_matching + FD_Q + FEve + season + focal_plant_structure`

Purpose: represent the measured interaction/trait state before adding geography.

If `FD_Q` or `FEve` is absent from the same row-level response table and cannot be joined uniquely by site × season without ambiguity, it is omitted **for synchronization reasons**, with the omission recorded. It is not imputed from figures or medians.

### E1-C2 — residual-origin model

`E1-C1 + mainland/island origin and/or distance_from_mainland`

- If both origin and distance are directly available, distance is the primary geography term because it is the continuous upstream gradient used in the source paper; origin is a secondary sensitivity term.
- If only one is directly reconstructable from the locked source files, that term is used and the limitation is recorded.
- Island area is not added to rescue a residual effect; the published best models did not retain area for the audited network metrics.

### E1-C3 — interaction sensitivity only if pre-existing in source code

A geography × functional-state interaction is evaluated only if the archived source code already contains an equivalent interaction hypothesis or if required to reproduce a published model structure. It is not opened because C2 is weak or strong.

## Validation design

Primary validation is **leave-one-site-out** cross-validation (8 folds). Every observation from the held-out site is excluded from model fitting in that fold.

Within each fold:

1. fit C0, C1 and C2 on the remaining sites;
2. predict the held-out site's pollination-function observations;
3. retain prediction error and calibration summaries at both row and site level.

Primary predictive score: mean squared prediction error on the standardized response. Secondary summaries: mean absolute error and held-out correlation when defined.

Because there are only eight sites, no arbitrary train/test split is used and no fold is dropped because it is inconvenient.

## Decision rule

The conclusion concerns predictive information, not a fixed p-value threshold.

- **ecological_partial_state_convergence_supported**: C2 does not provide a reproducible material improvement over C1 across leave-one-site-out folds, and geography does not remove a systematic held-out residual pattern.
- **ecological_partial_state_incomplete**: adding geography produces a consistent held-out predictive improvement or corrects a systematic origin/distance residual pattern.
- **not_identifiable_from_archive**: the response and state variables cannot be joined at the required site × season × plant resolution, or the effective held-out structure is too sparse to compare C1 and C2 without inventing data.

A material improvement will be reported as the observed change in out-of-sample error with fold-level uncertainty/sensitivity; no effect-size threshold is tuned after seeing the result.

## Interpretation

If C2 improves prediction, the interpretation is **not** that `island` is itself a biological regime variable. It means the measured `I/T` state is incomplete at this scale. Candidate missing coordinates include partner movement, local resource context, reproductive assurance, genetic/mating state, or historical/memory variables.

If C2 does not improve prediction, the result supports only an **ecological partial-state convergence** for this coastal network system. It does not establish full eco-genetic convergence because `G/C/R/M` are not synchronously measured.

## Stop rules

Do not:

1. search additional network metrics until geography becomes negligible;
2. change the outcome definition after inspecting geography residuals;
3. collapse repeated site-season observations into independent pseudo-replicates;
4. infer missing genetic/connectivity variables from island distance;
5. add or remove islands/sites based on the result;
6. reinterpret a null geography coefficient as proof that all island histories are dynamically equivalent.
