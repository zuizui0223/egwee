# Spatial transfer does not certify temporal recruitment sentinels: source-pinned forward-year audit (2026-10-10)

## Scope and priority

**EGWEE empirical fragmentation ecology**, not the theoretical EGWE/NEE programme. This is an external **within-one-species/one-landscape, post-outcome-inspection** audit of a published dataset. It does **not** add any independent ecological programme or effect to the frozen EGWEE 5/8/16-programme denominators or the SF06 sign subset. Main manuscript effects and submission gates remain unchanged.

Question: **Is a demographic indicator that predicts recruitment across new plots/ranches in the same year also useful for predicting recruitment in future years?** And do flowering→recruitment lags explain non-transfer if measured under the same observation completeness standard?

The public *Heliconia acuminata* census archive (Bruna et al. 2023 *Ecology*, doi:10.1002/ecy.4174; Dryad doi:10.5061/dryad.stqjq2c8d) has 66,396 plant-years, 8,586 recorded individuals, 3,464 first-marked seedlings, and 13 0.5-ha plots across three ranches. This is one previously studied ecological system, **not 13 independently randomized landscapes**.

## Correct observation denominator

A previously verified all-missing census defect affects CF-4/CF-5 in 2000 and CF-6 in 2003; 565 plant-year records were all `missing`, and 513 of the same IDs were subsequently confirmed alive in the following year. Thus no measured plants cannot automatically be interpreted as no living plants or no recruitment. See `HELICONIA_LAGGED_FLOWERING_SENTINEL_2026-10-10.md`.

To compare **lag 1, 2 and 3** flowering on exactly the same rows, the forward audit uses outcome years 2001–2005 and predictor census years `t-1`, `t-2`, `t-3`. Each relevant census must include at least one confirmed measured plant. From 65 potential plot-years, **9 slots are excluded** due to prior/outcome all-missing plot-years, leaving **56 analyzable plot-years**. Forecast test years 2003, 2004, 2005 contribute **34 predictions**; the other 22 are available before the first forecast. Candidate models, observation status selection and forward folds were defined after earlier results were seen; all outcomes remain held out from each future-year fit.

## A genuine spatial-versus-temporal reversal in the specified simple models

The earlier [same-calendar-year held-out-ranch audit](HELICONIA_LAGGED_FLOWERING_SENTINEL_2026-10-10.md) let each model estimate its year intercept from *other plots' recruitment outcomes in the same year* and found prior living stock better than flowering. That is a valid conditional spatial transfer test, **not a future-year forecast**.

The new `scripts/audit_heliconia_forward_lag_prediction.py` has **no test-year response information** in fitting: train all earlier outcome years and predict the next calendar year across eligible plots. Ridge coefficients, feature means/scales and intercept are re-estimated in every chronological fold. Candidate fixed linear models use Gaussian squared-error prediction with non-negative clipping; ridge penalty 1 after within-training-fold standardization. These are descriptive predictive rules, not count-likelihood/capture models.

| Prediction rule | Strictly future-year MSE, 34 plot-years | Interpretation |
|---|---:|---|
| Earlier-year mean new recruits only | **467.61** | strong simple baseline |
| Earlier-year 2-year recruitment history per plot | **345.42** | exploratory best among the examined models |
| One prior-year recruits | 494.06 | not enough |
| Prior living stock (linear ridge) | **867.37** | fails temporal transfer relative to baseline |
| Recruitment proportional to prior living stock (trained rate) | **722.63** | nonlinear/intercept alternative still fails |
| Prior documented flowering, lag 1 | **1444.90** | unstable; very poor in 2004 |
| Prior documented flowering, lag 2 | **1444.75** | unstable |
| Prior documented flowering, lag 3 | 503.43 | closer to baseline, not an improvement |
| Prior living stock + lag 1 flowering | 1420.18 | adding flowering did not rescue transport |
| Stock plus all three flowering lags | 1100.97 | no support for incremental flowering benefit |

