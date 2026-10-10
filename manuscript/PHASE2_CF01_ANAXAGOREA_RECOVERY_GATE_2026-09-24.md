# CFTQ0165 Anaxagorea direct I-F recovery gate — 2026-09-24

## Frozen target

Programme: `P2_CF01_ANAXAGOREA_2012`.

The frozen retrospective contract requires one six-fragment frame:

- 3 large fragments;
- 3 small fragments;
- I = fragment-level pollinator abundance per flower;
- F = fragment-level fruit set, fruits per flower.

Independent unit = forest fragment.

## Full-text audit

The source Table 1 does provide six-fragment values for:

- fragment size;
- pollinators per flower;
- mature fruits per tree;
- monocarps per fruit;
- visitation rate.

However, the frozen primary F is **fruit set per flower**, not mature fruits per tree.

The source's flower-level pollinator + fruit-set follow-up is incomplete at the fragment level:
the article explicitly states that only fragments **A, B and D** yielded sufficient joint data for a
direct comparison of flower visitation against fruit and seed set.

Therefore the public source does not provide the frozen F endpoint on the same six-fragment frame
as the fragment-size I contrast.

## Decision

Status: **design-valid, quantitatively blocked by common six-fragment F effect-unit recovery**.

Direct I-F programme increment: **0**.

This is not an ecological null and is not a decision based on the published non-significant
large-versus-small result.

## Why mature fruits per tree is not substituted

Table 1 mature fruits per tree is a legitimate reproductive quantity, but substituting it now would
change the frozen F estimand after full-text values are visible.

That endpoint can remain descriptive process evidence, but it cannot rescue the registered
direct-I-F programme.

## No rescue

Do not:

- replace frozen fruit set per flower with mature fruits per tree after inspection;
- construct six fragment-level fruit-set values from flower-level pooled data that the source itself
  did not report;
- use 186 or 209 flowers as fragmentation n;
- use only A/B/D and relabel the study as a 2-large-versus-1-small direct contrast;
- digitize figures or reverse-engineer nested-model coefficients.

Reopen only if an authoritative source or author-provided dataset exposes fragment-level fruit set
per flower for all six source fragments.
