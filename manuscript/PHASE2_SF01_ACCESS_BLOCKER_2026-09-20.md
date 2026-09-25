# Phase-2 SF01 access blocker — 2026-09-20

## Result

SF01 (Aguilar et al. 2006; doi:10.1111/j.1461-0248.2006.00927.x) is source-verified at the article/supporting-table metadata level, but its row materialization is currently blocked by public data-object resolution.

The source metadata identifies Supporting Table S1 as a 93-row table containing 89 plant species and source-publication information. The historical KNB/DataONE package also identifies the data object as `bowdish.796.1`.

## Failure diagnosis

Three reproducible download routes were tested in GitHub Actions.

1. KNB DataONE member-node object URL:
   - `/knb/d1/mn/v2/object/bowdish.796.1`
   - returned HTTP 404.

2. Historical KNB Metacat route:
   - `/knb/metacat/bowdish.796.1/knb`
   - returned an HTML document rather than the tab-delimited Table S1 object.

3. DataONE Coordinating Node:
   - `/cn/v2/resolve/bowdish.796.1` returned HTTP 404;
   - a Solr query for the exact identifier returned zero matching documents.

The third failure shows that continuing to guess member-node paths would not be a justified repair.

## Scientific firewall

No SF01 effect magnitude has been imported into the Phase-2 evidence ledger.

The prepared materializer explicitly excludes source `Hedges_d` and `Vd` columns and is retained for later use if the historical data object becomes legitimately resolvable.

No table rows are reconstructed from article prose or metadata, and the source is not marked row-materialized.

## Current status

`source_verified_public_supplement_row_materialization_blocked_by_data_object_resolution`

SF01 therefore remains incomplete for the systematic-frame completion gate.

## Next action

Continue row materialization with source frames that expose current machine-readable public datasets. SF01 can be revisited if a stable publisher file or functioning DataONE object endpoint is recovered.
