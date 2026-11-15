# Arnica montana 2020 — locked within-programme genome–maternal-function pilot
## v0.1, committed before any maternal HL or reproductive-outcome value inspection

**Scope:** one observational maternal-plant dataset, not genetic-rescue causal evidence, not a multi-study meta-analysis, and not natural validation of the EGC–EGWE simulator. Primary source: Van Rossum et al. (2020), `Molecular Ecology`, DOI [10.1111/mec.15550](https://doi.org/10.1111/mec.15550). Public Zenodo dataset [10.5281/zenodo.3881439](https://doi.org/10.5281/zenodo.3881439), immutable source workbook `VanRossumetal_Arnica_fitness.xlsx` SHA-256 `052fef893ed6bb3dd00fec4882c77b6f4f48ed85767fa2643a4809505d4e8e62`.

## Why this pilot is admissible for a *conditional association* only

The published spreadsheet's first worksheet contains **145 maternal records** (not 145 independent restoration populations). Same-row headers include `Code` (maternal plant), `Site`, `source`, `HL mat plant` (maternal homozygosity by loci), ` Viable seed set`, `Seed germination`, and `Cumulative fitness`. The second sheet has F1 juvenile rosette measures and maternal HL, the third has F1 individual HL, while a fourth sheet covers established plants. This programme used three translocated sites and two source populations. Every seed, F1 recruit or locus is not an independent restoration treatment replicate.

**No allele values, HL numeric values, seed viability/germination/fitness numeric values, signed effects or fitted associations have been read while this plan is authored.**

### Locked estimand and analysis rules

- **Population of inference:** mother plants present in Zenodo `xl/worksheets/sheet1.xml` with complete maternal `Site`, `source`, `Code`, `HL mat plant` and ` Viable seed set`. Do not use flower/seed offspring or loci as extra independent maternal observations.
- **No-effect leakage key gate:** `(Site, source, Code)` must be unique among non-empty maternal records. If not, STOP; do not choose or average records after looking at fitness.
- **Genomic proxy G:** maternal `HL mat plant`, higher value meaning higher homozygosity across markers; not direct functional allele availability, effective genetic load or measured mating compatibility.
- **Primary F:** ` Viable seed set` as recorded by the source, *within the maternal reproductive-life-cycle domain*. Units may be proportion, percentage, count or cumulative index; rank-based inference will not assume one without original methods.
- **Primary statistic:** a within-`Site × source` pooled rank correlation: rank both G and F separately within each available source-site stratum (average ranks for ties); subtract each stratum's rank means, then compute Pearson correlation across centred ranks. Strata with <5 complete mothers are excluded by this frozen rule; report exactly which strata and how many mothers are excluded. Require at least two qualifying strata and ≥30 linked maternal records. No informative sign reversal or P-hacking.
- **Null and uncertainty:** two-sided Monte Carlo permutation of F ranks **within the same site-source strata**, 10,000 independently seeded permutations (seed 20261115); report permutation p, no claim of causal rescue. As a robustness diagnostic report each stratum's plain Spearman correlation and leave-one-stratum-out pooled association. Do not convert strata to independent studies.
- **Secondary descriptive endpoint:** `Seed germination`, same code and procedure, marked secondary. Do not claim reproductive recovery from a heterozygosity association in one cross-section.
- **Missingness:** keep all 145 source maternal records in the denominator; report numeric invalid/missing counts by primary exposure and outcome. Do not impute, treat absent values as zeros, or relabel existing zeros as missing after inspection. If the source contains special missing markers (NA, -, "none", "nan") treat these as missing and report them. A value outside [0,1] for HL is an error STOP; outcome must be finite and nonnegative.
- **Interpretation boundary:** this pilot can show marker homozygosity–seed reproduction correspondence conditional on site/source, but cannot establish translocation-caused genetic rescue or interaction-dependent pollen limitation. Original authors already analyzed maternal/site/source effects; a similar effect here is validation, not new independent discovery.
- **No cross-programme pooling:** Arnica (2020) and Dianthus (2021) are distinct plant systems but share managers, geography and management context, and raw measures differ. This pilot alone cannot justify a meta estimate or portability claim.

### Prior analysis frame and severe limits

The 2020 paper reports managed translocations with high density and mixed sources, genetic mixing and recruitment, but does not randomize *genomic heterozygosity*. Source/recipient environment, maternal condition and seed source can confound `HL → viable seed` associations. Site-source conditioning helps but cannot remove genotype–environment confounding, reverse selection or nonrandom seed sampling.

**Decision after prototype:** If the source passes eligibility, archive the exact derived `r` and confidence/uncertainty only as an exploratory *within-programme component*. Then preregister the same endpoint/variance family for independently recovered floral/crossing programmes before any pooled rescue analysis. If the data fail uniqueness or sample-size gates, report the exact STOP, not a null biological result.
