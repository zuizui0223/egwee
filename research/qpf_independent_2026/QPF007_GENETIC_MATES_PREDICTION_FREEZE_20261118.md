# QPF007 genetic mating stage: postprimary exploratory original-source design

**2026-11-18 — specification before inspecting new genetic-outcome coverage, direction or fitted losses.** This is a separate, *post-primary/post-coverage exploratory* target in one 2026 *Brassica rapa* experimental study, stacked on PR #85. The prior source-registered 160/16 Q→P→per-fruit-seed test remains **COVERAGE_STOP** (145 complete, one session only 5 plants); its later exploratory seed forecast (+1.44%, 7/16 folds) remains **not confirmatory**. Neither is reclassified here.

## Verified source and prior work

Original Barbot et al. (2026), *PLoS Biology*, DOI [10.1371/journal.pbio.3003579](https://doi.org/10.1371/journal.pbio.3003579). Original Zenodo DOI [10.5281/zenodo.21628183](https://doi.org/10.5281/zenodo.21628183), main 160-mother file `data_ABPOLL_ID_resume.txt` SHA256 `5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe`, original flower-stigma `data_ABPOLL_flower_resume.txt` SHA256 `ec7217acb683a0d0475622f3510228f3062a72a8bfd17162888f160db369a495`. Original source plant/stigma key cardinalities 160/160 across **16 manipulated experimental sessions**. The paper **already establishes** effects of experimental Bombus abundance on mate access vs actual genetic fertilization; those results are prior art, not an EGWEE novel mechanism.

## Separate question and literal outcome

Within source mother×session, does original measured **mean stigmatic pollen load** improve **out-of-session prediction of genetically inferred female mating success** beyond original flower-visitation count, flower number, plant size and experimentally imposed pollinator density? Genetic mating success is the literal author source column **`gMS_fem_all`**, which must be found exactly once. Do not swap target for `SR_all`, total seeds, father diversity, offspring survival or other source columns after result inspection.

Target `y=log1p(gMS_fem_all)` for source finite nonnegative counts only. This is an *author-derived genotypic mating-success proxy from sampled offspring*, not a fully observed number of biological mates nor allele-specific compatible pollen, effective gene flow or seed survival. Original analysis has source `fix10` paternity subsample; unknown unresolved genotyping missingness/finite 10-offspring ceiling may limit inference.

The original source `data_ABPOLL_ID_level_detID.txt` directed visit→seed partner table includes 18 session labels vs 16 in the mother/flower file, and is **not joined**. The 1,099 raw offspring paternity records also have no verified plant/session assignment and must not be silently joined. We use only original already-aggregated author `gMS_fem_all` at the same verified source mother ID. No pseudo-observation of father identity.

## Pre-outcome source eligibility gate

First run code that inspects only exact source column names and **missingness/numeric validity flags**, not signed values, covariance, direction or genetic mate scores. Source condition:
- Original 160 distinct `session×ID_full` mother IDs, 16 source sessions; flower pollen file must contain the exact same 160 mother keys.
- Original experimental `poll_treat` category 2–5 labels, and numeric nonnegative finite `nb_visit`, `nb_flo_all`, `height_max`, `pl_mean`, `gMS_fem_all`. Never treat NA as zero; one maternal plant is one unit.
- At least **120** complete mother units, all **16 original sessions**, at least **2 mothers per session**. All target values are inspected only for finite/nonnegative validity; a zero-variance training target causes a later model STOP, not a source-only outcome inspection. Failing minimums yields `SOURCE_GENETIC_TARGET_COVERAGE_STOP`, no fitted coefficients. The original stronger **≥6/session** confirmation rule remains failed and is not altered: this new target cannot count as registered original confirmation even if admissible at ≥2/session.
- Report aggregate session min/median/max eligible n, total missingness per field and source digest. No raw individual keys, source genetic success values, visitor events or genomic alleles in GitHub records.

## Conditional frozen predictive model (do not fit before separate source-only gate)

- M0 predictors: original source pollinator density treatment one-hot with lexicographically first source reference, `log1p(nb_visit)`, `log1p(nb_flo_all)`, `log1p(height_max)`.
- M1: M0 plus exactly one `log1p(pl_mean)` column measured from source matched stigma sample(s).
- Same ridge lambda=1, intercept unpenalized, train-only feature z scoring (zero variance → 1, no test leakage), original source 16 whole experimental sessions held out once each. Predictions and response on original **log1p genetic mating success** scale; *not* comparable numerically to prior per-fruit seed MSE.
- Every original mother scored once. Report pooled mother-equal MSE, MAE, observed M0−M1 MSE, relative gain and wins among 16 whole-session folds. Two numerically independent ridge solvers must agree within 1e-8. No p-value or after-the-fact model selection.
- **Interpretation gate:** any sign is a *postprimary descriptive model-specific result*, NEVER confirmatory. Show the prior nominal 5%-and-12/16 positive rule for context only if useful; it cannot rescue the 145-source coverage STOP. Quantify source-fold influence using the already scored group losses, without refitting or changing the scientific decision.

## Required limitations

The target is original *genetically inferred mating success* (number of partners in source's genotyped sample), not genuine genetically compatible pollen on the same stigma or viable seedlings. The 16 pollinator-density sessions belong to one manipulated original study, **not 16 independent habitats/countries/natural fragmented regions**. Source mate counts can be ceiling-limited by genotyped offspring; detection error may correlate with counted seeds. A positive or negative signal cannot identify causal Q→P→genetic-F transfer. The original PLoS Biology paper already interprets mating episodes.

This add-on is useful only as a transparent *outcome-stage contrast* within one source, with the model/denominator/publication boundary exactly disclosed. No source original rows redistributed. No changes to main, PR #85's two original prospective protocols or exploratory seed endpoint, existing QPF001/004, crop/EuPPollNet work, natural fragmentation effect sizes, or theoretical egwe.
