# ML005 / PS011 Conospermum 2026 recovery result

## Terminal state

`source_access_blocked + source_exposure_values_not_reconstructable`

No C/G_offspring effect was calculated.

## What closed successfully before the block

- The study is a valid same-campaign candidate for contemporary pollen movement (`C`) and the 2017 seedling cohort (`G_offspring`).
- Independent unit is population; maternal plants, seedlings and loci remain nested.
- Primary C endpoint was frozen prospectively as the source `m_p + s` pollen-immigration estimate.
- Primary G endpoint was frozen prospectively as seedling expected heterozygosity (`H_E`) with a 10,000-resample locus bootstrap, RNG seed 20260913.
- The source Methods define an outcome-independent modified incidence-function connectivity index for the landscape state. This is the canonical primary exposure for any reopening.
- Populations G and H remain outside the confirmatory overlap because they produced no progeny; they are not coded as G_offspring zeros.

## Exposure audit and correction

The earlier provisional recovery contract used an `urban_barrier / permeable` binary class. That representation is now demoted to descriptive landscape context/sensitivity only.

Reason: some of the provisional class rationales referred to realized pollen immigration. Because pollen immigration is the primary `C` outcome, it cannot also help define the exposure used to estimate the C response.

The 2026 Methods instead provide a cleaner, prospectively source-defined exposure: the modified incidence-function connectivity index. The earlier programme paper uses the same landscape-isolation framework, and the 2019 Dryad landing page identifies `fruit_and_seed_set.csv` as containing population statistics.

However, exact population-specific isolation/connectivity values could not be recovered through the ordinary public routes available in this environment. The Dryad landing page exposes a preview endpoint for the 2019 CSV, but the preview request returned HTTP 500 from CI. Raw/download endpoints are separately protected as described below.

Therefore the connectivity definition is source-supported, but the exact population vector required for effect calculation remains unreconstructed.

## Dryad raw-data audit

Dryad DOI `10.5061/dryad.95x69p907` is public and exposes metadata for five files:

- `Paternity_dataset_unformatted.xlsx`
- `Paternity_dataset.xlsx`
- `README.md`
- `Seedlings_scoring_unformatted.xlsx`
- `Seedlings_scoring.xlsx`

The public landing-page description states that adult and seedling files use GenAlEx format: two metadata rows followed by individual name, population, locus names and diploid allele scores. Thus the planned population-level `H_E` reconstruction is structurally valid.

Automated byte retrieval was nevertheless blocked. Diagnostics found:

1. REST `/api/v2/files/{id}/download` returned `401 Unauthorized`;
2. the exact public landing-page href `/downloads/file_stream/{id}` returned an Anubis/HTML access page rather than workbook bytes from CI;
3. dataset-level REST `/download` returned `401 Unauthorized`;
4. browser-like cookie/referer attempts did not produce the workbook bytes.

This is an access-control/transport boundary, not evidence that the archive is absent or that the biological effect is null. No attempt is made to bypass the anti-bot challenge.

## Consequence for ML005

ML005 remains a **non-admitted candidate with zero quantitative effects**. There is no basis for switching to an easier predictor or alternative genetic metric.

The binary matrix-class file remains useful for biological narrative and future sensitivity checks, but it is not an admissible primary exposure for C/G_offspring synthesis.

## Reopen condition

Reopen ML005 only when both are available through ordinary authorized/source-valid routes:

1. exact population-specific values for the source-defined modified incidence-function connectivity index for the common C/G populations;
2. a browser-downloaded/author-supplied/otherwise legitimately accessible copy of the seedling genotype files.

On reopening, the frozen C endpoint (`m_p+s`), G endpoint (`H_E`), population frame, bootstrap rules and continuous connectivity exposure remain authoritative. Do not switch predictor or genetic metric after seeing the values.
