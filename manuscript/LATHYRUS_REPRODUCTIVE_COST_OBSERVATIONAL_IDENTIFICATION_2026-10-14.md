# Reproductive records, actual mature seeds and subsequent plant fate are different ecological endpoints: Lathyrus source audit (2026-10-14)

## Evidence status and ecological question

**Empirical EGWEE only, not theoretical EGWE.** This is an **exploratory reanalysis of an already published non-fragmentation ecosystem**, the Swedish perennial *Lathyrus vernus* (Fabaceae). It is an independent plant/source from the tropical *Heliconia acuminata* case but **NOT** an independent habitat-fragmentation treatment, **NOT** a newly discovered reproductive-cost mechanism and **NOT** a contribution to the five-primary, eight matched interaction–function, 16-programme or SF06 frozen synthesis denominators.

The narrower question is whether natural records of flowering or **mature seed production** can predict subsequent aboveground plant fate and size, and whether an apparent growth penalty withstands **previous size matching**, observation-condition awareness and deletion of a calendar year. This checks the ecological boundaries of calling a strong one-year flowering association either successful reproductive output or a physiological/reproductive trade-off.

**Provenance:** *Lathyrus vernus*, Ehrlén (2000) *Ecology* 81:1675–1684, 1,119 genets, 6 subplots, 1988–1991, from `dormancy1/lefko3` at immutable Git commit `1ddb6092e5e4f1f401432b594ee49bb7aac2c627`; `data/lathyrus.rda` Git blob SHA `c014e2728734eb83990f5511669030001a939fb3`. Original data documentation `man/lathyrus.Rd` defines annual `FCODE=1/0`, aboveground volume in mm³, `IntactseedXX` (some seed quantities model-estimated) and distinct `Dead/Dormant/Missing` fields. Source file hash and unique `SUBPLOT+GENET` identity are checked by the script.

## Cohort denominator and dormancy warning

Of **2,413** previous-year measurements with positive aboveground volume and a valid flowering code (three possible transitions: 1988→89, 1989→90 and 1990→91), next-year states are:

| Next-year archived state | Number of transitions |
|---|---:|
| Confirmed aboveground and flowering-status observed | **1,990** |
| Explicit dormant | 201 |
| Explicit dead | 194 |
| Explicit missing | 24 |
| Both dormant and missing flagged | **1** |
| Neither aboveground nor clearly classified | 3 |

One individual has both `Dormant=1` and `Missing=1`; this is preserved as a **joint original state**, not silently forced into an exclusive category. Next-year absent aboveground **cannot be substituted for mortality or reproductive cost**. Volume comparisons necessarily condition on reappearance aboveground, which can select individuals with distinct vigor or detection.

## Recorded flowering is strongly confounded with prior size

| Prior-year documented state | Prior-year plant-year records | Next-year confirmed aboveground | Mean log(previous volume) |
|---|---:|---:|---:|
| `FCODE=0` | 1,812 | 1,449 (**79.97%**) | 4.083 |
| `FCODE=1` | 601 | 541 (**90.02%**) | 7.054 |

The raw >10-point difference in subsequent aboveground appearance **is not a protective causal flowering effect**, because prior flowering plants were much larger on average. Within **subplot × calendar year × previous log-volume band** overlap-weighted comparisons, the *flowering minus nonflowering* aboveground appearance difference is only **+0.028** (2.81 percentage points) for log-volume bin width 1.0, **+0.011** for width 0.5 and **+0.055** for width 2.0. These are descriptive matched-bin differences without independence-calibrated uncertainty.

## Vegetative growth contrast depends on the estimand and size resolution

Using the same prior-size/subplot/year matching but only next-year confirmed aboveground plants:

| Outcome contrast (prior flowered minus not) | Log-volume bin width 0.5 | Bin width 1.0 | Bin width 2.0 |
|---|---:|---:|---:|
| Next-year `log(volume)` | +0.046 | +0.093 | +0.356 |
| `log(next volume / prior volume)` | **−0.003** | **−0.059** | **−0.067** |

This alone does not identify any consistent **biological cost**. The log growth ratio changes when the denominator `prior volume` is not exactly balanced, even within a prior-size band. For the same 1990/1989/1988 pooled transitions, the growth-ratio point difference changes sign or becomes negligible on year deletion: **+0.070** if 1990 is deleted, **+0.007** if 1989 is deleted, but **−0.305** if 1988 is deleted. Individual transitions likewise differ (+0.267 in 1988→89, −0.224 in 1989→90, −0.387 in 1990→91 under the 1.0 bin).

The previous size is not a randomly assigned baseline; a log-volume ratio alone can misleadingly suggest a current allocation cost. Flowering history is an observed marker of past plant condition rather than a randomized subtraction of reproductive resources.

## More biologically relevant exposure: mature seeds among flowering plants

