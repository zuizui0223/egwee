# Prospective Campanula effective-interaction predictive test

## Registration status

This is the required second exact-model preregistration after #113 established **`effective_interaction_state_identifiable`** from workbook structure and string labels only.

No numeric study-cell value from Koski et al. (2018) has been inspected by this project before this document is committed.

Locked source remains:

- Dryad doi:`10.5061/dryad.5nj81nf`;
- Zenodo record `4969330`;
- file `Koski et al. 2018_Data_ProcRoySoc.xlsx`;
- MD5 `2d26307743e8a22384781854b8f2f33b`;
- SHA-256 `b81b77248b75330049e1ddd8ae026db127f838e979620a0415a5addb9a7e8f27`.

## Scientific question

> **Does a source-defined, efficiency-calibrated pollen-transfer state predict population pollen limitation better across populations than raw pollinator visitation alone?**

This is a candidate-state adequacy test. It is intentionally upstream of any later residual-geography or cross-system convergence test.

## Unit and endpoint

The locked population sheet is `PopVis Rates_ PL_Depletion` and contains one header plus 23 population rows.

Validation unit: **population**.

Primary response:

- exact source column `Pollen Limitation 2016`.

The response is retained on the source scale. Metadata defines it as:

`(seeds from hand-pollinated fruit - seeds from control fruit) / seeds from control fruit`, with source-negative values already constrained to zero.

The project does not re-transform, threshold, winsorize, re-center or re-calculate this endpoint.

## Source-consistency gate before modelling

The test is `not_identifiable_for_primary_endpoint` if any of the following occurs before fitting:

1. sheet `PopVis Rates_ PL_Depletion` is absent;
2. the sheet does not contain exactly 23 non-header population rows;
3. `Population` is blank or duplicated;
4. any locked response/state column below is absent;
5. any locked response/state value is blank, non-numeric or non-finite;
6. fewer than 20 populations remain for any reason;
7. a leave-one-population-out fold cannot be fit with the fixed model.

No missing value is imputed and no population is deleted to rescue a preferred result.

## Fixed state representations

The four representations are fixed from schema/Metadata labels before numeric inspection.

### M0 — no interaction information

Training-population mean of `Pollen Limitation 2016`.

This is the no-interaction reference.

### M_raw — raw group-specific realised visitation

Exact columns:

- `Bumblebee Rate`
- `Megachile Rate`
- `Small Rate`

Metadata defines these as visits/flower/hour for the three pollinator groups.

No total-visitation collapse is substituted after inspection.

### M_phase — flower-phase-matched visitation

Exact columns:

- `Bumble Female Rate`
- `Megachile Female Rate`
- `Small Female Rate`
- `Bumble Male Rate`
- `Megachile Male Rate`
- `Small Male Rate`

Metadata defines these as group visitation rate multiplied by the group-specific proportion of visits to female- or male-phase flowers.

This representation asks whether behavioural phase matching improves transfer beyond raw visitation before adding per-visit efficiency.

### M_effective — source-defined efficiency-calibrated pollen-transfer state

Exact columns:

- `Bumble Grains Dep Per Hour`
- `Mega Grains Dep Per Hour`
- `Small Grains Dep Per Hour`
- `Bumble Grains Rem Per Hour`
- `Mega Grains Rem Per Hour`
- `Small Grains Rem Per Hour`

Metadata defines deposition flux as female-phase visitation rate × pollen grains deposited by one visit, and removal flux as male-phase visitation rate × pollen grains removed by one visit.

These source-defined fluxes are explicitly independent of population pollen limitation. They are derived from the separate single-visit calibration programme and are used exactly as supplied. The project does **not** estimate efficiency weights from `Pollen Limitation 2016`.

The three source-defined `... Depletion` columns are not included in the primary test because they are an additional derived representation and are not needed to answer the preregistered raw-versus-effective question.

## Fixed model family

For M_raw, M_phase and M_effective:

- `sklearn.linear_model.Ridge(alpha=1.0)`;
- numeric predictors standardized using training-fold mean and standard deviation only;
- intercept fitted by Ridge;
- no interactions;
- no polynomial terms;
- no feature selection;
- no hyperparameter search;
- no alternative alpha after the result.

M0 predicts the training-fold response mean and uses no fitted covariates.

## Leave-one-population-out validation

For each of the 23 populations:

1. hold out the entire population row;
2. fit each representation on the other 22 populations;
3. predict the held-out `Pollen Limitation 2016`;
4. retain squared prediction error.

No row-wise resampling within populations exists because the population is already the source unit.

## Fixed score comparisons

Positive gain means the second representation predicts an unseen population better.

For each held-out population calculate:

- **raw adequacy**: `SE(M0) - SE(M_raw)`;
- **phase adequacy**: `SE(M0) - SE(M_phase)`;
- **effective adequacy**: `SE(M0) - SE(M_effective)`;
- **phase gain over raw**: `SE(M_raw) - SE(M_phase)`;
- **effective gain over raw**: `SE(M_raw) - SE(M_effective)` — **primary contrast**;
- **effective gain over phase**: `SE(M_phase) - SE(M_effective)` — secondary decomposition.

Overall LOPO MSE for all four representations is also retained.

## Fixed uncertainty

Bootstrap the 23 held-out population score vectors with replacement **10,000 times**, RNG seed **`20260825`**.

For every comparison report:

- mean gain;
- 95% percentile interval.

A gain is `supported_positive_gain` only if the 95% interval lies wholly above zero.

No row-level bootstrap, alternative seed, confidence level or one-sided reinterpretation is opened.

## Primary decision rule

Let:

- `raw_supported` = M0→M_raw adequacy supported positive;
- `phase_supported` = M0→M_phase adequacy supported positive;
- `effective_supported` = M0→M_effective adequacy supported positive;
- `effective_over_raw` = M_raw→M_effective gain supported positive.

The locked overall decision is:

1. **`effective_interaction_supported_over_raw`** if `effective_supported` and `effective_over_raw` are both true;
2. **`effective_interaction_supported_no_gain_over_raw`** if `effective_supported` is true but `effective_over_raw` is false;
3. **`phase_matched_visitation_supported_no_effective_support`** if `effective_supported` is false and `phase_supported` is true;
4. **`raw_visitation_supported_no_effective_support`** if `effective_supported` and `phase_supported` are false but `raw_supported` is true;
5. **`no_interaction_representation_supported`** if none of raw, phase or effective representations is supported against M0;
6. **`not_identifiable_for_primary_endpoint`** if any fixed source/fitting gate fails.

The `effective gain over phase` comparison is always reported but does not replace the primary raw-versus-effective rule.

## Interpretation ceiling

A positive effective-interaction result would show only that the source-defined deposition/removal flux representation transfers across these 23 populations better than raw visitation under the fixed model.

It would not establish:

- a universal bee-size rule;
- that any pollinator group is universally mutualistic or antagonistic;
- a universal pollen-limitation threshold;
- full eco-genetic state sufficiency;
- cross-system functional-fragmentation convergence.

A null or adverse effective-interaction result would not invalidate the independent single-visit measurements; it would bound their usefulness as a population-level predictive state under this fixed representation.

## Stop rule

Do not switch to total visitation, female-only visitation, male-only visitation, one pollinator subset, the source `Depletion` columns, latitude/longitude, another response, another ridge alpha, interactions, nonlinear models, selected populations, alternative bootstrap seeds or outcome-informed efficiency weights because the result is weak or surprising.