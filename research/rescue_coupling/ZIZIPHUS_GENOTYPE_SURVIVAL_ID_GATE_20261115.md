# Pseudoziziphus public-genotype / transplant-survival record linkage gate — 2026-11-15

**Verdict:** `VERIFY_RAW_ID_CROSSWALK_FROM_SOURCE_DICTIONARY`. This is a **data-grain/identifier limitation**, not a demonstration that genotype has no survival or ecological-function effect. Biological outcome values and microsatellite allele columns remain unopened.

Published source: *Pseudoziziphus celata* parent genotypes and translocation survival, Figshare [10.6084/m9.figshare.30290722](https://doi.org/10.6084/m9.figshare.30290722), version v1. Original published source is included in `research/rescue_coupling/plant_primary_candidate_registry_v1.json`, candidate RC003, and is grouped with related reproductive studies under `Florida_ziziphus_restoration_programme` for nonindependence control.

## Executed, reproducible source audit

GitHub Actions [run 43682807494](https://github.com/zuizui0223/egwee/actions/runs/43682807494), artifact `14149505948`, script `research/rescue_coupling/audit_ziziphus_id_linkage.py`. Source file SHA-256 digests:

- `Zc_parentgenotypedata.xlsx`: `8e8e8a1d199ecd2e6fdf67464d7a66b7bfc9bf7aa2ca0a8c5d6771eece692ecd`
- `ziziphus.survival.txt` (**tab-delimited**, not CSV): `17395280f02a5fb88810555237ae637c993279a23da0bc6179f1233ca5f75b59`

The survival file contains **1,185 rows**, all with nonempty `plant_id` and `popcode` tokens. These rows contain **40 distinct local `plant_id` values**, **41 distinct `popcode` values**, **19 `genotype` labels**, **16 `Rgenotype` labels**, **11 introduction years** and **two introduction types**. These cardinalities are *identifier labels*, **not numbers of independent plants or genotyped individuals**. There were no recognized text-coded NA markers among these whitelisted identifier fields.

## Candidate keys do not yet define biological individuals

| Candidate combination | Unique string keys | Keys repeated across rows | Maximum rows per key |
|---|---:|---:|---:|
| `popcode × plant_id` | 98 | 51 | 315 |
| `popcode × intro_yr × plant_id` | 261 | 135 | 75 |
| `popcode × intro_type × plant_id` | 128 | 68 | 294 |
| `popcode × intro_yr × intro_type × plant_id` | 261 | 135 | 75 |
| `popcode × intro_yr × intro_type × genotype × plant_id` | 358 | 158 | 73 |
| `popcode × intro_yr × intro_type × Rgenotype × plant_id` | 261 | 135 | 75 |
| `popcode × intro_yr × intro_type × genotype × Rgenotype × plant_id` | 358 | 158 | 73 |

The candidate `popcode × plant_id` also maps to >1 genotype label for **25** keys, illustrating that it is not a stable genomic individual identifier. Even the richest candidate key repeats up to **73 rows**, so it cannot be promoted to a biological individual key without the original survey's location/cohort/plant identifier rules. The 1,185 raw records must not be analyzed as 1,185 independent plants.

The `Zc_parentgenotypedata.xlsx` first sheet contains **59 XML rows**. Its leading four fields have no explicit recognized sample-ID headers (header cells include numeric/unlabeled values). Comparing those unlabelled first-four-column values against survival `genotype`, `Rgenotype` and `plant_id` strings produced **zero exact overlap** in these selected fields. This is **not** proof the genomes and survival outcomes are unrelated: different coding, relational tables, plant-to-parent information, or additional source fields could connect them. No linkage is asserted.

## Strict interpretation

1. The source supplies valuable molecular and transplant-survival measurements, but the **published raw-file tables cannot be joined naively at a verified individual level**.
2. Survival is a `W_survival` or population viability endpoint, **not automatically pollination, mate compatibility, ecosystem service or `F_direct`**.
3. Genome/provenance and survival can be studied after a verified individual/cohort mapping. A positive association would not, by itself, establish a causal genetic rescue effect without transplant controls.
4. Given their shared `Florida_ziziphus_restoration_programme`, do not count this study and the earlier self-incompatible crossing study as independent programmes merely because they have distinct DOIs.

## Next eligibility decision

**STOP** for genotype-to-survival or genotype-to-ecological-function effect estimation using this raw table until the original dataset's record-identifier documentation, plant/pedigree crosswalk and independent sampling hierarchy are verified. Candidate-source admission remains as **B-level observational genotype/fitness source**, not a matched direct ecological-function rescue experiment. This STOP does not rule out recovering a valid analysis from later metadata or the author-provided codebook.

Source and script summaries are **derivative metadata only**; original third-party genotype/outcome files are not redistributed.
