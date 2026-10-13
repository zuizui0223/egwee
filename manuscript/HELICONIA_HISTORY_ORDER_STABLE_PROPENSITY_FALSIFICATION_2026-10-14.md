# Does annual flowering order encode short-term memory beyond stable individual propensity? A source-verified Heliconia falsification (14 October 2026)

## Scope and ecological hypothesis

This note belongs to **empirical `egwee`**, not theoretical `egwe` or NEE operator theory. The source is the **same already-published** *Heliconia acuminata* (BDFFP) programme, Bruna et al. (2023), *Ecology*, doi:10.1002/ecy.4174, Dryad doi:10.5061/dryad.stqjq2c8d. This is a **post hoc** exploration of one species in ten selected 0.5-ha plots across three ranches; there are no new independent ecological programmes and no modifications to EGWEE's frozen five direct clusters, eight I–F programmes, 16-programme map or SF06 data.

The prior audit showed a strong association between a surviving plant's documented inflorescences in adjacent years, even after matching calendar transition, plot, height and shoots: **stratified OR 2.777** (cleaned records) and **2.801** for originally entered numeric zero/positive pairs. Yet adding one prior recorded flowering state improved held-future-year forecasting only very slightly and inconsistently. In particular, **these ORs do not prove a causal flowering memory**.

We now target a biologically sharper question:

> Among repeatedly measured surviving plants with *exactly one positive flowering entry during the previous two years*, does it matter **which** of the two years contained that entry?

This equal-count history restriction distinguishes:
- **History `01`**: no documented flowering at `t−1`, positive at `t` (recent positive).
- **History `10`**: positive at `t−1`, no documented flowering at `t` (distant positive).

The outcome is an original or cleaned **positive inflorescence record at `t+1`**. We stratify the descriptive Mantel–Haenszel contrast by **plot × middle calendar year `t` × measured height band at `t` (25 cm) × shoot count at `t` (0–2, 3–4, 5–7, 8+)**. Ten-cm height bins, deleted calendar years and ranches are sensitivity checks. Both prior states and the future state require the *same plot+plant ID measured alive in all three annual census records*. Years `t=1999–2004` provide full coverage, and the core frame is `t=2001–2004`.

## Why an order-matched history is stronger than a one-lag odds ratio

Suppose a plant has a time-invariant latent propensity `u_i` and shared annual conditions `a_y`, and its flowering observations are conditionally independent over years with

\[
\operatorname{logit}\Pr(F_{i,y}=1\mid u_i,a_y)=u_i+a_y.
\]

Then, for two past years, the relative probability of histories is

\[
\frac{\Pr(0,1\mid u_i,a_{t-1},a_t)}
 {\Pr(1,0\mid u_i,a_{t-1},a_t)}
=\exp(a_t-a_{t-1}),
\]

which **does not depend on the stable individual propensity `u_i`**. Conditional on exactly one flowering-positive record, the two history orders select the same mixture of permanent `u_i` values under this narrowly specified model. Thus a positive lag-one association from stable individual heterogeneity need **not** imply a recency-order contrast.

The simplifying model will fail if morphology, energy stores, permanent detectability, season-specific survey effort, age, survival or underlying individual flowering propensity changes dynamically and differently across individual histories. **An observed order contrast is not automatically a causal flowering memory**, and a weak contrast does not establish an exact zero effect. This is an exploratory statistical falsification design, not a new biological theorem.

## Cleaned archive and ORIGINAL entered-zero verification

Source audit inputs are Git-blob pinned:
- Published clean `data/survey_archive/HDP_survey.csv` at commit `0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0`, 66,396 plant-year rows and Git blob `f82a6f241493a979a2923d1c5deef6a1be0ff3ed`.
- Pre-cleaning 2016 survey wide CSV `data/survey_raw/Hacuminata_98-09_12oct2016.csv`, 7,673 source rows and Git blob `b42963be30b993b93755f7f40ad09d1361def056`.

The public cleaned `infl=NA` intentionally encodes **conditional recorded inflorescences**, not independently certified absence. Original numeric zeroes were recovered with the source-verified mapping from `scripts/audit_heliconia_raw_inflor_zero_provenance.py`, linking only **unique** raw `plot+tag+subplot` rows to archival `plot_id+tag_number+subplot`. For the strict cohort all three years must have original entered numeric `0` or positive, agree with the cleaned record, and the same clean `plot+plant_id` be measured alive throughout. Ambiguous, unlinked and original/cleaned conflicts are **excluded, never imputed**. An extra `raw_stable_key` sensitivity requires the exact unique raw key in all three years; all eligible triples already pass that criterion.

**Verified source-level finding:**

| Middle years and archive basis | One-positive, triple-survivor comparisons | Next-year positive, recent `01` | Next-year positive, distant `10` | Plot/year/morphology-stratified OR |
|---|---:|---:|---:|---:|
| Cleaned `t=2001–2004` | **1,207** | 127/628 (**20.2%**) | 135/579 (**23.3%**) | **1.358** |
| Original raw-positive/zero confirmed `t=2001–2004` | **960** | 107/512 (**20.9%**) | 101/448 (**22.5%**) | **1.210** |
| Original confirmed, narrower 10-cm height strata | same 960 | same counts | same counts | **1.124** |
| Original confirmed all middle years `t=1999–2004` | 1,377 | 149/672 (22.2%) | 150/705 (21.3%) | **1.229** |

