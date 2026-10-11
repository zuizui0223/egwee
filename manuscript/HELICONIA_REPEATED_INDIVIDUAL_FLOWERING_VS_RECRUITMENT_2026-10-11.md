# In the same Heliconia plants, flowering records switch while stock persists — plot/year decomposition (2026-10-11)

## Status and empirical framing

**EXPLORATORY, post-exposure, one-species/one-landscape analysis.** This is empirical **egwee**, not the theoretical **egwe/NEE** programme. No study or effect is admitted to the frozen EGWEE five-cluster direct synthesis, eight matched I–F programmes, sixteen-programme translation map or SF06 literature corpus. Nothing herein licenses a new general ecological law, stage-specific causal mechanism or submission-ready claim.

**Question:** Do reproductive-activity pulses arise because plants disappear/are replaced, or because the *same surviving tagged individuals* have different recorded flowering activity? And does local flowering history contain reproductive-function information once stable plot differences, common year effects and standing plant stock are separated?

**Source:** Bruna et al. (2023), *Ecology*, doi:10.1002/ecy.4174, Dryad doi:10.5061/dryad.stqjq2c8d. Original public Git repository `BrunaLab/HeliconiaSurveys`, pinned commit `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`; `HDP_survey.csv` blob `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`. Source includes 66,396 plant-year records; the current repeated individual analyses use the ten plots admissible for the complete earlier 2001–2005 balanced recruitment window: CF-1, CF-2, CF-3, FF-1 through FF-7. Excluded continuous-forest plots were observation-blackout affected.

## Reproductive pulse is primarily a change in recorded activity within surviving plants

Matching `plot_id + plant_id` in consecutive annual censuses, and requiring `census_status=measured` in both years for the same-individual component, gives:

| Recorded flowering transition | 2001→2002 | 2002→2003 | 2003→2004 |
|---|---:|---:|---:|
| Positive flowering record in old year | 236 | 116 | 382 |
| Positive flowering record in next year | 116 | 382 | 165 |
| Both years measured: positive in both | 51 | 53 | 74 |
| Both years measured: old positive, next no positive record | 182 | 56 | 294 |
| Both years measured: old no positive record, next positive | 60 | 320 | 86 |
| **Within-plant recorded-positive net change** | **−122** | **+264** | **−208** |
| **Net due to newly/previously measured plant turnover** | **+2** | **+2** | **−9** |
| Total recorded-positive net change | **−120** | **+266** | **−217** |

The decomposition is an **accounting identity** on the same tagged IDs. In the 2001→2002 collapse, the loss **does not arise primarily from dead/disappearing reproductive plants**: among individuals *measured in both years*, positive flowering status is lost 182 times but newly recorded 60 times; the net from that stratum is −122, versus +2 from turnover. A similarly large positive shift occurs in 2002→2003 (320 new documented positives versus 56 old positives disappearing *within survivors*), followed by the next reversal.

**Precisely supported conclusion:** annual reproductive *records* change strongly within living tracked individuals. The stage has marked population-level temporal variability, even when the extant population stock persists. This is not a demonstration of true flowering cessation, reversible physiological suppression, carbon-resource trade-offs or maternal fitness, because **`infl=NA` is not certified flowering absence** and observation frequency/phenology may change. One cannot convert these counters into reproductive switching rates without calibration of the floral observation process. Note also that the first-recorded recruits are not offspring linked to those plant IDs.

## A critical scale/conditioning result: apparent flowering–recruitment correspondence is largely shared structure

On the **same 10 plots × 5 outcome years (2001–2005), 50 plot-years**, first-recorded new seedlings in year `t` are compared with recorded flowering-positive plants in `t-1`; all variables log(1 + count). The same source data and fixed cohort/eligibility gate apply to lag 1, 2 and 3.

| Lagged flowering predictor | Raw plot-year Pearson r with log recorded recruits | r after plot+year demeaning | Partial r after plot+year demeaning **and** adjusting log prior living stock |
|---|---:|---:|---:|
| `t−1` flowering-positive count | **+0.655** | −0.035 | **+0.096** |
| `t−2` flowering-positive count | +0.518 | −0.126 | −0.104 |
| `t−3` flowering-positive count | +0.639 | +0.024 | −0.028 |
| `t−1` recorded inflorescence count | +0.643 | −0.066 | +0.072 |

