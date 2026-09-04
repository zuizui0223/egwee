# E4 empirical audit — Miyake-jima movement-compensated island state

## Status

This is a quantitative audit of the *Camellia japonica*–*Zosterops japonicus* study programme on Miyake-jima after the 2000 eruption. The main anchors are Abe & Hasegawa (2008), DOI `10.1007/s11284-007-0345-4`, for pollination and reproductive success across volcanic damage, and Abe et al. (2013), DOI `10.1371/journal.pone.0062696`, for pollen flow and next-generation genetics.

This system identifies a natural condition that is nearly the opposite of the Montpellier *Crepis* condition: **local floral support declines, but partner movement and pollen mixing increase enough to compensate pollination/reproductive function.**

## Disturbance sharply reduced local floral support

Abe et al. (2013) compared six sites spanning volcanic-damage index (`IVD`) 1–4. Flower density ranged from only **21 flowers ha⁻¹** at one heavily affected site to **2,544 flowers ha⁻¹** at the least damaged TU1 site and was negatively associated with IVD (`Spearman r=-0.794`, `P=0.05`, six sites).

The 2008 reproductive study likewise found that volcanic gases reduced leaf survival and flowering activity and that pollinator densities were lower where flower resources were reduced.

If local resource density were a sufficient regime descriptor, these damaged sites should be classified as low-support / low-function states. They were not.

## Pollination and reproduction were compensated

The 2008 field study found **higher pollination rates in heavily damaged areas (83%) than in less damaged areas (26–45%)**, despite lower pollinator densities. Fruit abortion increased under heavy damage, but fruit-set rates remained about **16–29% and did not differ significantly among sites**; seed-set rates tended to increase with volcanic damage.

Thus the observed outcome is not `disturbance increases every component of fitness`. The important result is that the pollination component was maintained or enhanced sufficiently to offset a major loss of local floral resources.

## Partner movement changed in the compensating direction

Radio-tracking and pollen-parentage evidence show a process-specific movement response.

At TU, a high-flower-density, low-damage site, the reported *Zosterops* home range was about **0.26 ha**. At IG, with lower floral resources and greater damage, it was about **1.97 ha**. This approximately order-of-magnitude change is evidence that the pollinator's movement state changed with the resource landscape rather than remaining a fixed property of the island.

Within the six 0.3-ha plots in Abe et al. (2013):

- use of available flowering trees as pollen donors ranged from **37.5% to 100%**;
- mean within-plot pollen-flow distance ranged from **10.52 to 18.71 m**;
- pollen immigration from outside plots ranged from **0 to 33.8%**;
- pollen immigration increased with volcanic damage (`P<0.05`) and decreased with flower density (`P<0.05`);
- pollen-donor diversity within fruits ranged from about **0.62 to 0.96** and tended to increase with damage (`P=0.058`).

These are separate biological quantities. They must not be collapsed into the simulator's allele-frequency `migration_rate`.

## Next-generation genetic state did not collapse

Abe et al. (2013) genotyped **161 mature flowering trees and 1,068 seeds at 10 microsatellite loci**. Mean expected heterozygosity and allelic richness in seeds were approximately **0.589** and **3.947** and did not differ significantly among the six sites. The partitioning of allelic richness among seed families (`A_st`) decreased with volcanic damage and increased with flower density, consistent with greater mixing under stronger disturbance.

The natural chain is therefore:

`volcanic disturbance / low flower density (D↓)`

`-> broader partner movement (C_partner↑)`

`-> greater external pollen input / donor mixing (C_pollen↑)`

`-> maintained or enhanced pollination component (I_eff/F maintained)`

`-> next-generation genetic mixing maintained or increased (Gmix)`.

## Natural condition recovered

The most defensible empirical condition is:

> **movement-compensated local fragmentation: low local resource support is offset by a change in pollinator movement and pollen mixing, so realised pollination and next-generation genetic mixing do not decline in parallel with local flower density.**

Operationally, it requires observing the joint pattern

- `D_local` low or declining;
- `C_partner` broadened or redistributed;
- `C_pollen` / donor diversity increased or maintained;
- direct pollination/reproductive function `F` maintained relative to the resource decline;
- next-generation `G` not collapsing;
- disturbance/history `M` explicitly represented because it affects both resources and movement.

This is a **compensation state**, not an island state. The same island can contain different positions along this joint state.

## Why this is a critical counterpart to *Crepis*

Both systems begin with reduced local support, but their downstream states differ.

- Montpellier *Crepis*: `D↓ -> I↓ -> F↓`, with no strong autonomous-selfing rescue, despite nonzero immigration at the metapopulation level.
- Miyake camellia: `D↓ -> C_partner/C_pollen↑ -> pollination maintained/enhanced`, with next-generation mixing maintained or increased.

Therefore **local density/resource support cannot be the functional-fragmentation regime by itself**. Whether a compensatory movement/interaction route is active changes the realised state.

## What this does not prove

The volcanic studies provide unusually rich multi-layer measurements, but they do not constitute a prospectively repeated state-sufficiency trial over many independent future windows. The 2008 and 2013 analyses are also related parts of a study programme rather than one single synchronized annual table.

The evidence establishes the compensation mechanism and its measurable coordinates; it does not yet establish strict conditional independence

`future F ⟂ volcanic history | D, I, C_partner, C_pollen, G, M`.

Volcanic damage may also act directly on birds and vegetation, so `IVD` is not merely an upstream geometry variable. A residual IVD effect after conditioning could represent omitted physiology, resource history or other ecological memory.

## Exact empirical state-sufficiency test

A decisive repeated-site design would measure before each reproductive outcome window:

1. IVD / gas exposure and recent vegetation history (`M`);
2. flowering-tree density and flower density (`D`);
3. *Zosterops* abundance, visitation and movement/home-range or movement-network measures (`I`, `C_partner`);
4. compatible pollen deposition / pollination rate and fruit/seed production (`F`);
5. maternal, pollen-pool and offspring genotypes (`G`);
6. pollen immigration, donor diversity and inferred pollen-flow distance (`C_pollen`);
7. spatial alignment between high floral support, pollinator use, donor diversity and offspring genetic mixing.

Then compare held-out models across site-years:

- `E4-M0`: flower density + local vegetation state;
- `E4-M1`: `M0 + partner movement + pollination support + C_pollen + G + alignment`;
- `E4-M2`: `M1 + IVD / disturbance history`.

If `E4-M2` no longer improves future reproductive-function prediction, the measured compensated state is sufficient at that scale. If it does, the residual disturbance term identifies missing memory/process variables.

## Ecological implication for the present manuscript

Miyake-jima demonstrates why fragmentation or local resource loss need not monotonically degrade ecological function. **Behavioural movement can change the mapping from spatial damage to interaction support.** A monitoring programme that measures only flower density, local pollinator abundance or neutral diversity would miss the compensating pollen-transfer process.

## Provenance / claim boundary

- Abe, H. & Hasegawa, M. (2008). *Ecological Research* 23:141–150. doi:`10.1007/s11284-007-0345-4`.
- Abe, H., Ueno, S., Takahashi, T., Tsumura, Y. & Hasegawa, M. (2013). *PLOS ONE* 8:e62696. doi:`10.1371/journal.pone.0062696`.
- The observed compensation is specific to this plant–bird interaction and disturbance context; it is not a universal island rule.
- `C_partner` and `C_pollen` are empirical movement processes and are not equated to the model's allele-frequency mixing parameter.
