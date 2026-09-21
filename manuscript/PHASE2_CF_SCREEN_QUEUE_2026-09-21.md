# Phase-2 C-F screening queue — 2026-09-21

## Current state

Direct `C-F` coverage is **2/5** (ML001 + ML002).

The currently materialized cross-frame ledger does not contain an unresolved
identity already tagged with both C and F. Therefore the next outcome-blind
screen starts from SF05 records whose bibliographic/title-method metadata
independently indicate a movement/connectivity (`C`) layer.

After removing records already linked to existing EGWEE programmes, **17
publication identities** remain.

## Screening rule

A candidate can advance only if title/abstract/method information establishes:

1. a source-defined fragmentation exposure;
2. a reproductive-function (`F`) endpoint in the same programme;
3. C and F share the relevant fragmentation exposure;
4. fragmentation-level independent units are recoverable;
5. no lower-level tree, offspring, locus or paternity event is promoted to an
   independent fragmentation replicate.

Effect direction, magnitude, significance and source-meta-analysis result are
not screening inputs.

Machine-readable queue:
`evidence/meta_extraction/phase2_cf_fragmentation_screen_queue_v1.csv`.

## Next operation

Screen the 17 identities for same-programme C + F geometry. Close records that
contain C but no reproductive function before any numerical effect is opened.
