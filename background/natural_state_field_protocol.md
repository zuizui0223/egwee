# Prospective field protocol — identifying functional-fragmentation states in nature

## Purpose

This protocol turns the state-sufficiency theory and the empirical audits into a **field-identification procedure**. It is designed for urban, island, conventional fragmented terrestrial and other spatially structured ecosystems.

The target is not to assign a habitat label. It is to identify the smallest measured joint state that predicts what happens to a focal ecological function next.

The prospective null is:

`future functional trajectory ⟂ fragmentation origin/history | measured joint state at t`.

A residual origin/history signal means the measured state is incomplete.

## 1. Fix the sampling unit before measuring the state

The basic unit is a **population/site × observation window × cohort**.

Every state coordinate used in one row must refer to the same ecological unit unless an explicit lag is the object being tested.

Required identifiers:

- site / patch / population ID;
- survey year and season;
- focal species or focal interaction;
- focal genetic cohort (`adult`, `seed`, `seedling/juvenile`, pollen pool, etc.);
- pre-state window `t`;
- future-function window `t + Delta`;
- upstream fragmentation/history descriptor retained only for the final residual-origin test.

Do not merge measurements from different years or cohorts simply because they come from the same named study system.

## 2. Define one direct ecological function

`F` must be a realised endpoint, not a proxy for habitat or partner abundance.

Examples:

- compatible pollen deposition;
- fruit or seed set;
- successful recruitment;
- effective seed dispersal;
- another explicitly defined interaction-dependent function.

Presence, abundance, flower number, partner richness and neutral diversity are state coordinates or covariates, not substitutes for `F`.

The future response is defined before warning variables are inspected. Depending on the system it can be:

- continuous change in `F`;
- first passage below a biologically predeclared functional threshold;
- persistence/loss over the next fixed observation window.

## 3. Measure the candidate joint state

### `D` — demographic/resource support

Minimum:

- focal population or reproductive-adult density;
- flowering/resource density appropriate to the interaction;
- local habitat amount or carrying-resource measure.

Optional:

- effective size when independently estimable;
- age/stage distribution;
- local recruitment.

### `I` — realised interaction support

Prefer a functionally weighted interaction measure, for example:

`I_eff = Σ_j visitation_ij × effectiveness_ij`.

If effectiveness cannot be measured directly, retain partner-specific visitation rather than collapsing all partners into total visitation.

Minimum:

- partner identity or functional group;
- interaction frequency;
- sampling effort/time.

Preferred:

- compatible pollen deposition per visit or visitor effectiveness;
- partner-specific interaction strength.

### `T` — functional/trait state

Use only mechanism-relevant traits.

Examples:

- proboscis–corolla matching;
- floral-morph balance;
- partner functional diversity;
- sex ratio / compatible-mate structure where it determines interaction function.

Species richness is not accepted as a substitute for `T` unless a separate predictive test shows equivalence.

### `C` — process-specific connectivity

Never use one generic connectivity variable when multiple biological processes are relevant.

Record separately where possible:

- `C_pollen` — paternity/pollen-pool inferred pollen movement;
- `C_seed` — seed/propagule movement;
- `C_demo` — successful demographic immigration/recolonisation;
- `C_partner` — movement of pollinators, dispersers or other interaction partners.

For movement distributions, retain the dispersal kernel or at least distance quantiles and immigration fraction instead of only a mean.

### `R` — compensation / alternative routes

Examples:

- autonomous selfing;
- self-compatibility and realised selfing rate;
- alternative pollinator/disperser guilds;
- rewiring or compensatory interactions;
- vegetative reproduction where it substitutes for the focal demographic outcome.

A stable function under local resource loss is called compensation only when the compensating process is actually measured.

### `G_by_cohort` — genetic/mating state

At minimum distinguish:

- adult standing genetic state;
- current pollen/offspring mating state;
- seed/juvenile genetic state when available.

Possible measurements:

- heterozygosity and allelic diversity;
- inbreeding/fixation indices;
- parentage-derived sire diversity;
- pollen-pool differentiation;
- functional/adaptive variants where justified.

Do not assume adult neutral diversity describes the contemporary mating process. *Conospermum* and *Spondias* demonstrate why cohort identity can matter.

### `M` — ecological memory/history

Predeclare plausible memory variables before outcome inspection.

Examples:

- time since fragmentation;
- disturbance history/intensity;
- colonisation age;
- seed-bank or persistent soil-resource state;
- age structure;
- persistent interaction-route or learned-movement legacy.

### `A` — joint spatial alignment

The model counterexample shows that separate marginals can match while cross-layer spatial alignment differs.

Retain the patch-level vectors rather than only their means. Candidate descriptive summaries include population- or resource-weighted associations such as:

- `A_DI = cor_w(D_i, I_i)`;
- `A_IG = cor_w(I_i, G_i)`;
- `A_IC = cor_w(I_i, C_i)`;
- `A_IF = cor_w(I_i, F_i)`;
- multivariate cross-covariance or a predeclared joint embedding when sample size supports it.

