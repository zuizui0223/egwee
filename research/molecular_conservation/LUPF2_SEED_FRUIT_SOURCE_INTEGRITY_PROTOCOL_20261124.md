# LUPF2-SFI — original source fruit/seed measurement integrity audit (2026-11-24)

**Type: source data-quality investigation, POSTHOC and outcome-direction-blind.** This is a follow-up to the already completed exploratory LUPF2 positive result and the first pre-registered LUPF1 strict-integer stop. It is NOT an independent ecological test, a new model, or confirmatory analysis. No new signed phenotype–fitness association may be fit.

## Source and verified design
- Original publicly available article: Figshare `10.6084/m9.figshare.29606180.v1` (article 29606180), original `Lupinus_angustifolius_data_field.xlsx`, SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`.
- The original sheet2 first-row header audit (GitHub Actions run 45355170533) verifies exactly `id`, `population`, `line`, `genotype`, `shoot growth`, `flowering_onset`, `number of fruits`, `number of seeds`, `biomass`, `germinated seed weight`. No explicit block or plot identifier column.
- Author's 2023 thesis Chapter 4 (source https://burjcdigital.urjc.es/server/api/core/bitstreams/e43b6427-a0c1-4d55-ae97-83945eecee8d/content, printed pp.194–199) describes 2,808 sown seeds, four experiment blocks, source treatments CFL/EFL/OUTS2/SPL2, 36 sown per maternal genotype, eight rather than ten FRO SPL2 maternal genotypes. This *historical source design* does not by itself identify the 2026 spreadsheet's raw C/J/L/R/T/X codes or the six extra genotype labels. It describes counting seeds per harvested individual in its 2021 field campaign. The precise source derivation of the deposited 2026 numeric seed-index remains unverified.
- The 2025 related assisted gene flow article used number of fruits × mean seeds per fruit for a seed-production estimate (DOI 10.1111/eva.70087). **Do not assume identical 2026 measurement procedure** from a previous paper.

## Fixed checks prior to opening the fruit field
1. No method changes, regression re-fitting, genetic/treatment remapping, hypothesis sign inspection, or new p-values. Freeze source SHA and return STOP on mismatched file.
2. From original `sheet2.xml` only, read source fields `population`, `line`, `genotype`, `id`, `number of fruits`, `number of seeds`, `flowering_onset`. The other raw source columns (shoot growth, biomass, germinated seed weight) shall **not** be read as values, and no row-level values or IDs shall be exported.
3. For `number of fruits`, classify every value as missing/NA, finite nonnegative integer, finite nonnegative noninteger, finite negative, nonnumeric/nonfinite. Count explicit zeros separately. Also verify original `number of seeds` category counts against prior audit (990 missing/NA, 1,881 finite nonnegative integers, 153 finite nonnegative nonintegers, 0 negative).
4. Cross-tab **quality categories only**: fractional seed-index paired with positive/zero/missing fruit count; numeric seed index with zero fruits; missing seed-index with positive fruits; fruit missing with seed numeric; and 2x2 availability of seed and onset. No seed/fruit ratio or individual values are published.
5. Report the aggregate total and by source `population` (FRO/PIC) only. Preserve 3,024 denominator, stable original source-genotype label count 84; do not infer line code meanings.
6. Do NOT impute missing seed values from fruits or source metadata, convert missing to zero, round 153 fractional seed values, or use observed fruit counts as an additional predictor. A positive seed index with zero fruit is a **semantic discordance flag**, not proof an observation is wrong.
7. The goal is to classify whether the 2026 `number of seeds` index is compatible with the fruit count field and to identify **what remains unverified**: sampled per-fruit seed weights, counting/estimation procedure, sowing cohort, plant and block unit. Successful agreement **cannot prove** the exact derivation.

## Decision
The only allowed completed status is `POSTHOC_FRUIT_SEED_SOURCE_INTEGRITY_COUNTS_ONLY` or a source/field/semantic STOP. The existing LUPF1 stopped primary, LUPF2 2,008 complete-case 23.28% exploratory gain, and original LUPF2 5-fold negative flowering onset coefficients remain fixed and are never recalculated here.

An interpretation-grade linkage of treatments to performance still needs verified author codebook for C/J/L/R/T/X and cohort/plot/block keys; independently demonstrated ecological-function recovery still requires viable seed recruitment and effective partner/pollen data. 
