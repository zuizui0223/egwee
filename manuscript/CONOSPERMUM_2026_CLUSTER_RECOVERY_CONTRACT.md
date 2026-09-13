# ML005 / PS011 Conospermum 2026 cluster-recovery contract

## Goal

Attempt to recover a fourth independent multilayer cluster from Delnevo et al. (2026), *Ecology and Evolution*, DOI `10.1002/ece3.73406`, using the public Dryad archive `10.5061/dryad.95x69p907`.

Target layers:

- `C_movement_connectivity`: contemporary pollen immigration / pollen movement;
- `G_offspring`: genetic state of the 2017 seedling/progeny cohort.

Adult genetic summaries are programme-level historical context already owned by PS010 and must not be counted again.

## Independent-unit frame

Primary unit = population. Maternal plants and seedlings are nested below population and cannot become independent fragmentation replicates.

The confirmatory overlap is limited to populations with both a contemporary seed crop and reconstructable offspring-genetic state. Populations with no progeny are not converted to genetic-effect zeros.

## Locked landscape exposure

Primary exposure is the source-defined **modified incidence-function connectivity index** used in the 2026 Methods and explicitly linked there to the earlier Delnevo programme landscape definition. It is calculated from the spatial configuration/area of neighbouring populations and is defined independently of pollen-flow or genetic outcomes.

For the synthesis, fragmentation severity is the sign-reversed standardized connectivity value:

`fragmentation_severity = -z(connectivity_index)`.

Exact population-specific connectivity/index values must be source-recoverable for the populations entering the common C/G_offspring frame **before** either effect is calculated.

The previously assembled `urban_barrier / permeable` classes are retained only as descriptive landscape interpretation/sensitivity metadata. They are not the primary exposure. Some earlier class rationales mentioned realized pollen immigration; such outcome information cannot define the exposure for a C endpoint.

Do not substitute population size, straight-line distance, area, floral display, or the binary matrix class if exact source connectivity values remain unavailable.

## C endpoint

Primary C representation = source `m_p + s` pollen-immigration estimate (`m_p`) from Table 2 for each population with progeny, using source SE where estimable.

Do not switch to the `m_p only` model or Cervus estimate because it gives a stronger contrast. Those may be reported as secondary model-form sensitivities only.

## G_offspring endpoint

From the public seedling microsatellite data, derive one population-level offspring genetic-state summary without using adult genotypes as a new independent 2026 layer.

Primary offspring metric = expected heterozygosity `H_E` calculated across seedling multilocus genotypes within each population. This metric was frozen before raw genotype values were opened.

If the raw archive does not contain population-linked seedling genotypes sufficient to calculate population `H_E`, terminate as `offspring_genetic_state_not_reconstructable` rather than switching to a favorable genetic metric.

Population-level uncertainty must be estimated by a fixed locus bootstrap (10,000 resamples of loci with replacement; RNG seed 20260913). Seedlings remain nested observations used to estimate the population state, not independent landscape n.

## Effect representation

If exposure, C and G_offspring are all reconstructable on the common population frame:

1. compute the population-level association of each endpoint with the locked `-z(connectivity_index)` fragmentation-severity exposure;
2. preserve C source-model uncertainty and G locus-bootstrap uncertainty;
3. reconstruct within-cluster dependence from paired population-level C/G contributions or centered population values where mathematically possible;
4. require any working covariance block used for inversion to satisfy the declared dependence checks.

No covariance is silently set to zero.

## Source opening order

1. source paper/Methods to lock the connectivity-index definition;
2. Dryad metadata / filenames / schema and earlier programme sources to recover exact population-specific connectivity values without opening outcomes;
3. raw seedling genotype values;
4. one-shot population-level G summary and covariance-aware C/G cluster calculation.

## No-rescue rules

Do not:

- count adult G again as a 2026 effect;
- treat seedlings, maternal plants or loci as independent fragmentation n;
- code populations G/H with no progeny as G_offspring=0;
- replace `m_p+s` by another paternity model after observing the contrast;
- replace `H_E` with H_O, allelic richness, F_IS or another genetic metric after observing direction;
- replace the source-defined connectivity index with population size, distance, area, floral display or matrix class because those data are easier to retrieve;
- use realized pollen immigration to assign the primary landscape exposure;
- combine PS010 adult genetic values into the covariance block as if contemporaneous offspring data;
- use post-2017 genetic observations as the seedling cohort.

## Reopening requirements

ML005 can proceed only when **both** of the following are satisfied through ordinary authorized/source-valid routes:

1. exact population-specific values for the source-defined modified incidence-function connectivity index are recovered for the common analysis populations;
2. the public/author-supplied seedling genotype bytes can be read without bypassing access controls.

Recovering only one side does not authorize effect calculation.

Possible terminal outcomes include:

- `ML005_admitted_C_Goffspring_covariance_aware`;
- `source_exposure_values_not_reconstructable`;
- `offspring_genetic_state_not_reconstructable`;
- `common_population_overlap_insufficient`;
- `covariance_not_reconstructable`;
- `source_access_blocked`.

All outcomes are acceptable.
