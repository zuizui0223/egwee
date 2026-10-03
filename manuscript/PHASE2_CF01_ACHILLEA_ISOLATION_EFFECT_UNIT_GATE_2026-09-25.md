# CFTQ0283 Achillea isolation I-F effect-unit gate — 2026-09-25

## Programme

`P2_CF01_ACHILLEA_ISOLATION_2002`.

The source experimentally compares *Achillea millefolium* transplanted to isolated and non-isolated
Stockholm-archipelago islands while holding resource availability, population size and
inter-individual spacing constant.

Direct responses include pollen deposition and fecundity.

## Effect-unit rule

Independent fragmentation unit = **island**.

Transplanted individuals, flowers, seeds and germination observations are nested below island.

The current public source surface does not expose the number/identity of independent islands per
condition or island-level response dispersion. Therefore attaching the number of transplanted
individuals to a fragmented-vs-reference Hedges-g variance would be pseudoreplication.

## Decision

Status:
`blocked_island_replicate_count_and_fragment_level_IF_variance_not_publicly_recoverable`.

This is an effect-unit/access stop, not an ecological null. The reported lack of an isolation effect
does not establish equivalence.

## Reopen only if

An authoritative source provides:

- independent isolated and non-isolated island counts/identities;
- island-level pollen-deposition summaries or a valid island-level marginal effect;
- island-level fecundity summaries or a valid island-level marginal effect.

Do not use individual transplants as island n or set unknown I-F covariance to zero.