The **adjusted OR can exceed 1 even when the unadjusted group risk is smaller** because the two histories have differing sizes/site/year composition and MH pools only informative strata. Only **45 informative plot/year/size/shoot strata** exist for the primary raw-confirmed four-middle-year comparison (versus 303 total strata). No individual-year count is an independently sampled ecosystem.

**Sensitivity to removing a calendar transition:** In the original numeric-zero-confirmed core sample the OR becomes **1.044** after deleting `t=2001`, **1.741** after deleting `t=2002`, **1.037** after deleting `t=2003`, and **1.245** after deleting `t=2004`. Single-middle-year source-confirmed adjusted OR ranges from **0.693** (`t=2002`) to **2.574** (`t=2003`). Removing the dominant Esteio ranch leaves **insufficient within-stratum counterexamples to calculate a finite MH OR** in the strict raw-confirmed subset. It is not permissible to imply the recency contrast is replicated across all ranches.

The strong one-lag persistence OR near **2.8** and this small/unstable *equal-positive-count* history-order OR near **1.2** measure **different estimands in different selected subsets**. Their numerical difference is not a formal interaction test or a causal attribution. The result is *consistent with* a stable-individual-vigor/propensity explanation but **does not identify that explanation**.

## True held-future-year test of history ORDER

As a further falsification, condition on exactly-one-positive prior two-year histories and train a **morphology-only** baseline versus the same morphology cells plus `01`/`10` **order**. For each held middle year `t=2001,2002,2003,2004` (forecast outcome `t+1=2002–2005`) the models use only earlier completed middle-year outcomes. The feature/risk backoff counts and global rates are reconstructed inside each training fold. A simple hierarchical cell smoother uses 25 pseudo-cases toward global baseline and 20 toward the morphology-only risk for the order-specific cell; sensitivity weights are 5, 100 and 300. These smoothing schemes were compared **after seeing earlier data**; there was no preregistered calibration or independent landscape validation.

| Strict held-future-year subset | Morphology-only Brier | Morphology + order Brier | Result |
|---|---:|---:|---|
| Cleaned triple-survivors, **n=1,207** | **0.168836** | **0.170664** | Order worsens by **0.001828** |
| Original confirmed numeric 0/positive, **n=960** | **0.168541** | **0.170239** | Order worsens by **0.001698** |

For the original-confirmed subset, log loss likewise worsens **0.518045 → 0.521686**. In cleaned records the four individual held-year Brier improvements (baseline minus order model) are **−0.001872, +0.000916, +0.000304, −0.005619**, showing calendar inconsistency. For smoothing weights 5, 100 and 300, the pooled cleaned Brier difference remains **negative**, shrinking toward zero with stronger smoothing.

**The relevant negative result is narrow:** under this exact history-frequency-matched model family and source audit, knowing whether the positive entry happened more recently fails to increase prospective utility and often harms the score. It is **not equivalence evidence**, nor proof of zero physiological memory. These 960 or 1,207 transitions are concentrated in very few calendar years, ten plots and one known source study.

## Ecological interpretation, novelty and further falsification

1. **Individual propensity and reproductive activity remain distinct.** Strong adjacent-year record association can coexist with weak dependence on the *ordering* of the same number of past records. Persistent plant resources/individual condition or persistent flower-detection heterogeneity are competitive explanations, not identified causes.
2. **Prediction target matters.** Correlation and local rank of plants' flowering do not guarantee transport across unknown climatic/phenological years. The temporal translation problem is much larger at plot-level **recruitment**, which is a different outcome than individual flowering records and not covered by this history-order test.
3. **Annual source record semantics matter.** Explicit original numeric zeroes show `infl=NA` in the clean output often reflects a deliberate conditional coding, not necessarily missed flowering surveys. But neither original zero nor conditional archived field measures repeated-visit detection probability.
4. **Prior art already addressed positive flowering history versus costly reproduction.** Ehrlén & Van Groenendael (2001), *Journal of Ecology* 89:237–246, doi:10.1046/j.1365-2745.2001.00546.x, showed natural past flowering/fruiting can be positively related to future performance despite experimentally measurable delayed costs, including effects emerging under repeated flower removal. Size-dependent flowering in *Heliconia* and delayed environmental responses have also been published. **No new plant-memory principle is claimed.**

To establish a genuinely new ecological result, an independent landscape or species with annual *explicit true-zero documentation*, repeated flowering-visit effort, plant reserves or reproductive manipulation, and synchronized seed production → seed delivery → recruit tracking is required. Proposed hypotheses about real memory or costs should be preregistered with forecast calendar windows and the correct unit of independence.

## Reproduction and status

- Script: `scripts/audit_heliconia_flowering_history_order.py`, source-verified both raw and cleaned CSVs, and source-correction disagreements. Archived JSON includes all cohorts, temporal source-deletion and ranch-deletion influences, and prospectively scored prediction rules.
- CI: https://github.com/zuizui0223/egwee/actions/runs/38421487168 — **PASS**, including full source re-read and scoring.
- Earlier raw-verified one-lag association and forecast: `manuscript/HELICONIA_FLOWERING_MEMORY_VS_FORECAST_2026-10-13.md`.
- No changes to frozen source denominators, independent-programme counts, preregistered tests, manuscript headline or author approvals. PR #52 **remains draft**; `submission_ready=false`.
