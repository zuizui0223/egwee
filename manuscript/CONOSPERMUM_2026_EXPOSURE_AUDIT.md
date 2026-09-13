# ML005 / PS011 Conospermum 2026 exposure audit

## Decision

Primary exposure for any future ML005 quantitative analysis is the source-defined **modified incidence-function connectivity index**, represented as fragmentation severity `-z(connectivity_index)`.

The provisional `urban_barrier / permeable` classification is not the primary exposure. It is retained as descriptive landscape metadata/sensitivity only.

## Why the exposure was corrected

The 2026 source Methods explicitly define a connectivity index based on the modified incidence-function framework used in the earlier Conospermum programme. This is a landscape quantity defined independently of pollen-immigration and offspring-genetic outcomes.

The provisional binary matrix-class evidence included realized pollen-immigration information in some source rationales. Because pollen immigration is the primary `C` endpoint, using that outcome to help assign the exposure would create circularity. No C/G effect had been calculated before this issue was identified.

## Public-source audit

The 2019 programme Dryad landing page describes `fruit_and_seed_set.csv` as containing population statistics and reproductive output. The page exposes an ordinary preview endpoint for that CSV:

`/data_file/preview_check/155093.js`

The landing page is accessible from CI, but the preview endpoint returned HTTP 500 during the locked audit. The raw/download routes are independently behind the previously documented access controls.

Therefore:

- the connectivity/isolation **definition** is source-supported;
- exact population-specific connectivity values needed for ML005 are **not currently reconstructable from the ordinary public route available in CI**;
- this is not a biological null and does not justify substitution of another exposure.

## Current ML005 gate

ML005 remains at zero admissible quantitative effects. Two independent prerequisites must both be resolved before reopening:

1. exact population-specific modified-incidence connectivity values for the common C/G populations;
2. legitimately accessible seedling genotype bytes for population-level `H_E` reconstruction.

The frozen endpoints remain:

- `C`: source `m_p+s` pollen-immigration estimate;
- `G_offspring`: seedling `H_E` with 10,000-resample locus bootstrap, RNG seed 20260913.

Do not rescue the cluster with population size, distance, area, floral display, another paternity model, another genetic metric, or the descriptive binary matrix class.
