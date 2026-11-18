# QPF007: same-mother stigma-pollen quantity does not improve held-out genetic mating success in one *Brassica rapa* experiment

**18 November 2026 — postprimary exploratory predictor-stage audit; original source verified.** This is a separate QPF007 end-point follow-up on PR #85's original *Brassica rapa* source, NOT another natural fragmentation research programme, independent study or new confirmatory hypothesis. No theoretical `egwe` work is modified.

## Original source, precise stage and prior art

Barbot et al. (2026), [*Pollinator abundance shapes sexual selection in an angiosperm*](https://doi.org/10.1371/journal.pbio.3003579), *PLoS Biology*. Original data [Zenodo 10.5281/zenodo.21628183](https://doi.org/10.5281/zenodo.21628183). Author main plant table SHA256 `5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe`, original 1,967 stigma flower rows SHA256 `ec7217acb683a0d0475622f3510228f3062a72a8bfd17162888f160db369a495`.

The original authors already demonstrated pollinator abundance shifts sexual selection before vs after fertilization and that observing pollinator movement is not equivalent to counting offspring-inferred mates. **Those are their findings, not new EGWEE claims**. The new question is narrower: does **within-mother original stigma pollen count** add practical prediction of her **genotype-inferred genetic mating-success** relative to observed visits, experimental pollinator-density treatment, flower number and plant size, when a whole manipulated pollinator-observation session is held out?

Original source columns: `session × ID_full` unique mother, original `nb_visit`, `nb_flo_all`, `height_max`, `poll_treat`, source `pl_mean` from a separate stigma sample, literal `gMS_fem_all` genotypically inferred *female* mating-success. **Genetic mating success from offspring sampling is not viable offspring recruitment, the pollen donors on an excised stigma, or an original genetically compatible pollen receipt.** Same original plant, not same sampled flower; 16 session groups are manipulated replicate populations from one published experiment, not 16 independent countries/landscapes.

## Sequenced source-only check and postprimary model lock

A new [outcome-before-inspection exploratory source/design freeze](QPF007_GENETIC_MATES_PREDICTION_FREEZE_20261118.md) was committed at `2e28165b8be0149c9e4f8258619886a8b9ad31c4` before inspecting genetic target numeric direction or model losses. Since the seed endpoint was previously viewed on the **same mother source**, this is **postprimary exploratory by design**, not a new clean preregistration.

[Source-only Actions 44298728811](https://github.com/zuizui0223/egwee/actions/runs/44298728811) obtained the original Zenodo file, checked its SHA256 and exact 160/160 original source mother/stigma keys, then counted only source-numeric validity:
- **160** original mothers and **16** manipulated sessions, original treatment in 3 categories.
- **157** complete mothers for visit/flower display/size/stigma pollen + genetic `gMS_fem_all`; only **3** mother rows lack usable source `pl_mean`.
- Each of the 16 session groups retains **9–10** mothers. No missing genotypic outcome `gMS_fem_all` was found by the source-only gate.
- Prior stronger original source gate for **per-fruit seed target** remained **COVERAGE_STOP** at 145/160 due one 5-mother session. It is not silently converted to a registered confirmation by this more complete genetic endpoint.

## Original-source genetic mating success prediction

M0: original pollinator abundance class (two indicators), log1p(nb_visit), log1p(nb_flo_all), log1p(height_max). M1: all M0 plus exactly log1p(pl_mean). Both fitted as Gaussian ridge λ=1, unpenalized intercept, train-only standardized predictors; `log1p(gMS_fem_all)` output. Each of **16 entire experiment sessions** is held out once, one equally scored plant row per mother. A second, independently written coordinate-descent ridge solver agrees with the Gauss–Jordan normal-equations solver on the same folds to within 1e-8. No p-value is computed from nesting individual plants.

| Source-exact model performance | 157 mothers, 16 sessions |
|---|---:|
| M0 pooled held-out mother-equal MSE | **0.21969178** |
| M1 (+ measured stigma pollen) pooled held-out MSE | **0.22334284** |
| **M0−M1 predictive gain** | **−0.00365106** |
| Relative to M0 MSE | **−1.6619%** (worse) |
| Original sessions with positive gain | **7/16** |
| Removing one scored session from the *already fitted fold losses*, no retraining | **[−0.00431309, −0.00245093]** |

**Result:** in this *specific* source model, adding simple mean stigmatic pollen quantity does **not** improve predictive accuracy for offspring-genotyped female genetic mate number across unseen experimental sessions. This conclusion is about a small performance increment, not proof of biological independence or absence of a pollen effect. [Original source CI 44299220439, success](https://github.com/zuizui0223/egwee/actions/runs/44299220439), derivative artifact 14424993725.

## Same mother / different response: post-outcome source-cohort sensitivity

A separate, explicitly **post-outcome** [common-cohort specification](QPF007_POSTOUTCOME_COMMON145_FREEZE_20261118.md) was committed **after** observing both the seed and genetic scores but before recomputing them together. It retained **exactly the original 145 mothers with full per-fruit seed, visitor, size and pollen data**, including the one underpowered 5-mother session. It used the **same source 145×16 matrix, identical fixed predictors, fold assignments, penalty** for each response, without refitting the earlier 157 primary or choosing any model based on outcome signs.

The original post-coverage 145-mother **seed** forecast was independently reproduced across **all 16 original fold MSE values**, not merely its total: M0 **0.53354450**, M1 **0.52583749**, gain **+0.00770701 / +1.4445%**, **7/16** positive folds. It did **not** meet the original stronger 5%+12/16 numerical criterion, and the historical prospectively registered source eligibility was STOP.

On those **same 145 mothers**, the **genetic mating** endpoint gives:
- M0−M1 **−0.00284478 MSE**, **−1.3597%** of its own M0 MSE.
- **7/16** original session folds improve; the negative direction remains despite using the same mother cohort as the seed endpoint.
- This is a *post-outcome* inclusion-sensitivity finding, not a new preregistered contrasting effect, a statistical equivalence test, or a biological two-sided dissociation.

Source-verifiable whole-session/dual-model trial [GitHub Actions 44300158108, success](https://github.com/zuizui0223/egwee/actions/runs/44300158108) reproduced the original seed forecast **in every fold** using independently rebuilt eligible mother rows. Original author datasets and individual genotypes were not redistributed.

**Do not subtract the raw seed MSE gain 0.007707 from the genetic MSE gain −0.002845:** each outcome uses different log units, empirical variance and theoretical ceiling (genetic mate number bounded by genotyped offspring). Compare only directions and within-endpoint percentage gains descriptively, with all source-selection limitations explicit. Both endpoints have **only 7/16** positive sessions, and one original study cannot support a general statement about stage-specific information processing.

## Ecological conclusion and next independent experiment

- **Supported, narrowly:** In this experimentally varied pollinator density context, a directly recorded mean stigma pollen count does not consistently improve out-of-session prediction of **genetic mate success** beyond visits and maternal display. Similarly, the original per-fruit seed target has no stable large incremental gain, although its weak pooled point estimate has opposite sign in the same source cohort.
- **What original authors already know:** post-pollination competition can decouple potential mates inferred from pollinator movement from realized genetic fertilization. This project does not rediscover that principle.
- **Not supported:** that simple pollen quantity never matters; proof that genetic compatibility/quality drives the differences; that original genetic mate number measures direct pollen fathers on sampled stigmas; that seed quantity and mate diversity are statistically dissociated across taxa; any causal pollination→fitness translation/fragmentation law.
- **Future independent mechanism test:** genotype actual deposited pollen donor identities (or pollen-tube-compatible donors) on plants with independently tracked viable seed progeny; measure observed visits, floral exposure and pollen load with known effort within source region×site×maternal cohort. At least 3 genuinely independent biological research programmes, with a study-heldout validation and target-sampling effort calibration, are needed before a macroecological transfer claim.

## Reproducibility / repository firewall

- Original-source 157-mother target eligibility: `audit_qpf007_genetic_mates_source.py`, [CI 44298728811](https://github.com/zuizui0223/egwee/actions/runs/44298728811).
- Genotypic mate heldout model with two independent solvers: `run_qpf007_genetic_mates_session_holdout.py`, [CI 44299220439](https://github.com/zuizui0223/egwee/actions/runs/44299220439).
- Post-outcome exact common 145 mother re-evaluation: `audit_qpf007_common145_outcome_stage.py`, [CI 44300158108](https://github.com/zuizui0223/egwee/actions/runs/44300158108).
- Frozen pre-response and post-outcome design notes remain separate in Git ancestry; historical original QPF007 registered source STOP and 145 exploratory seed result unchanged.
- Original Zenodo raw rows, mother/offspring IDs, genetic assignments, pollen values, source visit traces and model prediction records are not added to the repository. Only source aggregate and fold-level error artifacts are emitted.
- This branch is a stacked draft on PR #85, not `main`; the original six-source QPF programme denominator, natural fragmentation five-cluster effects, EuPPollNet, CropPol, apple PR #86 and theoretical egwe remain untouched.
