# ML009 / PS002 Magnolia 2013 population-cluster recovery contract

## Goal

Test whether Suzuki et al. (2013), DOI `10.1186/1472-6785-13-10`, can provide the final candidate fourth independent multilayer cluster by reconstructing contemporary pollen immigration (`C`) and female seed production (`F`) on the same focal-population frame.

This is the final candidate-hunting gate in the current nine-study extraction queue. If it fails without an admissible fourth cluster, candidate hunting stops and the current three-cluster evidence ceiling is carried into synthesis/manuscript work.

## Locked common exposure

Primary fragmentation exposure = focal population size.

For common orientation define

`fragmentation_severity = -log(population_size)`.

Population size is fixed before population-level C/F outcomes are reconstructed because it is source-defined, available at the focal-population scale, and is explicitly included in the female reproductive-success model and the male reproductive-success model. Do not switch to neighbouring population size, local density, geographic separation, mating distance or a composite index after outcomes are opened.

## Common effect unit

Primary independent unit = focal population.

All primary C and F values must be reconstructable for the exact same set of source populations. Seed-parent genets, offspring, flowers, ovules and mating pairs remain nested observations and never become fragmentation replicates.

No population is imputed. If fewer than four exact common populations remain after applying the source definitions, ML009 is not admitted.

## Locked C endpoint

Primary C endpoint = population-level incoming pollen immigration fraction.

Where Table 1 reports seed-parent-specific paternity samples and immigrant-pollen counts/rates, reconstruct each focal population as:

`C_immigration = sum(immigrant_offspring_count) / sum(paternity_sample_count)`

over all source-listed seed parents in that population with valid paternity data.

Use counts rather than an unweighted mean of seed-parent percentages. If immigrant counts cannot be reconstructed exactly from the source table, do not infer them from rounded percentages.

The study-level 6.09% summary and mean dispersal distance are descriptive checks only; they do not substitute for the required population vector.

The male-success parameters beta (relative population size) and gamma (population separation) are source-model context/sensitivity only. They cannot replace the primary population-level incoming-pollen endpoint after results are seen.

## Locked F endpoint

Primary F endpoint = source population-level mean seed-production rate / ovule survival.

Preferred recovery order:

1. exact source-reported population mean seed-production rate, if present;
2. arithmetic mean of the source-listed seed-parent seed-production rates only if the article's definition of the reported population mean is consistent with that aggregation;
3. otherwise F is not reconstructable.

Do not weight seed-parent percentages by flower count unless the source explicitly defines the population estimate that way. Do not reconstruct successful-seed numerators from rounded percentages.

## Primary effect representation

For each layer compute a population-level gradient effect against the same locked exposure:

- `r_C = cor(fragmentation_severity, C_immigration)`;
- `r_F = cor(fragmentation_severity, F_seed_production)`;
- Fisher-transform each to `z = atanh(r)`;
- sampling variance for each scalar Fisher-z effect = `1 / (n - 3)` on the exact common-population frame.

Orient the ecological interpretation rather than changing the arithmetic sign post hoc:

- for F, higher seed production is reproductive support;
- for C, incoming pollen immigration is movement/connectivity support but may increase as a compensatory response to small population size. A positive C response under fragmentation is therefore retained as compensation/state separation, not forcibly recoded as deterioration.

## Cross-layer dependence

Estimate the C/F dependence from the same common-population frame after removing the common linear fragmentation gradient from each response:

1. regress C and F separately on standardized fragmentation severity;
2. compute Pearson correlation of the two residual vectors;
3. working sampling covariance = residual correlation × `sqrt(var_zC * var_zF)`.

Store this explicitly as a dependence proxy, not an exact known covariance. The resulting 2x2 working covariance matrix must be positive definite. Do not set covariance to zero by convenience.

## Source opening order

1. retrieve the open PMC/BMC Table 1 representation and exact focal population identities;
2. verify population size and paternity/seed-production columns before calculating outcomes;
3. verify source aggregation semantics for population-level seed production;
4. materialize one keyed population table using the locked rules;
5. calculate C/F Fisher-z effects and the residual-correlation covariance proxy in one fixed script;
6. compare reconstructed descriptive summaries with source-reported study/population summaries as QA.

## No-rescue rules

Do not:

- use maternal genets as independent fragmentation n;
- average rounded immigration percentages when exact immigrant counts are unavailable;
- switch the C endpoint to gamma or beta because it produces a preferred result;
- switch the exposure to neighbouring population size, local density, separation or mating distance;
- infer missing population values from figures;
- pool population and genet scales;
- set C/F covariance to zero;
- treat compensation (higher immigration into smaller populations) as an error requiring sign reversal;
- search for additional candidate studies if this final queue candidate fails, unless the evidence corpus itself is later expanded under a new prospective amendment.

## Terminal outcomes

- `ML009_admitted_C_F_population_size_covariance_aware`;
- `common_population_frame_not_reconstructable`;
- `C_population_immigration_not_reconstructable`;
- `F_population_seed_production_not_reconstructable`;
- `cross_layer_covariance_not_reconstructable`.

All outcomes are acceptable.
