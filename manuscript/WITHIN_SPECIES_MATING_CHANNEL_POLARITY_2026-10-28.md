# Same species, opposite manual-pollination outcomes: mating context versus geographic and temporal context

**28 October 2026 — exploratory empirical EGWEE macroecology extension.** This is **not** the theoretical \`egwe\` / NEE repo. No frozen fragmentation study-programme denominators (5 direct, 8 matched interaction–function, 16 mixed-tier) change; no separate mechanistic validation or new causal intervention is certified, and \`submission_ready=false\` remains.

## Central ecological question and source scope

When artificial **bagged manual outcross pollination** performs better than natural pollinator access for one group of plants, must that ranking be inherited by all conspecific plants in the same source publication?

This reanalysis tests whether the sign of the **published, same-endpoint fruit-set mean difference**

\[
D_{p,m,c} = FS_{\mathrm{bagged,\ manually\ outcrossed}}-
             FS_{\mathrm{unbagged,\ naturally\ pollinated}}
\]

can reverse **within the same plant species and published study**, rather than relying on between-species observations. Positive means bagged manual outcross has higher recorded fruit set. Negative means natural open control is higher; the sign is *not itself a statistically certified true treatment effect*.

**Source:** Bennett et al. (2018), GloPL, [Scientific Data doi:10.1038/sdata.2018.249](https://doi.org/10.1038/sdata.2018.249); [Dryad 10.5061/dryad.dt437](https://doi.org/10.5061/dryad.dt437), and the source-authored CSV (author commit \`abbe193770981b2c61713e75a0f01e004bdded8e\`). The egwee copy is a **UTF-8-derived transcription** of the legacy-encoded author file, Git blob \`0809eaeee54e4375d26bacfe002787241f8ff72e\`. Its numeric row/field recoverability is checked; it is **not** source-byte identical. Only cases having source \`Natural_X_FS\` and \`Bagout_X_FS\` enter the paired comparison.

## Evidence census, independent units and duplicate-paper defence

The source has **2,969 all-outcome cases** from 927 publications and 1,265 species. Same-endpoint Natural versus Bagout fruit-set means are available for **811 cases, 413 publication identifiers, 588 species**.

Within these 811, **613 publication × plant-species** groups are formed. Only **130 groups** have at least two comparable cases, involving different reported study conditions, and can therefore exhibit a *within-group* sign reversal.

- **29/130** repeated groups have at least one Bagout > Natural case and at least one Natural > Bagout case (26 distinct publication IDs).
- **13/29** contain opposite cases with a **nominal** \(|z|\ge1.96\) for each sign under separately reported treatment sample N/SD; such source-marginal z ratios are **not** joint covariance-aware tests and do not establish 13 true biological effect reversals.
- The \`Fleming_et_al\` 1994 and 1996 \`Pachycereus_pringlei\` female/hermaphrodite rows reproduce **exactly the same six numeric mean/N/SD cells for both cases**. Consequently, we conservatively treat the two reported profiles as **one numeric source profile**, not independent empirical evidence.
- **After the exact-profile duplicate screen:** **129** repeated groups, **28** signed polarity reversals, **12** with both nominal marginal signs, across **104 publication identifiers** in the repeated-group universe. This screen only removes exact same-species numeric repeats; it does not prove all remaining publications are disjoint field samples.

The independent study/publication is the **higher level for uncertainty and counting**. A 6-case landscape split, 3 different flower morphs, a repeated year or two papers reproducing the same raw numbers are **not** six, three, two or two newly independent experimental programmes.

## One ecological condition for sign reversal: reproductive-state and donor context

The original GloPL \`Additional_Treatment_Information\` and \`year_of_study\` / \`population\` labels permit a **retrospective, mutually exclusive condition taxonomy** with the following *declared priority*: explicitly named **pollen donor** (donor origin/flower type) → explicit **flower morph/sex** → distinct recorded **year or metadata year** → explicit **site/distance/population** → unclassified. These are *publication design labels*, not directly measured environmental stress covariates or an unbiased distribution of all plant mating systems. The taxonomy was constructed **after exploratory examination of outcomes**, and tests are not preregistered.

| Grouped condition label | Repeated study×species profiles, deduplicated | Profiles where Bagout−Natural point sign reverses | Profiles with two opposite nominal \(|z|\ge1.96\) cases |
|---|---:|---:|---:|
| Flower morph, sexual state or style class | **23** | **9** | 5 |
| Explicit pollen donor class | 4 | 2 | 1 |
| Distinct source year | 51 | 10 | 4 |
| Locality / patch / population | 41 | 6 | 2 |
| Unclassified experimental contrasts | 10 | 1 | 0 |

Grouped as **mating-context labelled** (morph/sex/donor), **11/27** profiles (40.7%) show sign reversals, versus **16/92** (17.4%) among **time/space** profiles. The difference is **+23.3 percentage points** in this *selected study-design census*. A publication-cluster bootstrap resampling entire original papers yields a broad exploratory positive interval (exact fixed-seed estimate retained by the executable); the source leave-one-publication interval also accompanies it.

**Do not interpret this difference as a species trait effect, population-wide incidence or proof of pollen-compatibility mediation**: it is especially likely that studies explicitly comparing floral morphs or different pollen donors are selected precisely for expecting mating biology to matter. Mixed outcomes are therefore easier to detect by design, and the bibliography and taxonomic groups overlap. This comparison is useful for **prioritizing the biological conditions to test**, not upgrading an observational label into a causal moderator.

## Concrete mechanisms already established in the original experimental literature

The most useful reanalysis contribution is to place multiple **independent, original mechanistic case studies** into the same *directional conditional-response frame* without presenting their published biological discoveries as ours.

### A. The clearest donor-channel anchor: Calystegia collina and remnant context

Within the six source rows of Wolf & Harrison (2001), [*Effects of Habitat Size and Patch Isolation on Reproductive Success of the Serpentine Morning Glory*, doi:10.1111/j.1523-1739.2001.99341.x](https://doi.org/10.1111/j.1523-1739.2001.99341.x), bagged manual pollen delivered from within the same patch gives a **lower fruit-set mean than the naturally pollinated control**, while pollen drawn from near or more distant patches yields higher fruit set. This is **prior published evidence for compatible-mate access, not a novel EGWEE discovery**.

| Habitat condition and donor source | Natural open control | Bagged pollen from **within patch** | Bagged pollen from **near patch** | Bagged pollen from **far patch** |
|---|---:|---:|---:|---:|
| Large serpentine habitat | **0.332** | **0.121** | **0.635** | **0.606** |
| Small serpentine habitat | **0.0865** | **0.053** | **0.416** | **0.280** |

The *average of near+far manual sources minus within-patch manual source* is **+0.4995** fruit-set probability on the large habitat and **+0.295** on the small habitat. All are in **one source publication**, and the rows share open controls, so these are **source-mean descriptive differences without an independent SE for that donor contrast**. There is no direct measurement of actual compatible pollen grains in the GloPL table, but the original authors interpreted this through available compatible mates rather than lower bee numbers.

This supports the **ecological plausibility** of a precise fragmentation question: *is the effective mating channel (compatible pollen origin), rather than just the abundance of visits, missing in some isolated plant populations?* It does not prove this mechanism in the other original EGWEE fragment programmes.

### B. Flower-morph and sex-state anchors

- **Oxalis squamata** (Marco & Arroyo 1998, doi:10.1111/j.1438-8677.1998.tb00738.x): source short-styled mean **Natural 0.527 versus Bagout 0.400** (negative Bagout−Natural), medium-styled **0.542 versus 0.850**, long-styled **0.457 versus 0.961** (positive). Same GloPL study × species. The underlying floral heterostyly and incompatibility are established prior biological knowledge.
- **Hugonia serrata** (Meeus et al. 2011, doi:10.1007/s00606-010-0400-4): source short-styled **Natural 0.270 versus Bagout 0.100**, mid-styled **0.430 versus 0.800**, long-styled **0.440 versus 0.540**. This source is especially relevant to ecological reasoning about **rare tristylous species endemic to La Réunion Island**, but the EGWEE census is not independent evidence that island isolation *caused* those morph contrasts.
- **Rourea induta** (Lenza et al. 2008, doi:10.1590/S0100-84042008000300003): short-styled **Natural 0.410 versus Bagout 0.270**; long-styled **0.250 versus 0.440**. The original authors reported intramorph incompatibility differences. Our source table captures an already documented **morph-specific reversal**, not a newly uncovered mechanism.
- **Pachycereus pringlei** (Fleming et al. 1994/1996): duplicate original female-versus-hermaphrodite numerical profiles, with natural **0.350** for both rows, manually bagged female **0.730** versus hermaphrodite **0.290**. They are **one** numerical profile for this audit, not two separate biological replications.

### C. Conditions requiring special caution

- **Dichorisandra incurva**: labels distinguish pollen from hermaphroditic versus male flowers, and the source mean signs differ. However **the natural control mean also changes substantially (0.430 versus 0.000)** across those source rows, so the GloPL record does **not** isolate donor identity as the single causal factor. The original buzz-pollination and breeding-system research by Sigrist & Sazima (2015, doi:10.1007/s00606-014-1131-8) is prior art.
- **Within-year/location contrasts:** GloPL study \`559\` *Eriocnema fulva* changes sign between recorded 1997 and 1998 populations; \`3015\` *Nematanthus crassifolius* between 2009 and 2010; and \`3088\` *Leptosiphon jepsonii* between named localities in the same recorded year. Observational conditions and covariates change together; do not call any an experiment manipulating temperature, bee abundance, pollen compatibility or islandness.

### Original prior-art and measurement caveats

Outcross pollen effects depend on quantity and compatibility, as established in the broader Harder & Aizen (2010) theoretical treatment of pollen limitation, doi:10.1098/rstb.2009.0226; fruiting under supplementation can further be confounded by reallocation (Knight, Steets & Ashman 2006, doi:10.3732/ajb.93.2.271). **Neither "mating quality is important" nor "pollen scarcity alone is not enough" is claimed as a new EGWEE ecological discovery.** The repeat-species source census newly **quantifies how often reported manual-versus-natural ranks switch within the same species/publication and which explicitly observed study-condition axes coincide with that switching**.

The source-marginal \(z\) screen uses \(\sqrt{SD_N^2/N_N + SD_B^2/N_B}\), which is not an experiment-level test of difference in differences among morphs or donors. The same natural controls may be reused, SD/N can differ among endpoints, and multiple cases within papers are dependent. Source-label comparisons have strong selection bias and publication/year duplications; a positive sign is not universal reproductive benefit.

## Promotable claim and next discriminating field experiment

What *can* be said now:

> **The ranking of natural pollination against manual outcrossing can be condition-dependent even within a single plant species in a single study. Floral morph, pollen source and year/patch context provide explicit source-level examples of this conditionality, but the relative importance of those factors has not been causally identified across studies.**

For the original empirical egwee fragmentation story, the biologically consequential distinction is:

- **Pollen quantity Q:** visits or pollen-tube counts.
- **Effective pollen channel E:** pollen from compatible genotypes/morphs, its arrival timing, and recipient reproductive state.
- **Plant function F:** fruit establishment, seeds per flower/fruit, survival/recruitment.
- **Context M:** mating morph/sex, source pollen provenance, isolation, resource/microclimate.

The **channel-gated hypothesis** to test is not that every island or fragment loses pollination, but that fragmentation decreases reproductive output when pollination events **fail to connect compatible mating partners** even if observed visitation quantity persists. This is a **new hypothesis motivated by multiple prior original studies, NOT a verified universal EGWEE law**.

Use randomized independently replicated fragment/continuous or island/mainland units; stratify known recipient flower morphs; cross **same-patch versus independently compatible external-donor pollen** while holding pollen dose, bag material, timing, sham handling, flower number and water/nutrient access constant. Observe **pollen tubes AND molecular paternity/compatible fertilizations**, fruit initiation, viable seeds, recruitment and next-year fecundity. The definitive discriminating quantity is not just a visit-to-fruit correlation but whether the compatible-donor treatment **restores downstream F when Q has been held constant**. Avoid inferring genetically compatible pollen from colour/shape alone.

## Reproducibility and publication boundary

- Script: \`scripts/audit_glopl_within_species_pollen_polarity_20261028.py\`; standalone Actions \`.github/workflows/glopl-within-species-polarity.yml\`.
- Output audit JSON includes 28 deduplicated mixed profiles with original case IDs, natural/manual means, N/SD reference z, source years, populations and meta-condition text, plus source-cluster confidence bounds. A corresponding source-case CSV permits manual verification.
- Frozen main manuscript, \`submission_ready=false\` and previous EGWEE 5/8/16 denominators remain unchanged. This exploratory experiment taxonomy is **not** merged into the registered fragmentation effect meta-analysis without independent new sampling.
