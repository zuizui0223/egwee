# When artificial pollen does and does not outperform natural pollination: a baseline-invariant cross-species census

**2026-10-29 | Empirical EGWEE only.** Post hoc source-backed macroecological reanalysis; not the theoretical \`egwe\` / NEE programme, not a new independent experiment and not admission of any new effect into the registered EGWEE five direct / eight matched quantitative / sixteen mixed-tier fragmentation programmes. Source data and study references are not independent of the earlier GloPL 2026-10-28 census. **Submission remains blocked (\`submission_ready=false\`).**

## Scientific question: does the reversal survive changing the natural baseline?

A species can appear to benefit from bagged manual outcrossing in one locality/morph/year but perform worse under the same treatment in another. However a sign switch in

\[
D_i=FS_{\mathrm{bagged\ outcross},i}-
FS_{\mathrm{natural\ open},i}
\]

could follow from a shift in natural-open fruit-set alone. Source rows often share plants, controls or publications.

For **each repeated publication × focal species group**, recover the original Natural and Bagout *fruit-set means* and apply a stronger, **pairing-independent** sufficient criterion:

\[
\min_i B_i < \min_i N_i
\quad \text{AND} \quad
\max_i B_i > \max_i N_i.
\]

This ensures the lowest observed manual-outcross result is below **every** observed natural-open result, and the highest manual-outcross result is above **every** natural-open result. **Any permutation of the natural means among the cases leaves both directions.** It does **not** establish statistical significance, prove a pollen-compatibility mechanism, or control other factors that changed between individual cases.

## Source-locked census and replication unit

GloPL source: Bennett et al. (2018), *Scientific Data* [doi:10.1038/sdata.2018.249](https://doi.org/10.1038/sdata.2018.249); [Dryad doi:10.5061/dryad.dt437](https://doi.org/10.5061/dryad.dt437). Source 2,969 literature-defined experimental cases. The egwee copy has stored UTF-8 Git blob \`0809eaeee54e4375d26bacfe002787241f8ff72e\`, unlike original author legacy byte blob \`d22fe333b19489c473e076dd173ed7a67b1afbf0\`; source numeric records are verified but original binary encoding is **not** claimed identical.

**Fruit set:** 811 Natural/Bagout cases in 413 publications and 588 accepted species. These form 613 publication × species groups, 130 of which have ≥2 comparable cases. One exact duplicated *Pachycereus pringlei* numeric source profile appears in two publications; retaining one gives **129 deduplicated repeated groups**. One paper containing several morphs/patches/years counts as **one publication**, not several independent studies.

| Eligibility and strength | Repeated publication × species groups | Distinct source publications | Families |
|---|---:|---:|---:|
| ≥2 recorded Natural/Bagout means after exact-source-profile deduplication | **129** | 104 | — |
| Opposite paired mean signs in different cases | **28** | 25 after duplicate correction | — |
| **Pairing-independent crossover** defined above | **10** | **10** | **9** |
| Crossover with ≥0.01 minimum margin on **both** sides of natural-control range | **8** | 8 | — |
| Crossover with ≥0.05 minimum margin on **both** sides | **4** | 4 | — |

The **10** strong source groups span morph/sexual state, donor-by-patch geography, locality and year. Only **three** of the strong groups have at least three cases; most are binary contrasts. A 10/129 ratio is not a plant-population prevalence or a general probability of incompatible mating. There is no new field replication here.

## Source-constrained example: an island species with strict mating compatibility

In *Hugonia serrata* (**Linaceae**, rare tristylous island plant on La Réunion; Meeus et al. 2011, [doi:10.1007/s00606-010-0400-4](https://doi.org/10.1007/s00606-010-0400-4)), three published morph-specific fruit-set means are:

| Flower morph | Natural fruit set | Bagged hand-outcross fruit set | Bagout − Natural |
|---|---:|---:|---:|
| Short-styled | **0.270** | **0.100** | **−0.170** |
| Mid-styled | 0.430 | **0.800** | +0.370 |
| Long-styled | 0.440 | 0.540 | +0.100 |

All natural controls are between **0.27 and 0.44**, while manual-outcross outcomes span **0.10 to 0.80**. This is an unambiguous *published-mean* crossover independent of which natural controls are compared. The same source reports \(N_N=30\) and \(N_B=8\) for each morph; applying a **within-this-group** Bonferroni-corrected normal reference band for its six marginal means still leaves the extreme manual means outside the envelope of natural controls. **This is only an approximate within-selected-group summary**: it does not correct the search over all 129 species/study groups, validate all marginal variance definitions or establish an island-caused effect.

Crucially, the **original 2011 authors already established heteromorphic self-incompatibility, pollen limitation and persistence of tristyly on La Réunion**. The new EGWEE contribution is a systematic *source-baseline-invariant classification*, not that biological discovery. It is biologically relevant to the **conditional mate-access** hypothesis: island isolation need not produce universal self-compatibility, and different resident floral morphs can retain unequal access to effective mating.

Other source-locked mean crossovers include *Oxalis squamata* (short vs medium vs long style), *Pachycereus pringlei* (female vs hermaphrodite; one exact duplicated numerical paper profile removed), *Kalmia latifolia* (locations), and *Eriocnema fulva* (years). **Do not interpret these source label axes as experimental treatments of one single common mechanism.**

## Habitat fragmentation source experiment: donor access rather than visitation count

*Calystegia collina* (Wolf & Harrison 2001, *Conservation Biology*, [doi:10.1111/j.1523-1739.2001.99341.x](https://doi.org/10.1111/j.1523-1739.2001.99341.x)), a serpentine-endemic, primarily self-incompatible clonal plant, is the one source anchor whose published study design directly crosses habitat context with **pollen donor origin**:

| Source means in a given habitat-size class | Natural open | Manual within-patch pollen | Manual from near other patch | Manual from farther patch |
|---|---:|---:|---:|---:|
| Large patch context | 0.332 | 0.121 | 0.635 | 0.606 |
| Small patch context | 0.0865 | 0.053 | 0.416 | 0.280 |

With a natural reference held *exactly fixed within each patch-size class*, externally sourced donor pollen always outperforms locally sourced pollen in the published fruit-set means. External near/far average minus within-patch result is **+0.4995 (large)** and **+0.295 (small)**. The original paper reports comparable bee visitation across outcrop sizes, alongside strong fruit-set and donor-origin effects. **These are published original ecological results, not a novel donor-manipulation experiment performed by EGWEE.** They support a concrete causal-competitor hypothesis for the different source-independent EGWEE fragmentation data: the functional deficit may concern **available compatible mates**, rather than observed pollen arrival alone.

**Source-label correction:** the 2026-10-28 automated post hoc context regex erroneously assigned the GloPL \`large_far/near/within\` and \`small_far/near/within\` labels solely to \`space\`, even though the original experimental axis explicitly includes pollen **donor origin**. Do not silently rewrite that older exploratory taxonomy. The new checker preserves *both* (a) the original historical labels and (b) an explicitly source-verified \`donor_by_patch_size\` interpretation for **this one independently identified source**. The original category rates and bootstrap values are therefore not used for causal inference or to claim a substantially stronger mating-context frequency.

## Cross-endpoint boundaries (same GloPL source, not new publications)

The same min/max natural-control range test was repeated for all other recorded outcomes, **without treating overlapping experimental cases as independent studies**:

| Original source outcome | Natural/Bagout same-case pairs | Deduplicated repeated source×species groups | Opposite paired mean signs | Pairing-independent crossings |
|---|---:|---:|---:|---:|
| **FS** Fruit set | 811 | 129 | 28 | **10** |
| **SO** Seeds per ovule | 159 | 25 | 7 | **1** |
| **SPFR** Seeds per existing fruit | 193 | 34 | 6 | **1** |
| **SPFL** Seeds per flower | 51 | 10 | 1 | **0** |
| **SPP** Seeds per plant | 14 | 3 | 0 | **0** |

One additional source group each passes the mean-invariant criterion in seeds per ovule (*Euthamia graminifolia*) and seeds per fruit (*Vriesea gigantea*). They do **not** constitute new source-independent studies or proof of the same underlying donor mechanism; later functional stages are much less frequently jointly measured.

## Statistical evidence ceiling: marginal source SDs and repeated-search risk

For FS, a stringent **within-selected-study Bonferroni** envelope of reported marginal source mean±normal-standard-error bands is crossed on *both sides* by only **one** of the 10 mean-invariant groups, *Hugonia serrata*. Even this does **not** correct for searching 129 repeated groups, nor for shared controls, unusual N/SD definitions or exposure/morph confounding.

More materially, some GloPL SD/N entries are **incompatible with being the sample SD of truly bounded 0–1 proportion observations**: among the 811 eligible FS rows, **17 Natural** and **15 Bagout** SD values exceed \(0.5\sqrt{n/(n-1)}\), the maximum possible sample SD if every underlying measured observation lies in [0,1]. Six source *Calystegia* rows are among them. Therefore **do not use GloPL's marginal SD/N as a universally valid binomial sampling-variance estimate** or call the full 10-group mean criterion an independently statistically proven true reversal. A source-author crosswalk is required to resolve the original SD definition and duplication within experiments.

The most defensible **positive empirical conclusion** is not that ten mating mechanisms were experimentally demonstrated. It is that **the same plant species and published study can exhibit artificial-pollination outcomes spanning *both sides* of the entire observed natural-pollination reference range**, even when the natural-control baseline is allowed to vary freely. The unresolved question is which **recipient morph, compatible donor source, habitat or temporal condition** determines that transition.

## Mechanism to discriminate in empirical EGWEE, not yet demonstrated globally

Define three non-exchangeable process components at the same reproductive and landscape frame:

- \(Q\): **quantity** of pollen tubes / visit observations (interactions).
- \(E\): **effective mating channel**, the proportion of transferred pollen able to fertilize given compatible donor identity, recipient morph/genotype and arrival timing.
- \(F\): **realized female function**, especially fruit initiation, seeds per flower, seed viability and successful recruitment.

The falsifiable **channel-gated hypothesis** is that loss of compatible mate links can reduce F even if Q stays similar; the **competing abiotic/resource** hypothesis is that F declines after successful fertilization under salinity, low water/nutrients or developmental abortion. Both may act jointly. A meaningful next cross-system test requires **same recipient genotypes in independent fragment/continuous or island/mainland landscapes**, known-dose **within- versus outside-patch donor pollen**, sham bagging, source-matched natural visits, genotype-based outcross paternity, viable seed production and subsequent recruitment. Predefine the natural-control pairing, measured flower stage and compatible-mate criterion *before observing* the treatment response. Without E or direct paternity measurements, the general mechanism remains unverified.

## Reproducible verification

- Script: \`scripts/audit_glopl_control_invariant_polarity_20261029.py\`
- CI: \`.github/workflows/glopl-control-invariant-polarity.yml\`; [successful GloPL baseline-invariant source contract run](https://github.com/zuizui0223/egwee/actions/runs/40843688932), stores per-endpoint complete JSON and every original case behind each of the ten FS strong groups in CSV.
- Original 2026-10-28 result: [WITHIN_SPECIES_MATING_CHANNEL_POLARITY_2026-10-28.md](WITHIN_SPECIES_MATING_CHANNEL_POLARITY_2026-10-28.md) (its original heuristic is preserved and semantically annotated here).
- **No theoretical egwe simulation**, no additional field data, no modification to approved source effects or \`submission_ready=false\`.
