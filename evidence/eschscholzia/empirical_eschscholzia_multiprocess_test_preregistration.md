# Prospective Eschscholzia multi-process state-sufficiency test

## Status at registration

This is the required **second exact-model preregistration** following the schema-only decision `joint_state_identifiable` in PR #104.

At the time of this registration, the project has inspected only source metadata and the locked CSV headers/hashes. **No data row, outcome value, outcome frequency, effect direction, fitted coefficient, p-value or model score has been inspected.**

The four source products, package hashes, member names and header labels are fixed in `artifacts/empirical/eschscholzia_joint_state_schema_locked.json`.

## Scientific question

The primary question is:

> After conditioning on an array-level pollinator availability/trait state, does floral habitat context retain transferable predictive information for direct seed function and mating/outcrossing state, or is the measured process state sufficient at one endpoint but not the other?

A secondary question asks whether experimentally measured plant-level reproductive capacity / reproductive assurance adds information beyond the common array-level state.

This is a **partial natural-state sufficiency test**, not a causal decomposition of habitat and not a claim that pan traps measure direct visitation to focal plants.

## Fixed hierarchy and held-out unit

The locked hierarchy is:

`Block -> Experimental array -> focal plant -> fruit/progeny`.

Pollinator information exists only at `Block + Experimental array`. Therefore every primary and secondary predictive comparison uses **leave-one-array-out (LOAO)** validation. All plants, fruits and progeny from the held-out array are excluded from fitting together.

Row-wise, progeny-wise or plant-wise cross-validation is prohibited because it would leak the same upstream pollinator state across training and test sets.

The expected design is 4 blocks × 4 arrays = 16 arrays. The pollinator source must expose all 16 distinct array keys. Primary endpoint analyses require at least 12 arrays after their endpoint-specific validity filters; otherwise that endpoint is `not_identifiable_for_endpoint`.

## Fixed key normalization

Only syntactic normalization is allowed:

- trim leading/trailing whitespace;
- convert field-name spaces to underscores for code access;
- stringify and trim `Block`, `Experimental array`, and `Plant identification number` values.

No fuzzy matching of array or plant identifiers is allowed.

For every common array key, `Block` and `Habitat` must be internally unique within each source and must agree across joined sources after string trimming. An inconsistency closes the affected endpoint as non-identifiable; it is not repaired by majority vote.

## Array-level pollinator state (`I/T`)

Source: DOI `10.5285/01906784-6742-44bf-b244-a4b63bed8d82`.

Source metadata states that pan traps were deployed at all 16 arrays in four surveys, captured insects in the main pollinator groups were counted/identified, and intertegular span was measured for captured insects.

Two and only two primary pollinator-state coordinates are constructed per array across all surveys:

1. **`I_count`** — number of source rows with a nonblank `Pollinator species` value for that array. The analysis uses `log1p(I_count)`.
2. **`T_mean_ITD`** — arithmetic mean of finite positive `Intertegular span (mm)` values in that array.

Species richness, guild-specific counts, survey-specific effects, ITD variance, abundance-weighted alternative trait summaries and other pollinator metrics are not opened after outcomes are seen.

If an array has no valid positive ITD value, primary `I/T` models are non-identifiable; ITD is not imputed.

`Survey date` is pooled across the four surveys. The source `Treatment` field is not used in the primary state because its biological role is not needed for the preregistered question and it will not be opened post hoc.

## Primary endpoint F — direct field-exposed seed function

Source: DOI `10.5285/8caf2d8a-564d-4f2e-a797-174165a83796`.

The primary response is fixed to:

`F_seed = log1p(Mean_number_of_seeds_from_field_exposed_flowers)`.

The source must contain exactly one row per `Block + Experimental_array + Plant_identification_number` for this endpoint. Duplicate plant rows close the F endpoint rather than being averaged post hoc.

`Number_of_seeds_from_supplemented_flowers` is reserved as the preregistered secondary **experimentally revealed reproductive-capacity coordinate** `D_capacity = log1p(value)`. It is not substituted for the primary response.

## Primary endpoint G — mating/outcrossing state

Source: DOI `10.5285/7b721c07-bc38-4815-8669-4675867663d0`.

Source metadata states that progeny were manually scored as selfed or outcrossed before Cervus paternity assignment. The primary response is therefore the row-level binary state derived from **`Parentage` only**:

- normalized text containing `outcross` -> `G_outcross = 1`;
- normalized text containing `self` -> `G_outcross = 0`.

No other column is substituted for this classification after values are seen. Rows whose `Parentage` text matches neither rule are excluded from G only and their count is reported. Both recognized classes must occur and at least 12 arrays must contain recognized progeny; otherwise G is `not_identifiable_for_endpoint`.

`Paternity_analysis` is not used to redefine outcrossing.

## Prespecified secondary endpoint C — pollen-movement distance

`Distance_of_pollen_movement` is a secondary connectivity endpoint, not part of the primary cross-endpoint decision.

For rows already classified as outcrossed, finite nonnegative distances are transformed as:

`C_pollen = log1p(Distance_of_pollen_movement)`.

No use is made of `Habitat_crossed` to replace missing distance. C is analysed only if at least 8 arrays contain at least one valid distance; otherwise it is reported `C_not_identifiable`.

## Plant-level alternative-route coordinate R

Source: DOI `10.5285/5b400b69-b828-45e8-b04e-7ccbfdb0987f`.

`Sample type` is classified by fixed semantic rules:

- normalized text containing `exclud` -> pollinator-excluded;
- normalized text containing `expos` -> pollinator-exposed.

The preregistered reproductive-assurance coordinate is:

