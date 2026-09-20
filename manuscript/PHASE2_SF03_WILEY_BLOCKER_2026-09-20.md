# SF03 Supporting Information access blocker — 2026-09-20

## Source

Aguilar et al. (2019), *Habitat fragmentation reduces plant progeny quality: a global synthesis*, Ecology Letters, doi:10.1111/ele.13272.

The publisher page publicly identifies two supporting files:

- `ele13272-sup-0001-Suppinfo.pdf` (~1.1 MB);
- `ele13272-sup-0002-AppendixS1.pdf` (~628.5 KB).

The source synthesis reports 179 unique plant species. The article text further reports a second literature search containing 90 publications and 108 plant species for progeny performance, but those aggregate counts are not a substitute for the complete Appendix S1 primary-study identity ledger.

## Reproducible access test

GitHub Actions probed Wiley's standard `action/downloadSupplement` route after visiting the article landing page and retaining session cookies.

Both files returned HTTP 403 and HTML challenge pages rather than PDF bytes:

- `Suppinfo.pdf`: 403, 6061-byte HTML;
- `AppendixS1.pdf`: 403, 6067-byte HTML.

The Wiley article page remains sufficient to verify filenames and public-supporting-information metadata, but not to materialize the row-level appendix reproducibly in the current execution environment.

## Alternative-source check

A public author-hosted copy of the article was found and confirms the 179-species synthesis plus aggregate literature-search counts. It does not expose the Appendix S1 bytes or a complete row-level primary-study ledger.

No complete alternative public mirror of Appendix S1 was located in the current audit.

## Phase-2 consequence

SF03 is therefore **source verified but row-materialization access-blocked**.

Do not:

- reconstruct the primary-study universe from incomplete article references;
- substitute the 179 species list for the source-publication ledger;
- infer missing studies from effect-size citations;
- open effect magnitudes before the candidate universe is recoverable.

Revisit only if a stable Wiley, author-repository, institutional-repository, or other legitimate public copy of Appendix S1 becomes available.
