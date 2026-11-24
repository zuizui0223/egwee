# LUPF2-DIR — executed descriptive coefficient-direction audit (2026-11-24)

**Result: 5/5 identical frozen 2026 field models show a negative flowering-onset coefficient, i.e. EARLIER recorded flowering is associated with HIGHER source-stored reproductive-index values among COMPLETE CASES.** This is a **posthoc descriptive audit** of an exploratory in-study predictive result, **not** a new confirmatory test, intervention effect, genotype-to-phenotype causal finding, or natural EGWE G×I×F validation.

## Executed source and frozen model audit

- Original public primary data: Sacristán-Bajo et al. (2026), *Annals of Botany*, DOI [10.1093/aob/mcag061](https://doi.org/10.1093/aob/mcag061); Figshare DOI [10.6084/m9.figshare.29606180.v1](https://doi.org/10.6084/m9.figshare.29606180.v1), `Lupinus_angustifolius_data_field.xlsx`, SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`.
- Original LUPF1 pre-outcome strict-integer rule frozen `28938fe193d01d7eca5bd2fe776f37ecb1f58e27` remains `SOURCE_ENDPOINT_INVALID_STOP` (noninteger source entries); original exploratory LUPF2 design frozen `053eca26bc1b527e828cb82cbac9318d20be7621` retains its original run [45328763380](https://github.com/zuizui0223/egwee/actions/runs/45328763380).
- Posthoc direction extraction **protocol committed before reading the signed fold coefficients** at `d9e2f7aa9c8179158d49b55637aa18e4ca178f4a`.
- [GitHub Actions run 45341693463](https://github.com/zuizui0223/egwee/actions/runs/45341693463), job `lupf2-posthoc-frozen-direction` completed successfully. [Original aggregate evidence artifact 14896985026](https://github.com/zuizui0223/egwee/actions/runs/45341693463/artifacts/14896985026), ZIP SHA256 `7066e3db06010ad0ff6e2e1efd07112d9d81772a02ea98fefb05ba09ebfcd2d5`. Source-only controls and 100% of five fold-metric reproducibility checks passed. No original individual rows, coded genotypes or source values redistributed.

## Coefficients from exactly reproduced original models

Outcome is `log1p(source-stored number of seeds numerical proxy)` within the 2026 field complete cases, with intercept, source population, **anonymous source line-code** categories and one training-standardized continuous `flowering_onset`; regularization lambda=1. Original per-fold M0 and M1 MSEs and overall MSE reproduced within 1e−8 before extracting any coefficient sign. N=2,008 complete cases; 84 original genotype **label groups**, not sequenced SNPs; grouped fivefold.

| Fold | Held-out records | M1 onset coefficient per raw source time unit | M1 standardized coefficient |
|---|---:|---:|---:|
| 0 | 503 | −0.06440531 | −0.50812353 |
| 1 | 244 | −0.06868967 | −0.54710571 |
| 2 | 244 | −0.06592176 | −0.52308269 |
| 3 | 482 | −0.06838989 | −0.54377814 |
| 4 | 535 | −0.06313331 | −0.50806388 |

All five onset slopes have the **same negative sign**, with minimum/maximum −0.06869/−0.06313 **per original source time unit**. This audit did **not separately verify** that raw `flowering_onset` is encoded in days vs another normalization; the 2025 and 2023 related original methods use day differences, but do not transfer units without checking this 2026 source field. Negative slope means *later* source-coded onset correlates with lower expected `log1p(seed-index)` **within observed plants**, after anonymous line/population adjustment; earlier onset correlates with higher index.

Reproduced original pooled external-prediction MSEs: baseline M0 **1.1348068697547518**, M1 + onset **0.8706748619478497**; identical to original LUPF2, **not a new validation dataset**. Gain **0.2641320078**, descriptive 23.28% MSE reduction, 5/5 fold gains. Descriptive fixed-prediction genotype cluster bootstrap gain interval [0.19137,0.33740] remains the original; **no new p-values or interval** generated for slope.

## Biology, competing pathways and conservation claim boundary

The sign is compatible with the hypothesis that earlier development offers more reproductive time/seasonal resource opportunity, but does **not establish** a causal flowering-time advantage. Unmeasured plant vigor, germination timing, local abiotic conditions, selfing physiology, seed-index estimation, and selection into phenotype observation may generate the association.

Source missingness is substantial: only 2,008/3,024 (66.4%) have both flowering and seed index; FRO 1,102/1,584 (69.6%) vs PIC 906/1,440 (62.9%), R/X anonymous source lines only in FRO. Thus no claim about fecundity of all sown individuals, about viable seedling recruitment, or about observation-missing-at-random.

Original author's 2025 assisted gene-flow study (DOI [10.1111/eva.70087](https://doi.org/10.1111/eva.70087)) already reports gene-flow-associated flowering advance and that its seed metric was estimated via fruit number × seeds per fruit. Precise derivation of the 2026 seed-index column and one-letter intervention line codebook remain unverified. 2025 vs 2026 individual IDs do not join directly. No 2026 cohort SNP states, independent population validation, compatible pollen delivery, field pollinator activity or next-generation recruitment are available in this combined source.

**Do not translate the posthoc negative slope into an assisted gene-flow fertility rescue effect or conservation intervention recommendation.** Distinct next biological tests: independent genotype/ancestry-verified mating and effective pollen in SI taxa; evaluate future seed viability and offspring recruitment, with prospective observation design and population/year holdout. Model's G×I×F relational mechanism and universal warning thresholds remain **NOT IDENTIFIABLE**.
