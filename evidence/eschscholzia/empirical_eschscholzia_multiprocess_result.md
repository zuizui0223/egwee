# Eschscholzia multi-process natural-state result

## Primary decision

**`multi_endpoint_not_identifiable`**

The preregistered multi-endpoint F+G convergence test could not be completed because the F endpoint closed at its predeclared source-consistency gate. This is not a weak or null F result: no F model was fitted.

At array `1||3`, the pollinator source encoded Habitat as `Fallow ground`, while the F source encoded the same array as `Fallow graound`. The second preregistration required exact Habitat agreement across joined sources and explicitly prohibited majority-vote repair. Therefore F was classified `not_identifiable_for_endpoint` and the primary F+G cross-endpoint decision became `multi_endpoint_not_identifiable`.

The apparent typo is intentionally not repaired after row inspection.

## Provenance

The result-generating head was `51b516fd9511dc0f18c236e91a17d88453a76b06`.

- workflow run: `32801092027`
- job: `97661887837`
- derived artifact: `9546498746`
- artifact digest: `sha256:455ffe9a1c075d2c92b6e36c06cbc3c495255b241097c479628cf186af55e79b`
- Protocol invariant CI: success
- two-repository reproducibility contract: success
- Paper completion sprint: success

All four source CSV member hashes matched the schema-only lock from #104. The EIDC outer ZIPs were regenerated and therefore had different container hashes; the pre-outcome source-lock correction retained source identity at DOI/UUID + exact member path + CSV-member SHA-256.

## G_mating — array-level pollinator availability was not predictively supported

The recognized `Parentage` mapping retained **457 progeny rows across all 16 arrays**. There were 48 paternity rows whose Parentage text matched neither preregistered `self` nor `outcross` rule; they were excluded from G exactly as declared.

Equal-array held-out NLL was:

| state | NLL |
|---|---:|
| S0 — Block | 0.387347 |
| S1 — Block + pollinator count + mean ITD | 0.383796 |
| S2 — S1 + Habitat | 0.385845 |

The S0→S1 process-state gain was `0.003551`, with 95% array-bootstrap interval `[-0.006385, 0.013203]`. It did not meet the preregistered positive-support rule.

The S1→S2 Habitat gain was `-0.002049`, interval `[-0.006579, 0.001205]`, also unsupported.

Decision: **`process_state_not_predictively_supported`**.

This is not evidence that pollinators are irrelevant to mating. It says that the particular **array-level pan-trap count + mean-ITD availability state** did not add reproducible held-out information about progeny outcrossing beyond block under this closure.

## R — experimentally revealed autonomous/reproductive-assurance coordinate

The exposed/excluded source identified `R_auto` for **48 plants across all 16 arrays**.

Adding R to the G model on the R-complete subset changed held-out NLL from `0.385845` to `0.384146`. The mean S2→S3 gain was `0.001699`, interval `[-0.004095, 0.007596]`.

Decision: **`no_detected_R_gain`**.

This does not show that reproductive assurance is biologically unimportant; it did not add robust transfer prediction for this G endpoint after the fixed state terms.

## C_pollen — the same availability state was also not predictively supported

The preregistered outcross-distance endpoint retained **254 rows across all 16 arrays**.

Equal-array held-out MSE was:

| state | MSE |
|---|---:|
| S0 — Block | 1.703951 |
| S1 — Block + pollinator count + mean ITD | 1.668285 |
| S2 — S1 + Habitat | 1.726978 |

The S0→S1 process-state gain was `0.035666`, interval `[-0.123473, 0.170571]`, so it did not meet positive-support criteria.

The S1→S2 Habitat gain was **`-0.058694`**, interval **`[-0.094528, -0.028381]`**. Thus adding Habitat reproducibly worsened held-out prediction of pollen-movement distance under the fixed model.

Decision: **`process_state_not_predictively_supported`**.

The negative Habitat gain is retained as predictive harm. It is not interpreted as biological irrelevance of habitat.

## What this adds to the natural-state programme

The important result is not merely that the primary F+G test was non-identifiable. The successfully estimable G and C endpoints show a measurement boundary:

> **a variable can be mechanistically upstream and ecologically plausible without being an adequate measured process state.**

E1 Honshu–Izu used functional diversity and trait matching closely tied to realised pollen receipt. E2 Zurich used function-specific pollinator interaction states. In those systems, adding upstream geographic/urban context did not improve transfer after the proximal state was supplied.

By contrast, the Eschscholzia pollinator coordinate is an **array-level availability proxy** from pan traps. Its count + mean-ITD compression did not receive positive held-out support for either mating/outcrossing or pollen-movement distance. The framework therefore does not say "condition on any pollinator variable and geography disappears." It requires a measured state that is itself demonstrated to carry future/process-relevant information for the endpoint.

Together with the Oenothera result, the natural evidence now separates three cases:

1. a sufficiently proximal ecological state can make upstream context predictively redundant (E1/E2);
2. a missing spatial mating coordinate can remain strongly informative after pollinator access is supplied (Oenothera);
3. a coarse pollinator-availability proxy may fail to be predictively informative in the first place (Eschscholzia G/C).

## Claim ceiling

Do not claim:

- multi-endpoint Eschscholzia convergence or insufficiency from F+G, because F was non-identifiable;
- that pan-trap availability measures direct focal-plant visitation or effective pollen delivery;
- that habitat is ecologically irrelevant because adding it did not improve G and harmed C prediction;
- that reproductive assurance has no biological role because its secondary G gain was unsupported;
- a universal pollinator body-size, habitat, fragmentation or connectivity rule.

The defensible inference is about **measurement/state adequacy**, not a universal ecological effect direction.
