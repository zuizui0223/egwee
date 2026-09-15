# Testing whether fragmentation acts as a single biological state: a cluster-first synthesis of plant interaction, reproduction and genetic responses

**Status:** active results-bearing manuscript. The primary direct-effect synthesis is closed at five admitted programme/study clusters for the current claim. The fifth-cluster robustness test has been completed; additional systems are not sought to repair significance.

## Abstract

1. Habitat fragmentation affects pollination, movement, reproduction and genetic state, but these responses are usually analysed separately. We asked whether multiple biological layers measured within the same fragmented plant systems can be treated as one exchangeable deterioration state.

2. We retained five independent direct fragmented-versus-reference programme/study clusters comprising 17 Hedges-g marginal effects, explicitly preserving within-system dependence and excluding incompatible continuous-gradient effects from the primary synthesis.

3. The five-cluster Fisher synthesis rejected complete layer exchangeability (`chi-square(10)=22.65`, `p=0.0121`), but the result did not survive removal of the influential *Serapias lingua* cluster (`p=0.1819`). Thus the pooled direct-effect result is not leave-one-cluster-out robust.

4. A fifth independent replicated Chaco programme provided a direct robustness test. Across three dependent species subsystems, fragmentation reduced both pollen-tube interaction support and fruit set, but their effect magnitudes were not detectably separated (`p_programme=1.0`). A separate continuous-gradient *Eucalyptus wandoo* system showed strong layer discordance but remained outside the primary Hedges-g synthesis.

5. **Synthesis.** Multi-layer deterioration and state separation are distinct ecological outcomes. Fragmented plant systems can exhibit either separated or concordant response regimes, and the current evidence does not support a universal fragmentation state-separation syndrome. The next empirical problem is to identify the biological conditions that determine which response geometry occurs.

## Keywords

eco-genetics; forest fragmentation; genetic diversity; meta-analysis; plant-pollinator interactions; reproductive function; response heterogeneity; state separation

## Introduction

Habitat fragmentation can alter plant density, pollinator visitation, pollen and seed movement, reproductive output, mating patterns and genetic diversity. Those responses are commonly synthesized one endpoint class at a time. Existing quantitative reviews have documented fragmentation effects on pollination and reproductive success, plant genetic diversity, progeny genetic and performance responses, fine-scale genetic structure and pollinator abundance (Aguilar et al., 2006, 2008, 2019; Méndez-Rojas et al., 2023; Olhnuud et al., 2025). This literature establishes that fragmentation is often detrimental. It does not, by itself, establish whether the affected biological layers behave as one common deterioration state within the same systems.

That distinction matters because a decline in multiple endpoints is not equivalent to equal decline across endpoints. A fragmented population could experience strong disruption of interaction or mating processes while adult standing genetic diversity remains relatively buffered by demographic and generation-time lags. Conversely, interaction and reproductive-function layers could deteriorate together at similar magnitudes. Treating these alternatives as one phenomenon can obscure which biological state has actually changed and which ecological function remains buffered.

EGWEE therefore asks a stricter within-system question: when multiple biological layers are measured under the same fragmentation contrast, are their standardized responses exchangeable, or do they separate? The focal layers are demographic/resource support (`D`), realised interaction or pollen receipt (`I`), movement or mating connectivity (`C`), reproductive function (`F`), adult standing genetic state (`G_adult`) and offspring or juvenile genetic/mating state (`G_offspring`). The paper distinguishes two propositions that are often conflated: fragmentation can affect multiple biological layers, and fragmentation can separate those layers so that effect magnitudes differ beyond sampling uncertainty. The second proposition is stronger.

### Primary hypothesis — response layers are not universally exchangeable

Our primary hypothesis was that biological layers need not share one fragmentation response. We therefore tested equality of admitted layer effects within each study/programme cluster and then asked whether evidence against exchangeability persisted across independent systems. Importantly, leave-one-cluster-out influence was treated as part of the claim rather than as an optional robustness appendix.

The current evidence also motivated two extensions: cohort/history lag between adult and offspring genetics, and process compensation linking movement or interaction responses to reproductive function. However, those extensions require more independently replicated same-frame systems than are currently available. They are retained as secondary hypotheses rather than used to enlarge the present conclusion.

## Materials and Methods

### Protocol and study universe

