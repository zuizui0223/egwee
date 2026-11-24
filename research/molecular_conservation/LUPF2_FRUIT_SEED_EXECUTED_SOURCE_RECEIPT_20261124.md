# LUPF2: executed original fruit–seed source alignment and scope ceiling, 2026-11-24

**Status:** `POSTHOC_FRUIT_SEED_SOURCE_INTEGRITY_COUNTS_ONLY` — SOURCE QUALITY, **NOT** a new ecological or genetic effect test. The original LUPF1 source-integer validity stop, LUPF2 exploratory 5-fold 23.28% predictive improvement, and negative posthoc onset coefficients stay unchanged.

## Original biological source, diagnostic, reproducibility

- Primary field experiment: Sacristán-Bajo et al. (2026), *Annals of Botany*, DOI [10.1093/aob/mcag061](https://doi.org/10.1093/aob/mcag061); original public Figshare [10.6084/m9.figshare.29606180.v1](https://doi.org/10.6084/m9.figshare.29606180.v1), source `Lupinus_angustifolius_data_field.xlsx`, SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`.
- Frozen targeted no-model protocol: `research/molecular_conservation/LUPF2_SEED_FRUIT_SOURCE_INTEGRITY_PROTOCOL_20261124.md`, committed `5e0ece3e6e9fc86c4876ca0517a5ad3f5f12fd65` before reading the original `number of fruits` values for this audit.
- Executed [Actions run 45355506975](https://github.com/zuizui0223/egwee/actions/runs/45355506975), job `lupf2-posthoc-fruit-seed-integrity`: SUCCESS. [Artifact 14901334420](https://github.com/zuizui0223/egwee/actions/runs/45355506975/artifacts/14901334420), `sha256:edb861755ea03e6b53d756b41bda084035177eb6945fcb36056ba797a85af16a`. Original third-party data never committed or redistributed; only category counts by FRO/PIC and total were saved. No modelling or p-value.

## Actual archived source quality

| Field or cross-field criterion | All 3,024 records | FRO (1,584) | PIC (1,440) |
|---|---:|---:|---:|
| `number of fruits` nonnegative **integer** | 2,035 | 1,113 | 922 |
| `number of fruits` missing or NA | 989 | 471 | 518 |
| `number of seeds` nonnegative **integer** | 1,881 | 1,060 | 821 |
| `number of seeds` nonnegative **fractional** | **153** | 52 | 101 |
| `number of seeds` missing or NA | 990 | 472 | 518 |
| Source `number of fruits=0` observed | 342 | 216 | 126 |
| Source `number of seeds=0` observed | 344 | 218 | 126 |
| **Fractional seeds and positive fruit count** | **153** | **52** | **101** |
| Positive fruit count, missing seed index | **1** | **1** | **0** |
| Numeric seed-index and onset jointly recorded | 2,008 | 1,102 | 906 |

Every numerical fruit entry is an integer; **all 153 fractional seed-index records have a positive integer fruit count**. There was **no recorded positive seed-index on a zero-fruit record**. Seed-index missingness almost exactly tracks fruit count missingness (990 vs 989), and observed structural zero counts are close (344 vs 342).

This alignment is consistent with the source seed-index being derived partly from fruit observations, but **does not identify or prove the exact 2026 computation rule**. A counted raw number of viable seeds should be an integer, whereas fractions could arise from fruit number times average seeds/fruit, sample-level estimation, Excel transforms, or other undocumented methods. Related 2025 experimental paper (DOI 10.1111/eva.70087) used fruit count times mean seeds/fruit as a reproductive estimate; author's 2023 thesis Chapter 4 describes collecting plants and counting seeds, but neither proves 2026 archived value provenance. The discrepancy requires primary author/source documentation or detailed original supplementary methodology.

## New source-methods reconciliation and prior art

Separate first-row header run [45355170533](https://github.com/zuizui0223/egwee/actions/runs/45355170533) verified all ten 2026 source columns: `id, population, line, genotype, shoot growth, flowering_onset, number of fruits, number of seeds, biomass, germinated seed weight`. No explicit physical block or sowing-point, no SNP calls, pollinator/paternity or viable offspring recruitment.

Original 2023 doctoral thesis Chapter 4, printed pp.194–199 (https://burjcdigital.urjc.es/server/api/core/bitstreams/e43b6427-a0c1-4d55-ae97-83945eecee8d/content) described an outdoor **four-block** experiment with 2,808 seeds (78 maternal genotype units ×36), two northern populations, and four biological treatment names (CFL, EFL, OUTS2, SPL2). The new 2026 deposited workbook has 3,024 rows, 84 genotype labels, **six opaque line letters** C/J/L/R/T/X, and no explicit block. The 2,808 matching C+J+L+T rows and 216 R+X surplus are an arithmetical coincidence consistent with a design revision, **not a verified treatment/pedigree crosswalk**. The thesis specified 8 source maternal genotypes for FRO SPL2; code J has 8 in FRO but is not proved to be SPL2.

Earlier Sacristán-Bajo et al. (2022 online/2023 print), DOI [10.1111/eva.13510](https://doi.org/10.1111/eva.13510), already reported an earlier-flowering versus more-seeds correlation in northern control lines under controlled common-garden conditions. LUPF2 is thus **not the first discovery of any flowering–seed association**, but a newer *exploratory within-source grouped prediction* for the outdoor filed data, with its own severe missingness and potential selection bias.

## Conservation and scientific decision

- **LUPF2 (already fixed, not rerun):** conditional on 2,008 complete cases, adding flowering onset to FRO/PIC + anonymous line gives MSE 1.134807→0.870675 (23.28% reduction) with five positive genotype-grouped heldout folds and posthoc negative onset coefficients; not out-of-physical-block or out-of-site validation, and **not fully independent of original published 2023 experiment**.
- **Source semantics improved:** archived seed measurement appears tightly related to observed fruit number; yet its exact computation is not verified and no original individual-level SNP–outcrossing–pollen–seed/recruitment join exists.
- **Next gate:** author-verified 2026 supplemental methods/line-code dictionary that explains (a) 6 letters to 4 treatment groups, (b) 216 extra records, (c) seed-index computation, (d) sowing-block/point crosswalk. In absence of these, report `SOURCE_FRUIT_SEED_ALIGNMENT_ONLY; T_TO_W_EXPLORATORY; GxIxF_NOT_IDENTIFIABLE`.
- **No further outcome model search** on this same positively evaluated source to manufacture a genetic or pollination rescue result. New natural conservation claim requires independent populations and prospective phenotype, pollen compatibility, paternity, and viable recruits measured on the same individual/cohort.
