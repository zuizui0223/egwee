# CFTQ0263 Brunsvigia radulosa I-F estimand gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_BRUNSVIGIA_RADULOSA_2005`.

Primary source: Ward & Johnson (2005), *Oikos* 108:253–262,
doi:10.1111/j.0030-1299.2005.13468.x.

The source studies fragmented grassland populations and explicitly records three related predictors:

- habitat fragment area;
- population isolation;
- population size.

It also measures direct seed production and pollen limitation using supplemental hand pollination.

## Why this requires an estimand gate

Population size is biologically important but is not itself the frozen EGWEE habitat-fragmentation
exposure. The source's published conclusions emphasize reduced seed production and stronger pollen
limitation in small populations, while habitat fragment area and isolation are weaker in the
published multivariable model.

Because those outcome directions are already public, EGWEE will not choose the predictor that
produces the strongest I-F pattern after inspection.

## Frozen rule

No numerical EGWEE effect is opened until the source methods/data support one **habitat** estimand:

1. fragment area, or
2. population isolation.

Population size remains a separate demographic / mate-availability moderator.

Independent unit = population/site. Flowers, hand-pollination treatments, seeds and juveniles are
nested below population.

Primary candidate I = population-level pollen limitation under the source open-versus-supplemental
pollination experiment.

Primary candidate F = population-level direct seed production per plant.

The same population IDs must support exposure + I + F.

## Effect family

If a continuous habitat variable and common population vector are recoverable, this programme enters
only the Fisher-z gradient/generalisation stream.

Do not dichotomize fragment area or isolation after seeing responses. Do not turn population size
into habitat-fragmentation severity.

## Terminal outcomes

- `brunsvigia_gradient_IF_covariance_aware`;
- `brunsvigia_fragment_area_common_IF_frame_not_recoverable`;
- `brunsvigia_isolation_common_IF_frame_not_recoverable`;
- `brunsvigia_habitat_estimand_not_identifiable`;
- `brunsvigia_population_level_I_not_recoverable`;
- `brunsvigia_population_level_F_not_recoverable`.

## No rescue

Do not:

- choose population size because it is the strongest published predictor;
- choose area versus isolation by significance;
- use juvenile recruitment as F;
- count flowers, fruits, seeds or juveniles as fragmentation n;
- claim equivalence from a non-significant fragment-area or isolation coefficient;
- use the result to validate a finite EGWE/NEE operator.

All terminal outcomes are retained.
