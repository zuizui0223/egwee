# External species check: one-lag flowering persistence is not the same as flowering-history recency in Lathyrus vernus (2026-10-14)

## Ecological question and independence

**Empirical `egwee`**: does the distinction between an adjacent-year flowering association and **recent-versus-distant order after the same number of flowering seasons** survive in another species and climate? This note is *external* and exploratory. It does **not** create a new fragmentation treatment effect, nor change frozen egwee five-direct, eight I–F, sixteen-programme mapping, or SF06 source denominators. **The theoretical `egwe` project is not involved.**

The second species is the temperate perennial herb *Lathyrus vernus* (Fabaceae) in Sweden, a separate published ecosystem and dataset from the Brazilian *Heliconia acuminata* BDFFP programme. Unlike Heliconia's 1998–2009 monitored plant-years, this historical demographic dataset covers **1988–1991 only**; it allows two consecutive three-year-history windows but **no claim of extensive held-future-year temporal replications**.

**Provenance:** The public R-package `dormancy1/lefko3` contains `data/lathyrus.rda`, 1,119 individual rows from **six subplots**, explicit `FCODE88–91` (1 flowering, 0 no flowering), aboveground `Volume88–91`, plus `DeadYYYY`, `DormantYYYY`, `MissingYYYY`, `FlowYY`, and intact-seed counts. The package's `man/lathyrus.Rd` credits *Ehrlén (2000), Ecology 81:1675–1684, “The dynamics of plant populations: does the history of individuals matter?”*. This prior study already addresses demographic history: **neither flowering history nor its ecological context is invented by EGWEE**. Source is frozen to public Git commit `1ddb6092e5e4f1f401432b594ee49bb7aac2c627` and `lathyrus.rda` Git blob SHA `c014e2728734eb83990f5511669030001a939fb3`. The audit requires annual positive aboveground volume and valid `FCODE=0/1` at every relevant year, not merely a present data frame row.

This **four-year, 1,119-individual** lefko3 dataset is *not the same file* as Valdés, Arnold & Ehrlén (2023), Dryad doi:10.5061/dryad.j6q573njx (22 years, 837 individuals; identifier `datadef.csv` has public SHA256 `5d2af58867b73e7d922ded33a60a5e558465a17028d63ac59fb8ef5579d90613`). The latter download was access-blocked via Dryad API (HTTP 401) and browser challenge, and **has not been analysed** here. The historical lefko3 study may share a Swedish species/population with subsequent research; do not count the two Lathyrus sources as two replications.

## Two explicitly different history estimands

1. **One-lag recorded persistence:** among the same aboveground-observed individual in adjacent years, compare later `FCODE=1` after prior `FCODE=1` versus after prior `FCODE=0`. Stratify for **subplot × first year × previous positive-volume category**, with volume categories based on `min(int(log1p(volume)//2),7)`. The source field's 0/1 semantics are explicit.
2. **Equal-frequency history ORDER:** among the same individual measured and aboveground in **three consecutive years**, retain only those with one flowering-positive year among the preceding two observations. Compare `[0,1]` (“recent” flowering) against `[1,0]` (“distant” flowering) for next-year `FCODE=1`, holding aboveground volume bin at the middle census, subplot and middle year fixed. Under a restrictive stable-individual logistic-propensity + additive calendar-year null, the conditional order selection does not depend on that stable individual intercept; but survival selection and dynamic condition remain uncontrolled. No physiological memory inference follows.

The source-verified run https://github.com/zuizui0223/egwee/actions/runs/38423583718 **PASSED** after installing pyreadr plus pandas in the CI. Initial run 38423117020 failed only because the first workflow had omitted the pandas/polars backend required by pyreadr 0.5.7; the corrected source+schema audit succeeded.

## Independently reproduced results

| *Lathyrus* historical panel | Source-matched pairs / histories | Stratified descriptive odds ratio |
|---|---:|---:|
| **One-lag flowering status**, 1988→1989, 1989→1990, 1990→1991 | 1,990 adjacent individual-year pairs | **2.385** |
| **Order** `01` versus `10`, 1988–1990 and 1989–1991 three-year windows | **231** triple-observed, one-positive histories | **0.897** |

The one-lag marginal frequencies are **336/541=62.1%** next-flowering when last year flowered versus **201/1,449=13.9%** when last year did not (the OR above is further stratified by subplot/year/volume). This strong unadjusted contrast may still reflect stable individual size, reserves and growing conditions, even after coarse previous volume stratification.

For the equal-frequency order contrast, next positive flowering is **35/77=45.5%** for recently recorded `01`, versus **67/154=43.5%** for earlier-recorded `10`. The stratified OR **0.897** differs from the unadjusted association because the two history groups occupy different subplots, size strata and years. There are only **16 informative subplot×year×size strata**; this is not evidence of equivalence or a negative-memory mechanism. The two year-specific order ORs differ considerably: **1.420** for middle year 1989 versus **0.536** for middle year 1990. Four total field years and two history windows are insufficient to estimate stable population-order effects.

