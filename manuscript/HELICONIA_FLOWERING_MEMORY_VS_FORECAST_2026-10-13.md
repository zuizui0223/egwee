# Heliconia annual flowering-record memory has little reliable next-year forecasting value (2026-10-13)

## Scope and scientific question

**Exploratory, one already-published study system, empirical `egwee`, not the theoretical `egwe`.** No new source programme/effect enters the frozen five direct-study clusters, eight matched interaction–function programmes, sixteen-process map or SF06 corpus. All data and candidate analyses were inspected post hoc. The PR remains a draft; these are not primary paper claims.

Question: **Can repeated-individual reproductive-history information that remains associated with flowering after size and site/year stratification actually improve a *genuinely future-year* prediction, and does the original source record distinguish entered zero inflorescences from merely non-entered inflorescence counts?**

Input: Bruna et al. (2023), *Ecology*, doi:10.1002/ecy.4174, Dryad doi:10.5061/dryad.stqjq2c8d, pinned public source commit `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`. The cleaned archive is 66,396 plant × census-year rows and the fixed observation-complete analysis panel consists of CF-1, CF-2, CF-3 and FF-1 through FF-7, 10 permanent 0.5-ha plots in **three** ranch contexts. Source-blob SHAs are verified before calculation; every pair requires the *same plot+plant identity measured alive in both years*, and numerical prior-year height and shoot observations. Thus 28,247 eligible individual-year transitions arise across calendar starts 1998–2004 (7 transitions). This is **not 28,247 independent landscapes**, nor a randomized flowering experiment.

## Strong within-year association remains after recorded morphology and observation stratum matching

A descriptive Mantel–Haenszel pooled conditional odds ratio compares whether an already living plant's positive documented inflorescence record in year `t` relates to its positive record at `t+1`. Strata are **plot × calendar transition × previous measured height band (25-cm categories) × previous shoot-count category** (0–2, 3–4, 5–7, 8+).

| Period / condition | Individual-year pairs | Stratified OR |
|---|---:|---:|
| 2001→2005, four transitions | 17,792 | **2.777** |
| 1998→2005, all seven transitions | 28,247 | **2.591** |
| Four-transition panel, additionally stratifying on `t+1` measured height | 17,780 | **2.366** |
| Four-transition panel, additionally stratifying on `t+1` height *and* shoots | 17,779 | **2.689** |

The first two numbers describe *recorded* persistence conditional on a coarse size/stock-health proxy, fixed plot and common calendar transition. Conditioning on the next year's morphology in the third/fourth rows is **a post-response descriptive sensitivity**, not valid causal adjustment. Single-transition adjusted ORs for all seven intervals: **3.06, 1.25, 2.85, 3.81, 2.09, 3.06, 2.41**, respectively. The interval beginning 1999 is much weaker: **do not claim invariant physiological memory**. For the 2001–2004 start-year panel, deleting any one of the three ranch regions yields OR approximately **2.71–2.85**; those are robustness of *this same landscape* only, not external replication.

**Supported:** previous positive flowering-record identity carries information about later positive-record identity *within measured survivors* beyond coarse previous height/shoot count and site/year strata. **Not identified:** a true individual physiological memory, reproductive cost, genetic propensity, belowground energy-reserve carry-over, flowering detection sensitivity, mating success, or a mechanism of fragmentation effects. Unmeasured vigor and an individual's repeated propensity to be observed remain viable alternatives. OR is a ratio of odds, **not 2.8× probability**.

## Strong association fails to become an operational future-year forecast

For a genuinely chronological comparison, each model is trained **only on earlier outcome years**, and forecast windows are `2002→2003`, `2003→2004`, `2004→2005`. The two simple nonparametric risk rules use the same previously measured height and shoots bins; the second additionally uses positive flowering history. All cell/global rates are trained *inside the training fold*. The primary prior-history cell shrinkage value is 20, tested against 5, 100 and 300 **post hoc**, with no hyperparameter selection from future-year responses.

| Forecast scoring target | Measured morphology only | Morphology + previous flowering | Extra gain |
|---|---:|---:|---:|
| **13,542** held-future individual-year predictions, Brier score | 0.039550 | 0.039496 | **0.000054** |
| Same predictions, logarithmic loss | 0.140470 | 0.140126 | **0.000344** |

Recorded positive flowering at the target census is **648/13,542** (4.8%), so absolute classification scores can be dominated by persistent nonflowering records. The Brier score improvement corresponds to only about **0.14% relative reduction**, not a practically calibrated decision-making advance.

Across the three strictly future-year folds, the Brier improvement **changes sign**:
- `2002→2003`: size-only **0.063238** versus size+history **0.062624** (history helps by 0.000614).
- `2003→2004`: size-only **0.030915** versus **0.030918** (essentially neutral/slightly worse).
- `2004→2005`: size-only **0.024356** versus **0.024800** (history worsens by 0.000444).

