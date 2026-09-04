# Empirical measurement crosswalk for functional-fragmentation conditions

## Purpose

A natural functional-fragmentation condition is not identified by a habitat label. It is identified by a **measured joint state before an outcome window** and by the realised functional trajectory that follows.

This crosswalk separates two questions that are easy to conflate:

1. **Is a coordinate measured somewhere in the study programme?**
2. **Is it measured in the same population/site-year and cohort as the other coordinates and the future functional outcome?**

Only the second supports a strict empirical state-sufficiency test.

## State coordinates

| code | ecological meaning | example field measurement |
|---|---|---|
| `D` | demographic / local resource support | census, flowering density, floral resources, local effective size |
| `I` | realised interaction support | visitation × effectiveness, compatible pollen receipt, interaction strength |
| `T` | functional / trait state | trait matching, morph balance, partner functional diversity |
| `C` | process-specific movement | pollen flow, seed/propagule flow, demographic movement, partner movement |
| `R` | compensatory route | selfing, reproductive assurance, alternative partners, rewiring |
| `G` | genetic / mating state | heterozygosity, inbreeding, donor diversity, offspring genetics, functional alleles |
| `F` | realised ecological function | pollination rate, seed/fruit set, dispersal effectiveness, recruitment |
| `M` | ecological memory / history / cohort | prior disturbance, colonisation age, cohort age, seed-bank/resource legacy |
| `A` | joint spatial alignment | co-location/covariance among `D/I/T/C/G/F`, not separate marginal means |

## Cross-system measurement matrix

Legend: `●` = directly measured in the cited design/programme; `◐` = partial/proxy or measured in a companion study rather than fully synchronized; `○` = major missing axis for the proposed state test.

| natural system | D | I | T | C | R | G | F | M | A | synchronization / immediate use |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| Montpellier *Crepis sancta* | ● | ● | ◐ | ● | ● | ● | ● | ● | ◐ | **Near-complete programme, not synchronized.** Interaction/seed-set and parentage/genetics come from different studies/years. Strong process anchor; needs same-patch-year resurvey for strict sufficiency. |
| Miyake-jima *Camellia–Zosterops* | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ◐ | **Near-complete compensation system.** Disturbance, resources, pollination, movement and offspring genetics measured across the same island gradient, but study components span related campaigns/years. |
| Honshu–Izu coastal 40 networks | ◐ | ● | ● | ○ | ○ | ○ | ● | ◐ | ◐ | **Immediate ecological partial-state test.** `I/T/F + season/geography` are matched across 40 site-seasons; add focal-plant genetics/parentage for full eco-genetic state. |
| Zurich 24 garden phytometers | ● | ● | ● | ○ | ○ | ○ | ● | ◐ | ◐ | **Immediate urban ecological partial-state test.** Raw design can test whether urban intensity adds prediction beyond `I/T`; standardized plants intentionally remove natural plant `G`. |
| Chicago *Penstemon hirsutus* green roofs | ● | ◐ | ◐ | ● | ● | ● | ● | ◐ | ◐ | **Connectivity/function-rich partial state.** Add standardized pollinator identity, visitation and effectiveness per roof. |
| Perth *Conospermum undulatum* fragments | ● | ● | ◐ | ● | ● | ● | ● | ● | ◐ | **Cohort/history-lag anchor.** Reproduction, historic adult genetics and contemporary offspring paternity are rich but temporally layered; synchronize adult/offspring/interactions in one outcome window for strict sufficiency. |
| Mexican tropical dry forest *Spondias purpurea* | ● | ● | ◐ | ● | ● | ● | ● | ● | ● | **Near-complete synchronized joint-state anchor.** Visitation, reproduction, paternity-derived pollen flow, sire diversity and adult/seed/juvenile genetics were measured within the same fragmentation comparison. Best current natural bridge from `I/C/F` to cohort-specific `G`. |
| fragmented Dutch *Primula elatior* | ● | ● | ● | ◐ | ● | ● | ● | ◐ | ◐ | **Strong terrestrial bridge.** Population size, genetics, morph balance, landscape, pollinators and seed production are jointly informative outside the urban/island framing. |

The matrix is a **measurement registry**, not an evidence score. A system with fewer filled cells can still be the best test of one causal coordinate.

## Four quantitative natural anchor conditions

### Anchor U-LIM — uncompensated interaction limitation (*Crepis*)

Observed pattern:

`D_local ↓ -> I_realised ↓ -> F_reproduction ↓`

with

`R_self` weak/incomplete and `C_pollen/C_seed` nonzero but heterogeneous.

Published anchors include pollinator presence of roughly 10% at low density versus 80% at high density, fertilised ovules of roughly 20% versus 80%, and parentage evidence for restricted local dispersal plus substantial external immigration in companion urban networks.

**Identification rule in nature:** call this pattern a candidate interaction-limited condition only when reduced local support, reduced realised interaction and reduced direct function are measured in the same causal sequence and no measured alternative route explains away the functional decline. Do not use a universal density threshold.

### Anchor I-COMP — movement-compensated local fragmentation (Miyake-jima)

Observed pattern:

`D_local ↓` together with `C_partner ↑ / C_pollen ↑`

while

`F_pollination` is maintained/enhanced and `G_offspring` does not collapse.

