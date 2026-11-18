# QPF004 — original *Mertensia ciliata* source confirms 62 ramet-level Q/P/F joins; pollen does not improve held-out week seed prediction

**18 November 2026. Status: `NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT`.** Source-matched original experiment, prospectively frozen before new response covariance inspection. This is one original biological research **programme**, with two distinct 2015/2016 experiments. No new species-level natural replication law or causal flowering-time mechanism is claimed.

## 1. Original source, source integrity and registered analysis

Gallagher & Campbell (2020), *Pollinator visitation rate and effectiveness vary with flowering phenology*, *American Journal of Botany*, [DOI 10.1002/ajb2.1439](https://doi.org/10.1002/ajb2.1439); original dataset [Dryad 10.7280/D19X0D](https://doi.org/10.7280/D19X0D). Original organism **`Mertensia ciliata` (Boraginaceae)**; the earlier “Mimulus/Erythranthe ciliata” atlas entry was incorrect and separately corrected in [PR #81](https://github.com/zuizui0223/egwee/pull/81).

The user provided `doi_10_7280_D19X0D__v20200619.zip`, SHA256 `635946881e42b2e67b25a3895111089db4d3d99081a7d27cb8be9e4775c1912f`. All four original Dryad entries were present, outer ZIP CRC passed, and the extracted files' bytes/SHA256 **exactly matched the independent official Dryad metadata**:

| Original file | Bytes | Original SHA256 |
|---|---:|---|
| 2015 phenology XLSX | 96,329 | `51263c0cabe9dd04dbf716a4594e7d700c5235dd3f85a65ab51f43fcef828411` |
| 2016 pollinator-effectiveness XLSX | 77,873 | `bbfcbbaf43b53b0ef835b891bd8932ae3761a383e4ecb1f38440a4ba9d477c38` |
| 2015 original non-spatial methods PDF | 236,709 | `14d97ecbf68da07252293c751987789d768181bba23da38a9b036dac0cd19972` |
| 2016 original non-spatial methods PDF | 206,337 | `f12e0588619e4a795d7f56a3d42f11cd4b7328716a901041e95f90c67e54ca7f` |

The two source-specific PDFs were **read directly**. The 2016 paper metadata identify a **single-visit**, clone-matched ramet experiment at Rustler’s Gulch (RG) and Schofield Pass (SP), with bagged and open controls; the 2015 metadata identify a distinct potted-plant **phenology manipulation**. Those two experiments do **not** share maternal/flower IDs and are not two independent published natural studies.

**Pre-outcome scientific freeze:** `ab174531e7311b3953e7df5daf86da3ffcb4a99f`, `QPF004_FROZEN_RAMET_POLLEN_SEED_WEEK_HOLDOUT_20261118.json`. The complete relevant original source row/ID counts, eligibility and missingness were checked before this commit; the new pollen/seed correlation and predictive models were first fitted **after** its creation. No outcome-dependent model or exclusion changes.

## 2. Actual observation-unit reconstruction: not 235 completely matched flowers

Original 2016 `gallagher&campbell_pollinatorEffectivenessData.xlsx` has three independently labeled source sheets:

- `Exp2.4_2016_AllData`: **232 unique ramets**, with source mean seeds per marked flower for all 232: **94 visited**, **65 open-no-observed-visit controls**, **73 bagged controls**.
- `Exp2.4_2016_seedCnt`: **232 source IDs**, exact matching **232/232** AllData IDs and year/week/site/experimental treatment/seed count, flower denominator and seed-per-flower values.
- `Exp2.4_2016_pollenDep`: **62 unique ramets**, exact matching **62/62** AllData source IDs, site, week, treatment and both pollen quantities, and all 62 have a recorded seed-per-flower result.

The **verified joint Q/P/F cohort is 62 source ramets**: **47 visited** and **15 open controls**, **zero bagged controls with measured pollen**. Source visitor categories in those 62 are **20 Bombus, 21 Muscoidea, 6 Osmia and 15 Open**. By site, RG **38**, SP **24**. Week counts **4, 18, 16, 20, 4**. The source row-level arithmetic `seedPerFlr = seedCnt / noFlrs` is reproduced in all **62/62** matched ramets. Of the 47 visited ramets, **28 have more than one marked flower**.

**Critical grain:** The 2016 Methods describe counting stigmatic pollen on marked flowers and reporting mature seeds across marked flowers as a **ramet mean**. Exact ramet matching is established, but it is **NOT** an exact same-flower stigma-to-seed match: destructive collection of a stigma does not follow that same flower to a mature seed. Within-clone visited/open/bagged triplets are described in the source Methods, but the archival sheets contain **no verified unique clone-triplet grouping identifier**. Do not assume 62 independent clone lines or use 235 marked flowers as 235 joint pollen-and-seed observations. Original 2016 bagged ramets are excluded from the P-complete set by measurement, not imputed as zero pollen.

Original 2015 `Exp2_2015_Means` comprises **40 potted plants** (10 per phenology week). All 40 have plant-averaged visits and seeds, but **36** have both conspecific/heterospecific pollen counts and seed result, with week counts **10, 9, 10, 7**. Underlying 2015 source includes 186 stigma-level pollen rows from 36 plants and 508 flower-level seed rows from 40 plants; they join **at plant level in source Means**, not as 186 same-flower pollen–seed pairs. Week 4 visit exposure was altered by the authors adding cut flowers after an initial 15 hours with zero observed visitors. These differences are explicitly retained.

## 3. Frozen predictive question

The original authors already showed that bumblebee visits deposit more conspecific pollen per event and that guild-composition changes offset an approximately fivefold phenology-related reduction in overall visits. **We do not claim that biological finding as new.** The additional falsifiable question is whether the measured **stigma transfer state P** improves **out-of-week prediction** of reproductive function F beyond source visitor identity, visitation/exposure and time.

**2016 registered primary test:** response is original `seedPerFlr` (0–4 mature seeds per marked flower); each of **62 ramets is one prediction unit**. M0 includes numeric week, site (SP vs RG), log available flowers and number marked, observed visited marked flowers per marked flower (Open controls coded **zero *observed* visits**, not assumed zero true visits), and visitor identity (Open reference, Bombus, Muscoidea, Osmia indicators). M1 adds `log1p(polDepMC)`, `log1p(polDepNonMC)` and their product. Both use training-only z-scored non-intercept predictors and Gaussian ridge **λ=1**, unpenalized intercept, seed-per-flower forecasts constrained to [0,4]. Validation holds out **one entire observation week** (5 folds, not random flower splits); a positive outcome requires **≥5% pooled MSE gain and ≥4/5 positive week folds**. No alternative outcome or pollinator grouping can rescue failure.

2016 **secondary** site transfer repeats the same source-pinned model with **2 whole-site folds** (RG vs SP). Weeks 1–3 are **entirely RG**, and weeks 4–5 **entirely SP**; date, elevation and site are not independent in this source frame. With only two geographical sites, site transport is descriptive, not replicated regional inference. Source Osmia visitors occur only at RG in the joint set.

The **separate 2015 secondary** uses 36 potted plants and their source means. M0 is phenology week, log original plant visitation rate, log flower number and soil water content; M1 adds plant-mean log CP, log HP and product. Same ridge and 0–4 seed/flower outcome, 4 whole-treatment-week folds. This secondary source has an altered floral display in week 4 and cannot be counted as an independent 2016 ramet replication, or used to replace the registered primary test.

## 4. Original 2016 five-week primary results

| Whole week left out | Matched ramets | M0 MSE | M1 MSE | M0−M1 gain |
|---|---:|---:|---:|---:|
| 1 (RG) | 4 | 0.799766 | **0.658107** | +0.141659 |
| 2 (RG) | 18 | **1.270491** | 1.304068 | −0.033577 |
| 3 (RG) | 16 | **0.515675** | 0.651027 | −0.135353 |
| 4 (SP) | 20 | **0.646433** | 0.871136 | −0.224703 |
| 5 (SP) | 4 | **0.301972** | 0.352911 | −0.050940 |
| **62-ramet pooled** | **62** | **0.781536** | 0.892846 | **−0.111310** |

Adding CP/HP made MSE **14.24% worse** and MAE **0.599759→0.638156**, with only **one of five weeks** improved. Registered primary decision: **`NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT`**. This is a failure of the *specific additional predictive state in the frozen model*, not a statistical test of a zero pollen effect.

### Secondary checks (NOT independent confirmatory tests)

| Separate observational holdout | Source units | M0 MSE | M1 MSE | M0−M1 | Positive folds |
|---|---:|---:|---:|---:|---:|
| 2016 RG vs SP, held-out entire site | 62 ramets | **0.967871** | 1.446190 | −0.478319 | **0/2** |
| 2015 potted plant, held-out phenology week | 36 plants | **1.440171** | 1.527759 | −0.087588 | **1/4** |

2016 site-transfer MSE worsened by **49.42%**, but the two sites and missing taxon/site support prevent general geographic claims. 2015 separate experiment MSE worsened by **6.08%**, with the changed week-4 display regime and limited plant-level P/F correspondence preventing a causal comparison.

### Numerical reproducibility

The actual source workbooks were imported through **artifact_tool**, with ridge evaluated by NumPy normal equations. A separately written **pure standard-library OOXML reader and Gauss–Jordan solver** independently reconstructed all original 2016/2015 joins, original treatment and source-row denominators and the **84 source-derived summary metrics** (5 weekly + 2 site + 4 phenology folds, 2 models × MSE/MAE/prediction mean, plus pooled metrics) to a **maximum absolute discrepancy 6.395×10⁻¹⁴**. Only source-level group counts, fitted fold scores and dataset SHA are published.

Source reproduction command:

```bash
python research/qpf_source_grain/run_qpf004_mertensia_source_weekholdout.py \
  --source-zip /private/doi_10_7280_D19X0D__v20200619.zip \
  --output /tmp/qpf004_2015_2016_original_aggregates.json
```

The public repository contains **neither the source ZIP/XLSX/PDF nor individual original row/clone/seed/pollen data**. CI only checks source-independent model contracts and the archived aggregate arithmetic; a successful Actions run alone is not the original biological data calculation, which was completed locally against the user-uploaded original.

## 5. Scientific meaning and next identification gate

**Evidence of process measurement alignment has improved:** we now know exactly where original single-visit insect identity/number, pollen delivery and seeds are measured on the **same ramet**, and what the joint subset includes. But this dataset cannot establish transfer to the *same flower's eventual function*, genetically compatible donors, actual clonal independence, loss or viability of progeny, or an independent cross-system hypothesis. The P-assayed ramet subset is only **62/232 seed-assayed ramets**, with no bagged pollen controls; the pollen missingness is part of the measurement process, not evidence of ecological zero.

In this **one original programme**, extra CP/HP transfer information failed to improve out-of-week seed/flower prediction beyond an already detailed visitor/exposure/time baseline; the other experiment and site check point in the same **descriptive prediction direction**. This **does not negate** the original authors' documented bumblebee pollinator effectiveness, or imply biological irrelevance of pollen.

For a genuinely general eco-genetic mechanism, matched original `Q/P/F` must also capture experimental **cohort M, spatial/site exposure, fruit/pollen selection and descendant genetic compatibility/recruitment**, with multiple independent regions/species using harmonized prediction targets. Two experiments from one 2020 paper are never counted as two independent studies. The original six-source atlas and prior LA001/LA002/LA005/CY002/QPF001 observations remain unchanged.
