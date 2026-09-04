# Cross-origin convergence preregistration — urban versus island state portability

## Status

This is a prospective **identifiability gate** written before fitting any pooled urban-versus-island convergence model. It uses only already-locked source schemas and previously declared within-system analyses.

The target hypothesis is:

> If island and urban systems are represented by the same future-relevant process state, does fragmentation origin add transferable predictive information about realised ecological function?

Formally, the target is a cross-origin portability statement of the form

`F_future ⟂ origin | S_measured`,

where `origin` distinguishes island and urban fragmentation routes and `S_measured` has the same biological meaning in every system.

## Locked source systems

Primary existing candidates are fixed to:

1. **Honshu–Izu E1** — Hiraiwa & Ushimaru (2024), Figshare `10.6084/m9.figshare.25025000.v1`.
   - held-out unit: whole site;
   - candidate process state: `TM_z + FDQ + FEve` plus season and focal-plant structure;
   - response: standardized pollen receipt `pollen_z`;
   - upstream context: distance from mainland.

2. **Zurich E2** — Reji Chacko, Moretti & Frey (2025), EnviDat `10.16904/envidat.676`, BetterBlooms commit `d6361f6874398e797322afe07a8fea85a3c7e927`.
   - held-out unit: whole garden;
   - candidate process state: focal-function-specific pollinator-guild visitation rates;
   - responses: six source-defined Poisson/binomial fruit/seed endpoints;
   - upstream context: local plant support and `Urban_500`.

No outcome from either system may be redefined to make the two archives easier to pool.

## Eligibility gates for a direct cross-origin model

A pooled or cross-system law is fitted only if **all** gates pass.

### Gate 1 — semantic state alignment

At least one predeclared process coordinate must have the same biological meaning and construction in both systems.

Allowed examples include the same effort-standardised partner-specific visitation variable, the same effectiveness-weighted interaction measure, the same functional-diversity metric from compatible trait definitions, or the same process-specific connectivity measurement.

Not allowed:

- treating `TM_z`, `FDQ` or `FEve` as interchangeable with guild-specific visitation merely because all can be z-standardised;
- replacing a missing state coordinate with habitat origin;
- inventing a latent common score after inspecting outcomes.

### Gate 2 — response alignment

The downstream functional response must represent the same ecological function at a defensible scale. A standardized pollen-receipt score is not silently equated with raw seed counts, fruit-set probabilities or another reproductive response solely by rescaling.

A common response transformation is allowed only if it is biologically and statistically predeclared independently of the urban/island result.

### Gate 3 — origin is not perfectly confounded with study identity

A direct origin effect or `origin × state` interaction is interpretable only if origin is replicated independently of study/protocol identity.

With exactly one island archive and one urban archive, `origin` is perfectly collinear with study, taxonomic composition, measurement protocol and response definition. Such a two-study pool cannot identify a general island-versus-urban residual-origin effect.

A direct cross-origin claim therefore requires either:

- at least two independent systems per origin class measured with a common protocol; or
- one coordinated study design containing both origins with the same state and response definitions.

### Gate 4 — independent validation is possible

Validation must hold out whole ecological units and include a genuine cross-system transfer test. Rows or endpoints from one study are not treated as independent systems.

## Decision rule

- `cross_origin_convergence_testable`: all four gates pass; fit the predeclared origin-blind and origin-augmented predictive models.
- `cross_origin_convergence_not_identifiable_from_existing_archives`: at least one gate fails before outcome fitting. Stop without inventing harmonisation.

Failure of identifiability is a design boundary, not evidence that urban and island systems differ biologically.

## Permitted narrower synthesis if the direct test stops

The already-locked within-system results may still support the narrower statement that upstream habitat/context scalars can become predictively redundant after measured partial process states in some island and urban systems. This does **not** establish a shared cross-origin dynamical law.

## Stop rules

Do not:

1. pool E1 and E2 by generic z-scoring of semantically different state variables;
2. convert pollen receipt, fruit set and seed set into a new common outcome after seeing results;
3. infer an origin effect when origin equals study identity;
4. treat six Zurich endpoints as six independent urban systems;
5. add new datasets because they produce a desired direction;
6. search many common metrics until urban/island equivalence appears;
7. interpret `not_identifiable` as evidence against convergence.
