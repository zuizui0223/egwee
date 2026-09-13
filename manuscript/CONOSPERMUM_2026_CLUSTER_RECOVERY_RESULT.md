# ML005 / PS011 Conospermum 2026 recovery result

## Terminal state

`source_access_blocked`

No C/G_offspring effect was calculated.

## What closed successfully before the block

- The study is a valid same-campaign candidate for contemporary pollen movement (`C`) and the 2017 seedling cohort (`G_offspring`).
- Independent unit is population; maternal plants, seedlings and loci remain nested.
- Primary C endpoint was frozen prospectively as the source `m_p + s` pollen-immigration estimate.
- Primary G endpoint was frozen prospectively as seedling expected heterozygosity (`H_E`) with a 10,000-resample locus bootstrap, RNG seed 20260913.
- Primary exposure was frozen before opening genotype values as source-defined urban matrix barrier/permeability rather than geographic distance.
- Frozen matrix classes: `permeable = A, B, D`; `urban_barrier = C, E, F`.
- Populations G and H remain outside the confirmatory overlap because they produced no progeny; they are not coded as G_offspring zeros.

## Dryad audit

Dryad DOI `10.5061/dryad.95x69p907` is public and exposes metadata for five files:

- `Paternity_dataset_unformatted.xlsx`
- `Paternity_dataset.xlsx`
- `README.md`
- `Seedlings_scoring_unformatted.xlsx`
- `Seedlings_scoring.xlsx`

The public landing-page/index description states that adult and seedling files use GenAlEx format: two metadata rows followed by individual name, population, locus names and diploid allele scores. Thus the planned population-level `H_E` reconstruction is structurally valid.

## Why the analysis did not proceed

Four access diagnostics were separated from the biological analysis:

1. REST `/api/v2/files/{id}/download` returned `401 Unauthorized`.
2. anonymous `/downloads/file_stream/{id}` returned `403 Forbidden` from CI.
3. dataset-level REST `/download` returned `401 Unauthorized`.
4. a browser-like cookie/referer session reached the landing page, but the file response was replaced by an Anubis JavaScript proof-of-work validation page rather than workbook bytes.

The fourth diagnostic identifies the actual boundary: public metadata are accessible, while automated file-byte retrieval from the CI environment is behind an anti-bot proof-of-work layer. This is an access-control boundary, not evidence that the archive is absent or that the biological effect is null.

No attempt is made to bypass the anti-bot challenge.

## Reopen condition

Reopen ML005 only when one of the following is available through an ordinary authorized route:

- a browser-downloaded copy of the Dryad files supplied to the project;
- author-supplied raw files;
- a Dryad access route that legitimately returns the public bytes without bypassing access controls.

On reopening, the frozen exposure, C endpoint, G endpoint, population overlap and bootstrap rules above remain authoritative. Do not switch predictor or genetic metric after seeing the values.
