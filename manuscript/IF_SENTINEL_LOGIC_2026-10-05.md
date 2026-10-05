# Interaction sentinel logic — generality and surprise audit (2026-10-05)

## Core question

Can fragmentation-driven change in interaction / pollinator quantity serve as a stand-alone sentinel for reproductive-function change?

## General result: no one-dimensional translation

The frozen 16-programme interaction→function map rejects a one-dimensional deterministic sentinel.

Logical counterexamples occur in both directions:

- **interaction decline is not sufficient for reproductive decline**: lower interaction occurs with lower F, higher F point estimates, and no detected F loss;
- **interaction decline is not necessary for reproductive decline**: lower F occurs when interaction is lower, higher, or has no detected loss;
- **apparently intact/elevated interaction does not guarantee intact function**: Wandoo and Hulting provide different forms of this failure.

This is not merely produced by ambiguous categories. After removing every `no_detected_loss` and `mixed` programme state, the strict subset still contains:

- interaction lower → F lower or higher;
- interaction higher/shifted → F lower or similar.

Thus the scale-stable ecological principle is **non-monotonic process→function translation**, not a fixed downstream rule.

## Stronger structural statement

The best deterministic lookup from interaction evidence state to F evidence state cannot fit the frozen programme set perfectly:

- full map: 16 programmes, minimum 5 mismatches;
- strict category map: 8 programmes, minimum 2 mismatches;
- strict quantitative-only subset: 5 programmes, minimum 1 mismatch.

The full and strict mixed-tier maps remain non-deterministic after every single-programme deletion.

These mismatch counts are **not prediction-error estimates or prevalence estimates**. They certify only that interaction state alone is insufficient to determine F state in the observed programme map.

## Surprising high-confidence asymmetry: false reassurance

The broader map contains both false-reassurance and apparent-over-warning / buffering geometries. However, the strongest representation-stable **resolved quantitative** mismatches are one-sided:

1. *Eucalyptus wandoo* — interaction/pollen quantity positive, seed production negative;
2. *Cardiopetalum calophyllum* — interaction weakly negative, fruit set much more negative;
3. Kakamega *Acanthopale pubescens* — visitation maintained/slightly positive, fruit set strongly negative; the mismatch survives g→lnRR re-expression.

These three programmes span three continents, three plant families, different growth forms and different pollination/mating systems.

No current quantitatively admitted I–F programme provides an equally representation-stable resolved reverse mismatch in which interaction quantity is more negatively affected than F.

This asymmetry is descriptive. It is **not** a 3/3 sign test and does not estimate how often false reassurance occurs in nature.

## Why this is ecologically important

A monitoring programme that measures interaction quantity alone can fail in two logically distinct ways:

- **false reassurance**: interaction looks intact or comparatively buffered while reproductive function is worse;
- **false alarm / over-warning**: interaction declines while reproductive function is buffered, similar, or higher.

The first failure mode is the strongest resolved quantitative pattern in the current corpus. The second is clearly present in the broader frozen evidence map but is less strongly resolved quantitatively.

Therefore interaction quantity is not merely a noisy predictor. It is a **non-identifying sentinel** unless additional biological state is supplied.

## Missing state suggested by the corpus

The complete quantitative I–F set has:

- quantity-level interaction endpoints: 8/8 programmes;
- direct effective-mating-quality endpoints on the same I–F frame: 0/8.

The missing state lies exactly between interaction quantity and reproduction:

`interaction quantity → effective mating / compatible pollen → reproductive function`.

Candidate dimensions include:

- pollinator identity / per-visit effectiveness;
- compatible versus self pollen;
- realised pollen-donor diversity;
- reproductive assurance / wind pollination;
- post-pollination filtering;
- direct resource or landscape effects on fruit/seed development.

## Novelty boundary

Already known:

- visitation can be a poor proxy for pollination effectiveness;
- pollen quantity and pollen quality differ;
- response and effect variables need not coincide;
- individual fragmentation studies can show visitation–reproduction decoupling.

What this synthesis adds is narrower:

> a frozen cross-programme **translation audit** showing that interaction state alone cannot deterministically identify reproductive state across matched fragmentation programmes, together with three representation-stable resolved false-reassurance anchors.

This is a fragmentation-specific empirical generalization, not a new response–effect theory.

## Claim ceiling

Allowed:

- interaction decline is neither necessary nor sufficient for reproductive decline in the frozen evidence map;
- the many-to-many interaction→function translation survives conservative category removal;
- deterministic interaction-only sentinel rules fail in the frozen map and remain non-deterministic under leave-one-programme-out for the full/strict mixed-tier maps;
- the strongest resolved quantitative proxy failures are false-reassurance cases;
- interaction quantity alone is insufficient to diagnose reproductive function across the audited programmes.

Not allowed:

- the 16 programmes estimate global proxy-failure prevalence;
- the minimum deterministic mismatch count is an out-of-sample error rate;
- false reassurance is universally more common than false alarm;
- all pollinator monitoring is uninformative;
- one hidden mechanism explains all mismatches.

## Machine checks

- `scripts/check_if_translation_map.py`
- `scripts/check_if_translation_category_sensitivity.py`
- `scripts/check_if_sentinel_determinism.py`
- `scripts/check_if_necessity_sufficiency.py`
- `evidence/meta_extraction/if_translation_map_v1.csv`
