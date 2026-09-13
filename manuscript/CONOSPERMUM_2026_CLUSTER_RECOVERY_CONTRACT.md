# ML005 / PS011 Conospermum 2026 cluster-recovery contract

**Locked:** 2026-09-13, before opening the public adult/seedling genotype values for effect estimation.

## Goal

Attempt to recover one additional independent multilayer cluster from Delnevo et al. (2026), *Ecology and Evolution* 16:e73406, DOI `10.1002/ece3.73406`, using the public Dryad dataset `10.5061/dryad.95x69p907`.

Target layers:

- `C_movement_connectivity`: contemporary pollen immigration;
- `G_offspring`: contemporary seedling genetic support (`H_O`).

The adult genotype table is historical/standing-cohort context already represented elsewhere in the Conospermum programme and is not counted again as a new `G_adult` effect in ML005.

## Independent-unit frame

The independent units are **populations**, not seedlings, maternal plants, loci, or paternity assignments.

Primary paired frame: populations that have both a source pollen-immigration estimate and a recoverable seedling genetic summary from the 2017 seed crop. Seedlings remain nested observations used only to reconstruct one population-level offspring-genetic value per population.

A population with no progeny is not coded as `G_offspring = 0`; absence of a recoverable offspring genetic state is missing data, not zero genetic support.

## Exposure lock

The primary fragmentation exposure is the source-defined **population connectivity index** described in the 2026 paper: the modified incidence-function measure incorporating distances to neighbouring populations and their areas.

For the quantitative gradient stream:

`fragmentation_severity = -z(source_connectivity_index)`

Standardisation is linear and therefore does not select a transformation after seeing outcomes. Higher severity means lower landscape connectivity.

### Exposure recovery order

1. recover the exact per-population connectivity index from the 2026 publication/supplement/source files;
2. if absent there, recover it from an earlier source table/dataset **only if** population identities are explicitly the same and the source confirms that the same connectivity definition is used/reused in the 2026 study;
3. if the exact continuous connectivity index cannot be recovered, stop the primary gradient admission attempt.

Population size, `H_O`, seed production, pollen immigration itself, or whichever landscape variable gives the strongest relationship cannot replace the locked connectivity exposure post hoc.

The built-up-versus-cleared/vegetated matrix interpretation is retained as mechanism/context. It is not converted into an ad hoc binary exposure unless the source supplies an unambiguous population-level categorical classification independent of the outcomes and a separate amendment is locked before fitting.

## C endpoint lock

Primary C endpoint: the population-level NMπ `m_p + s` pollen-immigration estimate reported by the source model, because that is the publication's selected neighbourhood model rather than an outcome-selected alternative.

Use the population point estimate as the population-level C response. Populations A/B are retained if they are in the paired frame even though immigration there includes unsampled plants within large continuous populations; the publication explicitly treats those estimates as a relatively intact baseline. Any population for which the source says the estimate is not estimable remains missing rather than being repaired from another model only because it helps the result.

Orientation: larger pollen immigration = greater contemporary connectivity support. Therefore stronger fragmentation severity is expected, but not required, to correlate negatively with C.

## G_offspring endpoint lock

Primary G_offspring endpoint: population-level seedling observed heterozygosity (`H_O`) reconstructed from the public `Seedlings_scoring_unformatted.xlsx` / equivalent Dryad file.

For each population:

1. score heterozygosity within each typed diploid locus for each seedling;
2. calculate the population `H_O` from typed genotype observations without treating loci or seedlings as independent fragmentation replicates;
3. retain one population-level value in the gradient analysis.

`F_IS`, allelic richness, or alternative offspring-genetic summaries may be retained as sensitivity representations, but cannot be added as independent G layers beside primary `H_O`.

## Effect representation

For each primary layer, estimate the population-level correlation with the locked fragmentation severity and transform it with Fisher's r-to-z transformation.

The effect stream remains `fisher_z_correlation_with_fragmentation_severity`.

Do not:

- use seedling N as the meta-analytic independent-unit count;
- substitute adult `H_O` for offspring `H_O` when offspring data are missing;
- switch from NMπ pollen immigration to Cervus or `m_p only` because another representation gives a stronger effect;
- choose population size/connectivity/matrix after comparing their effect directions;
- code populations with zero seedlings as zero offspring genetic diversity;
- count C and G as separate studies.

## Within-cluster dependence

C and G belong to one ML005 cluster. Preserve their paired population table.

If a stable sampling-covariance block for the two Fisher-z effects can be reconstructed from the paired population data under a prespecified method, store it with method/provenance. Otherwise mark covariance as known-but-not-reconstructable and use the already-declared cluster-robust fallback; covariance must not silently be set to zero.

No extra independent-cluster count is created by adult contextual genetics, selfing, pollen-distance endpoints, or multiple genotype metrics.

## Admission gate

ML005 is promoted only if all of the following are satisfied:

1. exact source-defined connectivity exposure is recoverable for the paired populations;
2. C point estimates are source-supported on those populations;
3. seedling `H_O` can be reconstructed from public raw genotype data on the same population frame;
4. at least four paired populations remain after source-defined missingness, so a Fisher-z gradient is estimable;
5. dependence is explicitly represented by a covariance method or cluster-robust fallback.

Possible terminal outcomes include:

- `ML005_admitted_C_Goffspring_gradient`;
- `offspring_genetics_recovered_exposure_missing`;
- `common_population_frame_too_small`;
- `source_connectivity_not_reconstructable`;
- `raw_genotype_schema_not_reconstructable`.

All terminal outcomes are acceptable. No rescue analysis is selected from observed effect direction.
