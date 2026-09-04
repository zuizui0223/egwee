# N3 preregistration — Mallorca carob process adequacy and residual context

Date frozen: 2026-08-27, before any project-computed association between the deposited reproductive outcomes and predictors was fitted or scored.

## Purpose

This is the first N3 island candidate to reach a prospectively analyzable process/function representation. It tests, in order:

1. whether direct pollinator visitation abundance earns held-out predictive information for realised fruit production; and
2. only if that process-adequacy gate is passed robustly across the two source-deposited visitation representations, whether upstream landscape/local-management context adds held-out predictive information beyond that partial process state.

This analysis does **not** estimate an island-versus-urban effect and cannot establish island–urban regime convergence by itself.

## Locked source and Stage-A facts

Source study: Gómez-Martínez et al. (2025), *Landscape conservation and orchard management influence carob tree yield through changes in pollinator communities*.

Locked public data:

- Zenodo version DOI: `10.5281/zenodo.13939480`
- file: `Dataset_CarobTree.xlsx`
- archived workbook MD5 observed during response-firewalled Stage A: `9cf7668ae8d825c72edda3346ebf36a6`

Source methods define pollinator abundance as the total number of flower-visiting individuals recorded per study orchard and year. Sampling effort was fixed at five sampling days × three observers × one hour per orchard-year, so dividing by 15 observer-hours is a constant rescaling to direct visitation intensity.

Stage A established, without computing any reproductive-outcome association:

- `FruitProduction` contains `StudyOrchard`, `Year`, `Tree`, `TotalFlowers`, `TotalFruits`, `Fruits1000`, `PolinAbun`, `Pnatur1k`, `FarmSys`, `ratMF`, `CCA1`, and `CCA2`;
- 568 tree rows represent 37 orchard-year keys from 20 independent orchards in 2019–2020;
- `TotalFlowers`, `TotalFruits`, `PolinAbun`, `Pnatur1k`, `FarmSys`, and `ratMF` are complete on those rows;
- all fruit-production orchard-year keys have a unique row in `PollinatorAbundance`;
- the four embedded predictor/context fields are constant within each orchard-year;
- `Pnatur1k`, `FarmSys`, and `ratMF` agree between the two sheets for every shared key;
- `PolinAbun` does **not** agree exactly between `FruitProduction` and `PollinatorAbundance` for 16 of the 37 production orchard-year keys.

That last fact is treated as a representation uncertainty, not silently repaired.

## Frozen biological unit

The analysis unit is **orchard × flowering year**, with orchard as the independent holdout unit.

Tree rows are deterministically aggregated within orchard-year before fitting:

- `fruit_count = sum(TotalFruits)`
- `flower_exposure = sum(TotalFlowers)`

The response therefore retains the source-defined fruit-production meaning while avoiding tree-level pseudoreplication. The model uses `log(flower_exposure)` as an offset, so it predicts fruit production per flower; multiplication by 1000 would only rescale the rate and is not used for fitting.

No orchard-year is dropped based on reproductive outcome magnitude. Rows may only be excluded for preregistered structural invalidity: missing required fields, non-positive flower exposure, negative fruit count, or a missing orchard/year key. Stage A found none of these problems in the 568 fruit rows.

## Direct-interaction representations

Two representations are mandatory because the deposited workbook contains a provenance disagreement.

### I-primary — embedded production-table representation

`I_embedded = FruitProduction.PolinAbun / 15`

This is primary because it is the source-deposited pollinator-abundance covariate already aligned to the production rows used by the source analysis.

### I-sensitivity — independently joined pollinator-table representation

`I_joined = PollinatorAbundance.PolinAbun / 15`, joined only by exact `StudyOrchard × Year`.

No fuzzy key matching, interpolation, averaging across years, or value-dependent reconciliation is permitted.

The two representations must both be reported. Neither may be selected after observing predictive performance.

## Primary endpoint

The only endpoint in this preregistered run is fruit production:

- observed count: `fruit_count = sum(TotalFruits)` within orchard-year;
- exposure: `flower_exposure = sum(TotalFlowers)` within orchard-year.

