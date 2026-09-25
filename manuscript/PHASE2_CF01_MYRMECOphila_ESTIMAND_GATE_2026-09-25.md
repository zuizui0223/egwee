# CFTQ0187 Myrmecophila christinae fragmentation I-F estimand gate — 2026-09-25

## Why this candidate matters

Parra-Tabla et al. (2011) surveyed **14 populations** of the endangered epiphytic orchid
*Myrmecophila christinae* in a fragmented coastal-shrub landscape and measured:

- population/demographic state;
- habitat fragmentation/disturbance variables;
- pollen limitation using hand-pollination comparisons;
- fruit production / fruit set.

Under the frozen EGWEE layer definitions, pollen limitation is an eligible
`I_interaction` endpoint and fruit production/fruit set are eligible
`F_reproductive_function` endpoints.

## Current ambiguity

The public abstract exposes at least two source-defined habitat axes:

1. **fragment size/area** — e.g. demographic differences in fragments <1 ha and higher fruit
   production in fragments >10 ha;
2. **habitat disturbance / affectation** — fruit set is lower in highly disturbed fragments.

It also reports that pollen limitation occurs across all studied populations and is not obviously
aligned with habitat disturbance.

Those facts make the study scientifically interesting, but they also make post hoc extraction
dangerous: choosing fragment size for F, disturbance for another F quantity, and then pairing either
with pollen limitation after seeing directions would manufacture the estimand.

## Frozen gate

No numerical EGWEE effect is opened until authoritative full-text methods/tables establish:

1. the exact population IDs and fragmentation-level independent unit;
2. the exact source coding of fragment area/size and habitat disturbance;
3. which one variable can serve as one response-free fragmentation estimand on a common population frame;
4. a population-level pollen-limitation quantity under the source pollination experiment;
5. a direct F endpoint on the **same population/exposure frame**;
6. recoverable sampling dispersion or raw population values without promoting flowers/plants/fruits to fragmentation n.

## Permitted outcomes

- `myrmecophila_gradient_IF_covariance_aware`;
- `myrmecophila_direct_IF_covariance_aware` if the source itself defines an eligible two-group
  contrast before response selection;
- `myrmecophila_common_IF_frame_not_recoverable`;
- `myrmecophila_fragmentation_estimand_ambiguous`;
- `myrmecophila_population_level_I_not_recoverable`;
- `myrmecophila_population_level_F_not_recoverable`.

## No rescue

Do not:

- choose fragment area versus disturbance because one produces a stronger I-F difference;
- choose fruit production versus fruit set by significance;
- treat individual flowers, plants or fruits as independent fragmentation units;
- convert the source into a binary small/large contrast unless that contrast is explicitly source-defined;
- infer absence of fragmentation effects from pollen limitation occurring in all populations;
- use this study to validate a finite EGWE/NEE operator.

All terminal outcomes are retained.
