# Lagged flowering is not an adequate substitute for living-stock history in the Heliconia public census: observation-screened predictive audit (2026-10-10)

## Status, source, biological question

**Post hoc external within-programme reanalysis** in the empirical EGWEE fragmentation project. Not EGWE/NEE operator theory; not independent cross-species replication, not a new causal demographic law, and no addition to any frozen five-cluster, 8 matched I–F, 16-programme or SF06 effect denominator.

Archived Bruna et al. (2023), *Ecology*, doi:10.1002/ecy.4174, Dryad doi:10.5061/dryad.stqjq2c8d. Reuse the source commit and exact Git blob hashes pinned in `scripts/analyze_heliconia_census_panel.py`; plot/year/plant identifiers and annual census statuses are checked before modeling.

Ecological question: **Does the number of documented reproductive plants (or inflorescences) in a preceding year predict first-detected seedling recruits in a new forest plot or ranch better than simply knowing the number of previously observed living plants?**

The original archive records **66,396 plant-years, 8,586 plants and 3,464 first-recorded seedlings in 13 0.5-ha plots** (6 continuous, 7 fragmented). The fixed response window is **1999–2005**, with previous-year predictors from **1998–2004**. Across all archived plot-year slots, this includes 2,590 first-recorded seedlings. The field source records flowering indicators and inflorescence counts, but it does **not** record matched pollen compatibility, fertilization, same-mother seed-to-seedling fate, viable seed arrival, or safe-site coverage.

## New source-level observation problem: whole-plot apparent zeroes

Three archive plot-years contain numerous plant-status records but **every single plant is `missing`**, with zero `measured`, zero `dead`, zero newly recorded seedlings:

| Continuous-forest plot/year | All missing | Same IDs alive at previous census | Same IDs alive at following census |
|---|---:|---:|---:|
| CF-4, 2000 | 116 | 113 | **111** |
| CF-5, 2000 | 171 | 170 | **155** |
| CF-6, 2003 | 278 | 266 | **247** |
| **Combined** | **565** | **549** | **513** |

The **513 re-detected survivors** disprove reading the three annual rows as whole-population death/extinction. Although the precise reason for the all-missing coding needs the original survey metadata, a year with no individual measured and all pre-existing individuals missing is **not a defensible denominator-complete biological zero for newly established seedlings**. This is different from individual-level later reappearance previously audited.

This finding **qualifies** past “seven balanced annual census years” language in EGWEE: the calendar grid is balanced, but **observation is not complete at the plot-year level**. A count of zero first-marked seedlings in these three years is best treated as a zero **recorded** entry with uncertain biological observability, not as confirmed zero recruitment.

Excluding the three all-missing outcome cells only (not their adjacent exposures) changes the equal-plot mean of recorded recruits per observed year in continuous forest from **36.9286** to **37.6310**; fragmented forest remains **21.2041**. Requiring both predictor and response censuses to contain confirmed living plants excludes six plot-year pairs, giving **85 of 91** analyzable plot-years: continuous **36**, fragmented **49**; the continuous equal-plot mean becomes **37.9143** and fragmented remains **21.2041**. These are alternative **descriptive observed-cell means**, not imputed rates or causal fragmentation contrasts. Screening on presence of living plants may itself exclude genuine zero-population sites in other datasets; here subsequent resightings motivate a missing-observation sensitivity.

## Reproductive-indicator source coverage

At the 1998–2004 lagged flowering years, each of the three ranches has at least one plot with a documented flowering record; the number of plots with positive flowering ranges from **10 to 13** per year. The recorded flowering individuals across all plots by year were **242, 213, 116, 254, 120, 395, 173**, respectively. The number of inflorescences was **261, 236, 119, 290, 132, 473, 196**, respectively.

These are *documented positive flowering* counts. An `infl=NA` cannot be assumed to represent a verified flowering zero without an observation protocol. Thus no conclusion about true flowering absence or population fecundity can follow from the naive lack of a record.

