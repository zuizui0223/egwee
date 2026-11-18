# Environmental information beyond measured pollinator quantity: two retrospective plant systems

**Date:** 2026-10-19. **Status:** exploratory, source-locked, independent-unit, post hoc stress test in the empirical **egwee** programme. Not a preregistered new confirmation, not a new meta-analysis admission, and not validation of the separate theoretical **egwe** model.

## Question and admission boundary

Does the observed quantity of pollen tubes or flower-associated beetles fully identify the reproductive state of a fragmented plant population, or do independent, source-measured environmental and landscape covariates retain information?

This is **not** an invention of the response–effect distinction, nor evidence of a universal common mediator. The species, exposures and responses are not pooled into a single coefficient. These studies already belong to the registered EGWEE evidence universe; neither increments the frozen 5 direct clusters, 8 matched quantitative I–F programmes, 16-programme translation catalogue, or phase-2 coverage.

Sources: Llorens et al. (2018), *Eucalyptus wandoo*, [original published study](https://doi.org/10.3389/fevo.2018.00039), Tables 1 and 6; Elias et al. (2012), *Cardiopetalum calophyllum*, Table 1, as source-locked in \`evidence/meta_extraction/phase2_cf01_cardiopetalum_table1_v1.csv\`. The original Wandoo authors **already reported** salinity/fruit and size/seed associations and jointly considered EC versus size. This audit adds a same-unit *conditional on pollen tubes* and cross-system comparison, not a new causal mechanism.

## Wandoo: size and EC jointly conditional on pollen tubes

Independent unit: **population**, 11 common year-2 measured populations J/K/F/C/E/G/B/I/A/H/D. Model, fitted separately for each response, is:

\`response ~ intercept + pollen_tubes_y2 + log10(soil_EC) + log10(population_size)\`

All responses are original source population means. EC units mS/m. Both environmental predictors now enter the **same** model, unlike the initial two separate additions. Each has n=11, 4 coefficients and 7 residual degrees of freedom.

| Year-2 response | Joint EC coefficient | Nominal OLS p | HC3 t-reference p | Joint size p | Six-test Holm-adjusted EC p |
|---|---:|---:|---:|---:|---:|
| Fruits per branch | −129.052 | 0.01396 | 0.05634 | 0.48265 | **0.06981** |
| Fruit:flower ratio | −0.58408 | 0.00982 | 0.00832 | 0.94887 | **0.05891** |
| Seeds per existing fruit | −1.10094 | 0.55959 | 0.75601 | 0.06556 | **1.00000** |

Holm family: three reproductive responses × two contextual predictors = six exploratory added-parameter comparisons, jointly corrected. No joint-model coefficient survives this six-test correction. HC3 uses small-sample t with seven residual degrees of freedom as a **reference**, not exact heteroskedastic inference. Fruit count and fruit:flower ratio share fruit outcomes and therefore are **not** two independent experiments. Different significance across responses does not itself establish different causal mechanisms or a formal interaction-by-stage test.

### Sensitivities that must accompany the point result

- In the 11-population joint model, all 11 leave-one-population EC coefficients for fruits per branch and fruit:flower ratio remain **negative**. Excluding G makes the ordinary EC p rise to **0.13532** (fruits) or **0.06532** (ratio). Apparent strong point direction is not a leave-one-population significance guarantee.
- HC3 weakens the fruit-number result (p 0.05634) more than the ratio result (p 0.00832), warning against treating OLS p as distribution-free.
- Including the legitimate **zero-fruit** population L (n=12) gives joint EC coefficients **−84.767** (fruits; nominal p 0.02053, HC3 0.12931) and **−0.39708** (ratio; nominal p 0.01241, HC3 0.09221). Seeds per fruit for L remain **undefined**, never imputed zero.
- Restricting to the populations with source reproductive N ≥10 removes J and K. Within the common11 nine-population subset, joint EC coefficients remain negative (fruits **−156.808**, ratio **−0.6799**); the joint native12 high-N frame has only 10 populations and HC3 uncertainty widens. This restriction was chosen post hoc and is not independent corroboration.
- Leave-one-population-out RMSE for common11 fruit production: pollen-only **29.917**, pollen+EC (earlier model) **24.127**, fully joint EC+size **24.285**. For ratio: **0.13414**, **0.08511**, **0.095** respectively. For seeds per fruit: pollen-only **1.190**, size-only **0.972**, fully joint **1.263**. The fully joint model offers no consistent predictive improvement over simpler formulations. Several unbounded models predict biologically impossible negative quantities, which are never clipped or hidden.

**Sampling coverage warning:** among the 19 source Wandoo populations, seven have no reproductive table measurements. EC ≥20 mS/m is seen in **3/7 unmeasured** but only **1/12 measured** populations. This threshold is descriptive and not a prospectively defined salinity class. The complete-case sample cannot establish relationships for all 19, and source means/SEs do not enable error-in-variables adjustment for individual pollen-tube counts.

## Cardiopetalum: landscape area rather than local plant density

Independent unit: **forest fragment**, n=10 (not individual flowers/beetles). Published Table 1 provides area, nearest-fragment distance, plant density, beetle abundance per flower and fruit set. Fragmentation severity is **−ln(area_ha)**, and the response is reported fruit-set mean. These data have already contributed a retrospective area-gradient matched I–F result in EGWEE; this is **not** fresh evidence or a new gradient discovery.

| Fruit-set model | In-sample R² | Leave-one-fragment-out RMSE |
|---|---:|---:|
| Measured beetle abundance alone | 0.080 | 0.11562 |
| Beetles + −ln(fragment area) | **0.875** | **0.04654** |
| Beetles + ln(local plant density) | 0.084 | 0.12396 |

The conditional severity coefficient in the beetles+area model is **−0.043512** per 1-unit increase in −ln(area), nominal p **0.000286**, HC3 t-reference p **0.000390**. Across all ten whole-fragment exclusions, this coefficient remains negative (approximately −0.0403 to −0.0475). Plant density does not supply an analogous improvement in the tested simple model. The area association is already central to the original fragment-size ecology and cannot be interpreted as an independently identified downstream mechanism.

**Landscape scale warning:** the seven smaller fragments are only 2.16–33.8 ha, followed by 455–929 ha for three larger fragments, leaving a **13.46× unsampled gap** between 33.8 and 455 ha. This does not identify a biological threshold. The within-seven-small-fragments log(area)–fruit-set Pearson r is **+0.813** (nominal p **0.026**, descriptive), which shows that the direction is not determined solely by the large/small split, but still not by a randomized manipulation. The species is insect/beetle visited; unmeasured compatible pollen and other plant-resource conditions may matter.

## Ecological conclusion, evidence ceiling and follow-on test

Two independent landscape systems exhibit a **conditional quantity insufficiency** pattern:

1. In *Eucalyptus wandoo*, pollen-tube quantity and population size do not exhaust association of soil EC with the fruit-establishment measures, but the joint-model six-test multiplicity result is unresolved and robust uncertainty varies across the two fruit endpoints.
2. In *Cardiopetalum calophyllum*, measured beetle abundance does not exhaust the very strong fragmentation-area gradient in fruit set. Density does not act as a comparable simple substitute; area can represent many correlated habitat processes.

These systems support the **need for environment and plant condition measurements alongside interaction quantity**, not a general causal salinity or area law. They demonstrate that local environmental conditions are plausible *competing explanations* for the observed I–F mismatch, rather than proving downstream post-pollination filtering. EC and fragment area are not the same ecological moderator and cannot be meta-regressed as one predictor from two studies.

A genuinely new test would synchronously collect pollinator abundance/visitation Q, compatible-pollen provenance E, maternal resource conditions, fruit establishment, and seed filling F at independent landscape units, followed by explicitly source-independent study replication. For Sevenello 2026, the fixed pollen-addition × edge design remains **unexecuted** due to the Figshare source-download HTTP 500 blocker; do not manufacture those treatment outcomes.

## Reproduction and publication boundary

- Script: \`scripts/audit_if_environment_conditional_20261019.py\`
- Inputs: \`evidence/meta_extraction/wandoo_reproductive_stages_20261019_table{1,6}.csv\`; \`evidence/meta_extraction/phase2_cf01_cardiopetalum_table1_v1.csv\`
- CI: \`.github/workflows/if-environment-conditional.yml\` installs NumPy/SciPy, checks fixed numerical guardrails, and uploads complete machine-readable model/LOO output.
- Existing Wandoo source HTML/PDF concordance, including its validation checker, remains separate and unchanged.
- This note does not update the frozen submission headline, replace the user-approved manuscript, override its content-hash freeze, or change \`submission_ready=false\`. The existing monolithic contract still has external Figshare HTTP 500 retrieval failures at the Brosimum workbook step: a source-access blocker, not a pass.