These are candidate compressions, **not assumed sufficient statistics**. The full patch-level state remains the reference until predictive sufficiency is demonstrated.

## 4. Recognise candidate natural conditions by process chains, not universal thresholds

### U-LIM — uncompensated interaction limitation

Required evidence in the same causal comparison:

1. `D_local` declines or is low;
2. realised `I` declines;
3. direct `F` declines;
4. measured `R` does not compensate sufficiently;
5. nonzero `C` does not by itself rescue local function.

Natural anchor: *Crepis sancta*.

Do not classify U-LIM from low density alone.

### I-COMP — movement/interaction compensation

Required evidence:

1. local `D/I` support declines;
2. at least one measured `C` or `R` process changes in a compensating direction;
3. direct `F` is maintained or declines less than expected from local support;
4. the compensation process temporally/spatially aligns with the maintained function.

Natural anchor: Miyake-jima *Camellia–Zosterops*.

Do not infer compensation merely from stable `F`.

### U-LAG — cohort/history lag

Required evidence:

1. current interaction, mating/connectivity or function indicates deterioration;
2. the monitored adult genetic cohort still reflects an older landscape state;
3. a contemporary offspring/paternity layer supports the temporal mismatch.

Natural anchor: *Conospermum undulatum*.

High adult diversity alone does not establish lag.

### T-JOINT — joint interaction–connectivity deterioration

Required evidence in a common comparison:

1. realised `I` declines;
2. process-specific `C` contracts or donor/mate diversity narrows;
3. direct `F` declines;
4. current offspring/mating genetics deteriorates or becomes more inbred;
5. cohort differences are retained rather than pooled.

Natural anchor: *Spondias purpurea*.

This is currently the closest natural analogue to the full eco-genetic state chain.

### T-MATCH — functional-partner / trait-matching limitation

Required evidence:

1. functional partner composition or `T` changes;
2. realised trait matching changes;
3. direct `F` tracks matching more closely than raw species richness;
4. geography/habitat label is treated as upstream context, not the state itself.

Natural anchor: Honshu–Izu coastal pollination networks.

## 5. Estimate the smallest sufficient natural state

Fit models in a fixed order.

### Model S0 — coarse landscape state

Use only habitat/geometry/category variables and simple abundance/richness summaries.

Purpose: quantify what would be concluded under conventional fragmentation monitoring.

### Model S1 — measured process state

Add the predeclared synchronized `D/I/T/C/R/G_by_cohort/M/A` subset available in that system.

Do not add variables after seeing whether origin remains important.

### Model S2 — residual-origin model

Add upstream origin/history last:

- urban/island/continuous/fragmented category;
- mainland distance;
- fragmentation route;
- disturbance origin;
- other predeclared upstream context.

The central question is whether S2 improves **held-out prediction/calibration** over S1.

### Validation unit

Hold out whole independent ecological units whenever possible:

- whole sites;
- whole islands;
- whole years;
- whole landscapes.

Do not randomly split observations from the same population-year across training and test sets.

## 6. Convergence decision

### `measured_state_convergence_supported`

Use only when adding origin/history after S1 provides no reproducible material predictive improvement at the declared hold-out scale.

Interpretation: distinct fragmentation routes are consistent with the same operational state **at the tested resolution**.

### `measured_state_incomplete`

Use when origin/history retains predictive information after S1.

Interpretation: search for a missing process, alignment term, cohort or memory variable. Do not declare the habitat label itself to be the mechanism.

### `not_identifiable_with_current_measurements`

Use when relevant coordinates are not synchronized to the same site-year/cohort/outcome window or independent hold-out units are insufficient.

This is an informative design result, not a null ecological effect.

## 7. Genetic-warning gate

Only after the loss-generating state has been defined and its future functional outcome is evaluable should genetic warning be tested.

Within each empirically supported state/domain:

1. set the genetic baseline before the outcome window;
2. predeclare relative/absolute warning endpoints;
3. preserve censored non-events;
4. test same-trajectory lead/tie/lag ordering;
5. replicate inside the same state before asking portability across states.

A warning that works inside one state is not automatically portable to U-LIM, I-COMP, U-LAG, T-JOINT or another state.

## 8. Minimum practical sampling set

If resources are limited, the **minimum useful synchronized set** is:

1. `D`: focal/flowering density;
2. `I`: partner-specific visitation with sampling effort;
3. `F`: direct function;
4. `C`: the biologically dominant contemporary movement process;
5. `G`: at least adult plus offspring/pollen-pool genetic state;
6. `R`: the main plausible reproductive/interaction compensation route;
7. site coordinates + fragmentation age/history;
8. repeated independent patches/sites sufficient for spatial alignment and held-out validation.

If only three layers can be added to a conventional fragmentation survey, prioritize **direct function, realised interaction support and contemporary process-specific connectivity** before adding another structural landscape index.

## Stop rule

Do not create universal field thresholds from the numerical values in the current natural anchors. The field programme searches for **process configurations and predictive sufficiency**, not a single global cutoff for density, pollen-flow distance, heterozygosity or island isolation.
