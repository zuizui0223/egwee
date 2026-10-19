# Sevenello: reserve-specific pollen supplementation and flowering-display accounting

**19 October 2026. Empirical EGWEE exploratory, single publication/single landscape, post hoc extension of a pre-outcome fixed analysis design.** The source study is Sevenello, Walker & Mayfield (2026), *Landscape Ecology*, [doi:10.1007/s10980-026-02305-2](https://doi.org/10.1007/s10980-026-02305-2). Source files: [Figshare 31072189](https://doi.org/10.6084/m9.figshare.31072189), **CC BY 4.0**, 2022 pollination experiment. The ecological pattern reported by the original authors, including species-specific pollen limitation, a LARO edge effect in their pollen-limitation index, and local bare-ground/floral-density associations, is **prior art**. The new outcome here is a differently defined *untrimmed, per-plant, independent-reserve-balanced* evaluation of the OP→OPSupp contrast, followed by a post hoc exact accounting decomposition.

The evidence is **not a second study**, not an additional frozen registered I–F programme, not a new mating-quality measurement, not theoretical egwe, and not approved for the main submission headline.

## Source data and experimental grain

Figshare download previously failed with HTTP 500. A public Figshare downloader->object storage route subsequently yielded the three complete CSVs and allowed source-exact mirroring:

| Original raw file | Rows | Bytes | Figshare MD5 |
|---|---:|---:|---|
| landscape_seeds.csv | **2,080** treatment-plant records | 135,336 | 40caf98755786e32bec89fffd4b114f6 |
| local_seeds.csv | **520** quadrats | 21,953 | 10f0b07ff3ff17ca94dbabdfbcec404e |
| landscape_bees.csv | 20 trap-transects | 1,775 | b6cbdd11787f5ef5210fefcd502a29f5 |

Every quadrat has **four different focal plants** assigned to OP (open/naturally pollinated), OPSupp (open plus hand-added conspecific pollen), Bag, and BagSup. Source methods describe *arbitrary*, not certified randomized, allocation. Each plant contributes its own flower count and visually viable-looking seed count. No hand-supplemented plant is the same individual as the open control. The 31 missing seed values across all four treatments are not imputed as zero. The matched OP/OPSupp complete-pair counts are **117/120 GORO**, **157/160 LARO**, and **115/120 POAR**.

The source's pollen limitation index (PLi) was per flower in LARO/POAR, with its published exclusion of the extreme negative tail (<−1, ~8%). The primary EGWEE analysis instead uses **untrimmed total viable-looking seed counts per plant**, and reports source-consistent per-flower sensitivity separately. It is **not** a claim that the paper's calculated PLi was false. GORO has no comparable flower denominator because the fruits dehisce.

## Fixed primary analysis: does extra pollen rescue seed output more at edges?

The fixed design predates reading the recovered outcome rows: [SEVENELLO_POLLEN_ADDITION_CONTEXT_DESIGN_2026-10-19.md](SEVENELLO_POLLEN_ADDITION_CONTEXT_DESIGN_2026-10-19.md). For each complete **quadrat**, define

\[
D_q = T_{\mathrm{OPSupp},q} - T_{\mathrm{OP},q}\qquad
\text{(visually viable-looking seeds per plant).}
\]

For each species independently: average D within each Edge or Core transect, subtract Core from Edge within the **same physical reserve × crop block**, average two crop blocks within a reserve when present, then give each **physical reserve equal weight**. A site is not multiplied into independent reserves by having two crops or multiple species. Independent reserve counts: **5 GORO; 6 LARO; 4 POAR**. The seven distinct named physical reserves across species overlap. POGN lacks consistently paired Edge and Core sites and remains outside this pre-fixed primary analysis.

| Species | n matched quadrats | independent reserves / matched crop blocks | Mean reserve Edge−Core of D, seeds/plant | Descriptive t 95% interval | Exact two-sided site sign flip p | Holm p (3 species) |
|---|---:|---:|---:|---|---:|---:|
| GORO — *Guichenotia rosea* | 117 | 5 / 6 | **+1.523** | [−13.893, +16.940] | 0.875 | 1.000 |
| LARO — *Lawrencella rosea* | 157 | 6 / 8 | **+3.854** | [−4.592, +12.300] | 0.34375 | 1.000 |
| POAR — *Podolepis aristata* | 115 | 4 / 6 | **−10.302** | [−239.073, +218.468] | 0.875 | 1.000 |

Every species has **both positive and negative independent-reserve edge contrasts**. An edge-specific universal increase in total-seed benefit from supplementation is **not established** by these few reserves. The t intervals assume exchangeable reserve-level contrasts and are descriptive. Enumerated sign flips are finite diagnostic tests under a symmetric site-null, not an intervention randomization test for fragmentation. Unresolved effects are not equivalence or proof of no pollen limitation. The difference of two independently observed treatment plants within quadrats is not itself a within-plant causal contrast.

**Within-site biological reversals:** reserve Edge−Core of D for GORO ranges −9.23 to +21.75; LARO −4.60 to +16.60; POAR −171.94 to +155.20 seeds/plant. These wide site differences, rather than a single monotone edge effect, are the clearest topology in the registered absolute-seed estimand.

## Important target/weight reversal in POAR

On the same **115** complete POAR quadrat pairs:

- Unweighted **quadrat mean** of total seed difference: **−8.304 seeds per plant**, but the quadrat-level **median is +4**, so the mean is influenced by strongly negative cases.
- Physical **reserve-equal** average of the supplementation difference, with equal Edge/Core and crop blocks: **+13.529 seeds per plant**. Thus even the sign of the aggregated mean changes with geography weighting, without a single plant record changing.
- Mean **seeds-per-flower** difference on these plants is **+1.149**. Comparing this number with total-seed differences is comparing *different denominators*, not detecting one treatment effect that changes biological sign.

This is an ecological scale/representation warning rooted in actual plant data: per-flower performance, total plant output, and independent-reserve geographical averaging answer different questions. It is not a demonstration of pollen supplement harm or that pollen is unimportant.

## Exploratory within-transect local environmental comparisons

Following the fixed secondary analysis, use the *same complete quadrat pairs*, center both predictor and each response within **species × physical reserve × crop × Edge/Core**, then calculate a single raw linear slope. These observations are **not independent 157/117/115 landscape units**; the only geographical independent units are 4–6 reserves. All secondary slopes are exploratory, with no small-cluster frequentist p-value asserted.

| Species | D slope per +10 percentage-point local bare ground | D slope per +1 natural-log unit of local floral count |
|---|---:|---:|
| GORO | +0.106 | +4.896 |
| LARO | +0.758 | −1.258 |
| POAR | −8.618 | **−101.892** |

For POAR the local-neighbourhood floral slope remains negative on deletion of **each whole physical reserve** (slope range **−135.622 to −56.374** seeds/plant per unit ln(1+neighbourhood flowers)); the four **within-reserve** slopes are all negative, albeit very different (approximately −61, −43, −64, −296). In LARO the analogous leave-reserve-out range crosses zero (−2.709 to +1.542). The POAR association is a useful *post hoc* ecological lead: the local floral neighbourhood covaries with the apparent supplementation contrast. It is **not** proof that floral competition reduces pollen delivery or that a particular landscape is a different mechanistic regime.

For context, LARO OP seed production is lower with more bare ground, also known from the original paper. Its D slope with bare ground is positive on this plant-total scale and retains positive sign in whole-reserve deletions (range +0.202 to +1.312), but source species × context × variable testing and low number of independent reserves forbid promoting a new drought-mediated pollen rescue mechanism.

## Exact, noncausal reproductive accounting: rate and floral display

This comparison was **designed post hoc after seeing the source and the POAR signal**, not a pre-registered test. It is an exact arithmetic identity for a pair of *different treatment plants*. Let \(F\) be each individual's observed flower count, \(Y=T/F\) its viable-looking seeds per flower, and \(T=F Y\) the total seeds. For treatment labels \(0=\mathrm{OP}\) and \(1=\mathrm{OPSupp}\),

\[
T_1-T_0 =
\underbrace{\frac{F_1+F_0}{2}(Y_1-Y_0)}_{\mathrm{flower\text{-}specific\ yield\ term}}
+
\underbrace{\frac{Y_1+Y_0}{2}(F_1-F_0)}_{\mathrm{floral\ display\ term}}.
\]

The two terms add *exactly* at each eligible quadrat; no assumed within-plant cross-treatment counterfactual is hidden. The source has positive flower counts in all 157 complete LARO and 115 complete POAR matched pairs; GORO's denominator is unavailable.

| Complete-pair, unweighted quadrat mean | Total seed difference | Flower-specific yield term | Floral display term |
|---|---:|---:|---:|
| LARO (157) | **+1.783** | +2.154 | −0.370 |
| POAR (115) | **−8.304** | **+8.985** | **−17.289** |

For POAR, the negative pooled per-plant difference is the sum of a positive rate-associated term and a larger negative flower-number-associated term. **This does not show that hand pollination caused flowers to disappear**: the number of flowers belonged to different, arbitrarily allocated individual plants. These data separate dimensions of realized production, not a causal mediation pathway.

The within-transect POAR neighbourhood-floral slope of −101.892 decomposes **exactly** into −61.555 (floral-display term) and −40.337 (yield term), using the source's actual flower counts and seed totals. The *plain unweighted seeds-per-flower contrast* has slope +0.908 and a whole-reserve deletion range spanning negative/positive values (−1.004 to +2.747). Thus the strong raw total-seed association should not be read as the same association in fertilization success per flower. It also cannot be attributed solely to flower number: both product components contribute to the raw slope.

An individual bloom-rich quadrat can also have treatment-plant differences in baseline flower count, seed variance, seed damage, or plant resources. In particular, the negative POAR seed-total response is **not** independently replicated by four studies; all four reserves are from the same landscape.

## Audit and evidence tier

- Exact original Figshare source bytes + attribution: [raw files](../evidence/meta_extraction/sevenello_2026_raw/).
- Fixed **pre-outcome** design: [SEVENELLO_POLLEN_ADDITION_CONTEXT_DESIGN_2026-10-19.md](SEVENELLO_POLLEN_ADDITION_CONTEXT_DESIGN_2026-10-19.md).
- Primary executable: [audit_sevenello_pollen_addition_20261019.py](../scripts/audit_sevenello_pollen_addition_20261019.py), [source-hash verified workflow](../.github/workflows/sevenello-pollen-addition.yml); source-MD5 and analysis CI passed at least once.
- Post hoc per-plant decomposition: [audit_sevenello_floral_display_decomposition_20261019.py](../scripts/audit_sevenello_floral_display_decomposition_20261019.py) and [dedicated workflow](../.github/workflows/sevenello-floral-display.yml); this must not be claimed green without a successful run.
- Every published pair was preserved with no treatment-specific negative-result deletion. Only 11 quadrats were excluded from the **three-species primary pair set** due to missing OP and/or OPSupp seed counts; no zeros were substituted.
- This is independent of previous Wandoo and Cardiopetalum data **as a publication**, but its three plant species and seven sites are **not three or seven independent publications**.
- The current five-primary-cluster corpus, 8 matched quantitative I–F programmes, 16-programme process-function qualitative map, publication freeze, and \`submission_ready=false\` are all unchanged. The failed existing monolithic check depends in part on externally inaccessible *Brosimum* Figshare binaries; new source-specific successful CI cannot override it.

## Strongest honest ecological takeaway

**Within an experimentally manipulated, species-rich remnant landscape, geographic and focal-plant floral context can change the sign and apparent magnitude of measured pollen-supplementation benefit, even using the same observed seeds.** These patterns support measuring the **whole plant's floral display, per-flower seed yield, and site-level environment together** when evaluating whether interaction quantity translates into fitness. They do not demonstrate universal edge pollen stress, a new abiotic limitation law, compatible pollen quality, or a causal post-pollination filter.
