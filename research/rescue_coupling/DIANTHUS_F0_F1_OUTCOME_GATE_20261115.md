# Dianthus deltoides — prospective molecular/fitness outcome gate (2026-11-15)

**State: outcome-blind source admission.** Do not treat discovery of two source workbooks as a completed join, fit a novel rescue effect, or reinterpret the original 2021 authors' finding as a new ecological mechanism.

## Provenance

- Primary research: Van Rossum and Le Pajolec (2021), *Molecular Ecology*, [10.1111/mec.15930](https://doi.org/10.1111/mec.15930), 14 microsatellite markers, founder transplants (F0) and F1 seed/recruit fitness.
- Published microsatellite file: [10.5281/zenodo.4650464](https://doi.org/10.5281/zenodo.4650464), `VanRossum_Raspe_Dianthus_molecular.xlsx`, sheet1 contains the source columns `Population`, `Generation`, `Source`, `Ind. code` plus 28 allele columns (14 loci × 2).
- Published fitness file: [10.5281/zenodo.4650488](https://doi.org/10.5281/zenodo.4650488), `VanRossumetal_Dianthus_fitness.xlsx`:
  - sheet1: 619 transplant rows, `Population` + `Source` + `Transplant code`, outcome `Total number of flowers` (current reproductive effort proxy, NOT direct seed set);
  - sheet2: 125 maternal-transplant rows, `Population` + `Source` + `Transplant code`, `Totalseed set` + `Viable seed set` + `Germination` + `Maternal fitness` (candidate direct reproduction);
  - sheet3: 1,171 F1 offspring rows, `Population` + `Source` + `Maternal transplant` + `Seedling code`, leaf numbers + plant mass + `HL` (juvenile *general fitness*, not direct pollination function).
- The genotype sheet has 1,173 record rows. Counts are **raw rows, not independent experimental units**. The population/site/source/maternal-family nesting is not yet validated.

## Locked accession check before outcomes

The script `audit_dianthus_genome_fitness_ids.py` checks literal ID agreement (case and whitespace only) for `Ind. code` vs (1) F0 `Transplant code`, (2) F1 `Seedling code` under progressively strict `individual`, `population+individual`, `population+source+individual` keys.

**Admit a linked row only if:** the source code/individual string has a documented biological meaning, population and source strata match, and the genetic sample is from the corresponding F0 or F1 cohort. Identical ID strings in other populations are not considered same individuals. A mother-to-seedling link via `Maternal transplant` is a relationship, not identical genotype; never attach a mother's multilocus genotype to an F1 seedling as if observed.

Keep all F0 seed endpoints separate; do not collapse flower counts, seed counts and juvenile biomass into a single rescue score without outcome-specific effect-size protocols. Repeated F1 seedlings from one mother are not independent maternal observations.

## Proposed effects only after valid linkage

1. **F0 reproductive function:** conditioned on population and origin/source, relate genetically measured F0 ancestry/heterozygosity or pedigree-supported mating structure to `Viable seed set`/germination. This would be an observational **G→F association**, not an intervention causal `genetic rescue` effect unless assignment/comparator permits it.
2. **F1 genome–fitness association:** measured F1 genotype/ancestry or heterozygosity vs F1 seedling growth/rosette at appropriate maternal-family clusters. This is `G→W_general`, **not** proof of regained interaction-dependent function.
3. **Genetic mixing design:** original common-source translocations must be compared at the proper plot and recipient-patch grain; transplants and progeny from one site do not supply independent programme-level meta replicates.

**No effect direction or source outcome column has been opened for this programme.** If literal ID linkage fails, use source metadata or corresponding author crosswalk, not string guessing.