Seed production and seed weight are **not** fallback endpoints. They cannot be opened in this N3 run to rescue an unfavorable fruit-production result.

## Model family and preprocessing

All fitted models use an NB2 negative-binomial likelihood with log link and offset `log(flower_exposure)`, matching the source study's negative-binomial treatment of fruit production while preserving an integer count response.

Continuous predictors are standardized using the training-fold mean and population SD only. The fitted transformation is then applied to the held-out orchard. If a required training-fold SD is zero/non-finite, the preregistered model is not identifiable; no alternative transformation is substituted.

`Year` is categorical. `FarmSys` is categorical using the lexicographically first training level as reference. An unseen held-out category makes the fold non-identifiable rather than being recoded post hoc.

## B1 — process adequacy

For each direct-interaction representation separately:

- `B0: fruit_count ~ Year + offset(log(flower_exposure))`
- `B1: fruit_count ~ Year + z(I_visit) + offset(log(flower_exposure))`

Validation is leave-one-orchard-out. All orchard-years of one orchard are held out together.

Within each held-out orchard, negative log likelihood is averaged across its one or two orchard-year observations so every orchard receives equal weight. Define:

`delta_process = mean_NLL(B1) - mean_NLL(B0)` per held-out orchard.

The total score is the sum of the 20 orchard-level deltas.

A deterministic orchard bootstrap uses seed `20260827`, `10000` bootstrap samples, resampling the 20 orchard-level deltas with replacement and summing each draw.

`process_information_detected` requires both:

- total delta < 0; and
- the upper bound of the bootstrap 95% interval < 0.

Otherwise the representation receives `no_detected_process_information`.

### Representation gate

B2 may open only if **both** `I_embedded` and `I_joined` independently receive `process_information_detected`.

If both fail, the system is classified `process_measurement_not_supported_for_primary_endpoint`.

If they disagree, it is classified `process_representation_sensitive`; B2 remains closed. This is a representation-boundary result, not permission to choose the favorable representation.

## B2 — residual upstream context

Only if the B1 representation gate passes, compare within each visitation representation:

- `C0: fruit_count ~ Year + z(I_visit) + offset(log(flower_exposure))`
- `C1: fruit_count ~ Year + z(I_visit) + z(Pnatur1k) + FarmSys + z(ratMF) + z(ratMF)^2 + z(Pnatur1k):FarmSys + offset(log(flower_exposure))`

The quadratic male-to-female term and landscape × farming-system interaction are fixed here because they are source-defined biological/context terms, not because of the project-computed outcome values.

Validation, orchard weighting, bootstrap seed/sample count, and score definition are identical to B1:

`delta_context = mean_NLL(C1) - mean_NLL(C0)` per held-out orchard.

`residual_context_information_detected` requires total delta < 0 and bootstrap 95% upper bound < 0. Otherwise the representation receives `no_detected_residual_context_information`.

A robust `context_predictively_redundant_given_partial_process_state` result requires `no_detected_residual_context_information` under **both** visitation representations after both passed B1.

A robust `residual_context_required` result requires `residual_context_information_detected` under **both** visitation representations.

If the two context decisions disagree, classify `residual_context_representation_sensitive` and do not claim redundancy or necessity.

## Model-identifiability stop rule

The NB2 model is fit independently inside every training fold. If any required model fails to converge, returns non-finite parameters/dispersion, cannot encode the held-out design, or produces non-finite held-out likelihood, the corresponding stage is `primary_model_not_identifiable`.

No Poisson, Gaussian, alternate link, predictor deletion, threshold change, outlier deletion, orchard deletion, year deletion, seed change, or alternate endpoint may be substituted after seeing the failure.

## Interpretation ceiling

A B1 pass would show that direct visitation abundance earns endpoint-relevant predictive information in this island crop system under the locked representation.

A subsequent B2 no-gain result would show only that the measured upstream context variables add no held-out predictive information beyond the locked partial process state for this endpoint/model. It would **not** prove causal irrelevance of habitat loss/management or that historical origin can universally be forgotten.

Even a fully successful carob result plus the Toronto result remains one island system and one urban system. N3 already requires at least two independent systems per origin with matched estimands before a cross-origin convergence claim becomes eligible.
