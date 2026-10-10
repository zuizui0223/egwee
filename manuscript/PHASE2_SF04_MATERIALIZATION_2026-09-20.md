# Phase-2 SF04 materialization — 2026-09-20

## Result

SF04 (González et al. 2019; doi:10.1111/cobi.13422) has been row-materialized
from the public Figshare dataset `10.6084/m9.figshare.7520456.v1`.

The public files contain:

- allelic-richness case rows: **42**;
- expected-heterozygosity case rows: **50**;
- total source case rows: **92**;
- deduplicated source publications: **38**;
- unique plant species represented: **38**.

All **38** references in `references.txt` are represented in the materialized
case files.

## Outcome-blind firewall

The publication universe retains only source identity and prespecified screening
metadata:

- species;
- molecular method;
- disturbance class;
- latitude;
- life form;
- lifespan;
- reproductive system;
- origin;
- whether the source appears in allelic-richness, expected-heterozygosity, or both streams.

It deliberately excludes all treatment/control outcome columns:

- `Xe`, `Se`, `Ne`;
- `Xc`, `Sc`, `Nc`.

No new EGWEE effect magnitude is opened by this operation.

## Next operation

Screen the 38 source publications by title/abstract/methods for same-system
`G_adult` overlap with contemporary process/function layers, crosswalk duplicates
against SF01-SF07 and existing EGWEE programme IDs, and only then open numerical
effects for candidates that pass the fixed independent-unit and exposure gates.
