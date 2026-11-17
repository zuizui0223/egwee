# LA001 — why visit-rate transfer failed at site 24-43 (post-outcome diagnostic)

**Date:** 2026-11-17. **Status:** DESCRIPTIVE ONLY, not a new experiment, causal mediation result, or accepted alternative to the frozen negative primary. Parent source: Layman et al. (2017), *Evolution*, DOI [10.1111/evo.13167](https://doi.org/10.1111/evo.13167); original Dryad dataset [10.5061/dryad.2pj0j](https://doi.org/10.5061/dryad.2pj0j), ZIP SHA256 `82bcaa1c3a504cc779bc9c2aa95199a657dd404b3fdf62f7059e4ff5028b39c1`. Original LA001 protocol: `78af346b100b70c61bc12eb71f4d57afe7f28722`.

## Source-locked replication

The original site-held-out prediction for all 252 eligible field plants, 4 source sites, and 121 complete half-hour visitor observation periods was independently recomputed from the user's exact-source ZIP. All **12 M0/M1/M2 fold MSEs** agreed with the original saved LA001 values to **1e−10** absolute tolerance. No original worksheet or plant-level genotype/seed/visit record is redistributed.

**Frozen original conclusion unchanged:** `NO_ROBUST_SINGLE_PROGRAMME_INCREMENT`, as pooled M0 MSE=0.670754 and M1(+AH/BF effective-guild visits) MSE=0.701567 (gain **−0.030813**).

## Training support and extrapolation

The post-hoc upper-support check compares each held-out site's observed effective guild visit rate (AH+BF visits per recorded open-flower hour) to the **95th percentile of that predictor in its three training sites**. This percentile is a descriptive diagnostic, **not** an optimized gate or a significance test.

| Left-out site | Plants | Training-rate 95th percentile | Held-out plants above 95th | Trained M1 visit coefficient (raw log unit) | Original M0−M1 MSE gain |
|---|---:|---:|---:|---:|---:|
| Waco | 62 | 4.219 | 1 | −0.130 | +0.0522 |
| Quarry | 63 | 4.400 | 0 | −0.365 | +0.0110 |
| **24-43** | **64** | **2.608** | **22 (34.4%)** | **−0.888** | **−0.2120** |
| Landersville | 63 | 4.400 | 0 | −0.059 | +0.0298 |

All **22** 24-43 predictor values above its training 95th percentile were **2014** plants, or 22/32 of that year's eligible plants at this site. When trained on the other three sites, M1 assigned a negative coefficient to visit rate; extrapolating it into the highest visit rates drove large downward shifts in predicted seed output. A negative fitted coefficient **does not demonstrate that visitation biologically reduces fecundity**.

## Within-site/year/SC source-grain diagnostic at 24-43

| Year | Group | Plants | Mean AH+BF rate / flower-hour | Original M0−M1 MSE gain | M1−M0 mean prediction shift |
|---|---|---:|---:|---:|---:|
| 2014 | SI | 16 | 3.153 | **−0.7643** | −0.4822 |
| 2014 | SC | 16 | 3.719 | +0.0558 | −0.6294 |
| 2015 | SI | 16 | 0.436 | −0.0847 | +0.0804 |
| 2015 | SC | 16 | 0.531 | −0.0550 | +0.0241 |

The SI 2014 subgroup contributes approximately **−0.191** to the full 24-43 site's −0.212 mean MSE gain. This is **post-outcome** contribution accounting, not proof that SI changes pollinator effectiveness, and not permission to choose a favored subgroup. The five most negative plant-level differences together contribute **−0.2103** to the site's mean gain, revealing high influence but not establishing that those observations are errors. Do not drop or winsorize them.

In the archive, 24-43 had **9 completed observation sessions in 2014 versus 19 in 2015**, contributing to different possible sampling precision and observed flower-hour denominators. Lower observed flower-hours, real pollinator behaviour, seasonal phenology, genotype composition and the original observation schedule could all contribute; these components are **not individually identified**.

## What the result actually changes

The former vague sentence “visitation does not transfer” can now be stated more precisely:

> The site-held-out prediction failure was concentrated in a test-site/year with exceptionally high observed per-flower visitation relative to the training sites. A negatively estimated pooled visit-rate coefficient extrapolated poorly into that region. The available natural data cannot distinguish whether this reflects ecological heterogeneity, sampling/exposure uncertainty, genotype-specific mate constraints or omitted compatible pollen processes.

The old **negative primary result stands**. The new result is a failure-mode and transport-support diagnosis. This is not evidence for a universal interaction–genetic principle, and no model retuning, alternative inclusion threshold or posthoc significance claim is approved.

## Reproduction and firewall

The source-withheld tool `diagnose_la001_site_transfer.py` accepts the local exact original ZIP, reruns original `run_leavenworthia_LA001.py` feature construction, checks the original 12 holdout MSEs and confirms the source-pinned aggregate diagnostics. It produces only four-site and site×year×genotype aggregate summaries.

```bash
python research/compatibility_function/diagnose_la001_site_transfer.py \
  --source-zip /path/to/doi_10_5061_dryad_2pj0j__v20161228.zip \
  --output /tmp/LA001_source_verified_site_transfer.json
```

The original source ZIP and individual values are never committed. CI can test the code and saved summary integrity **without** the original private conversation upload; a fresh source-level check requires that SHA-pinned ZIP. No prior EGWEE meta-analysis or *Theoretical Ecology* source results are changed.
