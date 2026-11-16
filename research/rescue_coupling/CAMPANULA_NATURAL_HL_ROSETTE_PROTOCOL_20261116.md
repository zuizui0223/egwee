# Campanula glomerata natural populations — preregistered population-grain HL–juvenile-growth pilot
## Protocol v0.1, written before opening the 2022 source's HL/rosette numeric values — 2026-11-16

**Study purpose:** establish whether a neutral-marker-derived genetic state (seed-progeny homozygosity by loci, `HL`) is associated with juvenile plant growth (rosette diameter) **across independent natural populations**, while preserving the family/seedling nonindependence problem. This is an **exploratory within-one-programme G→W study**, not a causal genetic rescue experiment, not a direct plant–pollinator functional rescue endpoint, and not an estimate of the finite EGC/EGWE model's natural predictive AUC.

### Source and pre-outcome pin

- Original research: Van Rossum et al. (2022), *Frontiers in Conservation Science* 3:829332, https://doi.org/10.3389/fcosc.2022.829332.
- Exact public source: Zenodo https://doi.org/10.5281/zenodo.5676272, original `Campanula_fitness.xlsx`, SHA-256 `a1c50c74d0bd2c9a00b7a0d42322c31c30c53789e3b5cadbe67b08cee878f6a7`.
- Raw first worksheet row denominator: **507** excluding the header, with **502** rows containing a readable whitelisted identifier field (`POP`, `Ind`). Earlier source-only audit: `research/rescue_coupling/CAMPANULA_2022_2024_ID_LINKAGE_GATE_20261116.md` (PR #58).
- Same-sheet headers (not numerical values) include `POP`, `Ind`, `Rosette diameter (cm)`, `HL`. The separate 680-row genomic workbook is **not joined** for this pilot; exact Pop×Ind matching covers only 30 across cohorts, of which 22 are progeny candidates.

### Exposure, outcome and independent unit

- Genetic proxy `G`: source `HL`, the measured homozygosity-by-loci index. It is not genome-wide ROH, inbreeding depression itself, a causal genotype, measured pollen compatibility or SNP `p` in EGC.
- Growth endpoint `W_juvenile`: same-row `Rosette diameter (cm)`, nonnegative continuous growth proxy. It is **not** seed set, pollinator performance, or direct ecological-function recovery.
- Individuals within a maternal family may share parents and environment; the source workbook contains no separately verified mother/family code. **No individual-level p-value is allowed.** The primary unit is source `POP`, not 502 apparently independent seedlings.
- A single source study contributes **one** potential independent *programme*, regardless of the number of populations or offspring.
- Only complete rows with `POP`, `Ind`, `HL`, and rosette numeric values enter a population mean. Require exact unique (`POP`, `Ind`) within the admitted records; if duplicate, **STOP**, no result-based averaging of phenotypes.
- Numeric `HL` must lie in [0,1], rosette diameter must be finite and nonnegative; unknown textual tokens (`NA`, blank, `-`, `null`) are missing, never zero.
- A successful primary analysis requires at least 5 eligible source populations, each with at least 5 complete seedlings. If fewer, **coverage STOP**. Exclude sub-threshold populations under this predeclared rule; report their N (not outcome values) and source denominator.

### Primary estimand and exact uncertainty

For each eligible population, calculate the **mean `HL`** and the **mean juvenile rosette diameter**, using one contribution per eligible plant. Primary cross-population statistic:

`rho_population = Spearman( mean_HL_pop, mean_rosette_pop )`

Rank each population mean (average rank under ties), compute Pearson correlation of those ranks. One population contributes one point. For **K≤8** eligible populations, enumerate **every distinct permutation of the population-level endpoint ranks** and calculate the exact two-sided null p-value as fraction with `|rho_perm| ≥ |rho_observed|` (no pseudo-replication from individual seedlings). For K>8, use 10,000 Monte Carlo permutations with frozen RNG seed 20261116 and Monte Carlo p = (b+1)/(10000+1). The source claims seven populations; do not force seven when raw source differs.

Report:
- complete/missing HL and rosette rows, source ID rows, eligible population count, individual denominator per population (counts only, anonymized if possible)
- population-level `rho` and exact or Monte Carlo permutation p
- **leave-one-population-out** `rho` distribution and range
- a descriptive, non-inferential within-population centred-rank `r` across individuals, explicitly without p because shared maternal families cannot be disambiguated

No partialling of site/source effects after outcomes are inspected; no changing effect scale, threshold, sample unit, endpoint or sign orientation. Report both positive and negative effects. Spearman `rho` does not identify heterozygosity gain from translocation or a causal rescue effect.

### Confirmation and falsifiers

A result can be recorded as a bounded population-level marker/juvenile fitness *association* only if the source file hash matches, all independent-grain gates pass, the relationship retains a consistent sign under leave-one-population-out and there are enough independent populations. If `rho` is unstable, label it **influence-sensitive**, not independently reproduced and not evidence against a biological role for genetic diversity.

The original 2022 study analyzed genetic and offspring fitness consequences; reproducing its association is a **harmonization pilot** for a future preregistered cross-study comparison, not a new scientific finding. It cannot be pooled numerically with the Arnica 2020 **maternal HL → viable seed set** estimate (within-site/source centred-rank `r=-0.0185`, 135 mothers, six strata, permutation p=0.8341) as if seed set and juvenile diameter were one standardized response.

**Critical STOP:** Do not claim broader genetic rescue or ecological function restoration from either study. Those require controlled interventions or synchronized genotypes with direct reproduction/interaction function and appropriate independent landscapes or study programmes.
