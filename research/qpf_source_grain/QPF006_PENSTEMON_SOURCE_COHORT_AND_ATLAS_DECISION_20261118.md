# QPF006 source admission: *Penstemon digitalis* measures components, but not same-flower Q→P→F

**2026-11-18. Primary source methods audit, not an original-data numeric effect.** The aim is to prevent the frozen six-candidate natural Q–P–F atlas from treating co-occurrence of visitation, stigma pollen and seeds **across distinct experiments** as matched transfer to reproductive function.

Original paper: Dieringer & Cabrera R. (2026), *Adaptive floral traits that impact stigma pollen load and seed production in Penstemon digitalis (Plantaginaceae)*, *Nordic Journal of Botany* DOI [10.1002/njb.04977](https://doi.org/10.1002/njb.04977). Original data and publicly displayed README: [Dryad 10.5061/dryad.xpnvx0kwt](https://doi.org/10.5061/dryad.xpnvx0kwt), published 2026-05-20. The original six-source registry's QPF006 candidate remains a **single original research programme**.

## The decisive evidence is an experimental grain mismatch

The Dryad README states that each record is a sampled flower, flowers sampled across floral days are **independent**, and plants from separate experiments were **not necessarily the same plants**. The published Methods/Results go further for the pollen accumulation vs seed production comparison: **distinct sets of plants were used**, so the authors explicitly state **no direct individual relationship between stigma pollen and seeds per flower can be inferred**. These statements determine the source's ability to support a *same-flower* model independently of whether raw XLSX files can be downloaded.

| Original file/experiment | Interaction Q | Direct transfer/provenance P | Reproduction F | Valid common unit |
|---|---|---|---|---|
| `Single_visit_pollen_deposition.xlsx` | One documented bee visit to virgin flower | Grains deposited on subsequently **collected stigma** | **No matched mature fruit/seed from that flower** | Q+P assay flower only |
| `Stigma_pollen_over_day_and_year.xlsx` | No directly recorded visit history per stigmatic flower | Stigma grains by year, D2/D3 | Seed results in a **different flower sample** | P only; can compare aggregate year/day |
| `Seeds_over_day_and_year.xlsx` | No specific visitor event record | No grains from same flower | Seeds per fruit by year, D2/D3 | F only; separate experimental source |
| `Pollen_tubes_top.xlsx`, `Pollen_tubes_base.xlsx` | No same-flower visit history | Tube progression at top/base of **sampled style** | No matching mature seed follow-up | Separate destructive transfer-success assays |
| `Stigma_pollen_grains.xlsx` | No matched visitor time series | Pollen grains across anthesis phases | No matching seed outcome | P/phenology assay only |
| `Breed_system_data.xlsx` | Hand/outcross/open/bagged treatment, not actual visit rates | Neither compatible pollen nor donor origin quantified | Fruit production under treatment | Breeding treatment→fruit only |

The same `Plant_ID` spelling, `Year` or `Day` across separate files does **not** certify the same flower nor guarantee the same mother, and pollen style microscopy is destructive. Matching only year/day into artificial Q+P+F rows would be an invalid ecological observation join. This is not proof that every possible cross-experiment plant ID is disjoint; the **same source biological flower** is explicitly not jointly tracked.

## Meaningful biology, already prior art

The original authors found low grain deposition per single visit (often on the order of 4–13 grains), no successful fruit production following their single-visit deposition assay, pollen tube progression across two days of female-phase receptivity and **floral longevity as a buffer against unpredictable early-spring bee visitation**. This is a strong *independent experimental mechanism* of temporal reproductive assurance, but it **cannot** be counted as our new matched natural Q→P→F effect. The paper already established its biological interpretation.

The focus of EGWEE's independent prediction exercise remains separate: a measured direct P state must correspond to a source-defined **same flower or defensibly same ramet/maternal plant and interval** as Q and subsequent F; these biological units and any attrition/recovery must be explicit, not inferred from filenames or common floral phase.

## Status of the original six-source atlas after primary-source verification

| Candidate | Current source/unit status | Admissible matched direct P? |
|---|---|---|
| QPF001, *Oenothera fruticosa* | Original Dryad verified, **93 same-flower** Q+CP/HP+F complete cases, 29/122 unrecovered fruits, eight date-heldout negative practical prediction test | **YES**, one study/site |
| QPF002, *Argentina anserina* | Source original 13 populations; visitation in 2020–2021, pollen histology 2019–2021, fruit/seed mainly 2022 and one population 2021; original cohort/year match not proven | **NOT YET ADMITTED** at same mother/time; population summaries not interchangeable |
| QPF003, *Brassica carinata* | Original paper 35 managed/agricultural sites, visits and seed yield, but **direct pollen transfer not measured** | **NO direct P** |
| QPF004, *Mertensia ciliata* | Original Dryad verified, **62 same-ramet** 2016 Q/CP/HP/seed complete cases, 170 of 232 seed-assayed ramets lack stigma P; 2015 separate **36 potted plants** with plant-average Q/P/F | **YES at ramet/plant level**, one published programme; no same individual flower |
| QPF005, *Primula modesta* | Snowmelt network/seed programme, direct P not source-certified; one alpine hillside | **NOT YET VERIFIED direct P** |
| QPF006, *Penstemon digitalis* | Single visit + stigma P assays and independent year/day seed experiments using separate flowers/plants | **NO same-flower direct Q+P+F source** |

**Result:** source-backed strict direct transfer/provenance + reproductive outcome is currently available for **two original programmes**, QPF001 and QPF004, but their response grains and site/season missingness differ and both failed their separate registered practical predictive portability tests. The originally specified **≥3 independent, genuinely comparable complete Q+P+F programmes** gate remains **UNMET**, even after obtaining actual source data for these two. Do not manufacture a third by merging separate Penstemon experiments or treating two Mertensia years as different studies.

## What the data permit versus what remains scientifically unidentified

The original bumblebee/per-visit quality compensation in Mertensia and the Penstemon floral longevity buffer are positive ecological findings **in the original authors' papers**. The QPF001 and QPF004 separately registered held-out predictive test failures are **ours**, but they cannot adjudicate whether the established pollen mechanisms cause fruit set or ecological stability; the source observation process, season, treatment/site, and matched functional units all differ.

The next independent source search must require at minimum:

- A **unique original maternal/ramet/flower ID**, observation date and exact survey effort;
- Q contact and observed pollinator identity, P conspecific pollen and preferably **pollen tube/compatibility or source father**, F mature viable seed/recruitment, and **P-assay assignment plus fruit loss/attrition status**;
- Original source overlap in **site×time and treatment×time** cells, so held-out fold groups do not become deterministic indicators of another exposure;
- True independent ecological regions/programmes for a leave-study-out *harmonized estimand*, rather than significance-seeking changes to the two existing original negative results.

This source audit is about **measurement alignment**, not another functional-fragmentation regime result. The frozen QPF six-candidate selection, 2020 Mertensia original PR #82 outcome and posthoc source-assay selection PR #83, 2021 Oenothera original PR #77, all LA/CY studies and EGWE theory manuscript remain untouched.

## Source-only executable proof

`audit_penstemon_QPF006_public_source.py` checks the official Dryad version metadata and original XLSX filenames/size/SHA and first-row worksheet structure when the public file streams are reachable. It neither recombines biological rows across experiments nor estimates an outcome. If the original file route returns 401/403/429, the public experiment design is still disqualifying for same-flower Q–P–F as published; the access failure is not a biological negative result.
