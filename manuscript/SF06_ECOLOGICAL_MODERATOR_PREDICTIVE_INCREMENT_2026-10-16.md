# Classical reproductive moderators do not rescue held-source pollination-to-female-fitness prediction (2026-10-16)

## Scientific question, status and prior art

**Post hoc exploratory prediction audit in empirical `egwee`; NOT theoretical `egwe`.** This analysis is a restricted, already-published supplement reanalysis, not an independent new data source or a replacement for the primary published meta-analysis. It changes **zero** primary EGWEE effect/cluster denominators, eight matched I–F programmes, sixteen-programme map or the previously frozen SF06 sign-pair counts. PR #52 stays draft and `submission_ready=false`.

**Question:** can reproductive assurance or pollinator guild categories help translate a known quantitative habitat-fragmentation effect on *pollination* into the associated quantitative effect on *female reproductive fitness* in a genuinely different publication?

Prior work makes this a biologically motivated, but **not original**, predictor hypothesis: Aguilar et al. (2006), *Ecology Letters* 9:968–980, doi:10.1111/j.1461-0248.2006.00927.x, showed average habitat-fragmentation sensitivity differs by plant compatibility system. The broader updated analysis `Anthropogenic land-use change decreases pollination and male and female fitness in terrestrial flowering plants` (2025 online full text https://pmc.ncbi.nlm.nih.gov/articles/PMC11805932/) likewise reported stronger average negative effects in self-incompatible plants and invertebrate-pollinated species.

**Important distinction:** whether compatibility predicts *average susceptibility to habitat degradation* is not the same question as whether it improves prediction of *which female-fitness effect accompanies an already observed pollination effect in another paper*. We evaluate the latter **predictive increment**, without asserting the former trait relationship is false. The full original published synthesis is broader than this public-fragmentation-only, paired numeric subset.

## Source and effect-scale gate

The source is the pinned public Supplementary Table S1 derivative `evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv`, exact Git blob `80edf240425c0e4439a276176bc1996c651fab92`. The machine-checker refuses changed input bytes or unexpected counts.

Distinguish **separate estimands and eligible denominators** rather than silently mixing them:

| Data universe | Paired units | Reason |
|---|---:|---|
| All physical public-S1 paired land-use effects | **59** | Includes non-fragmentation uses |
| Habitat fragmentation, sign-consensus endpoints | **54** | Original sign-sentinel diagnostic; mixed constituent sign excluded |
| Habitat fragmentation, continuous numeric `d_I/d_F` | **55** | Includes one additional numeric estimable but sign-mixed case |
| **Known SI/SC in numeric frame, fixed for EVERY model below** | **49** (27 publications, SI 28 / SC 21) | Allows trait comparisons on identical targets |
| Same but source-publication disjoint from the frozen EGWEE I–F map | **26** (18 publications, SI 14 / SC 12) | Separate source-overlap sensitivity |

The 49-pair continuous numeric frame is **not** the 54-pair consensus sign frame and is **not** a new independently sampled meta-analysis. Both `d_I` and `d_F` are Hedges-d-type standardized effects extracted from heterogeneous study endpoints with limited synchronized site/year or joint covariance information. Publication-level effect direction and uncertainty remain important.

## Held-publication quantitative prediction

Every held-publication fold removes **all species rows contributed by that source** before fitting. The held publication's outcomes are never used to select coefficients, rescale covariates or tune the intercept within that fold. We fit an intercept (context only), numeric pollination effect `d_I`, SI/SC system alone, `d_I + SC`, and exploratory specialist/generalist, vertebrate/invertebrate or interaction extensions.

For all models, use **identical** 49 (or 26) scored units. The source-level ridge model sets `lambda=1` on training-standardized covariates with the intercept unpenalized, and tests `0.1` and `4` as post hoc sensitivity; the main table is **equal-row training and equal-row scoring**. Outcome is held-publication mean squared error (MSE) on quantitative female-fitness effect `d_F`, not the binary sign.

| Predictor | Full 49 pairs / 27 papers | EGWEE-source-disjoint 26 pairs / 18 papers |
|---|---:|---:|
| Context-only intercept | **0.395171** | **0.519519** |
| Plant breeding system (SI/SC) alone | 0.410250 | 0.531824 |
| **Continuous pollination change `d_I` alone** | **0.383411** | **0.502302** |
| Continuous `d_I` + SI/SC | **0.399648** | **0.529272** |
| Continuous `d_I` + vertebrate/invertebrate | 0.392268 | 0.519653 |
| Continuous `d_I` + specialist/generalist | 0.391531 | 0.525046 |

Against the context-only model, `d_I` alone reduces MSE **2.98%** in the full 49 and **3.31%** in the disjoint 26. However, **adding SI/SC to `d_I` increases error 4.23% and 5.37%, respectively**, *relative to the already better `d_I`-only model*. Compatibility system alone is worse than context only. The other coarse guild labels also fail to improve on `d_I` in these particular linear score rules.

The same qualitative conclusion about **lack of positive SI/SC incremental value** holds when training publications are **given equal aggregate weight**: on the full cohort, `d_I` alone MSE **0.377402** versus `d_I + SC` **0.389260**; in the disjoint cohort, `d_I` **0.513932** versus `d_I + SC` **0.545744**. There is **not** a universal gain from `d_I` however: in the 26-pair disjoint corpus, *equal-publication* outcome scoring after publication-balanced fitting slightly prefers context only (0.420782 versus 0.424385); this prevents generalizing modest row-weighted `d_I` gain to every utility metric.

## Source deletion: not one dominant publication, but still small-sample and model-dependent

A **nested leave-one-publication-deleted** audit recomputes complete LOPO prediction after removing each publication from the eligible population:

| Matched frame | Deletions where `d_I` beats context by row-weighted MSE | Deletions where adding SC improves `d_I` |
|---|---:|---:|
| Full 49 / 27 publications | **27/27** | **0/27** |
| Nonoverlap 26 / 18 publications | **15/18** | **0/18** |

This persists as a *negative SI/SC increment* in both the equal-pair and equal-publication **training-weight** analyses at the chosen penalty. In the disjoint 26-pair subset, the `d_I` improvement can turn negative after deleting certain sources (range of baseline minus `d_I` MSE **−0.00959 to +0.04271**). So the mild `d_I` benefit is **not source-deletion invariant** in the smaller independent-source subset.

### Measurement-precision and species-level sensitivity (important limit to the modest `d_I` benefit)

Repeat **the same held-publication outcomes** but refit using inverse variance weights proportional to `1/(var_F+floor)`, with exploratory `floor=0,0.1,0.5`; predictions are still scored using unweighted held-source squared error. This is **not** a full errors-in-variables meta-regression because `d_I` sampling variance and within-pair `d_I/d_F` covariance are not modeled.

| Training weight and frame | Context-only | `d_I` only | `d_I + SC` |
|---|---:|---:|---:|
| Full 49, `1/var_F` | 0.416236 | **0.397240** | 0.400914 |
| Full 49, `1/(var_F+0.1)` | 0.399136 | **0.386343** | 0.398058 |
| Disjoint 26, `1/var_F` | **0.547989** | 0.548385 | 0.583103 |
| Disjoint 26, `1/(var_F+0.1)` | 0.531220 | **0.514200** | 0.540309 |

The source-disjoint **unfloored** precision-weighted `d_I` model is **marginally worse** than the intercept-only model (0.548385 vs 0.547989). This is one reason **not** to claim an invariant general `d_I` predictive advantage across all representations and weights. The **SC add-on fails to improve over `d_I`** in all the displayed precision scenarios, as well as at floor 0.5 and the main equal-pair/equal-publication fits.

Holding out **species instead of publications** and training with equal row weights likewise does not support SC incremental value: the full 49-pair female-effect MSE is `d_I=0.381625` versus `d_I+SC=0.395026`; the disjoint 26-pair MSE is `d_I=0.515006` versus `d_I+SC=0.551324`. Species-held-out does **not** block shared publication methods; the publication-held-out test remains the stronger source-independence diagnostic.

For coefficient shrinkage `lambda=0.1` or `4.0`, the full and disjoint selected frames with equal-row training likewise do not show a positive `SC` add-on, but shrinkage and variance-floor choices are **post hoc method sensitivities**, not a new confirmatory selection procedure.

The final JSON contains these species-held-out predictions, alternative shrinkage strengths, source influence deletions and SI/SC × `d_I` interaction models. They are part of **sensitivity and falsification**, not support for post hoc selection of a best ecological moderator.

## Biological interpretation and limits

1. **Average trait susceptibility is not the same as a sufficient process→function sentinel.** A biological trait linked to average plant vulnerability under landscape change need not transport to a conditional predictive model that already knows the magnitude of the upstream pollination response.
2. **Continuous pollination effect has a modest transferable signal in these models.** This is compatible with the positive average quantitative regression in the frozen SF06 subset, and separately with failure of binary sign-only probability prediction. Do not say that pollination is wholly uninformative.
3. **SI/SC is not the same as realized reproductive assurance.** SC plants may still require pollinator-mediated geitonogamy and outcrossing; pollen quality, available compatible mates, autonomous selfing ability, dominance of viable self pollen, pollinator identity and post-pollination loss are not measured in this trait-only audit. A lack of incremental SI/SC MSE improvement **does not show breeding system is ecologically irrelevant** or that a more informative mating-quality variable would fail.
4. **Source-specific confounding remains.** Species, family and publication extraction are not independent randomized contrasts, data are highly uneven across source studies, and reported endpoint variances differ. Publication and species deletion tests are diagnostics, not independent replications or calibrated inferential intervals.
5. **No predictive universality or mechanism is established.** Changing loss targets, coefficient shrinkage, measurement uncertainty models and genuinely prospective landscapes could change the results; no post hoc tested model should be declared universally optimal.

**Next mechanistically discriminating test:** do directly quantified compatible pollen delivery, outcross siring/donor diversity, and viable seed arrival explain *held-landscape recruitment shortfalls* over and above interaction frequency, coarse breeding-system labels and standing population stock? This requires synchronized, jointly observed stages or randomized pollen × safe-site interventions; the present source subset cannot answer it.

## Reproduction, workflow and freeze

- Executable pinned-source checker: `scripts/audit_sf06_moderator_held_publication_transfer.py`
- CI: https://github.com/zuizui0223/egwee/actions/runs/38920896277 — **PASS**, including held-species and marginal female-effect precision-weight sensitivities; archived `build/sf06_moderator_transfer_v1.json` includes exact denominators, 2 training weightings, penalty sensitivity, source deletions, species-held-out scores.
- Main egwee `main` remains unchanged, PR #52 remains **draft**, `submission_ready=false`. The unrelated submission-freeze contract intentionally fails if the evolving manuscript hash differs from the dated frozen manifest; this is **not** a license to relax the gate.
