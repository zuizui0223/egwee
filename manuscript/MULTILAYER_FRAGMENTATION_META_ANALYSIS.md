# Testing whether fragmentation acts as a single biological state: a cluster-first synthesis of plant interaction, reproduction and genetic responses

**Status:** active results-bearing manuscript spine. The primary direct-effect synthesis is closed at five admitted programme/study clusters for the current claim. The fifth-cluster robustness test has been completed; additional systems are not sought to repair significance.

## Central empirical question

Habitat fragmentation is usually analysed endpoint by endpoint: pollination, gene flow, reproduction, adult genetic diversity, or offspring genetic state. The empirical question here is different:

> **Within the same fragmented plant systems, can those biological responses be treated as one exchangeable deterioration state, or do response layers change by different magnitudes?**

The paper therefore distinguishes two propositions that are often conflated:

1. fragmentation affects multiple biological layers;
2. fragmentation separates those layers, so their effect magnitudes are not exchangeable.

The second proposition is stronger and is the primary target of EGWEE.

## Primary evidence architecture

The primary stream contains only direct fragmented-versus-reference contrasts represented in the same Hedges-g effect family. Effects are oriented so negative values indicate reduced biological support/function under fragmentation. Continuous fragmentation gradients remain in a separate Fisher-z stream and are never pooled into the primary Fisher statistic.

The independent denominator is the **programme/study cluster**, not the number of extracted rows, species, endpoints, plants, flowers, progeny, or loci.

The current primary denominator is **five independent clusters / 17 marginal effects**:

1. `ML001` *Serapias lingua*: C / F / G_adult;
2. `ML002` *Brosimum alicastrum*: C / F;
3. `ML003` *Spondias purpurea*: C / G_adult / G_offspring;
4. `ML014` *Eucalyptus socialis*: G_mating / F;
5. `ML020` Aizen–Feinsinger Chaco programme: three dependent species × I / F, counted once.

Within-cluster dependence is reconstructed where possible. Missing layers are not coded as zero and incompatible effect families are not converted merely to enlarge the denominator.

## Primary hypothesis — response layers are not universally exchangeable

For each admitted cluster, EGWEE tests whether the retained biological-layer effects can be treated as equal on that cluster's own Hedges-g scale. Cluster-level p-values are then combined with Fisher's method, with leave-one-cluster-out sensitivity reported as part of the claim rather than as an optional diagnostic.

Current cluster-level p-values are:

- ML001 *Serapias*: `0.00354530`;
- ML002 *Brosimum*: `0.19911670`;
- ML003 *Spondias*: `0.17406774`;
- ML014 *Eucalyptus socialis*: `0.09831774`;
- ML020 Chaco programme: `1.00000000`.

The five-cluster Fisher combination is:

- `chi-square(10) = 22.64771647`;
- **`p = 0.01212432`**.

Thus the current primary corpus rejects complete exchangeability of biological response layers **as a pooled five-cluster statement**.

## The decisive robustness result — the pooled rejection is Serapias-dependent

The pooled rejection is not leave-one-cluster-out robust. The key sensitivity test was defined before admitting a fifth independent same-effect-family programme: does the conclusion survive removal of `ML001 Serapias`?

It does not.

After adding ML020 and omitting ML001:

- retained clusters: ML002 + ML003 + ML014 + ML020;
- `chi-square(8) = 11.36345148`;
- **`p = 0.18194353`**;
- do not reject layer exchangeability.

Other leave-one-cluster-out analyses retain rejection:

- omit ML002: `p = 0.01276794`;
- omit ML003: `p = 0.01407214`;
- omit ML014: `p = 0.02116199`;
- omit ML020: `p = 0.00384724`.

The paper therefore **must not claim robust general cross-system state separation**. The defensible result is narrower: the present corpus contains clear state separation, but the cross-system rejection is materially driven by the strongest *Serapias* system.

## Independent fifth-cluster test — fragmentation can depress I and F together

ML020 provides the requested independent same-effect-family test using the replicated Aizen–Feinsinger Chaco programme. The source has four study landscapes and three source-explicit species with the habitat treatments replicated on the common four-site frame. All three species were retained as dependent subsystems inside one programme cluster rather than selecting the species with the strongest contrast.

The primary comparison is small fragment versus continuous forest, using one site-specific habitat-unit mean per site and condition. Plant, flower, fruit and pollen-tube counts are nested and are not promoted to fragmentation replication.

For all three retained species, fragmentation reduced both pollen-tube interaction support and fruit set, but the magnitudes were not detectably separated:

