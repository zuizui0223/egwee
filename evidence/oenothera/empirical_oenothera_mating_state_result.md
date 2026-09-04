# Oenothera natural mating-state result — residual spatial isolation after pollinator state

## Decision

**`residual_isolation_detected`**

Using the preregistered *Oenothera harringtonii* comparison, maternal spatial isolation retained both predictive and permutation-supported information about correlated paternity after pollinator-exclusion treatment was supplied.

This is a **contemporary mating-state (`G_mating/C_pollen`) result**, not a direct ecological-function or functional-loss result.

## Locked source

- Rhodes, Fant & Skogen (2017), *Molecular Ecology* 26:4296–4308, doi:`10.1111/mec.14115`
- archived dataset: `10.5061/dryad.p24q3`
- public Zenodo mirror: record `4942351`
- file: `multiplePaternity.csv`
- published and observed MD5: `600f6f370ffa8ad205d0ccb6bc92ab65`

The archive describes each row as a sample of seeds from one fruit. The final locked data structure contained **60 fruit/seed-family rows from 23 maternal plants**. There were 37 repeated rows beyond one row per maternal plant. Pollinator treatments were `c`, `de` and `ne`.

## Schema correction before outcome inspection

The first workflow stopped before fitting the declared models because `plantID` was repeated. A later schema-only audit showed that repeated maternal plants may carry multiple fruit-level pollinator treatments while `isolation20` remains a maternal-plant spatial attribute.

Accordingly, the final validation held out one **maternal plant** at a time, with all fruit rows for that plant excluded together. `isolation20` was permuted only among maternal plants with an identical treatment-profile multiset. No response, isolation metric, treatment variable, permutation count, RNG seed or decision rule was selected after seeing an outcome result.

Treatment-profile counts were:

- `c/de`: 4 maternal plants
- `c/de/ne`: 14
- `c/ne`: 3
- `de/ne`: 2

## Fixed comparison

`M0: correlatedPaternity ~ treatment`

`M1: correlatedPaternity ~ treatment + z(isolation20)`

Higher `correlatedPaternity` means that two offspring are more likely to share a father and therefore corresponds to **lower realised paternal diversity**.

### Held-out prediction

| model | leave-one-maternal-plant-out MSE | MAE |
|---|---:|---:|
| M0 — pollinator treatment only | 0.116186 | 0.285155 |
| M1 — treatment + isolation | 0.091870 | 0.241071 |

Adding `z(isolation20)` reduced held-out MSE by **0.024317**, a **20.93% improvement**, and reduced MAE by **0.044084**.

### Incremental isolation term

The full-data standardized isolation coefficient was **+0.156378** on the correlated-paternity scale. Thus, after pollinator treatment was included, more spatially isolated maternal plants were predicted to have higher correlated paternity and hence lower paternal diversity.

The RSS gain from adding isolation was **1.456477** (`6.286539 -> 4.830062`). Under the locked 10,000-permutation test, where plant-level isolation was permuted only within identical treatment-profile strata, the one-sided p-value was **0.00129987**. The central 95% range of permuted RSS gains was `[0.000292, 0.902154]`, below the observed gain.

## Ecological interpretation

The result supplies the counterexample that the state-sufficiency programme needed. E1 Honshu–Izu and E2 Zurich showed cases where an upstream geographic/urban descriptor did not add transferable prediction after a measured interaction-functional state was supplied. *Oenothera* shows the opposite boundary for a different process layer: **pollinator functional access alone does not absorb the spatial information relevant to contemporary mating state**.

Operationally,

`pollinator state I/T + spatial mating opportunity C -> realised mating state G_mating`

is better supported than

`pollinator state I/T -> realised mating state G_mating`

for this dataset.

This means that a natural eco-genetic state cannot generally replace process-specific connectivity or mating opportunity with pollinator identity, visitation or another interaction variable. Whether an upstream spatial descriptor becomes redundant depends on **which downstream process is being predicted and which state coordinates have actually been measured**.

## Claim ceiling

Permitted claim:

> After conditioning on the available pollinator-exclusion state, maternal spatial isolation retained independently validated information about correlated paternity in *Oenothera harringtonii*. This supports retaining spatial mating opportunity / contemporary pollen-connectivity information as a distinct natural-state coordinate when predicting mating state.

Not permitted:

- that `isolation20` is a universal fragmentation threshold;
- that the result directly demonstrates ecological-function loss;
- that all spatial context remains informative after a complete eco-genetic state is measured;
- that the result establishes a universal causal effect of geographic isolation on genetic warning.

## Provenance

- GitHub Actions run: `32721630217`
- job: `97414084955`
- scientific head: `d9688dae3ec609376d36ee4a7df9b193137938fb`
- artifact: `9519204842`
- artifact digest: `sha256:97a2b2359ec44b2fbd94ecd54975f206f240be3c994ef2a50c636678ee882eb1`
- 10,000 permutations
- RNG seed: `20260824`

No third-party raw data are committed to this repository.