`R_auto = log1p(mean Number of seeds across pollinator-excluded fruits for that plant)`.

No exposed/excluded ratio, pseudocount ratio, threshold or alternate sample-type mapping is opened after outcomes are seen.

R is used only in a secondary extension of the G model on the subset with available `R_auto`; the corresponding comparison model is refit on the identical subset.

## Model family and fixed regularization

The analysis is predictive; no model is chosen by in-sample p-values.

Continuous predictors are standardized within each LOAO training fold. The two array-level pollinator coordinates are standardized using **unique training arrays**, not repeated plant/progeny rows. Plant-level secondary coordinates are standardized using unique training plants.

Categorical `Block` and `Habitat` are dummy encoded from training-fold levels. A held-out level absent from training closes that fold as invalid; it is not silently encoded as zero.

### Continuous outcomes F and C

Use scikit-learn `Ridge(alpha=1.0, fit_intercept=True)` with no hyperparameter search.

### Binary outcome G

Use scikit-learn `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=10000, fit_intercept=True)` with no hyperparameter search.

Training rows receive inverse-array-frequency sample weights so that every training array contributes total weight 1 regardless of the number of plants/progeny. Held-out scores are first averaged within each array, and arrays are then weighted equally in all primary summaries.

## Fixed nested state sequence

For both primary endpoints F and G, and for secondary C when identifiable:

### S0 — design block only

`Block`

### S1 — measured pollinator process state

`Block + z(log1p(I_count)) + z(T_mean_ITD)`

### S2 — pollinator state plus upstream habitat context

`S1 + Habitat`

`Habitat` is the registered source field and is treated as a categorical upstream context descriptor. The source metadata describe florally rich versus florally poor habitat, but no numeric habitat ordering is imposed.

### Secondary F capacity extension

On the same F rows:

`S3_F = S2_F + z(D_capacity)`.

### Secondary G reproductive-assurance extension

On the R-complete G subset, refit `S2_G_Rsubset`, then compare:

`S3_G = S2_G_Rsubset + z(R_auto)`.

These S3 comparisons are secondary and do not alter the primary residual-habitat classification.

## Held-out scoring

For every valid held-out array:

- F and C: mean squared error (MSE) on their log1p response scale;
- G: mean Bernoulli negative log predictive likelihood (NLL), with predicted probabilities clipped only for scoring to `[1e-8, 1-1e-8]`.

Define per-array predictive gains so positive is better:

- `gain_process = score(S0) - score(S1)`;
- `gain_habitat = score(S1) - score(S2)`;
- `gain_capacity_F = score(S2_F) - score(S3_F)`;
- `gain_R_G = score(S2_G_Rsubset) - score(S3_G)`.

## Cluster bootstrap

For each comparison, resample the valid held-out **array-level gains** with replacement 10,000 times using RNG seed `20260825`. Each bootstrap sample contains the same number of arrays as the observed comparison.

Report mean gain and percentile 95% interval.

A preregistered positive predictive contribution requires:

- observed mean gain > 0; and
- the 95% bootstrap lower bound > 0.

No alternative confidence level, repeated bootstrap seed, precision increase or one-sided interval is opened after the result.

## Endpoint decisions

For F and G separately:

- **`process_state_informative_no_detected_residual_context`** — `gain_process` has positive predictive support and `gain_habitat` does not meet the positive-support rule;
- **`residual_context_detected_after_process_state`** — `gain_habitat` meets the positive-support rule, regardless of the S0->S1 result;
- **`process_state_not_predictively_supported`** — `gain_process` lacks positive support and `gain_habitat` also lacks positive support;
- **`not_identifiable_for_endpoint`** — source/key/class/fold requirements fail.

A negative habitat gain is retained as predictive harm, not reinterpreted as evidence that habitat is biologically irrelevant.

## Primary cross-endpoint decision

Using F and G only:

- **`multi_endpoint_partial_state_convergence_supported`** — both endpoints are `process_state_informative_no_detected_residual_context`;
- **`multi_endpoint_state_insufficiency_detected`** — at least one endpoint is `residual_context_detected_after_process_state`; report whether the residual is shared or endpoint-specific;
- **`multi_endpoint_convergence_not_established`** — no endpoint has detected residual context, but at least one primary endpoint lacks supported S0->S1 process-state improvement;
- **`multi_endpoint_not_identifiable`** — F or G is non-identifiable.

All outcomes are accepted.

## Secondary coordinate decisions

- `capacity_adds_function_information` if `gain_capacity_F` meets the positive-support rule; otherwise `no_detected_capacity_gain`.
- `R_adds_mating_state_information` if `gain_R_G` meets the positive-support rule; otherwise `no_detected_R_gain`.
- C receives the same S0/S1/S2 endpoint classification when identifiable but does not change the primary F+G cross-endpoint decision.

## Claim ceiling

Even a positive result is bounded to this experiment and measurement closure.

Pan-trap state is an **availability proxy**, not direct visitation or effective pollen delivery. `D_capacity` and `R_auto` are experimentally revealed contemporaneous plant coordinates and are not treated as temporally prior causal states. Habitat residual prediction indicates missing or retained upstream information; it does not by itself identify the missing mechanism.

No universal threshold, pollinator-body-size rule, fragmentation category, or city/island equivalence is inferred.

## Stop rule

Run this source lock once after implementation. Do not switch from `Parentage` to another mating field, replace F with supplemented seed set, search species/guild subsets, alter the ITD summary, add survey-specific pollinator metrics, change the held-out unit, tune ridge/logistic regularization, substitute `Habitat_crossed` for C distance, or rerun alternative bootstrap seeds because a result is weak or surprising.
