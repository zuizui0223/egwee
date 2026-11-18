# QPF007 original *Brassica rapa*: verified 160 plants, source COVERAGE_STOP, separate weak exploratory prediction

**2026-11-18 — Scientific status: original `COVERAGE_STOP`, followed by an explicitly labeled POSTSTOP exploratory analysis that is never confirmatory.** This is an independent 2026 **experimental** plant-pollinator study, **not a third natural fragmented-landscape QPF system**.

## Primary original source and biological unit

Barbot et al. (2026), *PLoS Biology*, DOI [10.1371/journal.pbio.3003579](https://doi.org/10.1371/journal.pbio.3003579), original source [Zenodo 10.5281/zenodo.21628183](https://zenodo.org/records/21628183). The original authors already documented how bee abundance changes visitation, mating opportunity and genetic reproductive success, so those relationships are **published prior art**.

Original source was downloaded through official Zenodo versioned-record file links in GitHub Actions and checked with original MD5/byte sizes and SHA256. Verifiable key-level provenance:

| Source | Original SHA256 | Source structure |
|---|---|---|
| `data_ABPOLL_ID_resume.txt` | `5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe` | **160 individuals, 16 experimental pollinator-abundance sessions** |
| `data_ABPOLL_flower_resume.txt` | `ec7217acb683a0d0475622f3510228f3062a72a8bfd17162888f160db369a495` | **1,967 flower records on the same 160 mothers** |
| `data_ABPOLL_fix10_paternities.txt` | `984d60b26e870c58252b39177d923fa0707af6ea62acadfa9bf8f497da1ce6a6` | 1,099 offspring paternity rows, **not** joined in this analysis |
| `data_ABPOLL_ID_level_detID.txt` | `7f00bbe673eb849c11de5b7fcbeb2d2b60012765cde0f1f6bc25168dd6aedfc5` | 1,363 original pairwise rows, **18 source session labels** and 138 matching focal keys, **excluded** pending original source eligibility explanation |

**Exactly 160/160 `(session,ID_full)` mother keys match** across original individual and stigma-flower source. This establishes original **same-plant** Q/P/F structural alignment, but stigma pollen and seed output were measured from **different flowers of a plant**, not one tracked flower.

The published Zenodo README names a pairwise file `data_ABPOLL_ID_level_ID.txt`, but the actual original manifest contains `data_ABPOLL_ID_level_detID.txt`. The correction was committed **before source biological values** were inspected. No synthetic original pairwise join was invented.

## Original prospective source and model lock: STOP

Scientific source model protocol was frozen at Git commit `1d4b78a1a0ee82cc267b287f7cc0e4a3899486c3` after source-only ID/header verification **and before any new numeric pollen/seed relationship was fitted**. Fixed models for response `log1p(nbGr_mean)` (**mean mature seeds per sampled fruit**, not total offspring across whole plant):

- **M0:** categorical source bee-abundance treatment `poll_treat` + `log1p(nb_visit)` + `log1p(nb_flo_all)` + `log1p(height_max)`.
- **M1:** M0 plus one source-derived plant pollen term `log1p(pl_mean)`; source stigmatic pollen is a transfer quantity proxy, **not pollen compatibility or actual father identity**.
- **Method:** unpenalized intercept, training-fold z-scored predictors, Gaussian ridge λ=1, **16 whole-session holdout folds**, each original source mother scored once. Positive confirmation had required ≥5% pooled MSE improvement and ≥12/16 positive entire-session folds **and** a source-admission gate ≥120 complete plants, ≥6 from every one of 16 sessions.

Official original source read [GitHub Actions 44296293991](https://github.com/zuizui0223/egwee/actions/runs/44296293991) established a real **source eligibility STOP**: 160 plants, **145** complete source Q/P/seed/trait rows, **15** excluded due to 13 missing `nbGr_mean` and 3 missing `pl_mean` (one overlaps), and **one original session with only five complete mothers**, below the preregistered minimum of six. The original confirmatory trial **did not fit or score any M0/M1 numeric output**. This is **not** a negative biological effect estimate, and the registered original sample/threshold was **not retroactively altered**.

## Distinct postcoverage exploratory result (145 original plants, all 16 sessions)

A separate postcoverage **before-model-fit protocol commit** `0933180d563150885968ee4d2eceb3f8fbb0245b` retained *every* eligible plant and kept the same response, predictors, ridge λ1 and heldout session partitions; it explicitly waived the one small-session coverage stop for **exploratory description only**. The original pre-outcome STOP remains the scientific confirmation status.

| Held-out experimental session (anonymous source order) | Mothers | M0 MSE | M1 MSE | M0−M1 |
|---|---:|---:|---:|---:|
| 1 | 10 | 0.088148 | 0.159824 | -0.071676 |
| 2 | 9 | 0.440544 | 0.402473 | +0.038071 |
| 3 | 10 | 0.443673 | 0.407978 | +0.035695 |
| 4 | 10 | 0.801086 | 0.720286 | +0.080800 |
| 5 | 9 | 0.231037 | 0.229215 | +0.001821 |
| 6 | 9 | 0.628141 | 0.633884 | -0.005744 |
| 7 | 9 | 0.359583 | 0.379418 | -0.019835 |
| 8 | 8 | 0.665425 | 0.667755 | -0.002330 |
| 9 | 9 | 0.593210 | 0.635690 | -0.042480 |
| 10 | 9 | 0.476510 | 0.511109 | -0.034599 |
| 11 | 9 | 1.089518 | 1.008765 | +0.080753 |
| 12 | 9 | 0.429263 | 0.365100 | +0.064163 |
| 13 | 10 | 0.677345 | 0.700871 | -0.023526 |
| 14 | 5 | 0.955452 | 0.774522 | +0.180929 |
| 15 | 10 | 0.456144 | 0.474390 | -0.018246 |
| 16 | 10 | 0.436908 | 0.490739 | -0.053831 |
| **145-plant pooled** | **145** | **0.533544** | **0.525837** | **+0.007707** |

Original-source **poststop exploratory** M0 MSE **0.533544**, M1 **0.525837**, small pooled difference **+0.007707**, **1.44%** relative improvement; only **7/16** sessions positive. It also does **not** meet the original *numerical* screen (≥5%, ≥12/16). MAE decreases slightly (**0.611806→0.600116**), which was never a replacement criterion.

**Influence/fragility diagnostic:** the **five-plant under-covered session** alone contributes **+0.006239** or **81.0%** of the already-scored full 145-plant positive MSE difference. The remaining 140 originally predicted plants have only **+0.001520** pooled difference when their existing forecasts are algebraically regrouped. **No refit, date deletion or confirmatory subsetting** occurred in this descriptive breakdown.

Original verified source execution [run 44297136780](https://github.com/zuizui0223/egwee/actions/runs/44297136780) archived **only aggregate 16-session fold scores**, [artifact 14424835913](https://github.com/zuizui0223/egwee/actions/runs/44297136780/artifacts/14424835913), SHA256 `sha256:c29a270714afcbcae10e2b124c8ca4a3205a003b1e230eb67b8c938fdfffb7b9`. Independent penalized Gaussian normal-equation and coordinate-descent implementations agree across every heldout source prediction with maximum absolute discrepancy **3.36e-13**.

## Exact scientific ceiling

**Allowed:** An independently published *Brassica rapa* experimental programme provides observed plant-matched visitor, stigmatic pollen, and sampled-fruit seed coordinates. Their one-feature additional heldout-session predictive gain is **small, unstable and only postcoverage exploratory**. The strict 16-session original trial stopped at its prespecified data-coverage gate.

**Not allowed:** claiming a new causal pollen effectiveness mechanism, a directly observed compatible donor or individual paternal transmission, 16 independent landscapes, offspring viable recruitment, a common island/urban functional-fragmentation regime, or a positive preregistered full QPF test. Mean seeds per sampled fruit has its own fruit-observation selection; original paternity (1,099 children) and pairwise 18-session source were **not matched** into this 160-plant trial.

**Current replication count:** QPF001 *Oenothera* original 93 same-flower Q/P/F fruits and QPF004 *Mertensia* original 62 same-ramet Q/P/F units remain two differently structured strict source programmes from the **frozen six natural-source registry**; QPF007 is a separately discovered manipulated crop experiment and does **not** satisfy the original ≥3 comparable independent natural programme requirement. Neither QPF001/QPF004 historical predictive negative result nor the original QPF007 source STOP was edited.

All original public source data, individual IDs, flower/offspring paternity observations and author code remain on source Zenodo, **not republished in EGWEE**. Only verifiable source hashes, aggregate source coverage, 16 session fold losses and reproducible source-verified scripts are included.