Published anchors include flower density from 21 to 2,544 flowers ha⁻¹, *Zosterops* home ranges of approximately 0.26 versus 1.97 ha in contrasted sites, pollen immigration of 0–33.8%, donor diversity of about 0.62–0.96, and higher pollination in heavily damaged sites despite lower pollinator density.

**Identification rule in nature:** call this a candidate compensation condition only when movement/alternative-route variables change in the compensating direction and direct function is measured. Low local resource density plus stable function without a measured compensation process is not enough.

### Anchor U-LAG — contemporary-connectivity / adult-genetic lag (*Conospermum*)

Observed temporal pattern:

`M_historical connectivity -> G_adult legacy`

while

`built matrix -> C_pollen current ↓ -> F_reproduction ↓`, with little/no selfing rescue.

Published anchors include fruit production decreasing from about 35% to <20% with lower floral display, seed output approximately halving across strong isolation, adult genetic diversity remaining broadly similar under recent fragmentation, and contemporary paternity showing essentially no pollen immigration between remnants separated by built residential matrix.

**Identification rule in nature:** a candidate cohort-lag condition requires direct evidence that the genetic cohort being monitored records an older landscape state than the contemporary interaction/mating process. Do not infer lag merely because adult neutral diversity is high.

### Anchor T-JOINT — joint interaction–connectivity limitation with cohort-emergent genetic deterioration (*Spondias*)

Observed pattern:

`I_realised ↓ + C_pollen kernel contracts + donor diversity ↓ + F_reproduction ↓`

followed by

`G_seed/juvenile deteriorates before G_adult necessarily shows the same magnitude of change`.

Published anchors include mean realised pollen-flow distance of about **209.15 m** in continuous versus **44.91 m** in fragmented forest, a narrower effective paternal pool in fragments (`N_ep` about **2.58** versus **1.58**), and much stronger heterozygosity loss/inbreeding in fragmented seed and juvenile cohorts than is evident from adult standing diversity.

**Identification rule in nature:** call this a candidate joint-deterioration state only when interaction support, direct function, contemporary mating/connectivity and at least one next-generation genetic cohort are measured in a common fragmentation comparison. Adult neutral genetics alone is insufficient.

This anchor is especially valuable because it links the state coordinates in one study rather than assembling a mechanism from companion publications.

## What counts as the same functional-fragmentation regime

Two natural systems should not be matched by raw units such as flowers ha⁻¹, kilometres of isolation or heterozygosity. Cross-system convergence is a **predictive equivalence claim**:

`future functional trajectory ⟂ fragmentation origin/history | measured joint state at t`.

A practical workflow is:

1. define the focal function and prediction window;
2. measure the candidate state before the outcome;
3. ensure genetic, interaction and demographic measurements refer to the correct cohort/time layer;
4. compress each ecological coordinate only with predeclared, biologically interpretable summaries;
5. preserve spatial alignment/covariance across patches;
6. fit the future-function model without habitat origin;
7. add origin/history last and assess held-out prediction/calibration;
8. if origin/history helps, identify the missing process/memory coordinate.

The target is the **smallest sufficient measured state**, not the largest covariate set.

## Existing-data versus new-measurement frontier

### Can be tested now as partial or joint state

- **E1 Honshu–Izu:** ecological residual-origin test using functional diversity, trait matching, season and direct pollination success; no matched genetics. A preregistered public-data discovery/residual-origin workflow is now the first direct test.
- **E2 Zurich:** urban residual-context test using local ecological context, guild-/trait-specific interaction support and direct fruit/seed set; no natural plant genetics.
- **E3 *Crepis*:** process audit can be done from existing open parentage/dispersal data, but full state cannot be synchronized retrospectively from the separate 2006 and 2013 studies.
- **E4 Miyake:** published tables permit a quantitative compensation-axis audit; a strict prospective sufficiency test needs repeated synchronized site-years.
- **E5 *Conospermum*:** existing reproductive, historical-genetic and contemporary-parentage studies establish the temporal mismatch mechanism, but a strict state test needs the three layers aligned to the same populations, cohorts and years.
- **E6 *Spondias*:** the published study already contains the strongest near-synchronized `I/C/F/G` bridge. The next step is a reanalysis/temporal extension that asks whether habitat class/history adds predictive information after the measured joint state, rather than merely re-testing fragmentation effects one variable at a time.

### Highest-value new measurement

The largest common gap is **interaction + function + genetics/connectivity measured in the same population-years and cohorts**. The most efficient additions are:

1. genotype focal plants and offspring/pollen pools in the existing Honshu–Izu repeated network design;
2. resurvey *Crepis* patches with interaction/function and parentage in the same season;
3. repeat Miyake site-years with movement, pollen flow, reproduction and offspring genetics synchronized;
4. align adult, offspring and pollinator observations in *Conospermum* remnants to distinguish current state from historical genetic memory;
5. add direct pollinator observation/effectiveness to Chicago roofs where paternity and reproduction are already available;
6. revisit *Spondias* populations through time so the already-rich joint state can be tested prospectively against future reproduction/recruitment rather than cross-sectionally only.

## Interpretation boundary

The model's state variables are not field variables by fiat. `D/I/T/C/R/G/F/M/A` are an empirical **search basis** assembled from measured mechanisms in natural systems. Any coordinate can be removed only if predictive sufficiency survives its removal; any residual origin/history signal is evidence to search for an omitted state or ecological memory variable.
