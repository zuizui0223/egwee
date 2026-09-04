# Campanula predictor-only rescaling diagnostic result

## Locked decision

**`constant_rescaling_confirmed`**

The response-firewalled diagnostic completed successfully without reading `Pollen Limitation 2016` or any other outcome values.

Provenance:

- result-generating head `d50a2d819fc63d93851be1bcf5ff19531e578339`;
- workflow `32831523960`;
- job `97751069300`;
- artifact `9556920701`;
- artifact digest `sha256:5d456fa4c03628e2700c842daa7625f53058004627d1fa8531daef31631a9166`.

## Six fixed predictor pairs

All six preregistered phase-to-effective pairs were constant positive rescalings across the 23 populations.

| Phase coordinate | Effective coordinate | Constant ratio | Max relative ratio deviation | Max absolute z-score difference |
|---|---|---:|---:|---:|
| Bumble Female Rate | Bumble Grains Dep Per Hour | 41.78 | 0 | 8.88e-16 |
| Megachile Female Rate | Mega Grains Dep Per Hour | 25.5253 | 1.39e-16 | 8.88e-16 |
| Small Female Rate | Small Grains Dep Per Hour | 22.0423 | 1.61e-16 | 8.88e-16 |
| Bumble Male Rate | Bumble Grains Rem Per Hour | 5261.05 | 0 | 8.88e-16 |
| Megachile Male Rate | Mega Grains Rem Per Hour | 10460.09 | 1.74e-16 | 2.22e-16 |
| Small Male Rate | Small Grains Rem Per Hour | 5734.76 | 1.59e-16 | 2.22e-16 |

For every phase-rate zero, the corresponding effective coordinate was also zero.

Thus for each pair `y_j = c_j x_j` with positive constant `c_j` across populations. Independent feature-wise z-standardization therefore gives

`z(y_j) = z(c_j x_j) = z(x_j)`

up to machine precision.

## Interpretation

This confirms the representation explanation for #114's machine-identical `M_phase` and `M_effective` models. The effective pollen-transfer columns did contain source-defined efficiency multipliers, but the preregistered StandardScaler normalized each column independently and removed those constant multipliers before Ridge fitting.

The supported conclusion is therefore **not** that per-visit efficiency is biologically irrelevant. It is that:

> A mechanistically meaningful state coordinate can lose its mechanistic weighting when the analysis representation applies a transformation invariant to that weighting.

This adds an analysis-layer requirement to state sufficiency: candidate state variables must not only be measured at the correct ecological scale; the downstream representation must preserve the information that made them mechanistically distinct.

## Relation to previous natural-system boundaries

- *Eschscholzia*: a plausible pollinator availability/trait proxy did not earn endpoint-relevant predictive adequacy.
- *Oenothera*: a missing spatial mating coordinate retained independent information after pollinator treatment.
- Koski *Campanula*: independently calibrated efficiency information existed, but the chosen feature-wise standardization collapsed effective and phase representations.

Together these imply a three-part empirical gate:

`measurement adequacy -> representation/information preservation -> residual origin/history test`.

Only after a candidate state passes both the measurement and representation gates should it be used to ask whether upstream habitat origin/history is redundant.

## Claim ceiling / stop rule

This diagnostic does not alter #114's `no_interaction_representation_supported` decision and does not authorize rerunning that pollen-limitation endpoint with summed fluxes, unstandardized predictors, alternative scaling, selected groups or nonlinear models.

Any future efficiency-state test must prospectively define a representation that preserves mechanistic weights and must use an independent outcome/dataset.