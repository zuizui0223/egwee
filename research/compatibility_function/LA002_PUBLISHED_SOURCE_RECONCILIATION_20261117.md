# LA002 source-vs-paper measurement reconciliation gate — unresolved

**Date:** 2026-11-17. **Classification:** `UNRESOLVED_VISIT_COUNTING_UNIT` and `UNRESOLVED_CONTROL_DENOMINATOR`. These are source-definition differences, not grounds for deleting original observations or selecting a new predictive model. Original raw source SHA256: `82bcaa1c3a504cc779bc9c2aa95199a657dd404b3fdf62f7059e4ff5028b39c1`.

## Independent source inspection

Source XLSX `Pollinator+Data+2014.xlsx` and `Pollinator+Data+2015.xlsx` use 121 *completed* half-hour periods, identified by a source `Open Flowers` row and a closing `TOTAL` row (45 and 76 periods, respectively). Decoding the actual event rows inside those periods produces:

| What was counted | Source-derived count |
|---|---:|
| Complete 30-minute observation periods | **121** |
| Insect-event rows (numeric insect index with a taxon code) | **2,850** |
| Plant-position tokens in those event rows, including source anomalies | **6,702** |
| In-range position 1–32 tokens | **6,701** |
| In-range tokens targeting a position with 0 logged open flowers | **38** |
| In-range tokens retained for LA001/LA002 field rate | **6,663** |

These are **different observational counting units**. The paper's published Table 2 (*Evolution* 71:884–897, [DOI](https://doi.org/10.1111/evo.13167)) reports **3,748 visits across 121 half-hour periods**. **Neither 2,850 insect-event rows nor 6,702 flower-position tokens reproduces 3,748.** The article's 121 period count is reproduced, but this is not a numerical validation of its visit numerator. The source workbook `TOTAL` rows total 6,702 position tokens, not 3,748. Even counting only unique positions per insect row yields 5,064, not 3,748. The raw source does not provide a verified cleaning/mapping rule that reconciles this difference. Do **not** claim the 6,663 accepted source positions are published 3,748 visits.

Separate `Emasculation+experiment.xlsx`, `Final pass`, has 72 rows: 22 solitary, 9 bee-flies, 17 other flies, 2 honeybees, 1 ant and **21 controls**. Original article Methods/Results describe **17** bagged control flowers, one with a single-seed fruit. The source has 21 controls, also one fruit/seed. The paper's species-specific visits (22/9/17), fruit counts (14/6/2) and conditional seed means (~4.07/3.83/3.50) match source assay values, but **which four control rows should be excluded is not identifiable** from this archive alone. No control-based correction was applied to frozen LA002's weights.

## Effect on current conclusions

- LA001 and LA002 define **source-position exposure** from 6,663 admitted position tokens. Their negative held-out MSE results are algebraically reproducible **for that explicitly declared definition**; they are **not yet a complete reproduction of the paper's Table 2 visitation estimates**.
- LA002 uses mean seed output per assigned single-visit flower for AH/BF/F (57/22, 23/9, 7/17), not Table 2's *conditional* seeds per fruit; this is a legitimate fixed but distinct proxy. It does **not** directly measure cross-compatible pollen or viable subsequent recruitment.
- Do not reinterpret the discrepancy as scientific evidence for data error, fraud, or pollinator biology. It could reflect processing rules, row inclusion criteria, unit choices or manuscript exclusions **not recoverable in the available source**.
- **Next priority is author/source-method correspondence or a verified script deriving the reported 3,748 from these original tables**, or a clearly disclosed alternative raw-record operationalization tested in a genuinely independent dataset. Do not tune visits to force published rates or refit the negative model after the outcome is opened.

## Evidence and source

Original paper: Layman, Fernando, Herlihy & Busch (2017), [*Costs of selfing prevent the spread of a self-compatibility mutation that causes reproductive assurance*](https://academic.oup.com/evolut/article/71/4/884/6725895), Methods and Table 2. Published tally: 3,748 visits, 121 periods; bagged controls 17. Independently checked provided Dryad archive (dataset DOI [10.5061/dryad.2pj0j](https://doi.org/10.5061/dryad.2pj0j)). The table and workbook are not assumed equivalent without this missing transformation.
