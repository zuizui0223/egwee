# Independent original-observation crop Q→F coverage gate — empirical EGWEE

Date: 2026-11-18. **Outcome-blind source selection and scientific question**, deliberately independent of PR #72 and #74's EuPPollNet European wild-flower guild-use analysis. This is **not** the theoretical `egwe` project, not a re-opening of the five-cluster/17-effect natural fragmentation corpus, and **not** a pollen-provenance (P) measurement.

## Target question and prior art

Do **differences in flower-visiting guild composition** provide predictive information about directly measured crop reproductive production **beyond total pollinator visitation** across legitimately independent crop study programmes? A publishable result would require replicable source-grain **within-crop/study** comparisons with study-level uncertainty and externally tested predictions, not a positive coefficient from pooled pseudo-independent fields.

Published work already finds visit-abundance/yield associations and richness effects using CropPol; Millard et al. (2024, DOI 10.1111/geb.13843), and 2025 JAE 10.1111/1365-2664.70042, directly analyze parts of the same dataset. We are not claiming the basic pollinators→yield link is new. A novel addition, if structurally possible, is a guild-specific **monitoring sufficiency / conditional transferability** test, asking whether simple total visits lose predictive adequacy when bee-versus-hoverfly composition changes under otherwise matched crop programmes. This analysis **must not** cherry-pick a crop or guild after seeing response signs.

## Selected immutable original data

Author maintained repository: `ibartomeus/CropPol` commit `99c69dbab4fa7cbdb630ff3e9bd9989b3de9548b`, `master`. Database latest file version history marked **2.1.0**, but do not assume that reflects 2026 field sampling.

- `Final_Data/CropPol_field_level_data.csv` source Git blob `cd19a354741ac40428e6b94aa1ec2ee596ff0547`, GitHub inventory ~2.20 MB. One row per field/study sample as defined by source; verify original source grain/ID columns before using counts.
- `Final_Data/CropPol_sampling_data.csv` source Git blob `b7ab3fd92da0be5e8ec41b6ada50c2da7d4756c2`, GitHub inventory ~22.08 MB. Original insect records/nested sampling; not automatically separate independent study replicates.
- `Final_Data/CropPol_data_ownership.csv` file inventory source only (not required for effects).
- Data paper Allen-Perkins et al. 2022 DOI 10.1002/ecy.3614; source licence/noncommercial terms must be acknowledged. No original rows or raw source files to be redistributed in EGWEE.

Source methods and fields including `study_id2`, `visits_or_abundance`, `taxa_recorded` were added in source version 2.0.0. **A source codebook, not a column-name guess**, must certify whether an observation reports actual flower visits and whether an apparent 0 hoverfly count is a genuine surveyed zero (not unobserved guild).

## Order of scientific gates (do not open yield values until Gate A/B)

A. **Now:** download immutable original author CSV bytes by official public GitHub raw link, bound file size and verify exact Git blob (SHA-1) plus row counts and headers **without reading source yield or insect values**. Record source SHA256 digest, source metadata/version, and original structural columns. Dryad access history irrelevant; this repository provides a legitimate independent source.

B. **Before any numerical yield association:** select one joined `source study×crop×year × independent field` key with no >1 many-to-many expansion, document study groups and sampling effort, verified yield metric and unit within a source programme, observed sampling method, actual visitors vs passive abundance, and same crop/year/field matching. Missing/blank is NOT zero for visits or yield. Bee definition excludes `Apis mellifera` and distinguishes other wild bees/bumblebees; hoverflies must be `Syrphidae`, NOT all Diptera. Check which source fields already contain category-specific counts; use raw sampling data only if exact source fields yield independent and attributable visits. Complete comparative frames without direct guild coverage STOP.

C. **Post-schema new prospective target** requires >=10 independent programme×crop frames with >=8 source independent fields and >=20 group-positive fields in total; at least 5 programmes must contain independently recorded wild-bee and Syrphidae source visits with comparable effort and unambiguously eligible crop yield. If not, report `COVERAGE_STOP` without outcome model.

D. If B/C pass, freeze programme-balanced cross-field CV criterion `M0 total visits and source-context` versus `M1 M0 + wild-bee-vs-Syrphidae composition` before reading yield effects. Metrics within-study normalized with train-only means and variances, whole-site/field nesting preserved, leave-*study*-out transport separately where source-replicated crops permit. A source study programme may contribute multiple field rows but never multiply the number of independent studies.

## Limits of an eventual result

Crop yield is influenced by irrigation, cultivar, management, pests, and experimental conditions; flower-visitation species composition is not pollen donor quality or successful compatible fertilization. Current crop synthesis already treats visits as an imperfect proxy. Even a positive incremental prediction would be an **observational ecological association** in agricultural contexts, not a fragmentation causal mechanism, seed recruitment, or validation of NEE theory. Crop results cannot be meta-pooled with EuPPollNet plant-use JSD or the five natural fragmentation Hedges g.

## Revision firewall

PR #72, #74, #66 and the main natural 5-cluster effects unchanged. Full original data remain in the original author repository; this branch commits only protocol, code and small derivative records. No yield model may be opened on this branch until exact source grain and relevant source codebook passed.
