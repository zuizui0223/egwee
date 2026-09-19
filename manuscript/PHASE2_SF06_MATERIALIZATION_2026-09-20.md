# Phase-2 SF06 materialization — 2026-09-20

## Result

SF06 (Aguilar et al. 2024 online / 2025 volume; doi:10.1093/aob/mcae076) has
been row-materialized from public Supplementary Table S1.

The source DOCX contains:

- source effect rows: **426**;
- deduplicated source publications: **255**;
- unique plant species represented: **261**;
- female-fitness rows: **267**;
- male-fitness rows: **88**;
- pollination rows: **71**.

## Outcome-blind firewall

The Phase-2 publication universe retains publication identity, species, family,
response family, land-use factor and ecological/life-history metadata.

The numerical source-result cells `Hedges' d` and `V(d)` are deliberately
excluded from the materialized ledger. No new EGWEE effect magnitude is opened.

## Next operation

Screen and crosswalk the source publications for repeated same-system I/F/C
programmes and duplicates with SF01-SF05, SF07 and the existing EGWEE registry
before any new numerical extraction.
