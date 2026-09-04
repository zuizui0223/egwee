# Cross-origin convergence result — existing urban and island archives do not identify a shared law

## Decision

**`cross_origin_convergence_not_identifiable_from_existing_archives`**

The preregistered identifiability gate stops the direct Honshu–Izu versus Zurich convergence test before any pooled outcome model is fitted.

This is not evidence that urban and island systems occupy different regimes. It means the current two archives cannot identify the stronger claim that a common measured state makes fragmentation origin redundant across systems.

## Gate audit

### Gate 1 — semantic state alignment: FAIL

The primary Honshu–Izu E1 process state is

`TM_z + FDQ + FEve`,

where the coordinates describe community trait matching, pollinator functional diversity and functional evenness.

The Zurich E2 process state is a focal-function-specific vector of effort-standardised pollinator-guild visitation rates. Different plant functions use different guild sets.

These are not the same biological coordinates. Generic centering/scaling would put them on numerically comparable scales but would not make them equivalent measurements of state.

### Gate 2 — response alignment: FAIL

Honshu–Izu predicts species-level standardized pollen receipt (`pollen_z`). Zurich predicts six separate reproductive endpoints with source-defined Poisson or binomial response families, including seed counts, fruit set and seed set.

The current project has no prospectively declared biological mapping that makes standardized pollen receipt interchangeable with those fruit/seed outcomes. Creating one after the within-system results are known would add an outcome-facing representation choice.

### Gate 3 — origin independent of study identity: FAIL

The available comparison contains one island/coastal-network archive and one urban-garden archive. Therefore

`origin == study/protocol identity`.

Any pooled `origin` coefficient would also absorb differences in focal taxa, sampling design, state construction, response construction, geography and study protocol. With only these two study identities, a general urban-versus-island residual-origin term is not identified.

The six Zurich reproductive endpoints do not solve this problem because they are repeated functions within one urban study, not six independent urban systems.

### Gate 4 — genuine cross-system validation: FAIL under the current archive set

Both existing analyses use strong within-system validation — whole-site holdout for E1 and whole-garden holdout for E2. But a direct convergence claim requires transfer across independently replicated systems/origins. With one study per origin, leaving out an origin is equivalent to leaving out the only study that defines that origin, so study and origin effects cannot be separated.

## What remains supported

The narrower within-system pattern remains informative:

- in Honshu–Izu, mainland distance did not improve held-out pollen-function prediction after the preregistered `TM_z + FDQ + FEve` partial state;
- in Zurich, none of six fixed reproductive endpoints showed reproducible held-out gain from adding the preregistered urban/local context layer after the source-defined interaction state.

Together these support the **methodological possibility** that an upstream habitat/context scalar can become predictively redundant after a proximal process state is supplied.

They do not establish

`P(F | S, island) = P(F | S, urban)`.

## Counter-boundary retained from Oenothera

The *Oenothera harringtonii* result prevents an overgeneralized interpretation. Pollinator treatment alone did not absorb spatial information relevant to contemporary mating state; adding maternal spatial isolation improved held-out prediction and retained permutation-supported information.

Therefore the next matched urban–island test must include process-specific connectivity/mating opportunity when the endpoint can depend on mate or pollen movement. Interaction state alone is not assumed complete.

## Minimum design that would identify the hypothesis

The direct cross-origin hypothesis becomes testable only with a matched measurement core across independently replicated systems.

### Required shared core

For the same site × time/cohort unit in every system:

1. `D` — focal reproductive/flowering density;
2. `I` — partner-specific visitation with common effort units, preferably `sum(visitation × effectiveness)`;
3. `T` — the same mechanism-relevant functional/trait metrics;
4. `F` — the same direct realised function, preferably compatible pollen deposition or a predeclared comparable reproductive endpoint;
5. `C` — process-specific pollen/seed/partner connectivity where relevant;
6. `R` — reproductive assurance or compensating interaction route;
7. `G` — at least contemporary mating/offspring genetic state when eco-genetic convergence is claimed;
8. `A` — retained patch-level cross-layer alignment or a prospectively validated compression.

### Replication requirement

Use either:

- at least two independent island systems and two independent urban systems measured under the same core protocol; or
- a coordinated multi-landscape study in which both fragmentation origins occur under the same measurement and response definitions.

Then compare, prospectively:

`M0: F_future ~ S`

against

`M1: F_future ~ S + origin`

and, only if predeclared,

`M2: F_future ~ S + origin + S:origin`.

Validation must hold out entire systems/landscapes, not observations within a system.

## External candidate audit — bounded, non-exhaustive

A targeted open-data search found additional urban or island pollination datasets, but none was admitted into the direct test because the common-state gate was not already satisfied.

Examples include:

- Ushimaru et al. urban-rural *Commelina* data, Dryad `10.5061/dryad.pd775` — visitation and reproduction, but not the same E1 `TM_z/FDQ/FEve` state;
- Udy et al. urban-gradient plant–pollinator data, Dryad `10.5061/dryad.4mw6m906s` — network/interaction data, but no predeclared matched E1 functional-response bridge;
- Sookhan et al. Toronto urban pollination data, Dryad `10.5061/dryad.b8gtht7r4` — pollinator abundance/diversity and plant reproduction, but again not a matched E1 state protocol;
- Hiraiwa & Ushimaru island pollinator data, Dryad `10.5061/dryad.pm29d` — useful island network structure evidence, but not an independent matched urban–island realised-function protocol.

These candidates can motivate a future coordinated dataset build, but adding one opportunistically would not solve study-origin confounding.

## Scientific consequence

The stronger urban–island convergence hypothesis remains **open but now sharply identified**:

> different fragmentation histories may converge on a common future-relevant state, but existing Honshu–Izu and Zurich archives cannot test that equality directly because state semantics, response definitions and study identity are not harmonized.

The recovered result is therefore a design theorem-like boundary for the empirical programme: **cross-origin convergence requires matched state semantics and replicated origin independently of study identity.**
