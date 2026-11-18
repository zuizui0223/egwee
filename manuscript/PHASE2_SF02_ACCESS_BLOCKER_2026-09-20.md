# Phase-2 SF02 access blocker — 2026-09-20

## Result

SF02 (Aguilar et al. 2008; doi:10.1111/j.1365-294X.2008.03971.x) is source-verified at the article and Supporting Information metadata level, but Appendix S1 cannot currently be downloaded reproducibly in GitHub Actions.

The source article fixes the denominator at **101 publications / 102 unique plant species** and identifies `MEC_3971_sm_AppendixS1.doc` as the complete reference list.

## Failure diagnosis

Two legitimate public download attempts were made.

1. Direct Wiley `action/downloadSupplement` request for Appendix S1 returned HTTP 403.
2. A second request first loaded the public article page, retained Wiley cookies, supplied the article as Referer, and used a normal browser User-Agent. The Appendix S1 request still returned HTTP 403.

The article HTML itself is reachable. The failure is specific to the supplement-download layer.

## Scientific firewall

No 101-study bibliography is reconstructed from partial article references, search-engine snippets, or inferred citations.

No genetic-effect values are opened.

The source frame is therefore not marked row-materialized.

## Current status

`source_verified_appendix_row_materialization_blocked_by_wiley_download_access`

## Next action

Keep SF02 in the declared source universe and revisit only through a stable publisher supplement route or another legitimate complete copy of Appendix S1. Continue current Phase-2 work using source frames that are reproducibly materialized.