These are **descriptive residual correlations** only, not independent outcomes, inferential p-values or externally validated predictive effects. The partial `t−1` correlation is numerically small and inconsistent across source deletions. Leave-one-ranch-out partial correlations (after plot/year/stock adjustment) for lag one: excluding Esteio **+0.187**, excluding Dimona **+0.258**, excluding Porto Alegre **−0.015**. Leave-one-year-out values span **−0.014 to +0.359**.

A cross-plot relationship can coexist with weak *within-plot-and-within-year* residual association because larger, historically more productive plots tend to have both more flowering plants and more detected recruits, while year-specific weather, recruitment conditions and survey intensity can drive broad pulses. This is a **plausible statistical decomposition, not an identified causal attribution to any one branch**. Year fixed effects also remove potentially real ecological climate signals, and conditioning on post-fragmentation stock changes the estimand.

This pattern sharpens the previous spatial versus temporal predictive distinction: same-year cross-sectional association is not interchangeable with individual state, true mating/recruitment transition or future-year diagnostic value. The direct strict forward-year comparison was already source-reproduced separately (prior living stock MSE 867.37 vs a historical-mean 467.61 on 34 held-future plot-years).

## What prior ecology already established

1. **Individual flowering depends on size:** Bruna & Kress (2002), *Conservation Biology* 16:1256–1266, described increasing flowering probability with plant size in this species (and compared fragment categories). Thus a stable individual-size/vigor component is already known; this reanalysis does not discover it.
2. **Direct reproductive response to floral neighborhood was weak:** Bruna, Kress, Marques & Silva (2004), *Acta Amazonica* 34:467–471, doi:10.1590/S0044-59672004000300012, experimentally varied the local number of flowering neighbors and did not detect treatment differences in measured focal fruit/seed outcomes. Flowering counts are **not** validated as pollen transfer, seed supply or reproductive performance.
3. **Delayed climate effects on flowering are established:** Scott, Uriarte & Bruna (2022), *Global Change Biology*, doi:10.1111/gcb.15900, found nonlinear delayed SPEI effects in the same landscape system. It would be incorrect to claim the present temporal records demonstrate a previously unknown climate effect.
4. **Seed/safe-site limits already quantified:** Uriarte et al. (2010), *Ecology* 91:1317–1328, doi:10.1890/09-0785.1, evaluated seed production, dispersal and establishment and found safe-site limitation important for *Heliconia*. EGWEE cannot claim the discovery of this mechanism.

## Three distinguishable competing explanations

- **Real repeated-individual flowering plasticity:** actual changes in the same plants' flowering propensity dominate the recorded pulses. A repeated flowering-detection-calibrated model with plant size, previous flowering and seasonal resource/meteorological state would have to outperform a stable-vigor-only model in held-out *years*.
- **Observation/phenology aliasing:** positive inflorescences are missed in some annual seasons despite reproductive activity. Repeated flower-season surveys and seasonal survey dates could show stable true flowering beneath recorded changes. Without those visit-level records in this CSV, the hypothesis remains viable.
- **Downstream seed/safe-site control:** flowering pulses are real, but individual flowering, seed arrival and seedling establishment are not obligatorily proportional. Stage-specific seed/establishment experiments or observed mapped mother-to-recruit cohorts should predict the exceptions, not merely match pulses post hoc.

Use a different independent landscape/species and prospectively fixed stage measurements before claiming any general mechanism. The present **ten plots are nested within just three ranches in one study**, and the 2002/03 pulse and candidate lag set were selected after outcome exposure.

## Reproduction / frozen claims

- `scripts/audit_heliconia_individual_flowering_switch.py` runs the source-hash-verified plant-ID transition ledger, including every year-pair identity check, with output artifact on GitHub Actions.
- `scripts/audit_heliconia_plot_year_fecundity_translation.py` computes explicit `log1p` plot/year two-way demeaned and prior-stock-conditioned correlations, plus leave-one-year/ranch/plot diagnostics.
- Both new workflows are automatically dispatched on the active PR branch. **At the time of this note GitHub Actions were queued; workflow success was not yet certified**. Source-level summaries were independently recomputed against the exact Git blob directly (66,396 input records; the single comma-containing quoted `treefall_status` record is in CF-6 in 2007, outside the restricted rows).
- The original five-direct-cluster, eight quantitative I–F, sixteen-programme evidence map and SF06 publication/sign denominators are *unchanged*. `submission_ready=false`; PR remains draft. Do not promote this exploratory single-system analysis to the main-paper headline.
