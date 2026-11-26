# LUPF1 — frozen source-genotype held-out phenology→seed proxy test (2026-11-24)

**TYPE:** development-only within-programme source-derived predictive audit, not an EGWE early-warning validation, an eco-genetic interaction-function analysis, a randomized intervention effect, or an independent species replication.

**Freeze condition:** this protocol is committed to the PR branch **before any `number_of_seeds` numeric outcome is accessed by a new analysis script or CI workflow**. Published directional phenology effects are known from Sacristán-Bajo et al. 2026; this is a new held-out prediction check, not a claim to independently discover those effects. We will preserve null or negative results without modifying folds, covariates, penalties or endpoints.

## Source and study design

Official Figshare 2026 `10.6084/m9.figshare.29606180.v1`, file `Lupinus_angustifolius_data_field.xlsx` (source `sheet2.xml`); official DOI 10.1093/aob/mcag061. Source registered from exact Figshare article 29606180, original file SHA256 will be verified at execution, raw data downloaded in GitHub runner only and not published.

2026 source design audit found 3,024 rows, 84 distinct genotype **labels**, two original northern populations (FRO=1,584 and PIC=1,440 rows), and six unassigned `line` letter codes C/J/L/R/T/X. **Do not infer** that any code is control, artificial selection or gene flow. Source 2025 `10.6084/m9.figshare.28304024` has 1,776 earlier-generation rows, with ZERO exact cross-year population×line/ID-label matches. Do not join across years without a verified family pedigree.

Authors' 2023 doctoral thesis Chapter 4 describes a field protocol with 2,808 sown seeds, four biological treatments and individual harvested seed counts; **this differs by 216 from the 3,024 source 2026 records**. Treat 2026 original data as its own archive, without projecting thesis cohort counts or presumed treatment definitions. Outcome observation completeness is to be inspected as a declared stage, not filled in.

## Scientific question

Among **individuals in the 2026 experimental source with both a recorded flowering-onset value and a source-defined numeric seed-production value**, does flowering timing add out-of-genotype-family predictive information for same-season seed output above population and anonymously coded line? This is **observational trait–fitness association**, NOT `G×I×F` and NOT causal or long-run genetic rescue.

### Fixed grain and exclusions

- Source records: `id` field is a planted/observation-record label, not necessarily a unique surviving plant; `genotype` is an original experimental genotype/family *label*, not a sequenced SNP. Raw source format is one record per original sheet row. Do not count planted rows as seed outcomes.
- Grouping: identical `population` plus `genotype` **labels** as the indivisible cross-validation/uncertainty unit. A genotype-label group may cover many seeds/plants. No sample ID/allele inference.
- A complete case requires nonempty `population`, `line`, `genotype`, numeric finite nonnegative near-integer `number_of_seeds`, and numeric finite nonnegative `flowering_onset`; `id` not required for outcome model; missing values are excluded with counts, never converted to zero. Source negative or non-integer counts trigger `SOURCE_ENDPOINT_INVALID_STOP` (not quietly fixed). Positive seeds paired with absent flowering are counted separately as an ascertainment flag. All raw zero counts are retained where other fields are present.
- Do not infer if a blank `number_of_seeds` means death, no flower, failure to collect, or zero. The target is conditional on being observed, not a population-level mean across all sown seeds. Report known data denominators at each stage.
- No covariates measured after the reproductive period (e.g. `shoot_growth`, `biomass`) in this predictive check.

### Fixed comparison and scoring

- Response: `y=log1p(number_of_seeds)`. Seed **count is a reproductive-fitness proxy W**, not confirmed viable recruitment F or measured partner-mediated service.
- M0: intercept + population FRO/PIC + six literal `line` categories (one-hot with reference category, no artificial treatment mappings).
- M1: M0 + `flowering_onset` as a continuous scalar, centered/scaled using training fold only. No nonlinear terms, interactions, SNPs or hyperparameter search.
- Model for both: deterministic ridge least squares with penalty `lambda=1` on non-intercept coefficients, training-only standardized continuous column. Categorical one-hot is unchanged. Use a fixed common feature dictionary from audited source code categories, not outcome-selected.
- **Five folds** grouped by `population|genotype`, `fold=int(SHA256(group_token) first four bytes) mod 5`; no sharing family labels between train/test. No random restart, no resampling seeds as independent genotype groups.
- If any fold has fewer than 10 complete-case test records or fewer than 3 genotype groups, declare `INSUFFICIENT_FOLD_SUPPORT` and stop, without revising folds.
- Primary metric: pooled held-out mean squared error `MSE(M0) − MSE(M1)` (higher than zero favors phenology); per-fold MSE and fraction of improved folds. Both **positive pooled gain and at least 4/5 fold wins** required for a nominal `WITHIN_PROGRAMME_PREDICTIVE_INCREMENT`. Otherwise report `NO_ROBUST_WITHIN_PROGRAMME_INCREMENT`.
- Descriptive 95% cluster-bootstrap interval of `M0−M1` using fixed out-of-fold prediction residuals and 1,000 deterministic `population|genotype` group-level resamples (seed 20261124). Do NOT label as independent-system uncertainty, causal significance, or prospective temporal forecasting.
- No other outcomes, folds, feature selection, transformations, penalties or after-the-fact model changes are allowed to repair a failed result.

### Release/stop and interpretation

Only aggregate sample/missingness/fold scores/group-level interval, original archive SHA and exact code/freeze commit into the public repository; no raw individual source data, ID labels, donor genetic calls, or original copyrighted workbook redistributed. If source download fails, identifier conditions differ, or numeric values are not usable, report an explicit stop. If eligible, **this analysis can only show within-2026 phenotype→reproductive proxy prediction**. No interpretation of `line` as genetic intervention is permitted until source codebook confirmed. Neither a positive nor negative outcome updates the existing EGWEE five-cluster meta-analysis or EGWE flagship simulation claims.