The pooled Brier gain stays tiny when the smoothing weight is 5, 100 or 300. The addition of past recorded flowering may help calibration among the uncommon previously flowering plants but fails to deliver stable year-level, whole-population utility. **This does not prove exactly zero utility or establish statistical equivalence**; only three future-year test environments exist and the model family was chosen post hoc. Nor does it refute genuine individual-level autocorrelation. Different targets — in-sample association versus future calendar-year prediction — are not interchangeable.

## Critical original-record discovery: many cleaned `infl=NA` rows were entered as `0` in the raw survey

The upstream original wide file `data/survey_raw/Hacuminata_98-09_12oct2016.csv` is **not UTF-8** (free-text notes contain Latin-1 bytes). Its pinned Git blob SHA is `b42963be30b993b93755f7f40ad09d1361def056`. The public cleaned `HDP_survey.csv` has conditional `infl` counts: the original source cleaning function `clean_heliconia_data.R` explicitly describes `Infl` as **conditional on a plant being reproductive**. Therefore an archive `NA` is not necessarily an annual survey missing visit.

To avoid assigning identities based only on a potentially corrected tag number, the provenance checker accepts only **unique matched original plot + tag + subplot combinations**, pairs them to archive `plot_id + tag_number + subplot`, and separates explicit raw numeric `0`, positive numeric count, blank/unentered, ambiguous key and unlinked/corrected key. The source-blob-verified audit found these **archive `infl=NA` and raw explicitly `0`** matching live-plant-year records:

| Source year | Direct raw zero → cleaned archive `NA` |
|---|---:|
| 2001 | **3,706** |
| 2002 | **4,119** |
| 2003 | **3,762** |
| 2004 | **3,999** |

This corrects a previous blanket methodological caveat: the published conditional `NA` includes **large numbers of original data-entry zeroes** and should not all be treated as unknown flowering observations. Importantly, **not every `NA` can be mapped to raw zero**; some source identifiers are unmatched after survey cleaning/tag correction, and a small number of positive-versus-zero disagreements likely reflect corrected errors. Neither original numeric zero nor cleaned `NA` by itself proves every possible inflorescence was detected in the flowering season.

For unique source-verified plant IDs with explicit raw positive/zero entries on both years, documented transitions show independent support for changing recorded reproductive state:
- **2001→2002:** 3,626 matched source-confirmed pairs, consisting of 3,394 `0→0`, 149 `positive→0`, 46 `0→positive`, 37 `positive→positive` (one archive raw-state disagreement is retained as a warning, not silently adjudicated).
- **2002→2003:** 3,861 matched source-confirmed pairs, with 3,524 `0→0`, 42 `positive→0`, 255 `0→positive`, 40 `positive→positive` (archive source disagreements are recorded).

