# Interaction–function translation: interaction-metric sensitivity — 2026-10-05

## Question

Could the frozen many-to-many interaction→function map be an artefact of combining biologically different upstream measurements such as visitation/abundance and pollen-tube quantity?

## Frozen metric classification

The 16-programme translation map was classified from source-defined interaction endpoints before this sensitivity was evaluated.

- visitation / abundance / interaction-rate programmes: **13**;
- pollen-quantity programmes: **2** (Chaco, Wandoo);
- source-level pollination measure not reduced to visitation: **1** (Lithraea).

## Visitation/abundance-only result

Restricting the map to the **13 visitation/abundance programmes** does not restore a one-to-one translation.

Within this metric-homogeneous subset:

- lower visitation/abundance occurs with F lower, F higher as a point state, and no detected F loss;
- no detected visitation loss occurs with F lower or no detected F loss.

Thus at least two upstream visitation states remain compatible with multiple downstream reproductive-function states.

## Leave-one-programme-out

The visitation-only map remains non-identifying after deletion of every single programme: after each deletion, at least one interaction state still maps to more than one F state.

This directly rules out the simplest measurement-heterogeneity objection:

> **The frozen translation non-identifiability is not created solely by mixing visitation/abundance with pollen-quantity endpoints.**

## Conservative explicit-direction sensitivity

Removing every programme state coded `mixed` or `no_detected_loss` leaves six visitation/abundance programmes with explicit directional states.

In that strict subset:

- interaction lower → F lower or higher;
- interaction higher → F similar.

The lower→multiple-F ambiguity is therefore still present, but it is carried by the common-milkweed higher-F point estimate. Removing milkweed leaves lower interaction mapping only to lower F in this strict subset.

Accordingly, the strongest leave-one-programme-out claim belongs to the broader visitation-only map, not to the strict explicit-direction subset.

## Ecological implication

The broad result is not simply 'different pollination metrics disagree'. Even when the upstream indicator is restricted to visitation/abundance-type measurements, the same observed interaction response can correspond to different reproductive-function states.

This strengthens the monitoring interpretation:

> **Visitation/abundance alone is a non-identifying stand-alone sentinel of reproductive function across the frozen fragmentation evidence map.**

## Claim ceiling

Allowed:

- 13 visitation/abundance programmes form a metric-homogeneous sensitivity subset;
- visitation-only interaction→function translation remains many-to-many;
- the visitation-only non-identifiability result survives every single-programme deletion;
- the strict explicit-direction subset remains non-identifying before milkweed deletion;
- metric heterogeneity is not sufficient to explain the full translation result.

Not allowed:

- all visitation metrics are biologically equivalent;
- the 13 programmes estimate an error rate or prevalence;
- the strict explicit-direction ambiguity is leave-one-programme-out robust;
- pollen-quantity measures are irrelevant;
- one hidden mechanism explains the visitation-only mismatches.

## Machine-readable implementation

- `evidence/meta_extraction/if_interaction_metric_class_v1.csv`
- `scripts/check_if_interaction_metric_sensitivity.py`
- `evidence/meta_extraction/if_translation_map_v1.csv`
