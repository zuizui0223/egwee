# Phase-2 source-frame audit — 2026-09-18

## Current state

The systematic-coverage expansion is now separated from the five-cluster significance question. The frozen Phase-1 result remains the baseline; Phase 2 builds a source-defined candidate universe for effect-magnitude and moderator inference.

The seven seed syntheses have now been source-verified at the frame level. This audit does **not** claim that every primary-study row has been materialized yet. It records what the source itself exposes before new effect magnitudes are opened.

| frame | verified public source | source denominator now fixed | next operation |
|---|---|---|---|
| SF01 | Aguilar et al. 2006 Supporting Table S1 | 89 plant species, with source publication attached to each species | materialize and deduplicate source-publication rows |
| SF02 | Aguilar et al. 2008 Appendix S1 | 101 publications / 102 unique plant species | materialize Appendix S1 rows |
| SF03 | Aguilar et al. 2019 Supporting Information | 179 plant species | materialize primary-study bibliography and crosswalk G_offspring/F |
| SF04 | González et al. 2019 Figshare dataset | public dataset verified; exact deduplicated study denominator still to be materialized | materialize publication/species rows from dataset |
| SF05 | Miguel-Peñaloza et al. 2023 Table S1 | **materialized: 177 population rows / 65 source-selected studies / 31 meta subset / 25 title-method multilayer hints**; source flow implies **9 outcome-excluded identities are missing** | restore the missing 9 if identifiable and reconstruct the broader outcome-blind 243/200 frame before declaring SF05 complete |
| SF06 | Aguilar et al. 2024/2025 Supplementary Table S1 | 235 female-fitness publications / 79 male-fitness publications; 83 pollination effects from 75 species | materialize Table S1 and crosswalk repeated systems |
| SF07 | Olhnuud et al. 2025 Dryad | 80-study global dataset; abundance file: 78 observations from 40 publications | materialize publication identifiers; use only as discovery unless an eligible plant response links independently |
| CF01 | citation expansion | cutoff fixed at 2026-09-18 | execute only after source-frame rows are materialized |

## Public-source verification

- SF01: DOI `10.1111/j.1461-0248.2006.00927.x`; publisher page exposes Supporting Table S1 and states that it lists 89 plant species, effect-size metadata, ecological characteristics and source publication.
- SF02: DOI `10.1111/j.1365-294X.2008.03971.x`; source reports 101 publications and 102 unique plant species, with Appendix S1 as the study list.
- SF03: DOI `10.1111/ele.13272`; source reports 179 plant species and exposes two Supporting Information files.
- SF04: DOI `10.1111/cobi.13422`; public Figshare dataset identifier `7520456` is verified.
- SF05: DOI `10.1093/aobpla/plad019`; Supporting Table S1 contains 65 reviewed studies and identifies the 31 used in the complete meta-analysis.
- SF06: DOI `10.1093/aob/mcae076`; source reports 1203 female and 461 male search records, 235 included female-fitness publications and 79 included male-fitness publications, and exposes Supplementary Table S1 as the analysis dataset.
- SF07: Dryad DOI `10.5061/dryad.dz08kps9p`; README reports 80 studies across 28 countries and public richness/abundance CSVs.

## Coverage consequence

The current direct paired-response coverage remains:

- I-F: 1 independent direct programme (ML020) — 4 additional programmes required before pair-specific random-effects estimation opens.
- G_adult-G_offspring: 1 (ML003) — 4 additional programmes required.
- C-F: 2 (ML001, ML002) — 3 additional programmes required.
- G_adult-mean(I,F): 0 — 5 programmes required.

These are **analysis-opening counts, not recruitment targets chosen to obtain significance**. Once a family reaches five independent programmes, every eligible programme discovered in the frozen search universe remains in the analysis.

## Immediate recovery order

Existing programme recovery remains outcome-blind:

1. P1 — ML006 *Primula elatior*: potentially I-F plus contemporary-process/G_adult geometry.
2. P1 — ML007 replicated fragmentation experiment: D-I-F.
3. P1 — ML008 *Tillandsia*: direct I-F.
4. P1 — ML012 *Dieffenbachia*: C-G_mating.
5. P2 — ML010, ML004, ML005, ML011.
6. HARD CLOSED — ML009 and ML013 unless genuinely new independent landscape/reference units become available.

No reported direction, p-value or visually large effect is part of this ordering.

## Next executable milestone

The next Phase-2 milestone is **row materialization**, not model fitting:

1. create one deduplicated bibliographic ledger across SF01-SF07;
2. assign stable programme/system IDs before outcome extraction;
3. classify candidate layer coverage from title/abstract/methods/source metadata;
4. freeze the candidate-universe ledger;
5. only then open new numerical effects.

Until that milestone is complete, the five-cluster Journal of Ecology manuscript remains the valid baseline submission.


## SF05 row-materialization result

SF05 is now the first row-materialized Phase-2 source frame. Its published Table S1 yielded 177 population rows grouped into 65 source-selected studies; 31 match the source meta-analysis membership, 25 carry title/method multilayer-screening hints, and one DOI links to an already registered EGWEE seed. The source article reports 74 studies at the habitat-status + Sp stage but Table S1 contains only 65 because six non-significant FSGS studies and three outlier-Sp studies were removed. Consequently SF05 remains **outcome-blind-frame incomplete** and is not counted as systematic-frame complete.
