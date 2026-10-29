# SF05 outcome-excluded identity recovery audit — 2026-09-23

## Question

Can the minimum nine SF05 identities excluded by the source on outcome-related grounds be
recovered directly from the public Supporting Table S1 workbook?

## Public workbook audit

The public file `plad019_suppl_supplementary_table_s1.xlsx` was previously materialized by
reading every workbook sheet through the raw XLSX XML, without spreadsheet recalculation.

The workbook contains exactly six sheets:

1. `meta.references` — 32 rows including header; 31 deduplicated meta-analysis citations;
2. `sys.rev` — 178 rows including header; 177 population rows from 65 source-selected papers;
3. `sys.rev-meta.only` — 117 rows including header;
4. `meta-complete` — 44 rows including header;
5. `meta-outcross` — 35 rows including header;
6. `meta-tree.outcross` — 24 rows including header.

All sheets are the published 65-paper systematic-review subset or downstream meta-analysis
subsets. There is no public workbook sheet containing the **74 studies before the source removed
six non-significant-FSGS studies and three outlier-Sp studies**.

The materializer iterates all worksheet rows present in the XLSX XML, so ordinary hidden/filter
display state would not make those nine records disappear from the extracted matrices if they
were actually present as rows.

## Consequence

The nine source-outcome-excluded identities cannot be legitimately reconstructed from
Supporting Table S1 alone.

Do **not**:

- guess their identities from the final 65 studies;
- infer them from effect-size direction;
- treat the nine missing studies as biological zeros;
- relax the SF05 denominator warning.

The registered recovery route is instead the broader outcome-blind bibliographic programme:

1. CF01 backward/forward expansion of the frozen search-seed manifest;
2. reproducible bibliographic resolution of newly discovered records;
3. title/abstract/method screening under the frozen fragmentation/layer contract;
4. crosswalk any recovered records back to the SF05 pre-exclusion gap where identity can be
   established independently of outcome.

Until such identities are independently recovered, SF05 remains
`incomplete_outcome_blind_source_frame`.
