# Can captures, insect diversity or functional evenness diagnose plant seed set in an unobserved flower patch? (18 October 2026)

## Empirical question and study status

**Empirical `egwee` only, not theoretical `egwe`. This is one new *independent source ecosystem* as a qualitative/diagnostic comparator to the earlier Heliconia field programme, but NOT a new direct habitat-fragmentation contrast and NOT an independent admission to the EGWEE primary effect, eight matched I–F programmes, 16-programme map, or SF06 paper-effect corpus.** It does not validate a universal pollination-to-fitness failure or overturn prior literature.

The biological question is **whether observed insect counts, diversity or simple body-size functional-trait summaries improve the prediction of per-flower seed output in a *completely unobserved experimental flower patch***, after learning the usual seed set of each plant species in other patches. The target is an explicitly held-patch *sentinel* test, not the in-sample hypothesis of the original authors.

**Study and prior art:** Peralta, Webber, Perry, Stouffer, Vázquez & Tylianakis (2023), *Ecography* `e06453`, doi:10.1111/ecog.06453; archived CC0 field data doi:10.5061/dryad.5qfttdz9q, mirrored at https://zenodo.org/records/7618753. The original article **already reported positive seed-set associations with pollinator functional richness/evenness and interpreted interaction complementarity as a biological mechanism**. These are established prior art, not new EGWEE findings. Their formal original mixed models use negative-binomial seed response with random intercepts for patch and species, while our held-patch score asks a different empirical target under simplified predictors.

## Original-CSV provenance and true independent units

- `Data_S1.csv`: 1,470 captured insect visits with recorded flower-plant association, insect taxon labels and ITD. Exact Zenodo MD5 **`ae6df5d3d1a5d6cac12aa509752c74a5`**.
- `Data_S2.csv`: 3,430 recorded seed counts, exactly 5 sampled flowers for each of **686 separate plants**, seven plant species and 14 isolated experimental planted flower patches. Exact MD5 **`7a5c3020cbd084470ed4fe5e6de45cd3`**.
- Plant label aliases must be normalized before matching: insect-side `Anise.Hyssop` versus seed-side `Anise Hyssop`, and insect-side `Nepeta` versus seed-side `Napeta`. Then there are exactly **14 × 7 = 98** patch × seed-producing plant-species cells. These are **98 paired observations sharing only 14 spatial experimental patches**, not 98 independent ecological landscapes or 3,430 independent patch effects.
- Within-patch insects were captured during six 1-hour rounds under specified sampling conditions. Counts are *sampling-constrained* insect captures, NOT measured effective compatible pollen deposition, not standardized visits to any one tagged flower, and not true absolute all-season visitation.
- `75` distinct literal source `family|genus|species` **taxon-label strings** occur in these captures; this number must not be substituted for the source's independently verified pollinator species count. Morphospecies and classification inconsistencies can affect raw label richness.

There are exactly **19/98** plant-species×patch pairs with **no same-species insect captured during the sampling rounds but positive seed output**. Breakdown: Coreopsis 8, clover 5, lucerne 2, nepeta 2, anise hyssop 2. This is direct evidence that `zero captured insects ≠ observed biological zero seed set`, but not evidence of absent pollination, selfing alone, or seed production independent of insect visitors (observed samples are sparse).

The physical site is a **single** 105-ha sheep farm pasture near Oxford, North Canterbury, New Zealand. The 14 2m×2m flower patches are separated by local isolation distances; there is NO designed continuous forest versus experimentally fragmented forest treatment contrast. **Do not append this case to the frozen fragmentation treatment effect count or claim an independent fragmentation mechanism replication.**

## Exact held-entire-patch prediction

The response in each cell is `log1p(mean seeds per tagged flower)`. Each of 14 CV folds removes **all seven species outcomes of a given patch** and fits the species-specific training means/SDs and feature centering/scaling on the remaining 13 patches. A simple within-fold standardized linear ridge with penalty 1 estimates feature effects; the baseline is each species' held-source mean. All models are scored on **the same 98 cells**. The primary *descriptive* score weights seven species equally after within-training-fold response standardization. A second score assesses raw `log1p` seed units, because species-level seed ranges differ markedly and these targets can rank models differently. No error/p-value is interpreted using 98 independent landscapes.