- *Atamisquea emarginata*: I `g=-0.71280256`, F `g=-1.00477681`, I–F `p=0.79824355`;
- *Cercidium australe*: I `g=-0.63733120`, F `g=-1.13852812`, I–F `p=0.61830903`;
- *Prosopis nigra*: I `g=-0.48057139`, F `g=-1.13549676`, I–F `p=0.55736567`.

The frozen within-programme Bonferroni gate is therefore **`p_ML020=1.0`**.

This negative result is biologically informative. It shows that **multi-layer deterioration is not equivalent to state separation**: interaction and reproductive-function layers can decline together under fragmentation without statistically distinguishable effect magnitudes.

## Separate continuous-gradient generalisation

`ML015 Eucalyptus wandoo` remains a separate Fisher-z gradient cluster and is not combined with the primary Hedges-g statistic.

Its canonical effects are:

- I pollen tubes: `z=+0.69029123`;
- F seeds per fruit: `z=-0.87593080`;
- G_adult H_e: `z=-0.41117288`.

The strongest I–F contrast has `z=3.33386`, two-sided `p=0.00085651`; the within-cluster Bonferroni value is `p=0.00256953`.

This supports the existence of strong layer discordance in an additional natural system, but because it is a different effect family and exposure representation it is **generalisation evidence, not a sixth primary replicate**.

## What the current evidence supports

The strongest paper-level interpretation is:

> **Fragmentation responses cannot yet be summarized as either a universal single deterioration axis or a robust universal pattern of state separation. The current corpus contains strong cross-layer separation in some systems, but an independent replicated programme shows concordant interaction and reproductive decline, and the pooled direct-effect rejection does not survive removal of the influential Serapias cluster.**

That result changes the ecological question. Rather than asking whether fragmentation always separates biological states, the next biological target is **which system properties determine separation versus concordant decline**.

The present data are sufficient to establish that both regimes occur. They are not yet sufficient to estimate a stable moderator model explaining the regime boundary.

## Status of the original H2 and H3 extensions

### Cohort/history lag

Adult-versus-offspring genetic differences remain biologically motivated, especially in *Spondias* and *Conospermum*, but the current admissible primary corpus does not support a sufficiently replicated cross-system cohort-lag test for a headline conclusion. The *Spondias* adult–juvenile and adult–seed contrasts cross zero. Cohort lag therefore remains a secondary hypothesis rather than a current paper-level result.

### Process compensation

The original plan proposed C–F and I–F meta-regressions to test whether movement or interaction responses predict reproductive-function responses. The current number of independent same-frame paired clusters is too small for a stable cross-system moderator claim. Mechanistic systems such as Miyake *Camellia–Zosterops* and *Crepis* remain useful interpretation anchors, not evidence for a fitted general compensation law.

Neither extension should be used to inflate the present conclusion.

## Why this remains a useful synthesis

Existing fragmentation meta-analyses mainly ask whether a given endpoint declines on average. EGWEE instead enforces a harder unit of comparison: multiple biological layers measured within the same system under a common exposure and valid independent unit.

That architecture exposes three things that endpoint-specific syntheses cannot show as clearly:

1. a system can exhibit genuine cross-layer separation;
2. a system can show concordant deterioration across layers;
3. a pooled separation result can be statistically significant yet fail an influential-system robustness test.

The third result is especially important because it prevents a small heterogeneous literature from being presented as a universal mechanistic law.

## Claim ceiling

The current manuscript may claim:

- five direct same-effect-family programme/study clusters have been admitted under explicit effect-unit rules;
- the pooled five-cluster Fisher test rejects layer exchangeability at `p=0.01212432`;
- that rejection is not Serapias-independent (`p=0.18194353` after omitting ML001);
- ML020 independently demonstrates concordant I/F deterioration without detectable state separation;
- ML015 independently demonstrates strong discordance in a separate continuous-gradient effect family;
- natural systems therefore include both separated and concordant response regimes.

It may **not** claim:

- robust universal state separation across fragmented plant systems;
- a universal ordering of I, C, F, G_adult and G_offspring;
- a confirmed cross-system cohort lag;
- a general causal compensation mechanism;
- that the finite NEE operators have been directly validated in nature;
- that a sixth cluster should be sought merely to restore Serapias-independent significance.

## Current paper-level conclusion

> **Habitat fragmentation affects multiple biological layers, but the available natural systems do not support a single universal response geometry. Some systems show strong separation among interaction, movement, reproductive and genetic responses, whereas a replicated Chaco programme shows interaction and reproductive function declining together. The pooled direct-effect synthesis rejects layer exchangeability, but that rejection disappears when the influential Serapias system is removed. The empirical result is therefore conditional state separation, not a universal fragmentation syndrome.**
