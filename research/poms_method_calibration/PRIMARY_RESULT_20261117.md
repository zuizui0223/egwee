# PoMS 2017–2023 original-observation same-day method calibration — first confirmed outcome
## 2026-11-17 | PR #60 | Source-pinned preregistered primary estimator

**Status: primary contrast estimated, bootstrap interval spans zero.** This is a new *empirical original-observation analysis* in `egwee`, NOT evidence of causal pan-trap bias, pollinator abundance change, successful pollination, genetic rescue, or NEE/EGWE theory verification.

### Provenance
- Original full design: `PROTOCOL_20261117.md`, committed *before any outcome counts* (`4109adf`).
- Strict source field and site-date identifier audit: `SOURCE_ID_GATE_RESULT_20261117.md`, 95 sites/1,221 matched events with no numeric bee/flower outcomes opened.
- **Signed-outcome estimand freeze**: `OUTCOME_ESTIMAND_FREEZE_20261117.md`, committed before opening outcomes (`efe66bb0b2c037e6bdb50fd1643de4f4373bd9c0`).
- Implementer: `analyze_poms_paired_method_flora.py`. CI synthetic FE slope identity test succeeded. Actual derivative-only GitHub Actions run [44012285228](https://github.com/zuizui0223/egwee/actions/runs/44012285228) SUCCESS; the 1,000 site bootstraps all completed. Original EIDC CSVs were checked against pinned *uncompressed* member digests in the preregistered audit and are not redistributed.
- Source pan DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`; 1-km FIT DOI `10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618`. Self-selected public FIT excluded.

### Sample gate
- 7,050 raw pan samples, 3,053 1-km FIT samples.
- **1,221** exact square×date matches across **95** source sites, **2017–2023**.
- **249** matched date events lacked a bee+hoverfly observation total in one or both methods, so they cannot estimate the relative bee-to-hoverfly composition. Zero-pan event totals = 77, zero-FIT event totals = 204; these categories overlap and must not be summed as exclusive.
- Exactly **972** matched same-site same-date events retained, all **95** sites and all **7** years, with **86** sites contributing within-site flower-incidence variation.
- Flower source links **12,847/12,858** rows, with 11 orphan occurrence IDs excluded; none of the linked rows have empty prespecified source taxon keys.
- Eligible shared floral incidence: mean **1.827126** taxa per pan station, SD **1.174663**; observed site-date range **0–7**.

### Primary predeclared fit
At each valid site-date compare `Y_FIT=ln((bee_FIT+.5)/(hoverfly_FIT+.5))` to `Y_pan=ln((bee_pan+.5)/(hoverfly_pan+.5))`. The event-level difference `D=Y_FIT-Y_pan` is regressed on standardized *common pan-sampled floral taxon incidence*, site fixed effects, year and month, equal weight per matched event. Model and group definitions locked before signed outcomes.

| Parameter | Result |
|---|---:|
| FIT bee: hoverfly log ratio slope | **−0.015379287757** |
| Pan bee: hoverfly log ratio slope | **+0.035728652324** |
| **FIT minus pan differential slope (primary)** | **−0.051107940081** |
| **Site cluster bootstrap 95% percentile interval (1,000/1,000; seed 20261117)** | **[−0.172265033104, +0.094494312792]** |
| Fraction of site-bootstrap deltas positive | **0.222** |
| Leave-one-site-out: 95 fits | **−0.088615 to −0.032171; all negative** |
| Leave-one-year-out: 7 fits | **−0.081261 to −0.014080; all negative** |
| Excluding events with no recorded pan flowering taxon (956 events) | **−0.048519097139** |
| Total bee+hoverfly-count-weighted secondary slope | **−0.147610404614**, no confirmatory interval |

### Ecological conclusion and generality boundary
There is **directional stability of a negative method-by-flowers differential**, including every leave-site and leave-year deletion, but **no resolved sign at the predeclared site-block uncertainty level**: the 95% interval includes zero. Changing from equal-event to total-count weighting increases the negative point estimate; this cannot be promoted post hoc to a new primary effect or statistical significance claim. **No method-specific community response divergence is established**.

The likely reasons this remains unresolved include observation target differences (FIT observes one selected flower species, pan traps sample passive potential visitors), 10-minute vs ~6-hour effort, sparse bee/hoverfly FIT counts, and weather/habitat covariates. These are *candidate competing explanations*, not mechanisms identified from this model. No functional pollen deposition, viable seed, recruitment, genomic state, or partner contribution were measured.

**Novelty limit:** the UK PoMS 2026 study (DOI `10.1002/2688-8319.70327`) already compares survey methods and includes flower richness environmental models. We are **not** claiming that pan/FIT differ or flower environment affects trap catches is novel. A distinct same-date, same-1km-square, jointly sampled floral-context interaction was tested here, but this result is statistically inconclusive, and the paper-level generalization beyond UK or across functional ecology is not established. The result should remain a documented pilot / calibration analysis, not the lead claim of an independent research article.

### Future work gates (not yet executed as this result)
- Inspect first published PoMS environmental study's supplemental model details for its treatment of coincident dates (prevents duplicate publication of a previously tested estimand).
- Confirm if null-like differential persists in a separate source-native bee/hoverfly direct-interaction dataset with independent units; do not search for a significant result to repair this preliminary analysis.
- Evaluate weather (wind/sun), FIT target-flower selection, and real trap effort in **explicit, separate exploratory models**; do not reinterpret this primary fixed effect as corrected pollinator abundance.
