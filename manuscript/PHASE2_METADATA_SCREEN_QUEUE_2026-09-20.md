# Phase-2 metadata screening queue — 2026-09-20

## Current denominator

The resolved cross-frame ledger contains **351 canonical publication identities** across the currently materialized SF04/SF05/SF06 frames.

- already linked to existing EGWEE programmes: **11**;
- unresolved identities: **340**;
- unresolved identities with at least two metadata-level biological layers: **60**.

No effect direction, Hedges d, variance, p-value or significance field is used in this queue.

## Primary I-F screen

Current direct I-F coverage remains **1/5** (ML020 only), so the first design-screening lane is the prespecified I-F family.

Among unresolved identities:

- metadata indicate both pollination/interaction (I) and reproductive fitness (F): **36**;
- source land-use metadata explicitly identify habitat fragmentation: **32**;
- I+F records attributed only to agriculture/urbanization rather than fragmentation: **4** and are not in the primary fragmentation queue.

The 32-record queue is stored in
`evidence/meta_extraction/phase2_if_fragmentation_screen_queue_v1.csv`.

Each record must pass the same design gate before quantitative extraction:

1. fragmentation exposure is source-defined rather than inferred from the response;
2. I and F share the same exposure frame;
3. fragmentation-level independent units are recoverable;
4. nested flowers/plants/visits/fruits are not promoted to independent fragmentation replicates;
5. programme duplication is resolved before effect calculation.

## Other unresolved metadata geometry

- other multilayer hints outside the immediate I-F queue: **24**;
- single-layer/no-pair immediate hints: **280**.

They remain in the systematic universe and are not discarded. The I-F lane is processed first because its preregistered pair coverage is currently the sparsest opened target, not because any candidate result is favorable.

## Next executable operation

Run title/abstract/method design screening on the 32 I-F fragmentation identities. Close candidates on exposure or independent-unit geometry before opening numerical effects; advance only designs that can support a same-system I-F contrast.
