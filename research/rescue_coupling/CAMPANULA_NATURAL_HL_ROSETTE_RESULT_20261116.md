# Campanula glomerata — population-grain HL vs juvenile rosette growth result
## 2026-11-16 — frozen-outcome pilot, one natural programme (NOT genetic rescue)

**Status:** original-source observational **G→W_juvenile** pilot completed with exact randomization at seven-population grain. **This does not estimate causal genetic rescue, pollination or seed-function recovery, nor a meta-analytic mean across species.** Outcome interpretation and hypothesis were locked before exposure in source commit `52ff2c5b2212b6b8d91e802869fb963ebf4973ab`.

## Source and computational provenance

- Van Rossum et al. (2022), *Frontiers in Conservation Science* 3:829332, DOI [10.3389/fcosc.2022.829332](https://doi.org/10.3389/fcosc.2022.829332).
- Original Zenodo `Campanula_fitness.xlsx`: [10.5281/zenodo.5676272](https://doi.org/10.5281/zenodo.5676272), SHA-256 `a1c50c74d0bd2c9a00b7a0d42322c31c30c53789e3b5cadbe67b08cee878f6a7`.
- Locked study design: `research/rescue_coupling/CAMPANULA_NATURAL_HL_ROSETTE_PROTOCOL_20261116.md`, protocol commit `52ff2c5b2212b6b8d91e802869fb963ebf4973ab`.
- Reproducer: `research/rescue_coupling/analyse_campanula_natural_HL_rosette.py`.
- First successful fixed-estimand CI: [GitHub Actions 43879710797](https://github.com/zuizui0223/egwee/actions/runs/43879710797), metadata-only artifact `14229984945` (JSON `campanula_2022_natural_HL_rosette_population_pilot.json`). Original XLSX/individual measures are **not redistributed**.

## Denominator and eligibility check

- Original source: **507** non-header worksheet rows; **5** rows missing `POP` and/or `Ind`, excluded before outcome analysis.
- **502** rows have unique `POP×Ind` identifiers and complete usable HL and rosette diameter. **No** additional missing HL or growth values among these 502.
- **7** natural source populations: anonymous per-population seedling counts `31, 57, 67, 75, 85, 86, 101`. Each has at least five complete records; zero populations dropped by the frozen minimum.
- Individual seedlings may share parents or other local history, so **n=502 is not an independent permutation denominator**; the permutation experiment has **n=7 population means**. Those populations arise within one source research programme, not seven independent meta studies.

## Original prespecified primary result

| Parameter | Estimate |
|---|---:|
| Predictor | Mean offspring homozygosity-by-loci (HL) per natural population |
| Outcome | Mean seed-progeny rosette diameter, cm, per natural population |
| Primary Spearman association across **seven population means** | **ρ = −0.1428571429** |
| Exact two-sided population-label permutation test | **p = 0.7825396825** |
| Unique population-label permutations enumerated | **5,040 / 5,040** |
| Permutations with absolute association at least observed | **3,944** |
| Leave-one-natural-population-out Spearman range | **−0.37142857 to +0.37142857** |
| Within-population centred-rank r, *descriptive only* | **−0.10549584** (**no individual-based p-value permitted**) |

Leave-one-out primary coefficients in anonymized deterministic order: `−0.1429, −0.2571, −0.3714, −0.2571, −0.2571, +0.3714, −0.0857`. Direction changes when one population is omitted; association is therefore **influence-sensitive**, not a stable negative relation.

## Scientific interpretation

The natural source does **not** support a clear monotone relationship between population mean maternal/progeny neutral-marker homozygosity and mean juvenile rosette growth at the tested seven-population level. The original authors evaluated population genetic status, inbreeding and offspring fitness within this programme; the present calculation is a transparent **harmonization pilot**, not a new independent discovery or a result refuting genetic mechanisms.

Potential limitations: seven population-level samples provide weak precision; historical source structure and habitat differences can confound both HL and growth; within-population sibship is unresolved; and rosette diameter is **juvenile general fitness**, **not compatible pollen transfer or viable seed production**. The unpooled individual-centred rank r cannot be assigned an ordinary p-value because mother/family independence is unverified.

### Relation to prior Arnica pilot (nonpoolable endpoint families)

The separate 2020 `Arnica montana` predeclared source audit used **135 mothers across six site×source strata** and tested **maternal HL versus viable seed set**, yielding conditional rank r **−0.0185128592** and stratified permutation p **0.8341165883**. The present Campanula test is instead **seven population means of offspring HL versus juvenile rosette diameter**. The outcome, covariate structure, sampling units and uncertainty procedures differ. **Do not average the two r values or interpret their joint lack of significance as evidence of genetic or functional rescue failure.**

## Decision and next evidence gate

- Preserve as **one original study/programme, one observational G–W_juvenile analysis** in the candidate evidence map; primary direct ecological-function rescue endpoint `F_direct` remains **unobserved** in this Campanula population-level test.
- Do not pool with Arnica as a shared estimand or compare the two p-values as a formal meta-analysis.
- The 2023/2024 *Campanula glomerata* transplant dataset separately offers **144 F0 maternal family keys covering 990 F1 offspring rows**, potentially supporting a mechanistic cohort analysis; verified F0 genotype→maternal fitness ID keys are too sparse, so **gene-flow/genotype-to-function identification remains gated**.
- Next prioritize independent controlled pollen-mate compatibility/seed production programmes with directly measured genomic or pedigree state, plus source-exact mother/offspring and intervention controls. Only then reconsider a true pooled genetic-rescue × ecological-function moderator analysis.

**No new genomic diversity change, gene flow–intervention effect, or ecosystem service has been inferred by this pilot.**
