# LUPF2 — executed exploratory phenology × field reproductive-index prediction (2026-11-24)

**Status:** `EXPLORATORY_PREDICTIVE_INCREMENT` within one original field experiment. This is a **new exploratory source-data analysis**, not confirmatory inference, genetic/molecular causal evidence, pollination restoration, natural EGWE G×I×F transport or an ecological early-warning signal.

## Executed original-source and protocol provenance
- Source: Sacristán-Bajo et al. 2026, *Annals of Botany* DOI [10.1093/aob/mcag061](https://doi.org/10.1093/aob/mcag061); Figshare original file [10.6084/m9.figshare.29606180.v1](https://doi.org/10.6084/m9.figshare.29606180.v1) `Lupinus_angustifolius_data_field.xlsx`. Original workbook SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`.
- Original LUPF1 strict integer endpoint remains `SOURCE_ENDPOINT_INVALID_STOP` (run 45328288235); post-stop data-quality audit in run 45328462636 found 153 nonnegative fractional original source entries. **Do not overwrite original null/stop.**
- Separate **explicitly exploratory LUPF2** preread protocol at commit `053eca26bc1b527e828cb82cbac9318d20be7621`, *after knowing endpoint-validity counts but before the LUPF2 predictive comparison*. Same population/anonymous-line M0 and onset M1, ridge lambda=1, SHA256 5-fold grouping, fixed success rule; only eligibility changed to accept finite nonnegative numeric source seed-index, never round. See `LUPF2_EXPLORATORY_CONTINUOUS_SEED_PROTOCOL_20261124.md`.
- Original-data run [45328763380](https://github.com/zuizui0223/egwee/actions/runs/45328763380) completed successfully, CI job `lupf2-exploratory-continuous-reproductive-index`; original-source aggregated [artifact 14890453574](https://github.com/zuizui0223/egwee/actions/runs/45328763380/artifacts/14890453574), ZIP digest `sha256:39ccf790679b3a1c32a2df96ca50800dffddb6df6bc14fa72d351e262209198c`. Original third-party row-level source and ID labels were **not** redistributed.
- Independent source-only engineering tests and frozen protocol ancestor checks passed; no independent field study validation or publication of this posthoc estimate claimed.

## Actual source denominator / missingness

| Item | Recorded |
|---|---:|
| All original planted/experimental source records | 3,024 |
| Source-defined `population|genotype` groups (non-SNP family labels) | 84 |
| Missing source-stored seed-production index | 990 |
| Seed values nonnegative integer / fraction | 1,881 / 153 |
| Explicit numeric source zero seed-index entries (before complete-case intersection) | 344 |
| Missing flowering onset | 982 |
| Numeric seed-index but missing onset | 26 |
| Jointly numeric finite nonnegative seed-index + flowering onset | **2,008** |
| Fold group counts | 20, 11, 11, 20, 22 |
| Fold record counts | 503, 244, 244, 482, 535 |

Rows are NOT independent genetic-lineage replicates, and 2,008 complete cases are **not** the total successful germinants or viable next-generation recruits. Missing seed values may be nonrandom; do not substitute zeros or infer population-level total fecundity.

## Exploratory fivefold grouped out-of-fold prediction

Outcome `log1p(source-stored number of seeds numeric proxy)`. M0 includes the literal anonymized two populations and six line categories only. M1 adds a single continuous training-standardized `flowering_onset`. Neither includes SNP genotypes or inferred AGF controls. Groups `population|genotype` cannot cross fold boundaries; this tests *within-study unseen family-label transfer*, not unseen landscapes.

| Fold | n records | n genotype groups | M0 heldout MSE | M1 heldout MSE | Gain M0−M1 |
|---|---:|---:|---:|---:|---:|
| 0 | 503 | 20 | 1.273865 | 0.942877 | +0.330987 |
| 1 | 244 | 11 | 0.745584 | 0.579755 | +0.165829 |
| 2 | 244 | 11 | 1.237712 | 0.962147 | +0.275566 |
| 3 | 482 | 20 | 1.118447 | 0.924494 | +0.193953 |
| 4 | 535 | 22 | 1.149388 | 0.845267 | +0.304121 |
| **Pooled** | **2,008** | **84** | **1.1348068698** | **0.8706748619** | **+0.2641320078** |

**Descriptive normalized reduction in pooled MSE:** `(1.1348068698−0.8706748619)/1.1348068698` = **23.28%**. 5/5 fold gains positive. Fixed out-of-fold predictions, genotype-group bootstrap with 1,000 seeded replicates gave quantile interval for gain **[0.19137298, 0.33740039]**. This is **not** a full-model-refit bootstrap, an independent-field-system uncertainty interval, or a valid post-selection confirmatory p-value.

Primary exploratory answer: adding flowering time **improves out-of-family-label prediction of the source reproductive-index proxy within this single F3 field dataset** relative to a literal original-population + anonymized line baseline. It does not specify slope sign or establish that genetic variation or genetic rescue *caused* any seed-production benefit.

## Biological interpretation and claim ceiling

A biologically interesting but **unproven mechanism** is that shifting flowering time changes the length/conditions of successful reproduction, thereby linking an evolved developmental trait T to a reproductive proxy W under natural conditions. Actual seed-index derivation in the 2026 field data, and its reproductive observation/missingness process, remain under-specified. The same team's 2025 controlled-condition study computed a *seed-per-plant estimate* from fruit number × mean seeds per fruit; this establishes a plausible cause of noninteger values but **does not independently establish the 2026 protocol** (Sacristán-Bajo et al. 2025, DOI [10.1111/eva.70087](https://doi.org/10.1111/eva.70087), Methods §2.3).

The 2026 field experiment's treatment codebook C/J/L/R/T/X is not mapped to control/AGF/selection from verified source identifiers; 2025 and 2026 genotype-family labels have zero exact direct cross-study matches. This observational predictive improvement must **not** be attributed to assisted gene flow or molecular mechanism. There are no measured wild pollinator interactions, compatible pollen receipt, independent molecular genotype calls in the 2026 cohort, or viable offspring recruitment. It provides **T→W predictive alignment only**, one part of the much broader, still untested eco-genetic cross-layer theory.

Conservation implication is a **monitoring design priority**, not a management recommendation: co-measure flowering onset, effective pollen source/mating compatibility and next-generation seedlings by mother/family across independent environments; do not rely on neutral diversity or census alone. Preserve the original LUPF1 endpoint stop and distinguish all exploratory findings from independent natural tests.
