# QPF004 — pollen-assay ascertainment and induced site–week nonoverlap

**2026-11-18 — POSTHOC ORIGINAL-SOURCE COVERAGE AUDIT. No new biological hypothesis test.** The original *Mertensia ciliata* 2016/2015 same-ramet/source-plant Q/P/F study remains frozen: registered 2016 whole-week M0 MSE **0.781536** versus M1 (+CP/HP) **0.892846**, a 14.24% worsening with **1/5** week wins. Original pre-outcome protocol-only SHA `ab174531e7311b3953e7df5daf86da3ffcb4a99f` and [QPF004 result](QPF004_ORIGINAL_QPF_HOLDOUT_RESULT_20261118.md) are unchanged.

## 1. Original source and fixed measurement-unit selection

Original 2020 study: Gallagher & Campbell, *American Journal of Botany*, DOI [10.1002/ajb2.1439](https://doi.org/10.1002/ajb2.1439); original Dryad [10.7280/D19X0D](https://doi.org/10.7280/D19X0D). The user-supplied original archive (SHA256 `635946881e42b2e67b25a3895111089db4d3d99081a7d27cb8be9e4775c1912f`) and 2016 Excel (SHA256 `bbfcbbaf43b53b0ef835b891bd8932ae3761a383e4ecb1f38440a4ba9d477c38`) were verified against official Dryad source fingerprints. No raw workbooks, PDFs, individual `plantID`, visit/pollen/seed source values, or predicted individual outcomes were uploaded.

This diagnostic compares the **original same-ramet stigma-P measured versus P unmeasured** status across **all 232 seed-assayed ramets**. `P measured` was defined by an exact original `plantID` match to the source `pollenDep` sheet (62 rows) and never by seed yield or model improvement.

### Original pollen-assay coverage by experimental treatment

| 2016 original treatment | P assayed | P not assayed | Assay coverage | Mean seeds per marked flower, P assayed | Mean seeds per marked flower, P not assayed |
|---|---:|---:|---:|---:|---:|
| Single observed visit (V) | **47** | **47** | **50.0%** | **0.9343** | **1.0724** |
| Open/no observed visit (O) | **15** | **50** | **23.1%** | **0.0411** | **0.1071** |
| Bagged (B) | **0** | **73** | **0.0%** | **not measured** | 0.0296 |
| **All source treatments** | **62** | **170** | **26.7%** | **0.7182** | **0.3407** |

The pooled P-assayed group is **75.8% single-visit** (47/62), whereas only **27.6%** of the 170 unassayed ramets received that treatment (47/170). Original source seed data have **no P measurements in the entire bagged group**. Therefore **the all-arm pooled positive seed difference is compositional** and cannot be called a direct biological association between pollen deposition and seeds. In fact, **within the V arm** the mean seed/flower is slightly *lower* in the P-assayed subset (0.9343 versus 1.0724), and within the O arm likewise lower (0.0411 versus 0.1071). These are **descriptive**, not randomized comparisons of P measurement or causal tests. Their signs must not be used to select a different fitted model.

The P-assayed 62 ramets also have **50.0%** original zero-seed records, versus **72.9%** for the 170 without P measurement; the original source mean number of marked flowers differs (**3.66** versus **7.15**). These differences further show that the observed P-complete sample is not an unmodified random draw of the original 232-ramet outcome cohort.

## 2. P measurement itself removes site×week support

| Source site / week | All original seed-assayed ramets | P-assayed ramets | P assay coverage |
|---|---:|---:|---:|
| RG / 1 | 23 | 4 | 17.4% |
| RG / 2 | 58 | 18 | 31.0% |
| RG / 3 | 41 | 16 | 39.0% |
| **SP / 3** | **13** | **0** | **0.0%** |
| SP / 4 | 61 | 20 | 32.8% |
| SP / 5 | 36 | 4 | 11.1% |
| **Total** | **232** | **62** | **26.7%** |

The original 232-ramet seed dataset includes **SP week 3**, so source week and site are *not* perfectly separated in the full seed-outcome source. **But none of those 13 SP week-3 ramets have measured P.** Restricting to the 62 P-complete ramets leaves **all RG measurements in weeks 1–3** and **all SP measurements in weeks 4–5**, creating a perfect source-site versus observation-week block separation in precisely the data used for the pollen-augmented original predictive model.

This is a concrete **measurement/overlap failure**, not evidence that sampling caused the negative predictive result. Because site, week, visitor taxon and pollen-assay inclusion are entangled, a week-heldout P-increment regression cannot identify a transportable pollen causal mechanism or distinct temporal adaptation. The original two-site heldout secondary also had different source site/visitor support, so it was never sufficient independent landscape replication.

## 3. What this changes about the research story

- **Demonstrated**: 62/232 P coverage was treatment-dependent, absent in bagged controls, and removed an overlapping SP-week3 source cell. Therefore the original QPF004 M1 prediction is **conditionally about the P-assayed selection subset**, not all 232 source ramets or their unrealized paternal/pollen function.
- **Not demonstrated**: P measurement causally selected high or low seed producers, stigma grains were necessarily taken from the same eventual seed-producing flower, biological pollen effectiveness was zero, or the 2016 site difference is a historical eco-genetic regime transition.
- **Prior art**: Gallagher & Campbell (2020) already reported that higher per-visit bumblebee efficiency could buffer declining seasonal visitor abundance. Repeating that is not a newly discovered result. The new result here is an auditable **observation-support limitation of a separate out-of-sample analysis**.
- **Independent replication constraint**: Simply acquiring more seed outcomes with no stigma assays, or more CP/HP assays on unmatched flowers, cannot solve the support problem. A genuinely independent test must prerecord **P assay assignment/recovery (`M_P`), visit observation/effort (`M_Q`), fruit recovery and immature/aborted seeds (`M_F`)** for the same mother or ramet, experimental treatment, spatial site and seasonal interval, including overlapping site×time cells and enough original units per cell.

No alternative model, selected favorable site, conventional `p` value, causal inference or changed registered primary decision is introduced. The frozen six-programme atlas still has **two raw-source pilot programmes QPF001 and QPF004**, with different same-flower versus ramet grains; the minimum three genuinely independent complete comparable Q–P–F systems for a cross-study estimator is **not satisfied**.

## Original-source reproducibility

```bash
python research/qpf_source_grain/diagnose_qpf004_pollen_assay_selection.py \
  --source-zip /private/doi_10_7280_D19X0D__v20200619.zip \
  --output /tmp/qpf004_original_P_assay_selection_aggregate.json
```

The executable checks all four published Dryad original file SHA256/CRC, original pre-outcome Git protocol ancestry, original frozen 2016 null and **exact original `plantID` overlap**, then writes only treatment/site×week and response-completeness aggregates. GitHub CI validates its methodology on synthetic examples and the source-free aggregate receipt; Actions does **not** claim to replay the user's private 2020 original workbook.
