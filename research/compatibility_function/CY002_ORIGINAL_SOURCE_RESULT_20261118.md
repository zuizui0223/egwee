# CY002 — original *Cyanus segetum* whole-plot mating-state prediction: no portable increment from relative visitation

**Date: 2026-11-18. Result: `NO_PRACTICALLY_PORTABLE_INCREMENT`.** This is an **exploratory, source-denominator-corrected reanalysis** of one published French farm experiment, not a new biological discovery or fully blinded independent confirmation.

## Actual original source and why CY001 was stopped

- Original study: Labonté et al. (2024), *American Journal of Botany*, [10.1002/ajb2.16440](https://doi.org/10.1002/ajb2.16440), original Dryad dataset [10.5061/dryad.9p8cz8ws1](https://doi.org/10.5061/dryad.9p8cz8ws1).
- The **user-supplied, 44,060-byte ZIP**, `doi_10_5061_dryad_9p8cz8ws1__v20240920.zip`, has SHA256 `1d1f03c1f3dee00e3bd0d62b74099f5bd31162d61f7a61f4984e0a19b9c5d973`. Its original `Data_Dryad.xlsx` has **27,995 bytes**, SHA256 `18941f666c040c81c5db3f43c661d44fc157e9db636eef07a4aafd49f77b5332`, exactly matching the official Dryad file manifest; `README.md` SHA256 also matches `530018a194d6ccdad3bea3b504e48b5c1b0f9f1fe1e9945fe9ca8aa8708fbcb1`. ZIP CRC passes.
- The original source has **33 unique mothers in 12 plots**, nested in ONE original farm; 20 wildflower-strip and 13 grass–legume-strip mothers. Plot sizes: ten plots with 3 mothers, one with 2, one with 1. All registered key fields are complete.
- The original **CY001** prospective source gate (commit `a118ab77e71a097b46d264738e34c0428384a304`) expected **15–17 successfully genotyped offspring per mother**, following the simplified original README. However the original workbook has **one with 12**, **one with 15**, **five with 16** and **26 with 17**, totaling **549 genotyped offspring**. The **original paper Methods expressly state 12–17 offspring**, and the published Results confirm total 549. This is a **source-only admission/README discrepancy**, not an exclusion driven by the `rpm` outcome.
- The CY001 gate therefore remains a historical **SOURCE_GATE_STOP** (no CY001 numeric result). A separately committed `CY002_FROZEN_SOURCE_COUNT_CORRECTION_20261118.json` at SHA `98e2635626515950e7d7c29136b2d4c6c3f17722` retains **all 33 source mothers**, changing only the source offspring-number gate. It preserves all original CY001 predictor definitions, ridge penalty, 12 held-out plots and prespecified practical success rule.

**Blinding disclosure:** During first inspection of the original XLSX, an accidental 5-row spreadsheet preview included the **first four maternal observations' `rpm` and seed values**, before the CY002 source-only correction commit. No response regressions, whole-plot prediction or criterion selection were performed at that point; the main analysis conditions remained those of CY001. Nevertheless **CY002 is not strictly outcome-blind** and must not be presented as a fully preregistered independent confirmatory test.

## Original biological unit and frozen analysis

The README defines `Relative_MPA_n_visits_per_15_minutes` as **plot-level visitation weighted by each mother's floral display share**; it is *not* a directly counted individual pollen-deposition event. The response `rpm_progeny` is **offspring multilocus correlated paternity**: higher `rpm` indicates fewer distinct fathers, but it is not compatible pollen receipt, direct paternal identity, LA005's marker-detectable outcrossing indicator, or offspring recruitment.

- **M0**: maternal microsatellite allele count + `log1p` local conspecific pollen-donor density, floral richness and floral density + strip type.
- **M1**: M0 plus `log1p` relative maternal attractiveness (visits per 15 min).
- Gaussian ridge with `lambda = 1`, training-only predictor centering and SD scaling, unpenalized intercept, clipped `rpm` predictions to [0,1]. **12 leave-one-WHOLE-plot-out folds**, each original mother predicted once. Each plot contributes 1–3 mothers. No random split or per-child pseudoreplication.
- **Prespecified decision:** positive pooled `MSE(M0)-MSE(M1)`, at least **5% relative MSE reduction**, and **8/12 plots individually improved**. Failure of any part = `NO_PRACTICALLY_PORTABLE_INCREMENT`. No coefficient/p-value selected after outcomes.
- **Secondary (descriptive only):** same M0/M1 feature matrices and 12 plots, on `log1p` seed number from the same 33 **reproductively selected** mothers. The original article reports these 33 were randomly selected from **64 individuals with ≥20 successfully germinated seeds**, among 144 initial plants. Therefore this subset **cannot estimate the distribution of seed failure among all field plants**.

## Complete original 12-plot holdout

| Original plot | Mothers | M0 rpm MSE | M1 rpm MSE | M0–M1 (rpm) |
|---|---:|---:|---:|---:|
| F10 | 3 | 0.001813 | 0.001838 | −0.000025 |
| F3 | 3 | 0.004304 | 0.004410 | −0.000106 |
| F4 | 2 | 0.020527 | 0.020595 | −0.000067 |
| F5 | 3 | 0.000616 | 0.000585 | +0.000031 |
| F6 | 3 | 0.009140 | 0.009466 | −0.000326 |
| F8 | 3 | 0.003870 | 0.009105 | **−0.005235** |
| F9 | 3 | 0.002496 | 0.002754 | −0.000258 |
| G1 | 3 | 0.013638 | 0.013757 | −0.000118 |
| G2 | 3 | 0.024419 | 0.024412 | +0.000007 |
| G3 | 3 | 0.019983 | 0.019944 | +0.000039 |
| G5 | 3 | 0.012278 | 0.013129 | −0.000851 |
| G6 | 1 | 0.038745 | 0.039083 | −0.000338 |
| **Mother-weighted pooled** | **33** | **0.01083242** | **0.01146883** | **−0.00063640** |

The **primary pooled MSE worsened 5.875%**, and **only 3/12 plots improved**. Both requirements for positive support failed. Pooled MAE also worsened, **0.08445 → 0.08839**.

For the selected-mother seed count secondary, M0 `log1p(seed)` MSE was **1.64358**; M1 was **2.05094** (**24.79% larger error**); only **4/12 plots improved**. This seed result is a selected-subset comparison, not proof that visitation fails to affect reproduction in the source population.

## Independent numerical audit

The original XLSX was loaded using `artifact_tool`, fit by NumPy ridge normal equations, and independently reconstructed via **pure-standard-library OOXML decoding + Gaussian elimination**. Across **12 plots × 2 response variables × 2 models × 2 error metrics = 96 values**, the maximum absolute discrepancy was **3.2863×10⁻¹⁴**. No raw maternal ID, original `rpm`, seed count, genetic marker, or original XLSX was posted to the public repository. The posted aggregate JSON is `CY002_ORIGINAL_PLOT_HOLDOUT_RESULT_20261118.json`.

Original-source prediction was completed **locally against the uploaded file**, not inside GitHub Actions: CI is source-withheld and verifies the frozen design, source digest, synthetic XLSX parser and aggregate output consistency. It does not imply the original workbook was downloaded by the GitHub runner.

## Biological interpretation and limits

**The LA005 improvement of ~0.7% for a lower-bound nonmaternal-allele indicator did not replicate as an added-visitation improvement for `rpm` in an independently sourced *Cyanus* one-farm sample.** But different response estimands, local ecological setting, original sampling and conditioning mean this is **not** a pooled cross-study null, a sign reversal of the same coefficient, or evidence that pollinator-mediated mating is irrelevant.

The original study already established complex functional-pollinator-guild associations with correlated paternity and genetic diversity. Our M1 tests one **overall mother-attractiveness** coordinate, not the same original functional-guild abundance interactions, nor effective conspecific pollen delivery. No upstream-to-downstream causal mechanism or island–urban convergence is identified here. The data cannot distinguish partner-quality limitation, pollen donor provenance or unobserved site processes by this one extra predictor.

**Next admissible mechanism test:** independently replicated population/landscape datasets in which visits, *direct successful compatible pollen or paternal contribution*, and viable seed/recruitment from the same mothers are available. No choice of an alternate favorable pollinator feature is justified by this negative outcome.