This does **not** prove a general demographic memory law: (i) the 2-year model was added after observing earlier results, (ii) there are only three held-out years and one source ecosystem, (iii) annual weather and detection vary, (iv) a lagged flowering count is not measured seed rain, (v) predicting detected recruits is not forecasting a fully corrected biological transition, and (vi) models differ in estimator and assumptions. **Do not identify an ecological seed-bank duration from the favourable lag-3 result.**

## What failed: the recruitment–stock translation itself shifts over years

Under the consistent three-lag observability filter, the apparent ratio of newly detected seedlings to the previous census' total measured living plants varies strongly:

| Outcome year | Sampled plots | Mean observed new seedlings | Mean previous living stock | Aggregated detected new / prior measured stock | Within-year cross-plot OLS slope |
|---|---:|---:|---:|---:|---:|
| 2001 | 11 | 32.45 | 397.91 | 0.0816 | +0.1165 |
| 2002 | 11 | 42.55 | 434.36 | 0.0979 | +0.1178 |
| 2003 | 10 | 14.10 | 498.80 | 0.0283 | +0.0333 |
| 2004 | 12 | 26.92 | 426.50 | 0.0631 | +0.0202 |
| 2005 | 12 | 17.58 | 437.58 | 0.0402 | +0.0317 |

These ratios are *neither* true per-reproductive-adult birth rates *nor* causal fragmentation effects. Living stock includes nonreproductive stages, and apparent newly detected seedlings have unknown undetected arrivals. Plot composition also differs across years in this first table.

### Fixed-site falsification of the composition-only explanation

Intersecting the eligibility sets leaves the **same ten plots in all five years** (50 eligible plot-years; 30 strictly future-year forecast rows). Their yearly means are:

| Year | Mean recorded new seedlings | Mean prior living stock | Detected new / prior measured stock |
|---|---:|---:|---:|
| 2001 | 34.5 | 437.5 | 0.0789 |
| 2002 | **44.5** | **455.0** | **0.0978** |
| 2003 | **14.1** | **498.8** | **0.0283** |
| 2004 | 30.5 | 482.5 | 0.0632 |
| 2005 | 20.4 | 494.8 | 0.0412 |

Thus from 2002→2003, **new seedling entries fall ~68% while prior living stock rises ~9.6% in these same ten plots**. The apparent recruitment/stock ratio falls about **71%**. **9 of the 10 plots individually have fewer first-recorded seedlings in 2003 than in 2002.** This is source-based evidence that previous population size cannot by itself guarantee stable annual recruitment in the observation record; it is **not** proof that seed viability, climate, mate quality, or true demographic survival caused the fall.

The 2002→2003 decline is not confined to a single ranch or habitat category within those same ten plots:

| Fixed-site group | Plots | New entries per plot in 2002 → 2003 | Prior living stock per plot in 2002 → 2003 |
|---|---:|---:|---:|
| Dimona | 3 | 7.0 → 4.0 | 180.0 → 185.7 |
| Esteio | 5 | 70.2 → 22.0 | 630.6 → 691.0 |
| Porto Alegre | 2 | 36.5 → 9.5 | 428.5 → 488.0 |
| Continuous forest | 3 | 96.3 → 26.3 | 811.3 → 899.3 |
| Fragmented forest | 7 | 22.3 → 8.9 | 302.3 → 327.1 |

These summaries partition the **same ten plots two different ways**; they are **not additional independent replications**. They support a geographically shared temporal change in **recorded** recruitment and reject a pure single-ranch or single-habitat compositional explanation. No synchronized causal driver is identified, because year-specific observation, regional climate and seed-stage opportunity remain unmeasured in this reanalysis. Reproduced at https://github.com/zuizui0223/egwee/actions/runs/38046390486.

To guard against differing plot composition driving the prediction reversal, fully forward-year prediction of this ten-plot balanced panel again gives:
- prior-year mean baseline MSE **496.76**;
- two-year previously recorded recruitment history **385.95**;
- prior living stock **1012.59**;
- lag-one recorded flowering **1628.64**;
- lag-three recorded flowering **563.39**.

