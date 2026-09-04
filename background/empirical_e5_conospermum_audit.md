# E5 empirical audit — Perth *Conospermum undulatum* contemporary-connectivity / adult-genetic lag

## Status

This audit combines three explicitly different time layers from one threatened urban-fragmentation study programme in southwest Australia:

- Delnevo et al. (2019), DOI `10.1002/ece3.5653`: fragmentation, floral display, mating system and direct reproductive function;
- Delnevo et al. (2021), DOI `10.1007/s10531-021-02256-x`: present adult genetic structure interpreted against reconstructed historical habitat connectivity;
- Delnevo et al. (2026), DOI `10.1002/ece3.73406`: offspring paternity and contemporary pollen flow across fragmented versus continuous habitat.

The system identifies a third natural condition that is highly relevant to genetic warning: **current interaction/connectivity loss can be visible in reproduction and offspring parentage before standing adult neutral genetics has equilibrated to recent fragmentation.**

## Direct reproductive function is already fragmentation-sensitive

The 2019 study sampled twelve remnant populations varying in population size, isolation and floral display. *Conospermum undulatum* was experimentally shown to be **strictly self-incompatible** and dependent on pollinators carrying outcross pollen.

Quantitative functional responses included:

- fruit production falling from about **35% to <20%** as floral display decreased;
- population size spanning approximately **880 to 5 plants**;
- floral-display index spanning roughly **700 to 0.21**;
- seed output declining with smaller population size / floral display;
- seed output decreasing from about **6% to 3%** across the reported isolation gradient;
- seed germination increasing with population size and decreasing with isolation.

Because the species cannot rescue reproduction through autonomous selfing, reduced pollinator-mediated mating is a direct functional constraint rather than a route easily bypassed by reproductive assurance.

## Standing adult genetics retains historical connectivity

The 2021 study reconstructed past fragmentation from historical aerial photographs and compared it with current adult population genetics and reproductive performance.

Despite intense present fragmentation, adult populations retained similar levels of genetic diversity and weak spatial genetic structure. Historical structural connectivity was still associated with present genetic differentiation and within-population diversity. The authors concluded that the adult genetic layout retained the signature of the historically more connected landscape.

In their variation partitioning, the explained reproductive-performance variation included genetic, environmental and shared genetic–environmental components rather than a single genetic predictor. The key point for the present framework is temporal: **adult neutral genetic state is partly a memory variable for the pre-fragmentation landscape.**

## Contemporary pollen movement shows a much newer state

The 2026 paternity study directly estimated current mating and pollen movement from seed crops.

Its strongest landscape result is qualitative but sharp:

- pollen movement was maintained through continuous / unfragmented bushland;
- fragments separated by built urban infrastructure showed **near-complete to complete loss of inter-fragment pollen immigration**;
- the one fragmented population with notable inter-population immigration was separated from unsampled plants by about 650 m of cleared rural land rather than a built residential matrix.

Within sampled populations, inferred mean pollen-movement distances were on the order of a few tens of metres (roughly 25–35 m in the reported table), but the decisive state variable was not Euclidean distance alone: **matrix type determined whether contemporary inter-fragment pollen flow remained possible.**

The authors explicitly contrast this contemporary offspring-based signal with the weak adult genetic structure left by historical connectivity.

## Natural condition recovered

The resulting condition is:

> **cohort/history-lag functional fragmentation: current pollinator-mediated connectivity and reproduction are degraded, while standing adult neutral genetic structure still reflects an older, more connected landscape.**

In state notation:

`M_historical connectivity -> G_adult legacy`

while the contemporary pathway is

`built-matrix fragmentation -> C_pollen current ↓ -> mating/reproductive function F ↓`,

with `R_self ≈ 0` because the species is self-incompatible.

This makes `G_adult` and `C_pollen current` non-interchangeable state variables even within the same species and landscape.

## Why this matters for genetic early warning

This system supplies a natural version of an identification problem that the model treats abstractly. A genetic statistic from long-lived adults can be **temporally misaligned with the current loss-generating process**. The absence of a large adult diversity/differentiation response does not imply that ecological connectivity or reproductive function is intact.

For monitoring, the more future-relevant genetic layer may be:

- offspring parentage;
- pollen-pool donor diversity;
- contemporary mating-system estimates;
- recruitment-cohort genetic structure;

rather than adult neutral diversity alone.

This does not prove that offspring genetics is a universal early-warning indicator. It demonstrates why **cohort identity and habitat history belong in the empirical state** before any genetic warning is evaluated.

## Contrast with the other natural anchors

The three quantitative anchors now span distinct mechanisms:

1. **Montpellier *Crepis*** — local interaction limitation: `D↓ -> I↓ -> F↓` despite nonzero wider metapopulation movement.
2. **Miyake camellia** — movement compensation: `D↓ -> C_partner/C_pollen↑ -> F maintained`, with next-generation mixing maintained/increased.
3. **Perth *Conospermum*** — temporal state mismatch: present `C_pollen/F` decline while `G_adult` still reflects historical connectivity.

Thus density, connectivity and genetic diversity each fail as universal one-dimensional regime descriptors for a different empirical reason.

## Exact empirical state-sufficiency test

A decisive prospective test should align cohorts and time explicitly. For each remnant and reproductive year, measure:

1. current population size, floral display and local floral resource state (`D`);
2. pollinator identity/effectiveness and visitation (`I/T`);
3. built versus vegetated matrix resistance and historical connectivity (`M`);
4. current adult genetics (`G_adult`);
5. offspring/pollen-pool parentage and inter-fragment pollen immigration (`G_offspring`, `C_pollen`);
6. self-compatibility / realised selfing (`R`);
7. fruit/seed production, germination and recruitment (`F`);
8. joint spatial alignment of interaction support, contemporary pollen flow and reproductive output.

Compare future-function models that add information in temporal order:

- `E5-M0`: present patch size/isolation/floral display;
- `E5-M1`: `M0 + current I/T + C_pollen + mating state + offspring G + alignment`;
- `E5-M2`: `M1 + adult G`;
- `E5-M3`: `M2 + historical habitat connectivity / fragmentation age`.

If historical connectivity remains predictive after the current joint state is measured, it identifies unresolved ecological/genetic memory. If adult genetics adds little once contemporary parentage and interaction state are included, it confirms that standing adult `G` is not the right temporal compression for the current loss process.

## Immediate existing-data opportunity

The 2019 reproductive dataset is openly archived at Dryad (`10.5061/dryad.4cg374r`), and the 2026 paternity/genotype data are also publicly archived by the authors. These datasets should not be naively row-joined unless population identities, sampling years and cohort definitions are verified. The immediate safe analysis is a **study-programme process audit** followed by a prospectively synchronized design.

## Provenance / claim boundary

- Delnevo, N., van Etten, E.J., Byrne, M. & Stock, W.D. (2019). *Ecology and Evolution* 9:11494–11503. doi:`10.1002/ece3.5653`.
- Delnevo et al. (2021). *Biodiversity and Conservation*. doi:`10.1007/s10531-021-02256-x`.
- Delnevo et al. (2026). *Ecology and Evolution*. doi:`10.1002/ece3.73406`.
- The adult/offspring contrast is a temporal interpretation supported by the authors' fragmentation-history and paternity analyses; it is not a claim that every neutral genetic marker necessarily responds slowly.
- No universal time lag or connectivity threshold is inferred.
