# EGWEE meta-analysis Phase 2 status — 2026-09-17

## Current scientific state

The five-cluster Journal of Ecology manuscript remains frozen as the Phase-1 publication state. Phase 2 is a separately governed development programme for systematic coverage and moderator inference.

Phase 2 is **not** a significance-repair search and does not reopen the Phase-1 Fisher result as an optimization target.

## Completed before new outcome opening

1. Frozen Phase-1 reference values and scientific-base commit.
2. Registered eight systematic source frames (`SF01`–`SF07`, `CF01`).
3. Frozen paired layer-difference estimands: `I-F`, `C-F`, `G_adult-G_offspring`, and `G_adult-mean(I,F)` where jointly estimable.
4. Frozen moderator coding for mating system, reproductive assurance, pollination vector, woodiness/life form, fragmentation age/component, process-measurement type, biome/region and design.
5. Frozen model-opening gates: 10 independent clusters for univariable moderators, >=4 per categorical level, 20 clusters for multivariable models and >=10 clusters per moderator degree of freedom.
6. Reclassified the ten existing closed cluster attempts by coverage value rather than expected outcome.
7. Retained ML009 and ML013 as structural non-identifiability failures.
8. Added a machine-readable Phase-2 contract and fail-closed CI check.

## Recovery priorities fixed before reopening outcomes

### P1

- ML006 *Primula elatior* — common-frame I/F/G_adult coverage.
- ML007 replicated multi-species fragmentation experiment — D/I/F.
- ML008 *Tillandsia* — independent direct I/F replication.
- ML012 *Dieffenbachia* — direct C/G_mating coverage.

### P2

- ML010 *Penstemon hirsutus* — C/G_offspring gradient.
- ML004 *Conospermum undulatum* 2020 — I/F gradient.
- ML005 *Conospermum undulatum* 2026 — C/G_offspring gradient.
- ML011 *Magnolia stellata* — C/F gradient.

### Structural hard stop

- ML009 *Pistacia lentiscus*.
- ML013 *Swietenia humilis*.

These priorities describe information gain only. They do not encode expected significance or direction.

## Next active task

Materialise the primary-study lists from the predefined systematic source frames, deduplicate them to programme/study/species/campaign records, and perform outcome-blind first-pass multilayer tagging before opening new numeric effects.

The first execution tranche should prioritize source frames with structured/public study indexes (`SF03`, `SF04`, `SF05`, `SF06`, `SF07`) because they can enlarge the candidate universe reproducibly without selecting studies by known layer-separation outcomes.

## Promotion boundary

The current Journal of Ecology submission manuscript is not replaced merely because Phase 2 starts. Promotion requires completion of the systematic frame plus at least one frozen information condition in `meta_analysis_phase2_contract.json`. A smaller p-value is neither necessary nor sufficient for promotion.