The source has nonmissing original or modeled `IntactseedXX` counts for **601** prior-flowering transitions: **335 with zero** recorded intact mature seeds, **266 with at least one**. Restricting to prior flowering plants avoids confusing **flowering** with the resource allocation to **mature seeds**, but seed set and quantity are still observational and may encode pollen availability, pollination, herbivore effects, and plant health.

| Seed-positive vs seed-zero (only prior flowering plants) | Bin width 0.5 | Width 1.0 | Width 2.0 |
|---|---:|---:|---:|
| Next-year confirmed aboveground fraction difference | −0.0151 | −0.0153 | −0.0095 |
| Next-year log(volume) difference *among aboveground observed* | −0.0082 | −0.0245 | **+0.0319** |
| Log growth ratio difference | −0.0348 | −0.0648 | −0.0433 |
| Previous log(volume) imbalance *in that same subsequent-aboveground subset* | **+0.0267** | **+0.0403** | **+0.0752** |

Crucial **exact within-matched-subset identity** at bin width 1.0:

[
Deltalogleft(rac{V_{t+1}}{V_t}ight)
=Deltalog(V_{t+1})-Deltalog(V_t)
=-0.0245-0.0403=-0.0648.
]

This means the apparent negative growth-ratio contrast includes appreciable **remaining initial-size imbalance**, even after bin matching. The clearer endpoint, next-year log volume, is small and reverses under coarser size categories. With only 3 calendar transitions and no herbivory variables in this extracted model, these natural contrasts **cannot be promoted to evidence of a causal reproductive cost**.

The next-year log-volume seed-positive versus seed-zero differences by start year are **+0.0015 (1988)**, **−0.0356 (1989)**, **−0.0637 (1990)**. The negative growth-ratio differences are **−0.0529**, **−0.0606** and **−0.1017**; those comparisons retain the size-denominator coupling and selection on subsequent visibility.

## Biological prior-art ceiling: observational natural history versus manipulation

**Ehrlén & Van Groenendael (2001), *Journal of Ecology* 89:237–246, doi:10.1046/j.1365-2745.2001.00546.x**, already made the critical biological observation: natural reproductive/fruiting variation did **not** reliably expose negative costs, whereas experimentally **removing flowers for three consecutive seasons** increased later vegetative size and flowering/fruiting probability. The original research also tracked herbivore damage and plant rhizome resource storage, which our archive-level simple matching does not recover as aligned covariates. It would be incorrect to describe this negative-to-positive transition or delayed cost as newly discovered by EGWEE.

This **supports retaining distinct evidence layers**, not a new general law:
- prior recorded flowering is a predictor of a future reproductive *record*, not an intervention;
- next-year *aboveground appearance*, future *vegetative size* and eventual mature *seed* production are non-equivalent functions;
- experimental manipulation identifies an **intervention-sensitive reproductive cost** that natural indicator correlations can mask;
- no conclusion about habitat-fragmentation effects or seedling recruitment in this Lathyrus dataset is identified.

The similar *Heliconia* archive result—that first-recorded recruits do not always track documented flowering or prior living stock—offers a conceptual comparison, but it is a **different ecological endpoint**. These two species alone do not establish a population-level prevalence or novel fragmentation mechanism.

## How to genuinely test a new EGWEE ecological claim

An informative future **fragmentation-exposed** synthesis would need at least two independent landscape programmes with all three components observed *synchronously*: pollination/seed-input measures, confirmed seed–seedling/recruit vital transitions with detection calibration, and manipulated pollen versus safe-site or seed-availability opportunities. Compare held-out landscape **incremental prediction** for whole-patch recruitment and intervention leverage. A reversible difference between correlational association and experimental rescue would be valuable; asserting that reproduction has costs or that fecundity proxies sometimes mislead is already established prior art.

## Reproducibility and review gate

- `scripts/audit_lathyrus_reproductive_cost_state_tradeoff.py`: source-Git-blob-hash-verified `.rda`, explicit living/dead/dormant/missing source flags, overlap-weighted subplot/year/previous-size strata, six-plot and year deletion, flowering and intact-seed contrasts, and the algebraic log-growth denominator check.
- `.github/workflows/lathyrus-reproductive-cost-tradeoff.yml` installs pinned-compatible RData reader and runs both the pipeline and fail-closed checks.
- GitHub Actions **PASS**, source SHA-verified: https://github.com/zuizui0223/egwee/actions/runs/38565695588.
- An early run https://github.com/zuizui0223/egwee/actions/runs/38564983294 failed on an incorrect assumption that dormancy and missing flags were exclusive; fixed without dropping those cases. Subsequent **green** run verifies overlapping flag categories.
- **Submission-ready stays false**; PR #52 stays draft, original main frozen dataset and all independent programme counts remain unchanged.
