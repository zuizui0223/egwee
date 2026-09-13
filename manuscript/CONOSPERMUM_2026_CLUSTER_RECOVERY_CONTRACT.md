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

Primary exposure is the source-defined **urban matrix barrier / permeability class**, motivated by the paper's central landscape contrast:

- `permeable` = focal populations embedded in continuous/intact bushland or separated from potential pollen sources by non-urban cleared/rural matrix for which the source treats pollen movement as physically possible;
- `urban_barrier` = remnant populations separated from potential source populations by built-up residential/urban matrix that the source identifies as a barrier to the specialist native pollinator.

Exact population-to-class mapping must be recovered from the paper/supplementary map or source metadata **before** offspring genotype values are summarized.

Do not substitute straight-line distance as the primary predictor after seeing outcomes. Distance to nearest unsampled plants is retained only as a prespecified secondary continuous sensitivity because the source explicitly argues that matrix type modifies the meaning of distance.

## C endpoint

Primary C representation = source `m_p + s` pollen-immigration estimate (`m_p`) from Table 2 for each population with progeny, using source SE where estimable.

Do not switch to the `m_p only` model or Cervus estimate because it gives a stronger contrast. Those may be reported as secondary model-form sensitivities only.

## G_offspring endpoint

From the public seedling microsatellite data, derive one population-level offspring genetic-state summary without using adult genotypes as a new independent 2026 layer.

Primary offspring metric = expected heterozygosity `H_E` calculated across seedling multilocus genotypes within each population, because it is a standard cohort genetic-diversity state and can be computed without parentage-model tuning.

If the raw archive does not contain population-linked seedling genotypes sufficient to calculate population `H_E`, terminate as `offspring_genetic_state_not_reconstructable` rather than switching to a favorable genetic metric.

Population-level uncertainty must be estimated by a fixed locus bootstrap (10,000 resamples of loci with replacement; RNG seed 20260913). Seedlings remain nested observations used to estimate the population state, not independent landscape n.

## Effect representation

If both C and G_offspring are reconstructable on the common population frame:

1. compute the population-level association with the locked binary matrix-barrier exposure using the same contrast orientation (`negative = worse support/state under urban barrier`);
2. preserve C source-model uncertainty and G locus-bootstrap uncertainty;
3. reconstruct within-cluster dependence from the paired population-level C and G contributions / centered population values where mathematically possible;
4. require the resulting working covariance block to be positive definite.

No covariance is silently set to zero.

## Source opening order

1. Dryad metadata / filenames / schema only;
2. source paper/supplementary map to freeze exact population barrier classes;
3. raw seedling genotype values;
4. one-shot population-level G summary and covariance-aware C/G cluster calculation.

## No-rescue rules

Do not:

- count adult G again as a 2026 effect;
- treat seedlings, maternal plants or loci as independent fragmentation n;
- code populations G/H with no progeny as G_offspring=0;
- replace `m_p+s` by another paternity model after observing the contrast;
- replace `H_E` with allelic richness, F_IS or another genetic metric after observing direction;
- replace matrix barrier with geographic distance after observing results;
- combine PS010 adult genetic values into the covariance block as if contemporaneous offspring data;
- use post-2017 genetic observations as the seedling cohort.

Possible terminal outcomes:

- `ML005_admitted_C_Goffspring_covariance_aware`;
- `matrix_class_not_identifiable`;
- `offspring_genetic_state_not_reconstructable`;
- `common_population_overlap_insufficient`;
- `covariance_not_reconstructable`;
- `source_access_blocked`.

All outcomes are acceptable.
