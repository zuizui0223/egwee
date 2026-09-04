# Empirical condition map for interaction-mediated functional fragmentation

## Purpose

The mathematical condition map is now paired with a **natural-system condition map**. The aim is not to invent universal field regimes from a small set of case studies. It is to identify which measured ecological coordinates repeatedly separate functionally different outcomes and which coarse descriptors repeatedly fail.

The common question is:

> **When apparently similar spatial fragmentation or local interaction loss produces different realised functions, which measured state coordinates explain the difference?**

## Six natural mechanisms already visible in published systems

### 1. Density–interaction limitation — urban *Crepis sancta*

In highly fragmented Montpellier pavement populations, lower plant density was associated with lower pollinator activity and lower seed set. The same study programme also documents contemporary pollen/seed dispersal and immigration among urban patches.

Observed chain:

`low local demographic/floral support -> lower realised visitation -> lower reproductive function`

Important boundary: nonzero movement does not guarantee that local pollination function is maintained.

**Measured state coordinates:** `D`, `I`, `F`, with partial `R/C/G` from companion studies.

### 2. Functional-partner / trait-matching limitation — Honshu–Izu networks

Across 40 networks, mainland distance was associated with several network properties, but pollinator functional diversity (`FD_Q`, including representation of long-tongued pollinators) and flower–pollinator trait matching were the measured coordinates most directly linked to pollination function. Pollinator species diversity did not substitute for functional diversity in the published trait-matching/function models.

Observed chain:

`geography/season -> functional partner state -> trait matching -> pollination function`

Important boundary: `island`, distance and species richness are upstream descriptors, not sufficient definitions of the functional state.

**Measured state coordinates:** strong `I/T/F`; `G/C/R` are missing in the matched 40-network design.

### 3. Movement-mediated compensation — Miyake-jima *Camellia japonica*–*Zosterops japonicus*

Across a volcanic-damage gradient, local floral resources were reduced in more strongly disturbed areas, but Japanese white-eye movement broadened pollen transfer. Pollen immigration/donor diversity and seed genetic diversity increased rather than collapsing, while pollination/reproductive function was maintained or compensated.

Observed chain:

`disturbance -> lower local floral support`

but simultaneously

`disturbance -> broader partner movement/pollen mixing -> compensation of function/genetic mixing`

Important boundary: low local interaction resource density does **not** imply a low-function state when partner movement changes in the compensating direction.

**Measured state coordinates:** `D/I`, `C_partner/C_pollen`, `G_offspring`, `F`, plus explicit disturbance history `M`.

### 4. Focal-function-specific urban filtering — Zurich garden phytometers

Across 24 gardens, the stored source models show that the 500-m urban-intensity coefficient differs among focal functions: clear negative intervals for carrot seed set, radish fruit set and comfrey fruit set, but no clear effect for radish seed set or sainfoin fruit set. Pollinator guild coefficients are likewise function-specific; for carrot seed set, hoverflies and beetles are positive while honeybee abundance is negative in the stored model.

Observed pattern:

`urban context x focal plant/function x interaction guild -> realised reproductive function`

Important boundary: neither urban intensity nor total pollinator abundance/richness is a universal functional state.

**Measured state coordinates:** spatial context, `I/T/F`; natural focal-plant `G/C/R/M` are absent because phytometer material is standardised.

### 5. Cohort/history lag — Perth *Conospermum undulatum*

Across an urban-fragmentation study programme, reproductive performance and contemporary pollen flow respond to the present built matrix while standing adult neutral genetics can retain the signature of an older, more connected landscape.

Observed temporal pattern:

`historical connectivity -> adult genetic legacy`

while

`current built matrix -> current pollen connectivity/function declines`.

Important boundary: a genetic measurement is not interpretable without its **cohort and temporal reference**. Adult neutral diversity can describe past connectivity rather than the contemporary interaction/mating process.

**Measured state coordinates:** strong `D/I/C/R/G/F/M`, but temporal layers span related studies and must not be naively row-joined.

### 6. Joint interaction–connectivity limitation with cohort-emergent genetics — *Spondias purpurea*

In Mexican tropical dry forest, one fragmentation comparison jointly measured pollinator visitation, male/female reproductive performance, paternity-derived pollen flow, correlated paternity/effective sire number, and adult/seed/juvenile genetics.

Observed chain:

`fragmentation -> realised visitation ↓ + pollen-flow kernel contracts + donor diversity ↓ + reproductive function ↓`

followed by

`seed/juvenile heterozygosity ↓ and inbreeding ↑ before standing adult genetics necessarily shows the same magnitude of change`.

Mean realised pollen-flow distance was about 209.15 m in continuous versus 44.91 m in fragmented forest. The numerical values are one-system anchors, not transferable thresholds.

Important boundary: this study shows why adult neutral genetics, contemporary mating connectivity, interaction support and direct function should be measured as **different but aligned state coordinates**.

**Measured state coordinates:** near-synchronized `D/I/C/R/G/F/M`, with cohort-specific `G`; it is currently the strongest natural bridge to the joint-state logic.

## What these systems jointly falsify

The empirical literature already rejects several possible coarse definitions of a functional-fragmentation regime:

