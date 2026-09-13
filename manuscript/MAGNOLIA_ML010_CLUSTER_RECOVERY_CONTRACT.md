# ML010 / PS002 Magnolia stellata cluster-recovery contract

## Goal
Attempt a fourth independent admissible multilayer cluster from Suzuki, Nagamitsu & Tomaru (2013), DOI `10.1186/1472-6785-13-10`, while preserving the existing ML009 Pistacia boundary.

## Independent-unit frame
Primary independent unit = six seed-sampled populations Y, T, A, B, C and F. Maternal genets, flowers, offspring and mating pairs are nested below population.

## Locked common exposure
Primary exposure = source-defined **population size measured as summed basal area (summed size) of adult genets**. The paper Methods explicitly defines the modelled population-size variable this way. Adult-genet count must not be substituted.

Neighbouring population size is secondary only if exact population-level values are supplied by the source; it cannot replace the primary exposure after outcomes are seen.

## Endpoints
- `F_reproductive_function`: source Table 1 population mean seed-production rate for Y/T/A/B/C/F.
- `C_movement_connectivity`: between-population pollen export from each donor population, only if the electronic supplement provides an auditable donor-by-sink matrix and denominator. Total male siring, selfing, the paper-wide 6.09% flow summary and the mating-pair separation parameter gamma are not substitutes.

## Admission rule
Admit only if exact six-population summed-basal-area exposure values, valid C and F vectors on the same six populations, and a nonzero within-cluster covariance representation are all reconstructable. No maternal/offspring pseudo-replication and no figure digitization.

## Opening order
1. freeze this contract;
2. inspect publisher supplement schema without numeric data rows;
3. if required fields exist, freeze the exact effect/covariance calculation;
4. open numeric rows once;
5. accept admission or the preregistered non-identifiability closure without rescue.

Possible terminal outcomes include `ML010_admitted_C_F_covariance_aware`, `source_population_size_values_not_recoverable`, `C_population_vector_not_reconstructable`, `common_population_overlap_insufficient`, `covariance_not_reconstructable`, and `source_access_blocked`.
