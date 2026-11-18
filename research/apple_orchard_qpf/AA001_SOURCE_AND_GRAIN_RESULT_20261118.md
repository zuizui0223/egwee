# AA001: 2026 apple orchard Q–germinated-pollen–final-fruit original source and grain audit

**Status:** original source and strict three-layer source-cohort gate fully executed, **not a new causal ecological or same-flower result**. Independent crop orchard survey, empirical egwee (not theoretical egwe), published Riva et al. 2026. Do not count as a third natural QPF matched mother/flower programme.

## Original publicly reproducible source

Riva et al., *Climate impacts apple pollination, yield and economic outcomes of farmers*, *Science of the Total Environment* 1029:181767, DOI [10.1016/j.scitotenv.2026.181767](https://doi.org/10.1016/j.scitotenv.2026.181767); original data [Zenodo 10.5281/zenodo.19403906](https://doi.org/10.5281/zenodo.19403906). The original study used 33 orchards in multiple European/North African regions during 2022–2023, with source visitor Q, 2023 floral style P (germinated grains), and separate controlled-treatment F (initial/final fruit success); treatments were E (insect exclusion), O (open) and OH (open plus hand supplement). P styles were **excised**, meaning the matched site/plot is not a directly followed stigma-to-mature-fruit flower.

The source-only original Zenodo API retrieval initially returned only the file `self` link, which was **proved to be the original source text**, rather than the file-metadata JSON. The source-locked reader follows only that exact API advertised link, checks its original checksum and disallows arbitrary redirects/supplement guesses. [Successful final source verification](https://github.com/zuizui0223/egwee/actions/runs/44290503422):

| Native original file | Exact source rows | Source SHA256 |
|---|---:|---|
| `TransectIN.txt` | **390** | `9cf85041de39adbb50c881bd3236c7368eeb23f0a20c22e13b2b4c28d8851a09` |
| `GerminatedPollen.txt` | **1,061** | `69c12fd6744dcf5066c7ca08ddfc970f03565faf089721068a05a980d7897312` |
| `initial_final_fruitset.txt` | **816** | `2898dbeab9492d11b6a886373e82ce385d3e16a51c8163c402f8a30adad37ec0` |
| `apple_weight.txt` | **796** | `fdfc5b9923dc7047b62ca009875c5d068475cad3381e4baa7c6550d831618942` |

All 4 original header / original-byte SHA256 / Zenodo file digest gate PASS. No original data rows redistributed or source outcome correlations computed in source gate.

## Strict 2023 common observational grain: registered and failed before effects

At [source grain gate run 44291032341](https://github.com/zuizui0223/egwee/actions/runs/44291032341), with rules frozen in `AA001_GRAIN_FREEZE_20261118.md` before any signed biological response associations, we checked exact original **Region×Site×year 2023**:

| Source audit quantity | Original gate result |
|---|---:|
| 2023 Q observation rows | **204**; representing **16** valid Q orchards |
| 2023 orchard P source coverage | **18** valid orchards |
| 2023 orchard F source coverage | **29** valid orchards |
| Exactly paired same-orchard **Q+P+O(F)** orchard keys | **11 orchards, 3 original regions** |
| Exact common 2023 orchard+plot O(P,F) with source Q orchard available | **46 cells** |
| P and F same-orchard+plot across all available source orchards: E / O / OH | **72 / 76 / 81 source cells** |
| 2022 and 2023 Q row counts | **186 / 204** |
| Original apple-weight 2022 / 2023 rows | **301 / 495** |

The prospectively fixed source gate required **≥12 orchard Q+P+F overlaps** and ≥3 regions and >=20 same-orchard+plot O records. It failed **solely on the orchard denominator: 11 vs 12**. **Decision: `SOURCE_COHORT_COVERAGE_STOP`**. This is a strictly measured *coverage* result, **not** a biological negative effect. Do not weaken this gate post hoc to fit Q+P+F at 11 orchards, and do not combine styles, apples, plots or years to reach 12.

## Scientifically distinct P→F opportunity after the three-layer STOP

Exact original **P and F** source plot-treatment overlaps are more abundant and may support a separate, explicitly narrower orchard-scale contextual prediction. A **new question** was recorded in `AA001_PF_CONTEXT_PREDICTION_FREEZE_20261118.md` *before any P-vs-F coefficients*: open treatment **O**, 2023 only, same original orchard and plots, mean style germinated P vs separate fruit final rate F, temperature baseline, hold out whole original regions. This is **one source programme**, not a third same-flower QPF original programme and not confirmed ecological mediation.

A separate script `test_AA001_PF_context_region_holdout.py` uses exact source SHA and frozen >=12 PF orchards, >=3 regions with >=2 orchards each. If this narrower coverage fails or feature variance is insufficient, it reports STOP without posthoc rescue. This secondary source-context calculation does not change the original QPF coverage decision.

## Claim ceiling and broader ecological meaning

The published Riva et al. paper already found treatment- and climate-dependent pollen germination and fruit formation; EGWEE does **not** rebrand those authors' discoveries. This study's contribution so far is an inspectable *ecological unit audit*: three measurements described by one article do **not** imply three biologically matched layers in each orchard, and even common orchard context is more selective than nominal 33 orchard study coverage.

Original QPF atlas still has only two admitted same-ramet/flower experimental programmes (*Oenothera fruticosa* and *Mertensia ciliata*, each with nonportable separate held-out prediction), not three. Downstream fragment-function mismatches and EuPPollNet guild-use allocation remain valid but cannot be causally linked to this apple dataset. Site-level climate, orchard management, cultivar and pollen donor genetic quality are not controlled by this source gate.

No original row-level fruit, stigma, orchard identities, coordinates, numerical pollen values, raw Zenodo files or unidentifiable genotype fields were copied into EGWEE GitHub. Source reproduction and matched counts are provided by the scripts/CI with a small derivative-only artifact.
