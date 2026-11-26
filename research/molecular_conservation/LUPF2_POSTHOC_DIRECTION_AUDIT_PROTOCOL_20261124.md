# LUPF2-DIR — posthoc directional audit of the ALREADY FROZEN models (2026-11-24)

**Classification:** descriptive *posthoc* interpretation of the 2026 `LUPF2` exploratory T→W result, which itself followed the failed preregistered `LUPF1` strict-integer endpoint gate. **NOT another confirmatory hypothesis test, reparameterization, model selection, or new field replication.**

## Independent source and existing result to reconstruct exactly

Original authors' public field source: Sacristán-Bajo et al. (2026), Annals of Botany DOI 10.1093/aob/mcag061; [Figshare 29606180.v1](https://doi.org/10.6084/m9.figshare.29606180.v1), original `Lupinus_angustifolius_data_field.xlsx`, SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`.

Frozen exploratory LUPF2 protocol (committed before its outcome score): `053eca26bc1b527e828cb82cbac9318d20be7621`; same exact `source_prepare`, fold key `population|genotype`, 5 SHA256 partitions, common line one-hot dictionary C/J/L/R/T/X, ridge lambda=1 with intercept unpenalized, train-fold mean and SD for `flowering_onset`. LUPF2 aggregate run [45328763380](https://github.com/zuizui0223/egwee/actions/runs/45328763380), observed complete cases N=2008, groups N=84, baseline pooled MSE 1.134806869754752 and onset-added MSE 0.8706748619478497. Fold MSEs are in `LUPF2_EXPLORATORY_HOLDOUT_RESULT_20261124.md`.

## One fixed descriptive calculation

After downloading the exact source file, reconstitute the **same** frozen ridge M0 and M1 *without changing predictors, regularization, folds, group definitions, missingness or coding*. Verify **each fold's M0 and M1 MSE** and pooled MSE agree with the previously archived LUPF2 output within absolute tolerance `1e-8`. If any mismatch, **stop without printing slope sign**.

Then extract only the M1 standardized onset coefficient `beta_onset_sd` and its original-source-onset-unit coefficient `beta_onset_unit = beta_onset_sd / SD_train` from each **identically fitted original model**. Do not claim coefficient is gene flow, S-locus selection, pollinator efficacy or a causal intervention. If all 5 signs match, report descriptive direction and fold range; otherwise report unstable direction. Do not selectively omit folds.

Do **not** collect a new p-value, refit model at genotype medians, sample different outcomes, adjust for observed plant survival posthoc, exclude C/J/R/X etc, or change criterion in response to coefficient sign. Original LUPF2 result and LUPF1 stop must remain untouched.

## Interpretation hierarchy

1. **Within-study observed complete cases:** source-onset conditional association with the source-stored numeric seed production *proxy* after broad source population and **anonymous line-code** adjustment.
2. **Outside evidence:** 2025 original study DOI 10.1111/eva.70087 estimated total seed production as fruit number × average seeds per fruit; 2026 source precise seed derivation is not independently established by the available article abstract.
3. **Not supported:** causal early flowering → seed gain, fitness rescue over all 3024 planted records, molecular-G×I×F, predictive warning, independent biological landscape replication, universal management guidance. Observation completeness is 2008/3024 (66.4%) with FRO/PIC imbalance and line categories R/X only in FRO.

The directional audit is retained for generating a *prospective independently held-out* phenotype-to-seed/recruitment hypothesis. Its sign must **not** be treated as confirmed because source outcomes were already used for the LUPF2 positive predictive test.
