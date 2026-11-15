# RC001 Pyrus raw-data access gate — 2026-11-15

**Result: PUBLIC METADATA VERIFIED; RAW WORKBOOK NOT ACCESSED. No data reanalysis or estimated rescue effect.**

Published biological primary study:
Castilla AR et al. (2019), *Genetic rescue by distant trees mitigates qualitative pollen limitation imposed by fine-scale spatial genetic structure*, *Molecular Ecology* 28:4363–4374, https://doi.org/10.1111/mec.15233.

Published data DOI: https://doi.org/10.5061/dryad.6t72p3j (July 24, 2019).

The landing page documents the files:
- `Pyrus bourgaeana genetic rescue_07_15_19.xlsx` (62.30 KB)
- `README_for_Pyrus bourgaeana genetic rescue_07_15_19.txt` (4.53 KB)

The full study measured microsatellite-based fine-scale kinship in **two** biological *Pyrus bourgaeana* populations, **six** controlled pollen cross treatments, fruit initiation, fruit/seed properties and germination. This is a source-verified **molecular + direct reproductive function** design, but the **two populations are not two independent studies**.

Prospective CI schema probe `research/rescue_coupling/audit_pyrus_dryad_schema.py` (GitHub Actions branch run **43681573354**) recorded:
- Dryad dataset metadata: `verified`; correct DOI, title and publication date.
- `GET https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.6t72p3j/download`: HTTP **401 Unauthorized** without a Dryad API bearer token.
- Thus `bundle_status=access_stop`, `schema_status=not_verified_access_stop`, `decision=ACCESS_STOP_NO_RAW_COHORT_LINKAGE_CLAIM`.
- No workbook bytes, actual experimental sheet headers, treatment-specific independent-unit IDs, marker values, phenotype outcomes, gene-flow contrasts or effect sizes were read.

The [official Dryad API documentation](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md) describes bearer-token requirements for file downloads. **Do not** evade the authentication barrier, guess alternate file URLs, fabricate an Excel schema, reuse figure digitization as the original data, or treat 401 as evidence the publication's data are missing.

**Independent next route:** request an authorized Dryad API token or have the researcher download the public workbook through their permitted browser account and add it as an authorized input; alternatively, contact the corresponding author for an accessible citable copy. The analysis can then parse the source unit metadata and freeze design contrasts **before** reading signed treatment effects. Until then, retain RC001 as a strong empirical source **candidate**, not a confirmed reconstructible `G–F` source record for pooled meta-analysis.

All previous Clarke source classification (19 studies/27 entries, PS20/SR4/IR3, 19 aligned numeric post-generations/8 mismatched) remains unchanged.
