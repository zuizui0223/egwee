# EGWEE independent fatherhood-source coverage: accessible original wild programme, no false contact-pair replication

**19 Nov 2026.** Publisher-source original structural receipt [GitHub Actions 44513179110](https://github.com/zuizui0223/egwee/actions/runs/44513179110). This checks two **additional independently published original study programmes**, not two replicates of the exact Barbot 2026 genotype-to-contact edge test. No biological coefficient, parentage association or genotype value was inspected during this source-only stage.

## Leventhal et al. 2026 (*Brassica rapa*) — public file-stream access STOP

Original paper *Longitudinal and cross-sectional selection on flowering traits in a self-incompatible annual*, [Evolution](https://doi.org/10.1093/evolut/qpag047); publisher archive [Dryad 10.5061/dryad.tdz08kqdr](https://doi.org/10.5061/dryad.tdz08kqdr). The original public dataset's DOI, version file manifest and two advertised file names are **source-metadata verified**:

- `Leventhal_et_al_2026.zip` original ~1.67 MB, target source original paternity + maternal batch + detailed donor flower time/plant positions and plot-level visitor sampling.
- `README.md` original ~62 KB, accessible in official published web indexing.

The official Dryad API `stash:download` returned **HTTP 401** for each original file on the GitHub Actions public runner. We did not infer the files were private everywhere, bypass the publisher authentication, silently substitute scraped sources or fabricate a male–maternal pairing. `PUBLIC_ORIGINAL_SOURCE_ACCESS_STOP`, **0 original files opened**, **0 original sire/phenology/visitor keys verified**. The original published study describes 4 experimental populations, 854 donors, 180 male-sterile gene traps and 1,970 genotyped offspring, but **none of those advertised individuals have been reanalyzed here**. A four-population experimental original paper is **one source research programme**, not four independent natural ecosystem replicates.

## Rhodes et al. 2017 (*Oenothera harringtonii*) — all 9 original files verified

Original paper *Pollinator identity and spatial isolation influence multiple paternity in an annual plant*, [Molecular Ecology](https://doi.org/10.1111/mec.14115); original [Dryad 10.5061/dryad.p24q3](https://doi.org/10.5061/dryad.p24q3); its official published [Zenodo mirror record 4942351](https://zenodo.org/records/4942351), CC0. The publisher provided valid size+MD5 original file streams, all **9/9 exact file names and checksums passed**. Original text first-row schemas and physical rows were read without opening effect signs or per-plant values:

| Source original filename | Original data lines (excluding first row) | Verified original field labels |
| --- | ---: | --- |
| `multiplePaternity.csv` | **60** maternal seed-family rows | `plantID, treatment, isolation20, correlatedPaternity` |
| `pollenDispersal.csv` | **406** assigned-seed dispersal distances | `treatment, distance` |
| `pollinatorBouts.csv` | **175** source insect observation bouts | `time, visitor, flowersVisited` |
| `amPollinators.csv` | **24** binned source observation records | `abundance, pollinator` |
| `pmPollinators.csv` | **34** binned source observation records | `abundance, pollinator` |
| `overallPollinators.csv` | **58** source visitor summary records | `abundance, pollinator` |
| `obs.csv` | **4** observation summary records | `time, insect, rate, se` |
| `genotypes.xlsx` | Original XLSX source checksum PASS | workbook structure only; genotype cells unopened |
| `Rhodes et al. 2017.R` | Original author code MD5 PASS | code not executed |

**Biological grain:** 60 seed-family/fruits with mother `plantID` and original pollinator-exclusion `treatment` labels `c/de/ne`; spatial maternal isolation quantified by `isolation20`. The 406 pollen-dispersal original seed rows show only treatment and distance in the published source table, not father or maternal ID, and the 175 insect bouts have time/guild/flowers visited, not a source woman-plant-specific visitation partner. **DO NOT JOIN them** as if they were direct visitor→individual mother/father movements. The same directed mother→pollen-donor contact excess as PR #90 cannot legitimately be computed in this programme from these publicly advertised source tables.

The original authors previously established that hawkmoth versus solitary-bee access affects multi-paternity and maternal isolation reduces multi-paternity. Those are **original prior art**. A subsequent separately frozen original maternal-heldout forecast tests the narrower, *new prediction-sufficiency estimand*: does exclusion treatment add out-of-mother predictive information for the MLTR correlated-paternity proxy above isolation alone? The prediction must be evaluated on original maternal groups and is not the same as mate identity prediction.

## Generalization status

- Barbot 2026: 1 original programme with exact source-mapped mother/father genotype and directed inferred contact, +12.61 pp above offspring-marginal null under co10, pilot only.
- Leventhal 2026: metadata verified but source bytes blocked at this audited endpoint; **no source-matched direct visit-father replication**.
- Rhodes 2017: source bytes all verified, 60 maternal fruit records and 175 foraging bouts, but no direct mother–father visitor pair join; **not an independent replicate of the Barbot direct edge metric**. A new ecological outcome-level association may be measured with a different observation target but can **not** be pooled with PR #90 as an equivalent effect.

All original public datasets remain with source publishers. No original SNP/microsatellite genotypes, mother identities, paternity values, visit-bout observations, source rows or father ID assignments redistributed. No changes to theoretical `egwe`, egwee main fragmentation meta, previous scientific PRs or source-study denominators.