1. **geometry alone** — similar fragmentation can lead to limitation or compensation;
2. **local interaction/resource density alone** — Miyake-jima shows that movement can offset lower local floral support;
3. **species richness alone** — Izu functional diversity and trait matching are more informative for pollination function;
4. **urban/island label alone** — both categories contain different functional outcomes and mechanisms;
5. **one connectivity scalar** — plant movement, pollinator movement and pollen flow can decouple;
6. **neutral genetic diversity alone** — it is neither equivalent to interaction support nor sufficient to describe the joint spatial state;
7. **one genetic cohort alone** — *Conospermum* and *Spondias* show that adult standing diversity and contemporary offspring/mating state can encode different time layers.

## Empirical core state suggested by the evidence

The smallest **current candidate**, before any prospective sufficiency test, is:

`S_emp(t) = {D, I, T, C, R, G_by_cohort, F_baseline, M, joint spatial alignment}_t`

where:

- `D` = demographic/resource support;
- `I` = realised interaction support weighted by partner identity/effectiveness;
- `T` = functional/trait matching or equivalent mechanism-specific trait state;
- `C` = process-specific movement/connectivity;
- `R` = compensatory/alternative routes;
- `G_by_cohort` = genetic/mating state indexed to the cohort and process represented;
- `F_baseline` = realised function at the start of the prediction window;
- `M` = plausible ecological memory/history;
- joint spatial alignment retains whether these supports co-occur in the same patches.

This is deliberately larger than the model state. Natural systems contain processes and memory that the finite simulator omits. The empirical goal is to **reduce** this state only after predictive sufficiency is demonstrated.

## Natural candidate states, not habitat classes

The present literature suggests five broad candidate state patterns that can be searched for across habitats.

### A. Uncompensated interaction limitation

- low `D/I`;
- low effective partner/trait matching `T`;
- `C/R` insufficient to replace the lost support;
- declining `F` despite persistence of the focal population.

*Crepis* and parts of the Izu gradient approximate this pattern through different upstream routes.

### B. Compensated local fragmentation

- local `D/I` is low;
- `C_partner` or `C_pollen` increases, or alternative partners/reproductive routes compensate;
- `F` remains stable or declines less than expected;
- genetic mixing can remain high.

Miyake-jima camellia is the clearest current example.

### C. Function-specific filtering

- the same spatial context produces different `F` across focal species/functions;
- interaction identity/effectiveness, not total partner count, determines the response;
- habitat-level classification is therefore too coarse.

Zurich provides the clearest current example.

### D. Cohort/history-lag fragmentation

- current interaction/connectivity/function is degraded;
- adult standing genetics still records an older landscape state;
- offspring or paternity layers are required to diagnose the current process.

*Conospermum* is the clearest current example.

### E. Joint interaction–connectivity deterioration

- realised interaction support declines;
- process-specific connectivity contracts;
- direct function declines;
- mating/donor diversity narrows;
- genetic deterioration emerges most clearly in new cohorts.

*Spondias* is the strongest current near-synchronized example.

These patterns are **search templates, not universal biological classes**. They become regimes only if they predict future functional trajectories and replicate across independent systems.

## Stronger convergence test implied by the natural examples

The cross-system test should not compare raw metric values across unrelated ecosystems. Instead:

1. define a focal function in each system;
2. estimate its local interaction-support state and direct function;
3. measure process-specific connectivity/compensation;
4. align genetic measurements to the relevant cohort and outcome window;
5. retain spatial alignment among interaction, demography and genetics;
6. predict future change/loss in function;
7. then ask whether habitat origin/history still improves prediction.

The central statistical null is conditional independence:

`future functional trajectory ⟂ fragmentation origin/history | measured joint state at t`.

A residual origin/history effect identifies a missing state coordinate. It is not evidence that `urban` or `island` itself is a causal state variable.

## Immediate empirical programme

### Existing-data tier

- **Honshu–Izu E1:** the public 40-network archive is now prospectively targeted for a leave-one-site-out residual mainland-distance/origin test after conditioning on `FD_Q + FEve + trait matching + season`.
- **Zurich E2:** next calculation is a joint `interaction state + Urban_500` held-out predictive comparison once the raw EnviDat reproductive observations are loaded.
- **Miyake-jima:** published values support a quantitative compensation-axis audit; strict prospective sufficiency requires synchronized repeated site-years.
- **Crepis:** use parentage/dispersal datasets to quantify connectivity separately from density–pollination limitation; do not merge unmatched years/populations as one experiment.
- **Conospermum:** current reproduction/paternity and adult historical genetics establish a lag mechanism; synchronize cohorts and interactions prospectively.
- **Spondias E6:** use the already-rich joint comparison as the template for a temporal residual-history test and for designing future urban/island sampling.

### New-measurement tier

The highest-value missing measurement across most systems is **matched interaction + function + genetics/connectivity in the same population-years and cohorts**. For the Honshu–Izu coastal system this means adding focal-plant adult/offspring genotyping and parentage/pollen-flow inference to the existing repeated network design.

That single addition would connect the strongest existing island interaction–function dataset to the eco-genetic state directly, rather than treating genetics as a separate monitoring layer.

## Current empirical conclusion

The literature supports a stronger ecological statement than “fragmentation effects are context dependent”:

> **The same coarse fragmentation signal can map to function loss, compensation, focal-function-specific responses, temporal genetic lag, or joint interaction–connectivity deterioration depending on the measured configuration of interaction support, functional partner identity, movement/compensation, cohort-specific genetics and demographic state.**

What remains directly untested is whether those measured configurations are sufficient to erase predictive information about their urban, island or disturbance origins. The preregistered Honshu–Izu residual-origin analysis is the first direct data test of that criterion; *Spondias* provides the strongest natural joint-state template for extending it to an eco-genetic test.
