# SF06 public Supplementary Table S1 coverage boundary — updated 2026-10-07

## Structural result

A structural audit of the exact public DOCX used by the SF06 workflows shows:

- 7 Word tables total;
- table 0: header only;
- tables 1–5: 79 response-labelled data rows each;
- table 6: 31 response-labelled data rows;
- total public physical data rows: **426**;
- parsed response rows: **267 female fitness / 88 male fitness / 71 pollination**;
- each physical row contains one Hedges-d value and one V(d)+source cell.

The article reports hierarchical-analysis input counts of **312 / 105 / 83 = 500**. The paper-minus-public-file shortfall is therefore **45 / 17 / 12 = 74** inputs.

The accessible species rows begin at *Calystegia collina* and contain no A/B taxon, consistent with a public C–Z subset rather than a skipped first data table.

## Independent public-mirror check

The Europe PMC / EMBL-EBI BioStudies mirror for accession S-EPMC11805932 exposes exactly two supplementary files:

- mcae076_suppl_supplementary_table_s1.docx — **66,368 bytes**;
- mcae076_suppl_supplementary_tables_s2_s3_figures_s1_s2.docx — 2,656,075 bytes.

The mirrored S1 file has the same size as the publisher file used by EGWEE. No alternate complete 500-input data file is exposed in that public study package.

Thus the 74 missing hierarchical inputs are currently a **public-source coverage boundary**, not a recoverable parser omission.

## Sign-column correction

A later raw-column audit confirmed that negative Hedges-d values are encoded with spaces between sign and magnitude, for example `- 1.733`.

The first numerical parser dropped those spaced minus signs. Its negative compatibility coefficient and zero-mismatch topology are therefore retained only as **invalidated implementation outputs**, not as biological results.

Commit `800ccfa` corrected the sign parser. The corrected public-S1 analysis is authoritative for the accessible 426-row subset.

## Corrected external result

Within the accessible public-S1 habitat-fragmentation pairs:

- 54 constituent-consensus sign pairs are usable;
- minimum deterministic mismatches = 12;
- publication-LOO minimum = 8;
- species-LOO minimum = 11.

After deleting all publications overlapping the frozen EGWEE I–F map:

- 31 consensus pairs remain;
- minimum mismatches = 7;
- publication-LOO minimum = 5;
- species-LOO minimum = 6.

## Consequence

SF06 provides a robust **public-supplement subset** external generalization, but cannot certify the complete 500-input source database.

Missing inputs are not reconstructed from aggregate article statistics, figures or alphabetical inference.

## Claim ceiling

Allowed:

- complete analysis of all response-labelled rows present in the accessible public S1 DOCX;
- robust external generalization within that public subset;
- explicit reporting of the 74-input source-coverage shortfall.

Not allowed:

- claim that 426 rows reproduce all 500 hierarchical inputs;
- impute the 74 absent inputs;
- call the public-subset result a complete SF06 replication;
- cite the invalidated sign-loss outputs as biology.
