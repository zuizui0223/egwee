# Phase-2 SF06 materialization — 2026-09-20

## Result

SF06 (Aguilar et al. 2024 online / 2025 volume; doi:10.1093/aob/mcae076) has
been row-materialized from public Supplementary Table S1.

The accessible public source DOCX contains **426 response-labelled physical rows**. The article reports 500 hierarchical meta-analysis input effect values (312 female, 105 male, 83 pollination), so the public file is not a complete row-level representation of those reported inputs. Structural audit shows that its first Word table is header-only and the response-labelled data begin at *Calystegia*; no missing first data table can be recovered by simply scanning `tables[0]`.

The public DOCX contains:

- source physical effect rows: **426**;
- paper-reported minus public-row shortfall: **74** (=45 female + 17 male + 12 pollination);
- deduplicated source publications: **255**;
- unique plant species represented: **261**;
- female-fitness rows: **267**;
- male-fitness rows: **88**;
- pollination rows: **71**;
- exact metadata-only pollination–female-fitness paired units: **59**;
- exact habitat-fragmentation paired units before numeric eligibility: **55**;
- habitat-fragmentation paired units with unambiguous SC/SI metadata: **49**.

## Outcome-blind firewall

The Phase-2 publication universe retains publication identity, species, family,
response family, land-use factor and ecological/life-history metadata.

The numerical source-result cells `Hedges' d` and `V(d)` are deliberately
excluded from the metadata ledger. No missing A/B or otherwise absent paper-reported effect is reconstructed from article summaries, figures or aggregate counts.

The row-level metadata ledger and exact pair manifest are also frozen here so
pair construction cannot be changed after numerical outcomes are opened.

## Next operation

Screen and crosswalk the source publications for repeated same-system I/F/C
programmes and duplicates with SF01-SF05, SF07 and the existing EGWEE registry
before any new numerical extraction.
