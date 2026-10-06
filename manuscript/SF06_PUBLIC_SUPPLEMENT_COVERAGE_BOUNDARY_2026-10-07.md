# SF06 public Supplementary Table S1 coverage boundary — 2026-10-07

## Result

A structural audit of the exact public DOCX used by the SF06 workflows shows:

- 7 Word tables total;
- table 0: header only (2 nonempty rows, no response-labelled data);
- tables 1–5: 79 response-labelled data rows each;
- table 6: 31 response-labelled data rows;
- total public physical data rows: **426**;
- parsed response rows: **267 female fitness / 88 male fitness / 71 pollination**;
- each physical row has exactly one numeric effect token in the Hedges-d cell.

The article reports hierarchical-analysis input counts of **312 / 105 / 83 = 500**. The paper-minus-public-file shortfall is therefore **45 / 17 / 12 = 74** inputs.

The public materialized species range begins at *Calystegia collina* and ends at *Ziziphus lotus*; no A/B taxon occurs in the accessible parsed S1 data rows. This strongly indicates that the public DOCX is a C–Z subset relative to the complete analysis database rather than that EGWEE skipped a recoverable first data table.

## Consequence

The earlier 500-physical-row assertion is withdrawn.

SF06 can still be used as an external **public-supplement subset** test, but it cannot certify the complete 500-input source database. Missing inputs are not reconstructed from aggregate article statistics or figures.

The first 426-row numerical exposure is retained, including its inconvenient negative compatibility estimate and zero-mismatch preliminary topology. It is not erased or reclassified as a null merely because the public source is incomplete. The current implementation must rerun the same accessible public file under the frozen source hash, exact pair universe, publication normalization and current consensus-sign rules.

## Claim ceiling

Allowed:
- complete analysis of all response-labelled rows present in the accessible public S1 DOCX;
- comparison of public-S1 results with the published aggregate coupling;
- public-subset external support or failure of support.

Not allowed:
- claim that 426 rows reproduce all 500 hierarchical inputs;
- impute the 74 absent inputs;
- call a public-subset result a complete SF06 replication;
- hide the preliminary negative result.
