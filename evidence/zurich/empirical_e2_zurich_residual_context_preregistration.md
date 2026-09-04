# E2 preregistration — Zurich urban interaction-state residual-context test

## Status and source lock

This declaration is written **before downloading or fitting the EnviDat pollination-success observations for this residual-context analysis**.

Sources are fixed to:

- Reji Chacko, Moretti & Frey (2025), EnviDat DOI `10.16904/envidat.676`;
- the public BetterBlooms analysis repository at commit `d6361f6874398e797322afe07a8fea85a3c7e927`;
- the six direct reproductive endpoints used in the source analysis.

The study contains 24 Zurich home gardens. The source reproductive analyses exclude garden `Id=39`; this exclusion is retained prospectively and is not reconsidered after outcomes.

This is an **ecological partial-state test**. Standardised phytometer plants intentionally remove natural among-population plant genetic state, so E2 cannot establish full `D/I/T/C/R/G/M/A` sufficiency.

## Question

> Within each focal plant/function, does measured pollinator-interaction state absorb the predictive information carried by local plant richness and 500-m urban intensity, or does urban context still improve held-out prediction of realised reproductive function?

The target is not a universal urban coefficient. The six focal functions are analysed separately because the published/source models show different guild and landscape responses among plant functions.

## Six fixed focal functions

1. *Daucus carota* seed set;
2. *Raphanus sativus* fruit set;
3. *Raphanus sativus* seed set;
4. *Onobrychis viciifolia* fruit set;
5. *Symphytum officinale* fruit set;
6. *Symphytum officinale* seed set.

No endpoint is removed because its urban or interaction result is weak.

## Fixed interaction-state predictors

The interaction predictor sets are copied from the **full abundance models in the locked BetterBlooms source code**, not selected from the new residual-context result.

### Carrot seed set

- honeybee (`A_Apis_Carrot`);
- social bees (`A_socialBees_Carrot`);
- solitary bees (`A_solitaryBees_Carrot`);
- other Aculeata (`A_otherAculeata_Carrot`);
- hoverflies (`A_Syrphidae_Carrot`);
- beetles (`A_Coleoptera_Carrot`).

### Radish fruit and seed set

- honeybee (`A_Apis_Radish`);
- social bees (`A_socialBees_Radish`);
- solitary bees (`A_solitaryBees_Radish`);
- hoverflies (`A_Syrphidae_Radish`).

### Sainfoin fruit set

- honeybee (`A_Apis_Sainfoin`);
- bumblebees (`A_Bombus_Sainfoin`);
- solitary bees (`A_solitaryBees_Sainfoin`).

The source analysis excludes gardens 19, 28 and 52 from the scored sainfoin model after excluding zero-assessed-inflorescence observations. The same rule is retained.

### Comfrey fruit and seed set

- bumblebee abundance (`A_Bombus_Comfrey`).

The original source represents this with the first component of a second-order orthogonal polynomial. For the held-out predictive audit, the same single biological axis is retained. Any polynomial basis is fitted from the training fold only so held-out observations do not determine the transformation.

## Predictor construction

Interaction abundance is divided by phytometer-specific sampling effort in days, following source script `3a_reproductive_succ_1_data_prep.R`.

All continuous predictors are centered/scaled **inside each training fold only** and then applied to the held-out garden using training-fold parameters.

No interaction guild is added or dropped after viewing E2 results. If a locked source predictor is absent from the exact EnviDat/BetterBlooms join, the endpoint is classified as `not_identifiable_from_archive` rather than silently changing the state.

## Model sequence

The observation-level response and distribution follow the source endpoint:

- carrot seed set: Poisson count;
- radish fruit set: binomial successes/failures;
- radish seed set: Poisson count;
- sainfoin fruit set: binomial successes/failures;
- comfrey fruit set: binomial successes/failures;
- comfrey seed set: binomial seeds/unfertilised ovules.

The cross-validation models use fixed-effect GLMs for out-of-garden prediction; they are a **predictive state audit**, not a claim to reproduce every nested random-effect estimate from the source paper.

### E2-S0 — coarse urban/context model

`F ~ PlantS + Urban_500 + PlantS × Urban_500`

This mirrors the source habitat model family and represents conventional local/urban context.

### E2-S1 — measured interaction-state model

`F ~ locked function-specific guild abundance predictors`

### E2-S2 — residual-context model

`F ~ locked guild predictors + PlantS + Urban_500 + PlantS × Urban_500`

Primary comparison: **E2-S2 versus E2-S1**.

If S2 improves held-out prediction, measured interaction state is incomplete with respect to urban/local context. If it does not, no residual urban/context information is detected at this ecological partial-state resolution.

## Validation unit

Primary validation is **leave-one-garden-out** cross-validation after all prospectively fixed source exclusions.

Every reproductive observation from the held-out garden is excluded from fitting and from predictor scaling.

No random split of flowers, branches, fruits or plants across train/test is allowed.

## Predictive score

For each held-out garden and model, compute the mean negative log predictive likelihood under the declared response family.

Define per-garden residual-context gain:

`Delta_g = NLL_S1,g - NLL_S2,g`

so positive values mean that adding urban/local context improved prediction.

Report:

- equal-garden-weighted mean and median `Delta_g`;
- fraction of held-out gardens with `Delta_g > 0`;
- garden-bootstrap 95% interval for mean `Delta_g`;
- secondary MAE on the natural response scale where comparable.

Each garden is one bootstrap unit. Observations within a garden are never resampled as independent landscapes.

## Per-function decision

- `ecological_partial_state_incomplete`: mean `Delta_g > 0` and the garden-bootstrap 95% interval is wholly above zero.
- `no_detected_residual_urban_information`: the interval includes zero or lies at/below zero; this is **not** proof of equivalence.
- `not_identifiable_from_archive`: required locked predictors/responses cannot be joined without imputation, incompatible identifiers or outcome-dependent modification.

No minimum effect-size threshold or alpha is tuned after observing results.

## Cross-function synthesis

Do not pool the six endpoints into one common urban coefficient.

Report the six decisions and predictive-gain distributions side by side. A mixture of outcomes is interpreted as **function-specific state sufficiency**, consistent with the source study's no-one-size-fits-all framing.

## Interpretation boundary

Even a clean E2 result addresses only the ecological partial state `local context + realised guild interaction -> reproductive function` in standardized plants. It cannot identify:

- natural plant genetic state;
- pollen/seed connectivity;
- mating-system variation;
- fragmentation-age/cohort lag;
- full urban–island eco-genetic convergence.

Those require the larger synchronized field state defined in `natural_state_field_protocol.md`.

## Stop rules

Do not:

1. choose guilds by the new residual-context result;
2. remove focal functions because S2 behaves differently;
3. tune an urban buffer scale after seeing E2 results (`Urban_500` is fixed from the source reproductive habitat models);
4. use individual flowers/fruits as independent validation folds;
5. reinterpret a non-detected S2 gain as proof that urbanization has no ecological effect;
6. add natural-genetic claims to standardized phytometer plants.
