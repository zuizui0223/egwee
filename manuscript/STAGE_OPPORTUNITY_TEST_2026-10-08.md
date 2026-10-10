# Stage opportunity versus reproductive quality

Status: **post hoc causal-competitor crosswalk, not a fitted stage-switch law**. This note is an ecological exploration in EGWEE (empirical plant ecology), not EGWE/NEE operator theory, and does not add to any existing meta-analysis denominator.

## Question

Can habitat fragmentation reduce population renewal even where mating quality or early reproductive output looks intact, because the *availability* of suitable recruitment microhabitat changes independently of seed or seedling quality?

This must distinguish (i) performance conditional on being in an observed microhabitat, (ii) the abundance of each microhabitat across an entire patch, (iii) propagule arrival there, and (iv) subsequent survival. Simply counting visited flowers, measuring glasshouse germination or sampling only surviving seedlings conditions on different stages.

## Source-verified anchor: Myrtus communis

Gonzalez-Varo, Nora & Aparicio (2012; doi:10.1016/j.ppees.2011.11.002, open author manuscript at https://rodin.uca.es/handle/10498/34772) examined 10 Mediterranean woodland remnants, four large and six small, over 2007–2010; four large and four small patches underlie the published Figure 5 recruitment comparison. Their paper reports mean *cumulative* recruitment probabilities (CP) of 1.9e-4 in large versus 2.0e-5 in small patches (approximately 9.5-fold), but *overall*, microhabitat-availability-weighted probabilities (OPR) of 1.5e-5 versus 3.5e-7 (approximately 42.9-fold, described by the source as 44-fold). The relative contrast is therefore approximately 4.5 times stronger for OPR than for CP, using the displayed group means.

This **ratio of ratios is descriptive**. It is not a measured causal multiplier from experimentally changing safe-site area, nor an independently estimated parameter: grouped means, non-linear weighting, site coverage and years differ. The paper's own model-based decomposition attributes more than 75% of OPR differences to microhabitat availability; that claim belongs to the source, not to a new EGWEE causal estimate.

Gonzalez-Varo et al. (2010; doi:10.1111/j.1365-2664.2010.01879.x) found that effective outcrossing and greenhouse seedling production were highest in the small-connected group (mean t_m 0.62) and lowest in small-isolated plants (mean t_m 0.13). For the named overlapping patches, PTR had outcrossing t_m 0.72 and greenhouse final normal seedling production 68.3% but the lowest field early establishment performance in the 2012 study; CRB had t_m 0.13, greenhouse 43.3% and some better field early-stage percentages. The 2012 authors themselves discuss this rank reversal. Both papers include partially overlapping population names but not a synchronized tagged-seed series; CRB lacked accumulated juveniles despite relatively favourable short-term field percentages.

Gonzalez-Varo et al. (2015; doi:10.1111/1365-2664.12424) found current myrtle occurrence in 110 of 304 patches to align better with historical (1956) than contemporary (2002) woodland cover. The result supports lagged adult occupancy, **not observed subsequent population extinction**, and is a third publication from the same species-region system, not independent biological replication.

## Independent taxon, but not pooled replication

Uriarte et al. (2010; doi:10.1890/09-0785.1) studied tropical *Heliconia acuminata* in 10 mapped forest plots of 0.5 ha. Their analysis attributed the strongest establishment constraint to safe sites, and linked landscape fragmentation to less favourable light heterogeneity, with weaker fragmentation responses in seed production and dispersal. This strengthens the plausibility of a *distinct taxon and biome* route, but the two programmes lack common stage-level estimands and cannot be pooled as replicated effect sizes.

Duncan et al. (2009; doi:10.1890/08-1436.1) had already formulated recruitment functions based on seed supply and safe-site availability. The conditional-versus-available distinction, sequential bottlenecks and extinction debt are **not new discoveries**.

## Identifiable ecological contrast

Let a_m denote the fraction of a patch footprint that provides microhabitat m; let q_m be the probability of arrival and subsequent recruitment conditional on that microhabitat (using a consistently specified source population and reproductive episode). The minimal descriptive functional is

    R_area = sum_m a_m q_m

Only after measuring the full microhabitat coverage, including unusable or zero-recruitment area, does this estimate *whole-patch* recruitment opportunity. Normalizing the observed favourable sites to sum to one would discard precisely the spatial scarcity under test. Under habitat gradients, the q_m and a_m can change simultaneously and their contributions cannot generally be disentangled with a single cross-sectional observation.

The falsifiable disagreement is not whether R_area mathematically includes a_m. It is whether **measured changes in opportunity explain held-out field recruitment better than mating/seed quality alone and predict which restoration action succeeds**.

For each independent patch and reproductive episode, record: effective compatible donors / outcrossing and progeny quality; propagule number and spatial rain; microhabitat area and safe-site traits; seedling emergence, summer survival and cumulative recruits. Link maternal seed lots to experimental outplanting sites. Repeated flowers, seeds, seedlings and microsite plots are nested units, not extra landscape replicates.

## Critical three-way distinction: background loss, fragmentation contrast and rescue value

Three different stage rankings must not be conflated.

- **Background attrition**: a transition with a low reference probability p_ref,j loses many propagules in any landscape. A useful descriptive loss measure is -log(p_ref,j) when p_ref,j is positive.
- **Fragmentation sensitivity**: log(p_frag,j / p_ref,j) describes how that *same* transition differs between fragmented and reference sites. This does not identify the causal effect of fragmentation without a valid exposure design.
- **Intervention leverage**: improvement in actual recruits under an experimentally imposed action, compared with the randomized control, on a *fixed whole-patch denominator*. This is not identifiable from either the baseline attrition or the observational contrast alone.

A source-verified counterexample to treating these rankings as interchangeable is Valdes & Garcia (2013, doi:10.1016/j.baae.2013.08.006): in fragmented temperate forests, *Primula vulgaris* showed strong seed/dispersal limitation in experimental seed-sowing plots, but the seed-emergence limitation did **not** track measured landscape-alteration gradients. Survival and growth after subsequent summer/winter periods did respond to landscape and microhabitat conditions, including herbivore/predator exclusion in some settings. This is not an independent estimate of a universal stage switch; it is a concrete case where **the dominant standing bottleneck and the fragmentation-sensitive transition differ**.

Consequently the operative ecological hypothesis is more exact than 'fragmentation moves the bottleneck': **fragmentation can damage stages that are not the most limiting in the reference life cycle, so selecting restoration solely by the highest standing mortality can mis-target the fragmentation-associated deficit**. To establish that mechanistically, measure all three rankings on aligned biological units, then test which stage-specific intervention rescues whole-patch recruits in held-out landscapes.

## Three competing intervention models

**Quality-limited:** under controlled safe-site availability and arrival, experimentally improved compatible/outcross pollen raises viable-seed and later recruit yield; microsite enhancement adds little after adjusting for its own availability.

**Opportunity-limited:** the same standardized high-quality seeds establish poorly where suitable microhabitat is scarce or degraded; restoration of safe-site area/quality improves recruits per patch footprint more than pollen rescue, even if greenhouse progeny ranks higher elsewhere.

**Joint / switching constraint:** both treatments matter, with treatment rankings differing among patches or seasons; a cross-stage ranking reversal or interaction alone is not evidence of a new universal switching mechanism. Count interventions on the same downstream recruit scale and compare out-of-patch predictions.

A feasible prospective factorial separates pollen-provenance rescue on maternal plants and safe-site improvement during transplantation of their offspring. Split seed lots among spatial treatments, randomize within *independent* landscapes, measure actual dispersal separately, and predefine recruits per initial flower and recruits per standardized deposited seed as separate targets. Hold out complete landscapes for prediction. On an additive scale, a positive treatment interaction can arise mechanically from multiplied transition probabilities; mechanism demands stage-specific measurements rather than interaction significance alone.

## Longitudinal falsification check: Heliconia `stock` versus `transition`

An observational reanalysis of the published *Heliconia acuminata* demographic archive was conducted separately from the source-graded Myrtus/Primula/Heliconia literature ledger (see [cohort audit](HELICONIA_COHORT_OBSERVATION_AUDIT_2026-10-08.md)). In balanced 1999–2005 cohorts, the absolute average number of observed new seedlings per 0.5-ha plot is lower in fragmented forest (21.20) than continuous forest (36.93), but the corresponding count normalized by the **previous year's measured living stock** is almost identical (7.19 versus 7.25 per 100 prior measured individuals). This illustrates that an absolute per-area shortfall is not, by itself, evidence that *per-existing-individual* new establishment is impaired.

It does **not** establish that fragmentation causes the difference solely through population size: the denominator includes non-reproductive stages, stock can itself be a mediator of past fragmentation, and published life-table studies already find size- and stage-specific demographic effects. In the same archive, first-year survival among known fates differs little, but many tagged seedlings are initially unlocated and later found alive, so full survival and long-term population growth cannot be certified from this shortcut.

Thus the source-derived competing explanations now include not only mating quality versus safe-site opportunity, but also **population stock, life-stage structure and detection**. A claim that a stage is *the* fragmentation bottleneck requires a common outcome (new reproductive individuals or recruits per footprint), stage-resolved measurement, and held-out landscape-level test beyond normalizing away historical population differences.

## Three-year outcome does not rescue a single-stage explanation

The [multiyear Heliconia ascertainment audit](HELICONIA_MULTYEAR_SURVIVAL_AUDIT_2026-10-08.md) adds a critical falsification of a tempting alternative: comparing only the records present three years later falsely suggests a +3.75 percentage-point fragment survival advantage. Carrying forward every recorded death changes the 3-year plot-mean known-fate values to continuous 0.69455 versus fragment 0.69265 (ranch-restricted label-reallocation p≈0.954). Unknown states persist, and some missing individuals are later found alive. Thus an apparent reversal in long-term survival can be produced by the record structure alone. This is an **observation-process artifact**, not evidence of stage-specific compensation, and it does not identify biological survival equivalence.

The strongest ecological claim remains that raw recruitment, stock-normalized recruitment, true stage-specific survival, and population renewal are different quantities. A universal 'limiting stage moved' law is not identified. Source archives should not be treated as independent cross-species replications just because they contain many individual-year records.

## Stop rules and novelty ceiling

1. Do not add these case reports to the frozen 5-cluster direct synthesis, the 8 matched I-F programmes, the 16-programme topology or the SF06 public-S1 denominator.
2. Do not count 2010/2012/2015 Myrtus as three independent species/landscape replications; cross-paper rank inversion is not synchronized mediation.
3. Do not infer intervention-effect sizes from the 2012 observational microhabitat decomposition.
4. Do not call recruitment-stage importance or seed/safe-site limitation new. A genuinely stronger claim requires **held-out, independently replicated identification of which intervention increases realized recruitment**, beyond the best simpler quality-only, opportunity-only and baseline models.
5. Until such tests exist, this is a *mechanistic competing-explanation protocol* supporting a narrower EGWEE narrative, not a new confirmed law.

## 10 October observation-completeness qualification (post hoc)

A source-hash-verified ID-level audit [found three continuous-forest plot-years whose entire archived plant status was `missing`, not `measured` or `dead`](HELICONIA_LAGGED_FLOWERING_SENTINEL_2026-10-10.md): CF-4 and CF-5 in 2000 and CF-6 in 2003 (565 plant-year records). **513 of these same IDs were measured alive in the immediately following year.** Therefore seven complete *calendar* years does **not** imply complete observation of each plot-year; the all-missing cells' zero newly recorded seedlings cannot certify true zero biological establishment.

The new audit reports an 85/91 plot-year prediction sensitivity requiring both the preceding and outcome census to contain at least one confirmed observed living plant, and compares lagged observed reproductive-activity indicators with prior living stock in held-out plots and ranches. Prior nominal recruit counts are retained for provenance, **not** promoted to complete-ascertainment estimates. Neither the source audit nor the predictive model establishes a fragmentation-specific causal transition or a stage-switching law.

## Chronological validation update — 10 October 2026

**Important ceiling change:** the [source-pinned forward-year falsification](HELICONIA_TEMPORAL_TRANSFER_FALSIFICATION_2026-10-10.md) shows that the strong **same-year spatial transfer** performance of prior living stock **does not carry over to future calendar years** under the simple fitted models. On 34 truly forward-year predictions (2003–2005), prior-stock MSE is 867.37 versus 467.61 for an earlier-year mean baseline. A subsequently explored two-year history of prior *observed seedling entries* scores 345.42. A balanced ten-plot sensitivity retains the ordering (stock 1012.59, baseline 496.76, recruitment history 385.95). The direct 2002–2003 comparison in those same ten plots shows observed new entries 44.5→14.1 per plot while prior measured living stock rises 455.0→498.8, with 9/10 plots losing new entries. This is **not** identified as a common causal environmental shock, an effective pollination mechanism, or a multi-programme ecological law. Both spatial and temporal results remain valid for their **different prediction targets**; do not report the spatial leader as a certified future-year sentinel.
