# Preregistration — cross-origin minimal visitation–reproduction bridge

## Purpose

The full urban–island convergence hypothesis remains not identifiable from the current Honshu–Izu and Zurich archives because state semantics, response definitions and study identity are not harmonized. This secondary archive programme asks a narrower question without weakening that boundary:

> Across independently collected island and urban systems that all measure pollinator visitation and realised plant reproduction, does a minimally harmonized visitation coordinate retain reproducible predictive information for reproduction, and is any origin-level difference estimable once origin is no longer identical to one study?

This is **not** a test that complete eco-genetic states are equivalent across urban and island systems. It is a deliberately weak bridge designed to determine whether one directly observed process coordinate can be transported across origins before richer `D/I/T/C/R/G/A` states are attempted.

## Candidate lock

Candidate inclusion was based on archive contents described publicly, not on preferred effect direction. Four independent archives are locked before raw outcome values are inspected by this project:

| ID | origin | source | archive |
|---|---|---|---|
| `U1_commelina` | urban | Ushimaru et al. 2014, *Commelina communis* urban–rural populations | Dryad `10.5061/dryad.pd775` |
| `U2_chicago` | urban | Zink et al. 2024, Chicago phytometer pollination deficits | Dryad `10.5061/dryad.44j0zpcm6` |
| `I1_hiraiwa2017` | island | Hiraiwa & Ushimaru 2017, continental/oceanic island pollination networks | Dryad `10.5061/dryad.pm29d` |
| `I2_hawaii2019` | island | Aslan et al. 2019, Hawaii dryland pollination | Dryad `10.5061/dryad.tm575v4` |

Published papers necessarily report their own scientific conclusions; those conclusions are not eligibility criteria and will not be used to add/drop archives after schema inspection.

## Stage A — response-firewalled schema audit

The first pass may inspect only:

- file names and sheet names;
- column names;
- data types, dimensions and missingness counts if needed for feasibility;
- explicit metadata/README definitions;
- join-key availability.

It must not calculate associations with reproductive outcomes or inspect fitted effects.

Each archive must separately demonstrate:

1. a directly observed pollinator-visitation quantity with effort or enough metadata to recover a rate;
2. a realised reproductive endpoint from the same ecological unit or a defensible joinable unit;
3. a stable join key linking visitation and reproduction without using outcome values;
4. at least five independent ecological units for within-system held-out prediction.

If any item fails, that archive is `minimal_bridge_not_identifiable_from_archive` and is not repaired by outcome-facing feature engineering.

## Stage B — frozen minimal bridge if Stage A passes

Only after a schema passes is its exact mapping frozen.

### State coordinate

The sole shared process coordinate is effort-standardised total pollinator visitation to the focal plant/unit:

`I_visit = visits / observation effort`.

Partner-resolved data are retained in provenance but are not collapsed with effectiveness weights unless the same effectiveness definition exists in every admitted archive. Richness, functional diversity and trait matching are not substituted for visitation in this minimal bridge.

### Response

The preferred common response is a realised open-pollinated reproductive proportion such as fruit set or seed set per opportunity. Count outcomes are admitted only when a biologically defined denominator exists. A study-specific standardized score is not created solely to force unlike outcomes onto one scale.

If no common response semantics can be frozen across at least two island and two urban systems, the programme stops at `minimal_bridge_response_not_harmonizable`.

### Within-system test

For each admitted system, compare prospectively:

`M0: F ~ baseline/support covariates fixed from source design`

versus

`M1: F ~ baseline/support covariates + I_visit`.

Validation holds out whole independent ecological units (site/population/garden/plant cohort as justified by the source design). Scaling, if any, is learned inside each training fold only.

### Cross-system summary

The unit of transport is the **system-level held-out gain from adding `I_visit`**, not individual observations pooled across studies. Endpoint rows within one study are not treated as independent systems.

With only two systems per origin, any urban–island contrast is descriptive/precision-limited. A formal origin effect is permitted only if at least two independent systems per origin pass the same response-semantic gate and the system-level unit remains the inferential unit.

## Claim ceiling

Even a positive result would support only:

> realised pollinator visitation can be a transportable partial-state coordinate across some island and urban systems.

It would not establish:

- full `P(F_future | S, island) = P(F_future | S, urban)`;
- equivalence of urban and island fragmentation mechanisms;
- sufficiency of visitation alone;
- portability of genetic warning;
- equivalence of pollinator richness, functional diversity, trait matching and visitation.

## Stop rules

Do not:

1. drop an archive because its published or newly computed effect is inconvenient;
2. replace visitation with a different state variable after seeing reproduction values;
3. convert fruit set, seed count, pollen receipt and pollen limitation into a generic z-score merely to obtain a pooled model;
4. treat species/endpoints within one study as independent origin replicates;
5. add a fifth study after results merely to change an origin contrast;
6. infer a complete state-convergence result from this one-coordinate bridge.