| Predictor added to species mean | Held-patch within-species standardized MSE | Change versus 1.367720 baseline | Held-patch raw log-seed MSE |
|---|---:|---:|---:|
| None (species-mean baseline) | **1.367720** | — | **0.125032** |
| Captures on that seed-plant species | **1.391022** | **−1.70%** (worse) | 0.125457 |
| Total patch captures | 1.369617 | −0.14% | **0.117825** |
| All observed patch taxon labels | **1.318765** | **+3.58%** (better) | 0.121159 |
| **Taxon labels rarefied to 54 captured insects** | **1.332379** | **+2.58%** (better) | **0.129428** (worse) |
| Raw taxon labels + total captures | 1.349094 | +1.36% | 0.126703 |
| Rarefied labels + total captures | 1.364403 | +0.24% | 0.125827 |
| Capture-weighted mean insect body size (ITD) | 1.344143 | +1.72% | 0.127039 |
| Simple ITD log-size dispersion | 1.384208 | −1.21% | 0.126658 |
| Simple taxon-mean ITD range | 1.380983 | −0.97% | 0.134418 |
| **1D MST body-size evenness analogue (not verified dbFD FEve)** | **1.380295** | **−0.92%** | 0.124013 |
| Same evenness analogue, rarefied to 54 captures | **1.377576** | **−0.72%** | **0.119985** |

**Sampling effort check:** patch insect captures range from **54 to 152**. Higher raw taxon richness is partly a detection/sampling-effort variable. We therefore calculate the exact hypergeometric **expected richness from 54 draws without replacement** at each patch, keeping taxon frequencies fixed. At the standardized seed target this *still shows a small positive held-patch diagnostic score* (2.58%) but weaker than raw richness (3.58%). At the raw log-seed target the rarefied predictor is **worse than the species baseline**. Adding total capture intensity to rarefied richness leaves only a **0.24%** standardized improvement. **Thus the tempting 'diversity is a better general sentinel than visit count' claim is NOT score- and effort-robust.** The original paper's published body-size FEve and fragment-isolation estimands are different.

**Size-evenness check:** the extra 1D proxy sorts taxon mean ITD into a trait-space minimum-spanning tree and weights consecutive edge lengths by taxon abundances, optionally averaged over 300 deterministic 54-capture resamples per patch. These are **not independently checked against original R `FD::dbFD` FEve**, and cannot refute the source's functional evenness mechanism. In this simple held-patch regression family, neither raw nor rarefied proxy beats the standardized species baseline.

## Deletion influence, not new sample size

Original unrarefied taxon-richness model retains its small *within-species-standardized* MSE gain when each seed-producing plant species is omitted from scoring in turn (**7/7** deletions), and after omitting each single held-patch score (**14/14**). In contrast, species-specific capture count beats baseline under only **1/7** species deletions. **These deletions reuse massively overlapping model fits and correlated landscapes; they are not 7 or 14 independent replications**, nor confidence bounds for a population-level diversity effect. More fundamentally, the independent whole-study count here is **one**.

## Biological interpretation and prior-art ceiling

The limited new comparison suggests **source- and representation-specific differences in which field indicators contain out-of-patch seed-function information**. It is *consistent with*, but cannot establish, a general relationship of floral-network complementarity or redundancy to reproduction. A 19/98 sampling-zero discrepancy is useful for identifying the limits of a monitoring protocol but doesn't establish biological failure of pollination/seed production. And positive seed counts need not come from the insects captured on that exact patch during the sampling rounds.

The original study already evaluated effects of local patch isolation, pollinator functional diversity, interaction complementarity, and in-sample seed set. It reported functional evenness as marginal in the jointly adjusted model and positive effects when considered separately with collinear traits. Our simpler out-of-patch predictor comparisons **do not formally test the original causal, multivariate or count-regression hypotheses** and should not be represented as contradictions of that article.

To establish a new biological result in EGWEE, sample multiple **independent landscape programmes** with:
1. synchronized time- and flower-level direct visit counts, compatible pollen delivery, seed viability and eventual detected recruitment;
2. independently measured host traits, flowering resources and safe-site availability, rather than only indirect inferred diversity;
3. precommitted held-landscape/held-season diagnostic score targets and randomized pollen-quality versus establishment-opportunity interventions where feasible.

This is one exploratory **external comparative system**, with **no admitted fragmentation contrast**, no new primary inference, no universal law and no change to submission readiness.

## Reproduction

Source-pinned script: `scripts/audit_webber_2023_held_patch_sentinel.py`. CI workflow: `.github/workflows/webber-held-patch-sentinel.yml`; source-verified original patch/species baseline https://github.com/zuizui0223/egwee/actions/runs/39091376500, deletion audit https://github.com/zuizui0223/egwee/actions/runs/39091501773, rarefied label check https://github.com/zuizui0223/egwee/actions/runs/39091612479, and 1D functional-evenness proxy check https://github.com/zuizui0223/egwee/actions/runs/39091874675, all **PASS** with pinned source MD5 checks. Complete JSON archived as Action artifact. All code is scoped to PR #52 draft branch; the frozen EGWEE effect corpus and main branch remain unchanged.
