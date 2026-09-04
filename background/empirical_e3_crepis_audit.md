# E3 empirical audit — Montpellier *Crepis sancta* interaction-limited urban state

## Status

This is a **cross-study audit of one long-running urban study programme**, not a synchronized refit in which every state coordinate was measured in the same population-year. It uses Cheptou & Avendaño (2006), DOI `10.1111/j.1469-8137.2006.01880.x`, for local density, pollinator activity, seed set and mating-system response, and Dornier & Cheptou (2013), DOI `10.1038/hdy.2013.3`, for parentage-based contemporary seed/pollen dispersal and immigration.

The purpose is to identify a natural condition that is sharper than the label `urban`: **local interaction limitation despite nonzero metapopulation movement**.

## Measured local interaction–function chain

The 2006 study used tiny pavement habitat patches in Montpellier. The sampled HM and Roque patches were approximately 2.25 and 2.38 m², and the wider urban study system contained very small populations, from single plants to at most a few dozen plants per patch.

The field result is a direct density–interaction–function pattern:

- pollinator presence during 15-min observations increased from roughly **10% at low flowering-plant density to about 80% at high density**;
- number of visits also increased strongly with plant number;
- an individual-scaled pollination-support index increased from about **0.2 at low density to >2.2 at high density**;
- predicted fertilised ovules / seed set increased from roughly **20% at low density to 80% at high density**.

During the pollination survey the active pollinator recorded on *C. sancta* was *Apis mellifera*. The study therefore supports the observed chain

`low local flowering density (D) -> low realised pollinator activity (I) -> low reproductive function (F)`.

This is not merely a correlation between urbanisation and reproduction: the study measured the intermediate pollination process that changed with density.

## Reproductive assurance did not fully compensate

Progeny-array analysis showed only a slight, marginal increase in selfing in urban populations, and urban plants did **not** show a greater autonomous self-fertilisation ability than nearby rural populations in the insect-proof test.

For the present condition map this matters because the low-density functional decline was not obviously cancelled by an alternative reproductive route. In state notation, `R_self` was present but insufficient to erase the observed `D -> I -> F` limitation.

## Connectivity was nonzero and process-specific

Dornier & Cheptou (2013) later analysed two Montpellier urban patch networks with spatially explicit parentage models. Their global-marker fits estimated high apparent seed immigration (`0.59` in JC and `0.71` in HM) and pollen immigration (`0.71` and `0.84`, respectively). The authors explicitly cautioned that global estimates were inflated by marker limitations: a quality-diagnostic estimate of seed immigration in JC was about **0.43** (`0.38–0.51`), and the available six-locus HM diagnostics averaged about **0.693**.

At the same time, fitted local seed dispersal was spatially restricted. The preferred fits gave average radial seed-dispersal distances of about **12.6 m in JC** and **1.53 m in HM**; the expected fraction of seeds arriving from outside the local neighbourhood from the fitted local kernel alone was only **1–2%**. Mean fitted pollen dispersal distance was **<10 m**, and selfing was very low in those parentage analyses.

The biological point is therefore not `connectivity is high` or `connectivity is low`. It is that two different components coexist:

1. a **restricted local dispersal kernel**;
2. substantial and heterogeneous **external immigration / propagule input**.

This is exactly why a single scalar `connectivity` cannot identify the natural state.

## Natural condition recovered

The strongest defensible empirical condition is:

> **interaction-limited local fragmentation with incomplete reproductive compensation, embedded in a metapopulation that still receives pollen/seed immigrants.**

Operationally, the condition is recognised by the joint observation of:

- low local flowering/demographic support `D`;
- reduced realised pollinator activity `I`;
- reduced direct function `F`;
- no strong autonomous-selfing compensation `R`;
- nonzero but biologically heterogeneous `C_seed` / `C_pollen` / external immigration.

This condition is more informative than `urban`, patch isolation, or neutral gene flow alone. **Nonzero movement did not imply maintenance of local pollination function.**

## What this does not prove

The 2006 interaction/function observations and the 2013 parentage estimates are not one synchronized state vector. They involve overlapping study programmes and geography but not identical population-years, measurements or outcome windows. Therefore they must **not** be concatenated row-wise and treated as a completed state-sufficiency test.

The existing evidence supports the process decomposition and identifies measurable coordinates. It does not yet establish

`future F ⟂ urban fragmentation history | D, I, R, C, G`.

## Exact prospective test

A decisive Montpellier resurvey should measure, in the **same patch-year before the outcome window**:

1. flowering plant number/density and patch occupancy (`D`);
2. pollinator presence, visitation and preferably compatible-pollen deposition (`I`);
3. selfing/autonomous reproductive assurance (`R`);
4. direct seed/ovule set and subsequent recruitment (`F`);
5. adult and offspring genotypes with parentage-based pollen and seed immigration (`G`, `C_pollen`, `C_seed`);
6. patch geometry, matrix and recent colonisation/extinction history (`M`);
7. joint spatial alignment among high interaction support, high genetic/mating support and high function.

Then compare held-out future-function models:

- `E3-M0`: patch geometry + matrix + census only;
- `E3-M1`: `M0 + D + I + R + process-specific C + G + alignment`;
- `E3-M2`: `M1 + street/network identity + recent fragmentation/colonisation history`.

The empirical convergence criterion is whether `E3-M2` adds predictive information beyond the measured state. A remaining history effect would identify missing state or memory rather than make `urban` itself a regime variable.

## Ecological implication for the present manuscript

*Crepis sancta* supplies a natural example of the manuscript's central warning boundary: population presence and even nonzero movement are insufficient evidence that interaction-dependent function is secure. Monitoring would have to measure the **local interaction process and direct function**, not infer them from occupancy or genetic connectivity.

## Provenance / claim boundary

- Cheptou, P.-O. & Avendaño V, L.G. (2006). *New Phytologist* 172:774–783. doi:`10.1111/j.1469-8137.2006.01880.x`.
- Dornier, A. & Cheptou, P.-O. (2013). *Heredity* 111:1–7. doi:`10.1038/hdy.2013.3`.
- The immigration values from the global parentage fits are retained with the authors' marker-quality caution; they are not treated as exact exchange probabilities.
- No universal density, immigration or seed-set threshold is inferred from this system.
