# Internal interaction→function incremental sentinel value — 2026-10-07

## Purpose

Distinguish “non-identifying” from the stronger and generally false statement “contains no information”.

The frozen 16-programme translation map is evaluated as a deterministic classification problem:

- baseline: ignore interaction state and always predict the most common reproductive-function state;
- interaction lookup: for each interaction state, predict its most common reproductive-function state.

The difference in errors is the in-sample incremental classification gain. This is a descriptive structural diagnostic, not an out-of-sample prediction-error estimate.

## Full 16-programme mixed-tier map

Function-state counts:

- lower = 6;
- mixed = 3;
- no_detected_loss = 4;
- similar = 2;
- higher = 1.

Baseline majority-state rule:

- errors = **10/16**.

Best interaction-state lookup:

- errors = **5/16**.

Incremental gain:

- **5 correctly classified programmes** relative to the no-interaction baseline.

Thus interaction state clearly contains information in the richer mixed-tier state map, but remains non-identifying.

## Canonical strict 8-programme map

Using the existing category-sensitivity rules, all mixed and no_detected_loss states are removed.

Function-state counts:

- lower = 5;
- higher = 1;
- similar = 2.

Baseline:

- errors = **3/8**.

Best interaction-state lookup:

- errors = **2/8**.

Incremental gain:

- **1 programme**.

The strict map remains many-to-many and leave-one-programme robust.

## Strict quantitative-only subset

The five quantitative strict programmes have function states:

- lower = 4;
- higher = 1.

Baseline always-lower rule:

- errors = **1/5**.

Best interaction-state lookup:

- errors = **1/5**.

Incremental gain:

- **0 programmes**.

This is directly analogous to the corrected external SF06 binary sign result, where pollination sign also gives zero deterministic classification gain over the fragmentation-context baseline.

## Interpretation

The correct hierarchy is:

1. interaction state can carry ecological information;
2. information content depends on how finely the response states are represented;
3. that information does not make interaction a sufficient stand-alone sentinel of reproductive state;
4. in the strict quantitative direction-only map, interaction state provides no deterministic classification gain beyond the dominant downstream state.

Therefore EGWEE should avoid both extremes:

- not “interaction perfectly predicts function”;
- not “interaction contains no information”.

The supported statement is:

> **interaction response is informative but insufficient, and under conservative direction-only representations its incremental state-diagnostic value can collapse to zero.**

## Claim ceiling

These are in-sample structural diagnostics from a small frozen map.

They are not prevalence estimates, cross-validated prediction errors, or estimates of operational monitoring accuracy.
