# CF01 candidate screening contract — 2026-09-23

## Scope

This contract governs outcome-blind screening of new candidate works discovered by the frozen
CF01 backward/forward citation expansion through 2026-09-18.

It is frozen before any newly discovered candidate effect magnitude is opened.

## Candidate universe

A work enters ecological screening only after:

1. bibliographic resolution of its source seed;
2. citation-graph discovery through the uniform CF01 route;
3. publication date on or before the frozen cutoff;
4. removal/linkage of exact existing-seed identities by OpenAlex ID, DOI, or title + year;
5. adjudication of possible collisions with still-unresolved seed identities.

The screening denominator is the resulting candidate queue, not a subset chosen by search-engine
ranking or apparent result strength.

## Title/abstract screen

A candidate advances to full-text methods screening when title/abstract metadata support all of:

- a flowering-plant population, community, or reproductive system relevant to EGWEE;
- habitat fragmentation, habitat loss, remnant/patch isolation, connectivity, edge, habitat amount,
  or a source-defined fragmentation treatment/gradient;
- at least one plausible prespecified EGWEE biological layer.

When title/abstract information is insufficient, the record advances to full-text clarification.
Ambiguity is not an exclusion criterion.

## Layer hints

Layer assignment remains fixed to the Phase-2 definitions.

- I — pollinator/visitor abundance, visitation, pollination service, pollen limitation or another
  direct plant–pollinator interaction measure.
- C — pollen/seed movement, gene flow, paternity/parentage, immigration or directly estimated
  dispersal/connectivity.
- F — fruit set, seed set/production, fecundity, direct reproductive success or direct progeny
  performance.
- G_adult — adult standing genetic diversity/structure state.
- G_offspring — seed/embryo/seedling/juvenile genetic state.

Mating-system quantities are not automatically F. Seed/offspring genetic samples are not
automatically reproductive function. Genetic inference of dispersal is C only when it estimates
movement/connectivity rather than merely standing structure.

## Full-text design gate

A work can advance from full text to numerical extraction only when:

1. fragmentation exposure is source-defined;
2. the fragmentation-level independent unit is recoverable;
3. the target endpoint and its uncertainty can be reconstructed at that independent-unit level;
4. nested flowers, plants, fruits, seeds, offspring, loci, repeated visits or paternity events are
   not promoted to independent fragmentation replicates;
5. linked publications/campaigns are assigned one programme identity before effect calculation;
6. for a pair-specific analysis, both layers share the required exposure frame;
7. endpoint-to-layer assignment is fixed before calculating the candidate effect.

Gradient studies remain eligible for the registered gradient/generalisation stream but are not
converted into binary fragmented/reference contrasts by an outcome-informed threshold.

## Permitted screen decisions

- advance_full_text_design_screen
- advance_quantitative_recovery
- retain_gradient_or_moderator_stream
- link_existing_programme
- pending_identity_adjudication
- close_nonplant_or_wrong_biological_system
- close_no_fragmentation_exposure
- close_no_eligible_EGWEE_layer
- close_no_common_pair_frame
- close_independent_unit_not_recoverable
- close_duplicate_publication

A title/abstract exclusion must state the concrete design/biological reason. A full-text closure
must state the failed admission condition.

## Forbidden inputs

The following must not affect screening, queue order after the deterministic metadata triage, or
admission:

- effect direction;
- effect magnitude;
- p-value or confidence-interval significance;
- whether the source authors describe the result as significant;
- whether the result would increase or decrease an existing EGWEE pooled estimate;
- whether admitting the study would move a pair family closer to the five-programme analysis gate;
- whether it would improve the frozen Phase-1 Fisher result.

## Stopping rule

CF01 is complete only when every resolved seed has been expanded through the frozen cutoff, all
discovered candidate identities have been deduplicated/adjudicated, and every cutoff-eligible
candidate has a documented title/abstract/method decision.

Search completion, not statistical significance and not reaching K=5 in another pair family, is
the stopping condition.
