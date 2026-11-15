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

## Executed within-fitness mother–seed ID gate (2026-11-15)

An independent blinded source check was run on the original fitness workbook (SHA-256 `07e37aa193dfdf974de229cf29f0255126dc3e75d32c0189002d8eb81e77b5b2`). Script: `audit_dianthus_within_fitness_maternal_ids.py`. This uses **only Population / Source / Transplant code / Maternal transplant / Seedling code** from the three fitness sheets and checks that `HL` exists in the F0-flowering and F1-juvenile sheet headers. It reads neither HL values nor any reproductive performance values.

| Key contract | F0 seed rows matched to F0 flowering | Exact matched keys | Ambiguity |
|---|---:|---:|---|
| `Transplant code` alone | **84/125 (67.2%)** | 72 | Many-to-many label reuse: 23 matched flowering keys and 11 seed keys are duplicated |
| `Population × Transplant code` | **56/125 (44.8%)** | 49 | 13 matched flower keys and 6 seed keys duplicated |
| **`Population × Source × Transplant code`** | **31/125 (24.8%)** | 31 | **One-to-one literal links**, no duplicate keys within the matched subset |

All 31 strict matches are **candidate** same-transplant links: verifying matching strings is **not** verification of the original source's biological individual identity and cohort semantics. The strict key leaves **94/125 seed records (75.2%)** unmatched. Running a regression on only the 31 matched rows would risk cohort/source selection bias and would not represent the original 125 maternal records without explaining missingness.

For `F1 juvenile` (`Maternal transplant`), **0 of 1,171 rows** directly join to the F0 flowering `Transplant code`, whether unstratified, population-stratified or population+source-stratified. It is plausible that two original datasets use different maternal coding conventions; **no guessed prefix, fuzzy key or family assignment is permitted**.

The original published article already analyzed inbreeding, heterosis, seed/juvenile fitness and local origin effects (DOI `10.1111/mec.15930`). A reanalysis of just `HL→seed` in these same records is not in itself novel and cannot establish causal genetic rescue. The novel multi-study question still requires independently replicated, controlled genetic-vs-ecological function contrasts.

**Decision:** `STRICT_31_LITERAL_LINKS_ONLY; SOURCE_ID_DICTIONARY_AND_MISSINGNESS_STOP` for F0 seed-level molecular association; `F1_MATERNAL_ID_CROSSWALK_STOP` for mother–juvenile linkage. Keep the direct 0-match genotype–fitness file result as a distinct issue; an HL column already embedded in the fitness table is a different measurement route.

**No effect direction or source outcome column has been opened for this programme.** If literal ID linkage fails, use source metadata or corresponding author crosswalk, not string guessing.
