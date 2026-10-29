# Interaction–function translation category sensitivity — 2026-10-05

## Question

Does the 16-programme translation non-identifiability result depend on the categories `no_detected_loss` or `mixed`?

## Conservative sensitivity

We removed every programme whose programme-level interaction or reproductive-function state was coded as either:

- `no_detected_loss`; or
- `mixed`.

The remaining strict subset contains **8 independent programmes** with explicit directional/source states only:

- interaction lower → function lower or higher;
- interaction higher/shifted → function lower or similar.

Thus both retained interaction states still map to more than one reproductive-function state.

## Leave-one-programme-out result

The strict-category map remains non-identifying after deleting every single programme. At least one interaction state retains more than one downstream function state after every deletion.

This sensitivity removes the two category types most vulnerable to misreading:

- `no_detected_loss` is not treated as a true zero;
- within-programme `mixed` states do not generate the result.

## Boundary

This does **not** turn the map into a prevalence estimate or a homogeneous quantitative meta-analysis.

Some remaining states are still point-estimate or source-reported qualitative states. The result is therefore an existence/topology statement:

> **The observed many-to-many interaction→function translation is not an artefact of the no-detected-loss or mixed categories.**

## Machine check

- `evidence/meta_extraction/if_translation_map_v1.csv`
- `scripts/check_if_translation_category_sensitivity.py`
