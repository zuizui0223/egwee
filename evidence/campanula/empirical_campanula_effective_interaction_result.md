# Campanula effective-interaction predictive result

## Locked decision

**`no_interaction_representation_supported`**

The prospectively declared Koski et al. (2018) test completed successfully on the first numeric-analysis workflow after the exact-model preregistration.

Result-generating provenance:

- head `e85ab9f3e93ee292cf9555ab67165a992baa88c6`;
- custom workflow `32822571416`;
- job `97723643554`;
- artifact `9553670343`;
- artifact digest `sha256:eb8e01876183be863d1e633e3502f1019f40ecb46ccd664f6102079460bfde45`.

Locked source:

- Dryad doi:`10.5061/dryad.5nj81nf`;
- Zenodo record `4969330`;
- 23 population rows;
- response `Pollen Limitation 2016`;
- leave-one-population-out validation;
- StandardScaler + Ridge(alpha=1.0) for every fitted representation;
- 10,000 paired population bootstraps, seed `20260825`.

## Held-out prediction

LOPO mean squared error:

| Representation | MSE |
|---|---:|
| M0 — training-population response mean | 0.0426464373 |
| M_raw — three group visitation rates | 0.0562322242 |
| M_phase — female-/male-phase visitation rates | 0.0573147558 |
| M_effective — deposition/removal flux coordinates | 0.0573147558 |

No interaction representation improved held-out prediction over M0 under the preregistered rule.

### Raw visitation adequacy

`M0 -> M_raw` mean gain = **-0.0135857868**; 95% bootstrap interval **[-0.0482337598, 0.0125086405]**.

Decision: unsupported.

### Phase-matched visitation adequacy

`M0 -> M_phase` mean gain = **-0.0146683185**; interval **[-0.0514695704, 0.0137848527]**.

Decision: unsupported.

### Effective-interaction adequacy

`M0 -> M_effective` mean gain = **-0.0146683185**; interval **[-0.0514695704, 0.0137848527]**.

Decision: unsupported.

### Primary effective-versus-raw contrast

`M_raw -> M_effective` mean gain = **-0.00108253165**; interval **[-0.00510147314, 0.00237521920]**.

Decision: no supported positive gain.

### Phase versus effective decomposition

`M_phase -> M_effective` mean gain was approximately **-3.16 × 10^-17**, with interval **[-1.04 × 10^-16, 1.37 × 10^-17]**.

The two models were therefore identical to machine precision under the fixed pipeline.

## Important representation boundary

The machine-precision equality of M_phase and M_effective means this campaign must **not** be summarized simply as “per-visit efficiency does not matter.”

Metadata defines each effective coordinate as one phase-matched visitation coordinate multiplied by a group-specific per-visit deposition/removal quantity. The preregistered model then standardized every predictor column independently before Ridge fitting.

For a positive constant `c_j`, feature-wise standardization gives

`standardize(c_j x_j) = (c_j x_j - c_j mean(x_j)) / (c_j sd(x_j)) = standardize(x_j)`.

Thus, if the source effective flux is a fixed scalar multiple of its corresponding phase-rate coordinate across populations, the preregistered preprocessing removes that scalar calibration. In that case M_phase and M_effective are not distinct statistical representations after standardization.

A post-result predictor-only diagnostic may verify whether the six source column pairs are indeed constant rescalings. That diagnostic cannot change the locked decision and may not inspect `Pollen Limitation 2016`.

## Scientific interpretation

Two conclusions are supported.

First, **none of the preregistered interaction representations earned transferable predictive adequacy for population pollen limitation** under 23-population LOPO validation. Raw visitation itself predicted worse than the no-interaction mean reference on average, and neither phase matching nor the fitted effective representation rescued that result.

Second, the campaign exposes a new state-representation failure mode: **mechanistic information can be erased by the analysis pipeline even when it is present in the measured variables**. A biologically meaningful efficiency multiplier does not survive independent feature standardization if it acts only as a constant scale factor on an otherwise identical coordinate.

This is distinct from the earlier empirical boundaries:

1. Eschscholzia — candidate-state proxy existed but did not earn endpoint-relevant predictive adequacy;
2. experimental-colonization Campanula — desired realised visitation was absent on every response-bearing unit;
3. Koski Campanula — effective-interaction data are available and outcome-independently calibrated, but the preregistered feature-wise standardization can collapse efficiency-scaled coordinates onto phase-matched visitation.

## Claim ceiling

Do not claim:

- that per-visit pollinator efficiency is biologically irrelevant;
- that raw visitation is universally uninformative;
- that any bee group is beneficial or harmful from this project-generated prediction test;
- that an alternative aggregation of the same efficiency data would fail;
- a universal pollen-limitation or interaction threshold.

## Stop rule

Do not rerun this population pollen-limitation endpoint with summed fluxes, unstandardized variables, a different scaler, selected pollinator groups, source `Depletion` columns, latitude/longitude, another ridge alpha or a nonlinear model. Any future efficiency-state test must prospectively define a representation in which mechanistic weights cannot be algebraically removed by preprocessing, preferably in an independent outcome/dataset.