The active meta-analysis protocol was frozen on 11 September 2026 before the current synthesis. Screening started from major prior quantitative syntheses of plant pollination/reproduction, plant genetics, progeny responses, fine-scale genetic structure and pollinator responses to fragmentation, then extended backward and forward through the primary literature. Previously audited EGWEE systems were used as search seeds rather than automatic inclusions.

The primary target population comprised flowering-plant studies with a direct fragmented-versus-reference comparison or an equivalent source-defined two-group fragmentation contrast. Continuous-only fragmentation gradients were retained in a separate correlation-effect stream and were not converted into the direct primary effect family merely to enlarge sample size.

A study/programme entered the primary state-separation synthesis only when at least two predeclared biological layers could be represented under the same fragmentation comparison with valid independent units and recoverable sampling uncertainty. Nested plants, flowers, fruits, progeny, loci or repeated observations were not promoted to fragmentation replicates. Duplicate reports and shared biological observations were linked at the programme/study level.

### Response layers and effect orientation

Eligible endpoints were assigned before quantitative synthesis to the following biological layers: `D_resource_demography`, `I_interaction`, `C_movement_connectivity`, `F_reproductive_function`, `G_adult` and `G_offspring`. A measured endpoint was not moved between layers after its effect size was known.

The primary effect family was Hedges' `g` for fragmented minus reference conditions. Effects were oriented so that negative values indicate lower biological support or function under fragmentation. For deterioration metrics where larger raw values indicate poorer state, the sign was reversed only after preserving the raw direction and an explicit orientation rule. Sampling variances followed the canonical large-sample Hedges-g semantics already used across the direct EGWEE primary stream.

Continuous-gradient studies were analysed separately using Fisher-transformed correlations where an effect could be reconstructed without strong transformation assumptions. Hedges-g and Fisher-z effects were never pooled into one primary statistic.

### Cluster-first dependence handling

The independent denominator was the programme/study fragmentation cluster, not the number of extracted endpoints. Multiple layers from the same system were retained as dependent effects. When paired unit-level information was available, within-cluster covariance was reconstructed from aligned observations. Low-rank or pairwise covariance components were retained rather than forcing singular full matrices to invert.

For each direct cluster, covariance-aware pairwise contrasts were used to test equality of retained layer effects. Where a cluster contained more than one pairwise comparison, the cluster-level p-value used the declared within-cluster multiplicity correction. Each study/programme contributed one cluster-level p-value to the cross-system synthesis.

The five currently admitted direct clusters were:

1. `ML001` *Serapias lingua*: C / F / G_adult;
2. `ML002` *Brosimum alicastrum*: C / F;
3. `ML003` *Spondias purpurea*: C / G_adult / G_offspring;
4. `ML014` *Eucalyptus socialis*: G_mating / F;
5. `ML020` Aizen–Feinsinger Chaco programme: three dependent species × I / F, counted once.

Together they contain 17 marginal effects. ML020 contains three plant species sharing the same four Chaco landscapes and therefore contributes one programme cluster, not three independent systems.

### Cross-cluster state-separation test

Cluster-level p-values were combined using Fisher's method. The primary null was that within each direct cluster the admitted layer effects were exchangeable/equal on that cluster's Hedges-g scale. A pooled rejection was interpreted only together with leave-one-primary-cluster-out sensitivity.

After the four-cluster synthesis identified ML001 *Serapias* as influential, the scientific target for a fifth same-effect-family cluster was fixed as a robustness question: does the conclusion survive removal of ML001 after adding one independent admissible system? This was not a search for a smaller full-corpus p-value. The eventual ML020 Aizen–Feinsinger programme was discovered retrospectively because its public Appendix I values were visible during recovery. To prevent within-paper selection, all three species explicitly identified by the source as having the complete four-site replicated habitat frame were retained, with the same endpoint pair (pollen tubes as I and fruit set as F) for each species.

For ML020, each species used four small-fragment habitat-unit means and four continuous-forest habitat-unit means. Within-species I/F covariance was reconstructed from group-centred paired site values. The three dependent species-specific I–F tests were combined only through an internal Bonferroni programme gate, and the resulting ML020 programme p-value entered the primary Fisher synthesis once.

### Separate continuous-gradient generalisation

`ML015 Eucalyptus wandoo` was retained as a separate Fisher-z gradient generalisation cluster. It included interaction, reproductive-function and adult-genetic effects against a response-free fragmentation geometry, but it contributed zero direct Hedges-g primary effects and was never combined with the primary Fisher statistic.

