# Phase-2 CF01 seed work identity audit — 2026-09-23

## Why this ledger exists

The 363-row CF01 seed manifest is a frozen **search-seed manifest**, not an assumption that all
363 rows are distinct publications.

Bibliographic resolution is allowed to reveal that two or more seed records point to the same
publication. Those records keep their source provenance but the shared publication is expanded
through the citation graph once.

## Current bibliographic identity state

- manifest seed rows: **363**;
- resolved seed rows: **296**;
- unique resolved OpenAlex works: **292**;
- resolved-work duplicate groups: **4**;
- duplicate excess seed rows: **4**;
- unresolved seed rows: **67**;
- provisional work-level units: **359**.

The provisional work-level denominator equals unique resolved works plus each unresolved seed
retained separately. It is not final until the unresolved bibliographic identities are
adjudicated.

## Citation-expansion rule

For a duplicate resolved-work group:

- fetch backward references once;
- query forward citations once;
- attach every originating seed ID as provenance to discovered candidate edges;
- never count duplicate seed records as independent ecological programmes.

No effect outcome is opened by this identity audit.
