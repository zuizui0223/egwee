# SF06 leave-one-publication-out predictive-value audit — 2026-10-07

## Status

Post-exposure exploratory prediction audit. This is not part of the preregistered SF06 inferential test and is not used to redefine the external topology.

## Question

A significant association can be statistically real yet add little prediction for a new study.

We therefore compare simple leave-one-publication-out (LOPO) models using the corrected public-S1 habitat-fragmentation pairs.

## Analysis A — all 55 fragmentation pairs

For each held-out source publication:

- baseline: predict female-fitness d from the training-set intercept only;
- pollination model: predict female-fitness d from training-set d_F ~ d_I.

Predictions are evaluated only on the held-out publication.

### Row-weighted performance

- baseline MSE = 0.45536;
- pollination MSE = 0.44511;
- MSE reduction = **2.25%**;
- baseline MAE = 0.51740;
- pollination MAE = 0.52257;
- sign accuracy = **78.2% baseline vs 76.4% with pollination**.

### Publication-balanced performance

Averaging publication-specific errors equally:

- baseline MSE = 0.46446;
- pollination MSE = 0.44839;
- MSE reduction = **3.46%**;
- baseline MAE = 0.51572;
- pollination MAE = 0.50435.

Thus pollination effect size provides a small continuous-prediction improvement by squared error, but not a strong or uniformly better prediction gain.

## Analysis B — preregistered compatibility frame

Restrict to the 49 SC/SI fragmentation pairs.

For each held-out publication:

- baseline: d_F ~ SC;
- full: d_F ~ d_I + SC.

### Row-weighted performance

- SC-only MSE = 0.41084;
- d_I + SC MSE = 0.40070;
- MSE reduction = **2.47%**;
- SC-only MAE = 0.50306;
- d_I + SC MAE = 0.50148;
- sign accuracy = **77.6% SC-only vs 75.5% with pollination**.

### Publication-balanced performance

- SC-only MSE = 0.36310;
- d_I + SC MSE = 0.34960;
- MSE reduction = **3.72%**;
- SC-only MAE = 0.47348;
- d_I + SC MAE = 0.45635.

## Interpretation

The corrected in-sample model finds a statistically positive pollination coefficient, but the held-publication predictive increment is modest.

This sharpens the distinction among:

1. **association** — d_I and d_F covary;
2. **calibration** — d_I maps accurately onto d_F severity;
3. **classification** — d_I improves diagnosis of whether F is impaired;
4. **transfer prediction** — d_I improves prediction in a new source publication.

SF06 supports association, but the current public-S1 analysis gives weak evidence for large incremental calibration or transfer-prediction value and no sign-classification improvement.

## Claim ceiling

Allowed:

- significant in-sample coupling does not translate into large LOPO predictive gains in this public-S1 subset;
- the predictive audit supports the association-versus-sentinel distinction.

Not allowed:

- the LOPO result is a preregistered validation endpoint;
- the observed 2–4% MSE reduction is a universal effect size;
- publication-level cross-validation eliminates all dependence or heterogeneity;
- the result proves pollination measurements are useless.
