# Deterministic interaction-sentinel impossibility — frozen evidence audit

## Question

Can a deterministic rule based only on the observed interaction/pollen-quantity evidence state reproduce the observed reproductive-function evidence state for every programme in the frozen map?

## Result

No.

Using the coarsest biologically interpretable state classes and choosing, for each interaction state, the downstream F state that minimizes disagreement:

- full frozen map: **16 programmes; minimum 5 programme mismatches**;
- strict map excluding every `no_detected_loss` and `mixed` state: **8 programmes; minimum 2 mismatches**;
- strict quantitative-only subset: **5 programmes; minimum 1 mismatch**.

Thus no deterministic lookup from interaction evidence state to reproductive-function evidence state fits even the strict quantitative-only subset perfectly.

## Leave-one-programme-out

The full frozen map remains non-deterministic after deletion of every single programme: the best possible rule still misclassifies at least four remaining programmes.

The strict mixed-tier subset also remains non-deterministic after every single-programme deletion: at least one mismatch remains.

## Interpretation

This is an alternative expression of translation non-identifiability, not an estimate of predictive error in nature.

The programme set was not sampled to estimate out-of-sample classification performance, and category frequencies must not be interpreted as prevalence. The result is structural:

> **No single deterministic translation from observed interaction state to observed reproductive-function state is compatible with all programmes in the frozen evidence map.**

## Boundary

This does not imply that interaction information is useless. A richer predictor that includes pollinator identity, compatible pollen, mating quality, resources or species traits may identify F better.

The audit only rejects **interaction quantity state alone** as a universally sufficient deterministic sentinel within the frozen evidence set.

## Machine check

- `evidence/meta_extraction/if_translation_map_v1.csv`
- `scripts/check_if_sentinel_determinism.py`
