# Interaction–function response topology under fragmentation — exploratory synthesis

## Status

**Post hoc / hypothesis-generating.**

This synthesis was defined after the estimand-scale audit. It uses only sign topology and registered within-programme resolution status; it does not treat dependent panels as independent studies and does not estimate prevalence.

## Why topology matters

For positive-valued endpoints, Hedges-g and lnRR can disagree strongly about relative amplitude while retaining the sign of the fragmented-versus-reference response. Sign topology therefore carries a stronger scale-invariance property than bottleneck magnitude ordering.

## Complete I–F panel topology

The eight registered interaction–function programmes contain 18 primary panels.

- same-sign panels: 12;
- opposite-sign panels: 6;
- opposite `I+ / F-`: 2;
- opposite `I- / F+`: 4.

Opposite-sign point estimates occur in **5 of the 8 programmes**:

- Sevenello;
- Kakamega;
- *Eucalyptus wandoo*;
- Zurich BetterBlooms;
- common milkweed.

This is a descriptive programme inventory, not a 5/8 prevalence estimate.

## Resolved asymmetry

Only three programmes resolve an I–F mismatch under their registered dependence/multiplicity rules:

- Kakamega;
- *Eucalyptus wandoo*;
- *Cardiopetalum calophyllum*.

All three are **F-dominant**.

Two of the three resolved programmes show actual opposite-sign topology:

- Kakamega *Acanthopale*: `I+ / F-`;
- *Eucalyptus wandoo*: `I+ / F-`.

No registered programme resolves the reverse `I- / F+` topology. Reverse polarity is present as an unresolved point-estimate pattern in Sevenello, Zurich and common milkweed.

Thus the current evidence is asymmetric:

> **Hidden reproductive-function loss behind maintained or increased interaction quantity is resolved in two independent programmes; apparent reproductive compensation despite reduced interaction quantity remains suggestive but unresolved.**

## Within-landscape species heterogeneity

Four programmes contain at least three primary species/panels under a common landscape exposure.

- Chaco: `--`, `--`, `--` — homogeneous sign topology;
- Sevenello: `++`, `-+`, `-+` — heterogeneous;
- Kakamega: `+-`, `++`, `++`, `++` — heterogeneous;
- Zurich: `--`, `--`, `-+`, `--` — heterogeneous.

Thus **3 of 4 multi-panel programmes contain more than one process–function sign topology within the same programme**.

This is not a prevalence estimate, but it rules out a simple interpretation in which landscape exposure alone determines the direction of process–function coupling.

## Biological interpretation: quantity is not quality

The resolved `I+ / F-` pattern is consistent with interaction quantity becoming decoupled from interaction quality or effective mating.

- *Eucalyptus wandoo*: the source explicitly argues that high pollen-tube quantity in small populations can coexist with lower pollen quality because a greater proportion of pollen is self-pollen, reducing seed set.
- Kakamega *Acanthopale*: visitation occurrence is maintained while fruit set declines; the recovered data do not directly identify the compatible-pollen or post-pollination mechanism.
- Across the full I–F corpus, effective mating quality is not directly measured on the same fragmentation frame.

The unresolved reverse `I- / F+` cases suggest the converse possibility: fewer observed interactions can coexist with maintained function when visitor identity, outcross pollen quality, local plant context or non-pollination landscape effects compensate for lower abundance.

Common milkweed is especially informative because it is highly self-incompatible; the source study proposed that higher pollinator richness and more outcrossed pollen could alleviate pollen limitation despite lower urban pollinator abundance.

## Relation to previous synthesis

Previous fragmentation/land-use meta-analyses found average negative effects on pollination and female fitness and a positive cross-species association between their effect sizes. The present topology audit does not contradict that average coupling. It identifies **within-system polarity reversals and within-landscape species heterogeneity that an across-species mean association cannot diagnose**.

Previous individual studies have already shown that visitation frequency alone may fail to predict seed production. Therefore 'visitation is not enough' is not itself the novel claim.

The potentially distinctive contribution is the paired, scale-aware topology hierarchy:

1. endpoint sign topology is more robust to effect-scale choice than magnitude ordering;
2. opposite-sign process–function responses recur in several independent fragmentation programmes;
3. resolved opposite-sign decoupling currently points in one direction (`I+ / F-`), while reverse-polarity compensation remains unresolved;
4. response topology can differ among species exposed to the same landscape context.

## Claim ceiling

Allowed:

- opposite-sign I–F point estimates occur in multiple independent programmes;
- resolved opposite-sign decoupling occurs in Kakamega and Wandoo and is `I+ / F-` in both;
- no resolved `I- / F+` programme is present in the current corpus;
- multi-species programmes can contain different response topologies under the same landscape exposure;
- interaction quantity is not a sufficient universal sentinel of reproductive function.

Not allowed:

- estimating the population frequency of sign reversal from these programmes;
- a binomial/sign test on dependent panels;
- claiming all hidden reproductive loss is caused by pollen quality;
- claiming reverse compensation does not occur in nature;
- claiming species traits explaining topology have been identified.

## Machine-readable support

- `evidence/meta_extraction/if_sign_topology_v1.csv`
- `scripts/check_if_sign_topology.py`
- `scripts/check_bidirectional_masking.py`