### Search-stop rule

The fifth same-effect-family robustness test was treated as a terminal test of the current claim. A sixth cluster was not sought merely because removal of ML001 remained non-significant. Any future corpus expansion must be justified by a separately declared coverage or moderator goal before candidate outcomes are inspected.

## Results

### Primary direct-effect synthesis

The five admitted direct clusters produced the following cluster-level p-values:

- ML001 *Serapias*: `0.00354530`;
- ML002 *Brosimum*: `0.19911670`;
- ML003 *Spondias*: `0.17406774`;
- ML014 *Eucalyptus socialis*: `0.09831774`;
- ML020 Chaco programme: `1.00000000`.

Combining the five cluster p-values gave `chi-square(10)=22.64771647`, **`p = 0.01212432`**. The pooled direct-effect corpus therefore rejected complete exchangeability of biological response layers at the 0.05 level.

### Influence of ML001 Serapias

The pooled rejection is not leave-one-cluster-out robust. Removing ML001 after admission of the fifth cluster retained ML002, ML003, ML014 and ML020 and gave `chi-square(8)=11.36345148`, **`p = 0.18194353`**. Thus the direct cross-system rejection did not survive removal of *Serapias*.

The other leave-one-cluster-out analyses retained rejection: omit ML002, `p=0.01276794`; omit ML003, `p=0.01407214`; omit ML014, `p=0.02116199`; omit ML020, `p=0.00384724`. The last value recovers the previous four-cluster synthesis.

### Independent fifth-cluster test: concordant I and F deterioration

ML020 provided the independent same-effect-family robustness test using the replicated Aizen–Feinsinger Chaco programme. Fragmentation reduced both pollen-tube interaction support and fruit set in all three retained species, but their effect magnitudes were not detectably separated.

For *Atamisquea emarginata*, I was `g=-0.71280256` and F was `g=-1.00477681`, with covariance-aware I–F `p=0.79824355`. For *Cercidium australe*, I was `g=-0.63733120` and F was `g=-1.13852812`, with `p=0.61830903`. For *Prosopis nigra*, I was `g=-0.48057139` and F was `g=-1.13549676`, with `p=0.55736567`.

The frozen within-programme Bonferroni gate was therefore **`p_ML020=1.0`**. ML020 was admitted regardless of significance. Its result shows fragmentation-associated multi-layer deterioration without detectable state separation between the focal I and F layers.

### Separate gradient evidence

ML015 *Eucalyptus wandoo* showed strong discordance on the separate Fisher-z gradient scale. The canonical effects were I pollen tubes `z=+0.69029123`, F seeds per fruit `z=-0.87593080` and G_adult H_e `z=-0.41117288`. The strongest I–F contrast had `z=3.33386`, two-sided `p=0.00085651`; Bonferroni correction across the three endpoint pairs gave `p_cluster=0.00256953`.

This gradient result provides independent evidence that strong layer discordance occurs in nature, but because its exposure representation and effect family differ from the primary direct stream it was treated as generalisation evidence rather than a sixth primary replicate.

## Discussion

### Conditional state separation, not a universal syndrome

The primary synthesis separates two ecological statements that are easy to conflate. Fragmentation can affect multiple biological layers, yet those layers need not differ from one another in effect magnitude. Across the five direct clusters, the pooled Fisher test rejected complete exchangeability, showing that the current corpus contains genuine cross-layer separation. However, that result was materially dependent on ML001 *Serapias*. Once *Serapias* was removed, the pooled rejection disappeared even after admission of a fifth independent same-effect-family programme.

The defensible conclusion is therefore conditional state separation. The available systems do not support a universal single deterioration axis, because some clusters show strong layer discordance. They also do not support a robust universal state-separation syndrome, because the independent Chaco programme showed interaction and reproductive function declining together without detectable separation and because the pooled result failed the key leave-*Serapias*-out test.

### Multi-layer deterioration is not state separation

ML020 is especially informative because it was not excluded when it failed to reproduce layer separation. In all three Chaco species, both pollen-tube support and fruit set were lower in small fragments than in continuous forest. If the analysis had been based only on whether each endpoint declined, the system would have appeared to support a generic multi-layer fragmentation syndrome. The within-system comparison shows something different: the two layers declined at statistically similar magnitudes.

