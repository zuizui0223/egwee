# Phase-2 SF07 access blocker — 2026-09-20

## Result

SF07 (Olhnuud et al. 2025; Dryad DOI `10.5061/dryad.dz08kps9p`) is source-verified at the dataset/README level, but its row materialization is currently blocked in the reproducible GitHub Actions environment.

The public Dryad landing page exposes:

- `Abundance_20250630.csv` — 78 observations from 40 publications;
- `Richness_20250627.csv` — 109 observations from 63 publications;
- a declared global denominator of 80 studies.

## Failure diagnosis

Two independent download attempts were made from the public file links.

1. direct `curl --location` to the Dryad public `file_stream` URL returned HTTP 403;
2. a browser-like request that first loaded the landing page, retained cookies, supplied a Referer and a normal browser User-Agent reached the endpoint, but the downloaded body was an HTML **"Validating..."** anti-bot page rather than the CSV.

The second attempt therefore failed the CSV schema check before any source row was parsed.

This is an access-layer failure, not an analysis failure.

## Scientific firewall

No SF07 effect values have been opened or copied into the Phase-2 evidence ledger.

The planned materializer explicitly excludes `r_effect_size` and `Sample_size` from the bibliographic output. It remains available for later execution if a legitimate machine-readable Dryad download route becomes available.

No attempt will bypass Dryad access controls. SF07 is not marked row-materialized.

## Current status

`source_verified_public_dryad_row_materialization_blocked_by_download_access`

SF07 therefore remains incomplete for the systematic-frame completion gate.

## Next action

Continue row materialization with another source frame whose public supplement is reproducibly machine-readable. SF07 can be revisited through an official Dryad API/download route if authenticated/public programmatic access becomes available.