The **spatial-to-temporal failure** persists with identical plots throughout. The small three-year temporal sample and post hoc model menu prevent any confirmatory model superiority claim.

## Ecological interpretation: an interaction quantity versus demographic state distinction at a new observation scale

Two biological alternatives remain live:

- **Temporal recruitment opportunity / climate filtering:** a shared bad recruitment year can occur despite a sizable standing population, because viable seed arrival, suitable germination microhabitats and early survival need not co-vary tightly with total population stock. External controlled *Heliconia* seed-germination and fragmentation findings already support such pathways (Bruna 2002, doi:10.1007/s00442-002-0956-y). Thus the pathway is not an EGWEE discovery.
- **Climate-delayed vital rate + observation heterogeneity:** the same research system already exhibits climate impacts delayed by up to 36 months on survival, growth and flowering (Scott, Uriarte & Bruna 2022, doi:10.1111/gcb.15900); changing year-specific visibility or census effort may also alter the observed recruit count. Neither causal branch is separable in this audit using its currently extracted predictors.

The **general methodological phenomenon** that spatial CV alone does not certify temporal transfer is already established in ecology (e.g. Wenger & Olden 2012, doi:10.1111/j.2041-210X.2011.00170.x); EGWEE cannot claim this as a new principle. The useful project-specific contribution is auditing the exact *observation-and-stage conditions* under which the prior positive same-year indicator ranking fails as a future-year indicator.

The next genuinely independent falsification requires a full plot-year and organism-level observation model (missing/not-detected versus alive/dead), external weather/rainfall and safe-site proxies, source-resolved flower→viable-seed→recruit cohorts, and explicit comparison of field interventions or independently held-out study landscapes. A future-day climate predictor must be information-available by forecast issue date, not retrospectively filled with future realized weather. Realized downstream recruits per fixed habitat footprint remain the final conservation outcome.

## Reproduction, freeze and evidence ceiling

- `scripts/audit_heliconia_forward_lag_prediction.py` hashes/checks upstream archive via `analyze_heliconia_census_panel.load_csv`, verifies 66,396 rows, 3,464 marked seedlings and the exact three all-missing plot-years, reconstructs all years and forecast folds.
- `.github/workflows/heliconia-forward-lag-prediction.yml` runs a deterministic source-pinned audit and archives the full results.
- CI: https://github.com/zuizui0223/egwee/actions/runs/38046204079 (PASS).
- All reported rankings were formed *after viewing historical outcomes* and must remain **exploratory, one-system, non-causal, non-confirmatory**.
- Do **not** alter the EGWEE five-primary, eight-matched, 16-programme, or SF06 denominators; do not promote the leading 2-year model or the 2003 contrast to a universal biological law or as independent ecological replication.

## 10 October individual-ID and time-ordered climate competitor check

The independent [flowering/observation/weather timing audit](HELICONIA_RECRUITMENT_PULSE_MECHANISM_DISCRIMINATION_2026-10-10.md) sharpens but does not causally resolve the apparent 2002–2003 recruitment pulse: the same 10 plots had recorded prior-year flowering individuals **23.6→11.6** (10/10 declined), new seedlings **44.5→14.1** (9/10 declined), while old tagged plants' next-year status ascertainment was **97.14%→95.97%** (continuous subset **97.58%→97.66%**). This tagged-plant observation measure does **not** identify new-seedling detectability. Contextual NASA POWER rainfall **2001→2002** remained nearly unchanged (2261.59→2249.81 mm), whereas full **2003** rainfall was lower (1877.14 mm) but may include rainfall *after* a possibly February census. It is temporally invalid to use future-month climate to explain an earlier demographic census without field-specific dates. Flowering-to-recruit bookkeeping ratios change in opposite directions among ranches, not one common stage conversion. **No causal mating, climate, microhabitat or detection explanation is identified.**