This distinction matters for ecological interpretation. A system in which interaction and reproductive function fall together may require different mechanistic explanations and monitoring priorities from a system in which interaction, movement, reproduction and genetic state decouple. Endpoint-specific syntheses can establish average vulnerability; a cluster-first synthesis is needed to ask whether the response geometry itself is concordant or separated.

### Why the influential-system result is scientifically useful

The loss of significance after removing *Serapias* is not simply a weakness to be hidden by adding more studies until the p-value changes sign. It defines the current claim boundary. The five-cluster corpus is small and heterogeneous in which layer pairs are represented. Under those conditions, a statistically significant pooled result can coexist with substantial influence from one system. Reporting that influence explicitly prevents the synthesis from being presented as a general mechanistic law that the data do not support.

The result also reframes the next empirical question. Rather than asking whether fragmentation always separates biological states, future work should ask which system properties determine separation versus concordant decline. Candidate moderators include mating system, reproductive assurance, pollination mode, life history, fragmentation age and the distinction between standing adult genetic state and contemporary process measures. Those moderators should be tested only after sufficient independent same-frame systems accumulate.

### Status of the original H2 and H3 extensions

Adult-versus-offspring genetic differences remain biologically motivated, especially in *Spondias* and *Conospermum*, but the current admissible primary corpus does not support a sufficiently replicated cross-system cohort-lag test for a headline conclusion. In *Spondias*, adult–juvenile and adult–seed covariance-aware contrasts cross zero. Cohort/history lag therefore remains a secondary hypothesis rather than a current paper-level result.

Likewise, the original plan proposed C–F and I–F cross-system relationships to test whether movement or interaction responses predict reproductive function. The number of independent same-frame paired clusters is currently too small for a stable moderator model. Mechanistic systems such as Miyake *Camellia–Zosterops* and *Crepis* remain useful interpretation anchors, but they do not yet support a fitted general compensation law.

Neither extension is used to inflate the present conclusion.

### Relationship to the NEE theory programme

EGWEE was motivated as a natural-data counterpart to a theoretical programme in which fragmentation can reorganize multiple ecological and genetic states. The present synthesis does not validate those finite-model operators in nature. Instead, it tests the more basic empirical premise that biological response layers need not behave as one state under fragmentation.

The natural evidence supports that premise conditionally: separated and concordant regimes both occur. That result is more informative for theory than an unconditional confirmation would be, because it implies that any useful mechanistic framework must explain not only why states can separate, but also why they sometimes remain concordant.

### Limitations

The primary direct-effect denominator is five independent programme/study clusters. That is sufficient for the declared cluster-first synthesis and influence test, but insufficient for stable cross-system moderator estimation. The admitted clusters also differ in which biological layers are jointly represented, so the current synthesis tests non-exchangeability within systems rather than estimating one fully crossed layer-by-layer meta-regression across all taxa.

The overall meta-analysis is retrospective. ML014 was recovered under a prospectively locked additional-cluster contract, whereas ML020 was an external retrospective recovery whose Appendix I values were visible during discovery. The ML020 analysis therefore retained all source-explicit four-site species and a common endpoint pair to reduce within-paper selection, but it is not presented as an outcome-blind prospective validation.

Finally, the strong ML015 gradient result is deliberately kept outside the primary Hedges-g synthesis. Its concordance with the broader state-separation concept strengthens generalisation, but mixing effect families would create a larger denominator at the cost of a less defensible estimand.

## Conclusion

Habitat fragmentation affects multiple biological layers, but the available natural systems do not support a single universal response geometry. Some systems show strong separation among interaction, movement, reproductive and genetic responses, whereas a replicated Chaco programme shows interaction and reproductive function declining together. The pooled direct-effect synthesis rejects layer exchangeability, but that rejection disappears when the influential *Serapias* system is removed. The empirical result is therefore conditional state separation, not a universal fragmentation syndrome.

The current manuscript may claim five admitted direct same-effect-family programme/study clusters, a pooled Fisher rejection at `p = 0.01212432`, loss of that rejection after omitting ML001 at `p = 0.18194353`, an independent ML020 concordant-decline result with `p_ML020=1.0`, and separate ML015 gradient discordance. It may not claim robust universal state separation, a universal layer ordering, a confirmed cohort lag, a general compensation mechanism, direct validation of the NEE operators, or that a sixth cluster should be sought merely to restore Serapias-independent significance.
