# Reconciled primary methods and prior-art ceiling for Lupinus field phenology and reproduction (2026-11-24)

**Status:** source-triangulated original-experiment design and interpretation; no new model, effect, p-value, source normalization, or causal treatment mapping. This note supersedes the impression that the 2026 spreadsheet's anonymous line letters can be inferred merely from their counts.

## Source 1 — authors' original 2023 PhD thesis, Chapter 4

Sandra Sacristán-Bajo (2023), *Evaluation of assisted evolution as a conservation strategy for climate change adaptation*, original university PDF:
https://burjcdigital.urjc.es/server/api/core/bitstreams/e43b6427-a0c1-4d55-ae97-83945eecee8d/content ,
printed chapter pages 194–199 (PDF indexed lines ~9770–9900).

The original thesis describes:
- Four established biological experimental lines from F3 seed collected in 2020: **CFL** control selfing, **EFL** early-flowering selected/selfed, **OUTS2** selected early-flowering line from within-line outcrossing followed by F2/F3 selfing, and **SPL2** F3 descendants of northern mothers crossed with southern donor pollen at F1, then F2/F3 selfed.
- One in-situ common-garden grassland at **Zarapicos, Salamanca**, seeded November 2020, with **four randomized blocks**, 234 sowing points per block and 3 related seeds per sowing point. **2,808 sown seeds**, 36 seeds per source maternal genotype, 10 maternal genotype units per treatment-population *except 8 in FRO SPL2*. Thus 78 original-genotype units in the earlier reported study.
- First-flower onset recorded three times weekly and partly inferred for adjacent unobserved days; original intended phenology metric = **days from sowing to first flowering**. End-of-season plants harvested, seed number assessed as fitness proxy; plant biomass and shoot growth also recorded. These are original thesis descriptions, *not a complete validated 2026 version-specific codebook*.
- Original analyses of selection vs gene flow were **separate comparisons against the same CFL control**, accounting for `genotype` (maternal origin) as random effect, population as fixed, and initial germinated seed weight as covariate.

## Source 2 — new 2026 original deposited workbook (actually verified)

Sacristán-Bajo et al. 2026 *Annals of Botany* DOI 10.1093/aob/mcag061; official Figshare original DOI 10.6084/m9.figshare.29606180.v1, SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`. Source-only GitHub Actions [run 45355170533](https://github.com/zuizui0223/egwee/actions/runs/45355170533) verified **the exact ten first-row column names**:

`id`, `population`, `line`, `genotype`, `shoot growth`, `flowering_onset`, `number of fruits`, `number of seeds`, `biomass`, `germinated seed weight`.

There is **no explicit block, sowing point, donor genotype, paternity, pollinator service, S-locus or seedling recruitment column**. Total 3,024 experimental/source rows and 84 `population|genotype` family labels (both not independent population replicates). Original population coding FRO/PIC; anonymous source line letters C/J/L/R/T/X, meaning **unverified**.
- Source arithmetic: 2026 line codes `C+J+L+T=2,808` source rows (78 x 36). Extra source codes `R+X=216` rows (6 x 36). This numerical match does **not** establish biological identity or that R and X are true additions rather than corrections/revisions to treatments. **In FRO, code J has 288 rows (8 x 36), mirroring the thesis's eight FRO SPL2 maternal genotypes, but that is NOT a verified direct J→SPL2 mapping.**
- Original Excel 2026 `number of seeds` has 153 nonnegative fractional values and 990 missing values; the 2023 thesis says seeds were counted from plants harvested in 2021, and the 2025 independent greenhouse paper used estimated number of seeds from fruit counts × seeds/fruit. Neither alone validates how all 2026 uploaded fractional values were derived. A separate source-only fruit/seed numeric-consistency audit has been written but is not a new outcome model.
- 2,008 of 3,024 source rows (66.4%) have numeric flowering onset and seed-index concurrently; FRO 69.6%, PIC 62.9%; missingness potentially selective. The LUPF2 grouped CV held out maternal-genotype labels, **not physical randomized blocks**; in-situ transfer is therefore not a new-site validation.
- Header `germinated seed weight` is an originally measured potential baseline-covariate in thesis analysis, but it was **not included in predeclared LUPF2** and must not be added after seeing its predictive gain. May inform a **separate prospective independent study** only.

## Source 3 — already published phenology–seed biological association

Sacristán-Bajo et al. 2023 (online 2022) *Evolutionary Applications* DOI [10.1111/eva.13510](https://doi.org/10.1111/eva.13510) and 2023 thesis Chapter 1 report: in a controlled common garden, **earlier flowering in the northern control line was already correlated with greater biomass/seed number/seed weight** (original source thesis pp.55 and lines ~1352–1356). Hence **the qualitative earlier-flowering vs seed-production direction was previously published** in this research programme. It must not be presented as a first-ever finding from our LUPF2. What LUPF2 newly adds is a **source-specific exploratory, grouped-CV prediction of the 2026 field recorded seed-index on observed complete cases**, not a new causal mechanism or cross-study replication.
- The 2026 *Annals of Botany* abstract's main published results are assisted-gene-flow F3 flowering advancement and lower shoot growth vs controls; no claim of demonstrated viable offspring recruitment or partner-mediated recovery is established from the accessible abstract.
- The 2025 *Evolutionary Applications* article DOI 10.1111/eva.70087 reports 36 candidate genome-wide outlier SNPs associated with flowering/seed mass/growth; **do not infer those exact variants' genotype in the 2026 F3 individuals**, which are not joined by source-native family identifiers.

## Scientific / statistical inference boundaries

1. **Observation**: LUPF2's lower held-out seed-index error with observed flowering-onset + negative onsets across 5 folds are descriptive posthoc findings, conditional on 2,008 complete cases and **one field common garden**.
2. **Mechanism**: earlier flowering may extend available growing-season time, shift abiotic stress or reflect prior plant health. The species primarily self-pollinates before flowers open; no field S-locus/compatible pollen/outcrossing observations are present, so its result does not demonstrate eco-genetic *interaction-gated* mating.
3. **Intervention**: unknown line-code mapping, unmeasured physical plot/block in the XLSX, substantial selection into observed seed outcomes and no independent original genetic genotype calls prevent a causal assisted gene-flow → seed production claim from LUPF2.
4. **Next defensible source gate**: obtain original 2026 article's supplement/author source codebook establishing (a) C/J/L/R/T/X ↔ CFL/EFL/OUTS2/SPL2 treatment mapping; (b) whether extra 216 rows are valid in the final published cohort; (c) fruit/seed numerical computation; and (d) physical block or sowing-point crosswalk. Until then keep `T→W_EXPLORATORY_ONLY`, `G×I×F_NOT_IDENTIFIABLE`. No guessing or outcome-tuned retests.