## Prediction: entire plot or ranch held out

We fit a simple predeclared-in-code **year-intercept linear ridge model** for the number of *first-detected* seedlings in year t, with ridge penalty 1 on within-training-year standardized predictors, clipping negative predictions to zero. Every training transformation and coefficient is recomputed after holding out the *entire plot* or *entire ranch*. All models use the **same 85 observation-screened plot-year rows** for comparison. The primary outcome is equal-plot-year MSE of unseen observations, not per-individual significance.

| Predictors from t−1 (plus training-year intercepts) | Held-out plot MSE | Held-out ranch MSE |
|---|---:|---:|
| Year intercept only | 1108.48 | 1721.54 |
| Habitat fragmentation category | 1136.88 | 1907.44 |
| **Observed living stock** | **652.12** | **1025.24** |
| Documented flowering individuals | 869.43 | 1203.97 |
| Documented inflorescences | 894.92 | 1255.59 |
| Living stock + flowering individuals | 692.80 | 1042.09 |
| Living stock + inflorescences | 685.35 | 1056.05 |
| Living stock + habitat | 668.05 | 1024.89 |

Relative to the year-only reference, stock reduces held-out plot MSE by **41.17%** and held-out ranch MSE by **40.45%**. Recorded flowering has predictive association alone but **does not yield incremental improvement** once living stock is present under either held-out metric; the combined stock+flowering model scores worse than stock alone (plot MSE **692.80 vs 652.12**, ranch **1042.09 vs 1025.24**).

The unscreened 91-slot analysis gives the **same rank ordering** among stock, flowering and stock-plus-flowering, but uses the three all-missing outcomes as numeric zero. For transparency, unscreened plot MSE: year-only **1139.63**, stock **660.17**, flowering **890.30**, stock+flowering **702.78**.

## Interpretation and falsification boundary

**Supported narrow descriptive result:** within this one re-used Heliconia census archive, observed prior living stock is a better out-of-plot and out-of-ranch predictor of later detected seedling entries than positive flowering record counts. A simple additive flowering indicator does not improve held-out MSE over prior stock. The result persists after removing the three observation-blackout cells and the following exposure windows.

**NOT supported:**
- pollen flow, pollinator identity, mating quality or reproductive effort are ecologically unimportant;
- fragmentation influences recruitment *only* through stock rather than through safe sites, viable seeds, dispersal or detection;
- prior stock is a pre-fragmentation confounder: it is **post-fragmentation** and can embody the accumulated habitat effect;
- the 13 plots or three ranches support a universal prediction rule, or the 85 annual plot-years are 85 independent landscapes;
- the absence of a positive `infl` record certifies zero flowering or zero seed contribution;
- reduced MSE is evidence of equal biological recruitment rates or successful restoration leverage;
- this is a new stage-switch law. Relevant recruitment/demographic effects in *Heliconia* were already studied by Bruna (2002, 2003) and Bruna & Oli (2005).

**Ecological implication for EGWEE:** the next measurement target should be the actual state transition from **viable propagule production/arrival to observed recruitment**, with explicit whole-patch opportunity and detection. The result weakens any temptation to promote **reproductive activity** as a sufficient replacement for a stand-alone recruitment sentinel, but it cannot diagnose which hidden demographic path causes the mismatch.

## Reproduction and corrective use

- `scripts/audit_heliconia_lagged_flowering_sentinel.py` recomputes from the source-hash-verified archived CSVs and fails on unexpected all-missing plot-year fingerprints.
- `.github/workflows/heliconia-lagged-flowering-sentinel.yml` runs both full-grid and observed-cell sensitivities and archives machine-readable results.
- Successful Actions run: https://github.com/zuizui0223/egwee/actions/runs/38045633290
- This is a **post hoc source audit**. No change to the frozen EGWEE corpus or current manuscript headline is licensed; previous balanced-calendar recruitment summaries remain provenance values but should carry an **observation-completeness warning**, not be silently overwritten.