For context, the separate *Heliconia* raw-original-zero-confirmed cohort yielded a different main estimate, **one-lag adjusted OR 2.801** in 15,029 person-year pairs but equal-frequency two-history-order adjusted OR **1.210** (960 triple years, finer height bin OR 1.124), with strictly held-future-year order prediction actually worse than morphology alone. The tests involve different size definitions and landscape biology; **do not pool their odds ratios as a universal species-level mean, run a cross-taxon p-value, or interpret a small number of species as prevalence evidence**.

## Falsification boundary and manuscript relevance

The second study is a useful **independent organism/region check of the *logical contrast***: both species have strong recorded adjacent-year flowering association, while the specific “most-recently positive given exactly one previous positive” order contrast is weak and variable. This makes it substantially less defensible to call a one-lag flowering OR direct evidence of **short-term physiological memory**. But it does not demonstrate that plants lack true energetic reproductive costs, allocation tradeoffs, or state carry-over — previous studies of *Lathyrus* and other perennial herbs show why natural positive serial association can coexist with experimentally identified costs.

**Prior art and novelty limit:** Ehrlén (2000) already directly asked whether individual demographic history matters using historical matrix approaches in *Lathyrus*. Ehrlén & Van Groenendael (2001, *Journal of Ecology*, doi:10.1046/j.1365-2745.2001.00546.x) examined previous reproduction and flowering-removal costs. The present two-species check does not announce a new general flowering-memory theorem. The possible EGWEE contribution would require coupling original-verified flowering, seed arrival, establishment, **future-year forecasting and fragmentation exposure** in independent studies, rather than extending a one-species stage proxy interpretation.

**Crucial conditionality:** *Lathyrus* panel has no habitat-fragmentation treatment or matched effective pollen/seedling-recruitment endpoint, so it is an **external methodological/ecological control**, not new evidence for the EGWEE fragmentation main hypothesis.

## Reproduce

- Script: `scripts/audit_lathyrus_external_history_order.py`.
- Workflow: `.github/workflows/lathyrus-external-history-order.yml` (pin/download source .rda; validates SHA; pyreadr+pandas).
- Successful source-pinned GitHub Actions: https://github.com/zuizui0223/egwee/actions/runs/38423583718, archived machine-readable JSON.
- A later complete, strictly held-1991 forecast **passed** GitHub Actions https://github.com/zuizui0223/egwee/actions/runs/38424393937. With size bins only, 707 held-out transitions yield Brier **0.147126** (size) vs **0.147475** (size plus prior flowering), and log loss **0.448912** vs **0.459702**; with size+subplot, Brier **0.144842** vs **0.142604** but log loss **0.446281** vs **0.451126**. The sign depends on score and whether subplots enter; only one held outcome year exists. Do not claim useful stable temporal memory prediction.

**No changes to frozen EGWEE meta-analysis or submission gate; PR #52 stays draft and `submission_ready=false`.**

## 14 October independent natural reproductive-cost endpoint audit

A subsequent [source-hash-verified state-specific ecological audit](LATHYRUS_REPRODUCTIVE_COST_OBSERVATIONAL_IDENTIFICATION_2026-10-14.md) of the same historical Lathyrus source separates previous flowering, production of **intact mature seeds**, next-year aboveground confirmation and next-year vegetative volume. It reconstructs **2,413** eligible prior aboveground individual-year transitions, next-year **1,990** aboveground, **201** dormant, **194** dead, **24** missing and **one source record flagged both dormant and missing**, plus 3 other unclassified next states. Among 601 previously flowering transitions, 335 lack mature seeds and 266 recorded positive mature seeds.

When matching subplot/year/previous size, apparent negative growth-ratio contrasts for mature-seed-positive versus zero flowering plants are substantially altered by baseline-size differences within bins. For log-volume matching width 1.0, next-year log-size point difference is **−0.0245**, residual prior log-size difference **+0.0403**, hence the log growth-ratio difference **−0.0648** exactly. Finer/coarser bins change the next-year log-size contrast from **−0.0082** to **+0.0319**. Therefore a simple observational growth cost is not identified. The original Ehrlén & Van Groenendael (2001) paper *already* established reproduction costs from repeated three-year removal interventions even when natural flowering/fruiting patterns failed to detect them. This is prior art, not an EGWEE discovery. GitHub Actions https://github.com/zuizui0223/egwee/actions/runs/38565695588 **PASS**. The observational audit is a boundary control and makes no new fragmentation or multi-species fitness claim.