The further **strict raw-verified, morphology-stratified** odds test has now passed independent CI (https://github.com/zuizui0223/egwee/actions/runs/38405672751). Restricting to raw `0` or raw positive **and** non-conflicting cleaned labels, measured morphology and stable unique raw `plot + tag + subplot` linkage gives:

| Verified-original-record comparison | Strict matched pairs | Size/shoot/plot/year-adjusted MH OR |
|---|---:|---:|
| **Four-transition 2001–2004 starting-year panel** | **15,029** | **2.801** |
| All seven annual starts 1998–2004 | **23,937** | **2.576** |

These are very close to the **2.777** and **2.591** clean-archive estimates. The raw-only first-year 1999 interval remains weaker (MH OR **1.306**), so the effect is not invariant across time. This is a strong internal *record-provenance falsification*: the positive history association is **not solely an artifact of cleaned conditional `NA` overwriting original zeroes**. It is **not an independent biological replication**, since the same plants are being reclassified with an older source file. Source linkage selects a nonrandom subset, and original numeric zeros still cannot prove perfect flowering-season detection.

## Strict original-zero-record future-year sensitivity

The further **original-source-verified future-year** audit has now passed GitHub Actions: https://github.com/zuizui0223/egwee/actions/runs/38406225194. It uses only matched original *explicit positive/zero* counts agreeing with the clean source, and the same height-and-shoot hierarchical prediction rules and chronological holds as above. This restriction leaves **11,406** held-future individual-year transitions, **539** with positive flowering recorded in the held year. This is a *selected linked-tag sample*, not a new ecological programme or independent replication.

| Held-future-year comparison | Morphology-only Brier | Morphology + past positive record Brier | Brier improvement |
|---|---:|---:|---:|
| All 3 future years (n=11,406) | 0.039212 | 0.039102 | **+0.000110** |
| 2002→2003 | 0.060044 | 0.059587 | +0.000457 |
| 2003→2004 | 0.033719 | 0.033167 | +0.000551 |
| 2004→2005 | 0.023724 | 0.024374 | **−0.000650** |

This raw-confirmed sample gives a pooled relative Brier improvement of approximately **0.28%**, versus **0.14%** in the full cleaned archive. The 2004→2005 prospective score **worsens even when earlier nonpositive records were explicitly entered as zeros**. Thus the weak and year-sensitive forecast increment is **not solely a cleaned `NA` artefact**. It is not proof of no forecasting information; source tag-linkage selection, just three test-year environments, unmeasured year-specific flowering-detection conditions and method choice after viewing earlier results prevent a formal equivalence/invariance claim.

## Prior-art novelty boundary

Previous ecology already established that flowering schedules vary within perennial individuals and may carry reproductive history even after size effects:
- Ehrlén (2001), *Journal of Ecology*, doi:10.1046/j.1365-2745.2001.00546.x, analysed repeated-year flowering and past fruiting in *Lathyrus vernus* and found past flowering/fruiting history did not consistently imply negative reproduction costs.
- Roach and colleagues (2010), *Ecology*, doi:10.1890/09-0423.1, examined repeated individual reproductive schedules and environmental/size effects in *Plantago lanceolata*.
- Bruna & Kress (2002) previously documented size-dependent flowering in *Heliconia acuminata*, and Scott, Uriarte & Bruna (2022), *Global Change Biology*, doi:10.1111/gcb.15900, previously established delayed climatic influences on this population's flowering.

Thus **flowering persistence and environmental modulation are not new ecological principles** discovered here. A potentially useful EGWEE *hypothesis* instead concerns the **translation gap**: historically positive individual reproductive records may retain local signal while offering little information for independently forecasting population renewal across unknown years. This gap remains a **single-programme, mechanism-unidentified example**, not a generalized tested law. To establish generality requires separate study regions/species with original zero/nonzero flowering verification, actual recruitment detection/viable seed measurements, and independently held future study years.

## Reproduction and status

- `scripts/audit_heliconia_individual_record_memory_transfer.py` verifies cleaned source hashes, 28,247 original person-year pairs, source fixed-panel and future chronological model comparisons. GitHub Actions PASS: https://github.com/zuizui0223/egwee/actions/runs/38404369354.
- `scripts/audit_heliconia_raw_inflor_zero_provenance.py` verifies the Latin-1 original raw file by its Git blob SHA, joins only unique plot/tag/subplot identifiers, records genuine zero/positive entries and source correction conflicts. GitHub Actions PASS for the initial provenance audit: https://github.com/zuizui0223/egwee/actions/runs/38405340609. Strict additional morphology-stratified raw-only check **passed**: https://github.com/zuizui0223/egwee/actions/runs/38405672751. The matched-original-record **forward-year** prediction sensitivity **also passed**: https://github.com/zuizui0223/egwee/actions/runs/38406225194. The strict prediction does not remove observational/detection ambiguity; it qualifies the missing-value transformation explanation.
- Full results are archived by these workflows as machine-readable JSON, without modifying the frozen data/manuscript counts.
- The same ecosystem was already published and examined for seed/safe-site and climate effects. The core PR #52 remains **draft**, `submission_ready=false`, and the original phase-one baseline in `main` has not been changed.

## 14 October sharper history-order falsification

A separate [source-hash-verified comparison of the *order* of two prior flowering records](HELICONIA_HISTORY_ORDER_STABLE_PROPENSITY_FALSIFICATION_2026-10-14.md) now conditions on exactly **one documented positive in the preceding two seasons**. Unlike a single preceding-year OR, this `01` versus `10` contrast narrows the stable-plant-propensity explanation under an explicitly defined additive-individual-and-calendar-logistic null. Original-entered numeric-zero/positive verification plus three consecutive alive/observed-year records leaves **960** individual-year sequences (core middle years `t=2001–2004`): adjusted MH recency OR **1.210**, **1.124** using finer height bands, versus cleaned-file OR **1.358** on 1,207 sequences. Raw-confirmed leave-one-calendar-transition odds shrink to **1.044** or **1.037** after omitting some years, and one regional deletion yields no finite source-confirmed stratified OR. These findings **do not identify stable propensity or rule out a small/heterogeneous causal short-term carry-over**.

The genuinely earlier-years-only *order* forecasting comparison also fails to improve utility: raw-confirmed Brier **0.168541** with height/shoot morphology versus **0.170239** after adding order (`01` or `10`); corresponding cleaned data **0.168836→0.170664**. Both outcomes are recorded positive inflorescence status, **not** biological mating or seedling recruitment. This correction does **not** undo the earlier strong one-lag association; it separates *one prior positive record* from *recency conditional on the same number of prior positives*. Detailed rerun: https://github.com/zuizui0223/egwee/actions/runs/38421487168 (PASS). All claims remain exploratory within one published programme; frozen EGWEE source denominators and submission status unchanged.
