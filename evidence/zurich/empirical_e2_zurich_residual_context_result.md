# E2 result — Zurich urban residual-context test

## Decision

**All six preregistered reproductive endpoints: `no_detected_residual_urban_information`.**

This is the result of the one-shot EnviDat/BetterBlooms analysis declared in `empirical_e2_zurich_residual_context_preregistration.md`. The test asks whether source-defined urban/local habitat context adds held-out predictive information after the function-specific pollinator interaction state is supplied.

The result does **not** prove ecological equivalence or that urban context is biologically irrelevant. The permitted statement is narrower: under the locked garden-holdout design and source-defined predictor families, no reproductive endpoint showed a reproducible positive held-out gain from adding `PlantS + Urban_500 + PlantS×Urban_500` after the interaction state.

## Locked comparison

For every focal reproductive function:

- `S1`: source-defined pollinator-guild interaction state only;
- `S2`: `S1 + PlantS + Urban_500 + PlantS×Urban_500`;
- validation: hold out whole gardens;
- primary score: held-out negative log predictive likelihood;
- `Delta_g = NLL(S1) - NLL(S2)`, so **positive** values favour residual urban/context information;
- `ecological_partial_state_incomplete` required mean `Delta_g > 0` with a garden-bootstrap 95% interval wholly above zero.

No endpoint met that rule.

## Endpoint results

| endpoint | mean `Delta_g` | garden-bootstrap 95% interval | decision |
|---|---:|---:|---|
| carrot / *Daucus* seed set | -3.1047 | [-6.1169, -0.7893] | no detected residual urban information; context addition worsened held-out prediction |
| radish / *Raphanus* fruit set | +0.00027 | [-0.00357, +0.00376] | no detected residual urban information |
| radish / *Raphanus* seed set | -0.00543 | [-0.01039, -0.00094] | no detected residual urban information; context addition worsened held-out prediction |
| sainfoin / *Onobrychis* fruit set | -0.00315 | [-0.01608, +0.00941] | no detected residual urban information |
| comfrey / *Symphytum* fruit set | +0.00838 | [-0.00726, +0.02333] | no detected residual urban information |
| comfrey / *Symphytum* seed set | -0.00014 | [-0.00069, +0.00034] | no detected residual urban information |

Decision count: **6/6 `no_detected_residual_urban_information`; 0/6 `ecological_partial_state_incomplete`.**

Two endpoints (*Daucus* seed set and *Raphanus* seed set) had bootstrap intervals wholly below zero, meaning the larger context-augmented model predicted held-out gardens worse under this fixed design. The other four intervals included zero.

## Ecological interpretation

This result sharpens the earlier secondary Zurich audit. The stored source coefficients showed that `Urban_500` effects differed among focal reproductive functions. The direct open-data test now asks a different question: after giving the model the function-specific pollinator interaction state, does the urban/local context layer transfer to unseen gardens?

Under the preregistered test, **no** endpoint showed reproducible added predictive information from that context layer. Thus a single urban-intensity axis is not recovered as a portable residual functional-state coordinate in this design.

But this is not proof that `S1` is a sufficient ecological state. Interaction-only prediction is itself imperfect and is not uniformly superior to the context-only comparator. Missing variables can include pollinator effectiveness, floral phenotype, microclimate, phenology, natural plant genetics/mating state, partner movement, or ecological memory. The correct conclusion is therefore **absence of detected residual urban information after the measured interaction state**, not full state sufficiency.

## Connection to the cross-system hypothesis

Zurich supplies a within-city empirical falsification test of the broader convergence logic:

`future/reproductive function ⟂ urban context | measured interaction state`

The current data fail to detect a reproducible violation of that conditional-independence target across all six fixed functions. The stronger urban–island claim still requires matched eco-genetic state variables and independent systems; Zurich intentionally lacks natural focal-plant `G/C/R/M` because the phytometers are standardized.

## Provenance

- EnviDat dataset: `10.16904/envidat.676`;
- source resource SHA-256: `b1ea0dc54d0c6e33bfacb44d7285377ec3e113807cc945fc2dfbfcc3e534bcc9`;
- BetterBlooms repository commit: `d6361f6874398e797322afe07a8fea85a3c7e927`;
- workflow run: `32701131992`;
- Actions artifact: `9511364032`;
- artifact digest: `sha256:7023a893fc63777790d1fc885f9adb62a5c80d74deae968619bce0df77313ed0`;
- bootstrap replicates: 10,000;
- bootstrap seed: `20260824`.

No third-party raw data are committed to this repository.
