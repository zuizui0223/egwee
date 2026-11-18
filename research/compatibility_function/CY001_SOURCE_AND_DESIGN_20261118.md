# CY001 — original-source independent-programme mating/seed transport, plot-held-out

**Scientific protocol frozen before opening new original numeric outcomes at commit `a118ab77e71a097b46d264738e34c0428384a304`.** The original study is Labonté et al. (2024), *American Journal of Botany*, [doi:10.1002/ajb2.16440](https://doi.org/10.1002/ajb2.16440), open paper [PMC11659934](https://pmc.ncbi.nlm.nih.gov/articles/PMC11659934/). Original dataset: [Dryad doi:10.5061/dryad.9p8cz8ws1](https://doi.org/10.5061/dryad.9p8cz8ws1), original files `Data_Dryad.xlsx` and `README.md` (published 2024-09-20).

## What is new relative to LA005

This is a genuinely different **plant species and original data-generating programme**: *Cyanus segetum* (syn. *Centaurea cyanus*), a self-incompatible annual, sampled in Burgundy in 2019. The source states that 33 mothers have same-flowering-period measurements of focal visitation (E), potential donor density (F), floral context (G/H), offspring expected heterozygosity (C) and correlated paternity (D), and original mature seed number (AB). The 33 mothers came from **12 plots on one farm**. The original paper already studied functional pollinator effects on offspring mating; do **not** claim to discover that effect or compare its raw rpm to LA005's different allele indicator.

**Critical selection:** those 33 genotyped mothers were randomly sampled only from **64 plants that produced at least 20 viable germinable seeds**, out of 144 initially transplanted. Thus any seed-number regression on these 33 is **outcome-selected**; cannot estimate pollination limitation among all field mothers, and seed-number contrasts must remain *conditional descriptive outcomes*.

## Predeclared source and analysis gate

Use original Dryad official DOI/file/version metadata (not guessed mirror or fabricated data). Read original worksheet header and exactly 33 mother-level rows with unique mother IDs, exactly 12 plot codes and 15–17 genotyped offspring per mother. A missing or access-restricted original workbook produces **SOURCE_ACCESS_STOP**, not null ecology.

- Primary *mating-specific* endpoint: original multilocus correlated paternity `rpm`, 0–1; not an actual father ID or genetically compatible pollen count.
- Baseline M0: mother allele number, log1p local conspecific pollen-donor density, log1p floral richness/density, strip type, standardized on the training plots only.
- M1: M0 plus `log1p(Relative_MPA_n_visits_per_15_minutes)`, the original paper's mother-level attractiveness/visitation metric, not pollinator-visit events measured on every single flower.
- Fit ridge λ=1.0 without a penalized intercept, clip predictions for rpm to [0,1], validate **12 leave-entire-plot-out folds** (rather than pretending 33 mothers from one farm are 33 independent landscapes).
- Predeclared practical gain: pooled mother-level M0−M1 MSE positive, at least 5% of M0's MSE, and ≥8 of 12 plots positive. A smaller effect is NOT called portable merely for positive sign.
- Secondary: same CV and model architecture on `log1p(N_seeds_n)` within the **outcome-selected 33**, reported descriptively and **never used to rescue** the primary.

This is an independent-source test *of an endpoint-specific prediction problem*, not a cross-study pooled estimate because the response differs fundamentally from LA005. It is still one farm programme, not a basis for an island/urban fragmentation law.

## Scientific provenance and stop rules

The original paper's own predictor-selection/AIC results and ecological interpretations are already known. A new analysis can test *out-of-plot transport* and expose limitations, but no first-discovery novelty is assigned to pollinator guilds and gene flow. No post hoc changes to chosen columns, holdouts, modeling penalty, endpoint, field/offspring thresholds, or seed-selection exclusion. Original LA001, LA002, and LA005 outcomes remain frozen.

The new source-gate workflow reports **only original metadata, file-header structure and SHA** if publicly accessible. Raw third-party original XLSX, exact mother IDs, genomic data, row-wise counts and individual seed values are not committed. A later source file provided by the user can run the exact pre-locked analysis locally, without relying on an unverified guessed Dryad API download.
