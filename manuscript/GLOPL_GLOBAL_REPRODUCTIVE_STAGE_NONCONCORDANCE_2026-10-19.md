# GloPL: global within-experiment reproductive-stage nonconcordance

**2026-10-19 | Empirical egwee exploratory external macro-analysis**. Not the theoretical egwe programme. Source: Bennett et al. (2018), *Scientific Data*, doi:10.1038/sdata.2018.249. Original data doi:10.5061/dryad.dt437, CC0. Public original author repository: [idiv-biodiversity/pollen-limitation-data-descriptor](https://github.com/idiv-biodiversity/pollen-limitation-data-descriptor/blob/abbe193770981b2c61713e75a0f01e004bdded8e/Data/GloPL_with_id.csv).

## Question and prior art

Does the same pollen-supplementation experiment necessarily show the same directional response in (1) probability a flower sets fruit and (2) seed content of an existing fruit? GloPL originally demonstrated a generally positive response to pollen supplementation, positive correlations among different response types, a preference hierarchy for source effects (**seeds per plant > seeds per flower > seeds per fruit > fruit set > seeds per ovule**), and many ecological gradients. Those are all **prior discoveries**. This reanalysis instead quantifies the **point-sign topology within exactly the same case**, explicitly separating dependent studies and unresolved marginal effects.

**Do not conflate this with fragmentation:** the source cases do not contain independently registered comparable habitat fragmentation contrasts; they are independent experimental source records from another ecological domain. They do not add to frozen EGWEE 5/8/16 fragmentation programmes or source-disjoint SF06 estimates.

## 2,969-case source census

The public author source comprises **2,969 records, 927 publications and 1,265 accepted plant species**. Of these, **560 cases from 158 publications** have at least two source means for any of five outcomes.

Response endpoints and all usable nonnegative mean pairs:

| Source code | Response | Cases | Supplemented > natural | Supplemented < natural | Same rounded mean |
|---|---|---:|---:|---:|---:|
| FS | Fruit set (probability) | 1,361 | 1,104 | 211 | 46 |
| SO | Seeds per ovule | 466 | 337 | 122 | 7 |
| SPFR | Seeds per existing fruit | 480 | 367 | 98 | 15 |
| SPFL | Seeds per flower | 305 | 267 | 35 | 3 |
| SPP | Seeds per plant | 249 | 177 | 69 | 3 |

These rows are not mutually exclusive across responses, and publication/year/species cases from a study are dependent.

The prespecified ecology-first focus in this retrospective extension is **FS × SPFR**, two successive reproductive stages. It yields **344 same-experiment pairs from 86 publications**, of which 313 pairs in 84 publications have nonzero point contrasts in both endpoints. The 2×2 topology on 313 cases:

| Pollen addition effect on FS | SPFR increases | SPFR decreases |
|---|---:|---:|
| FS increases | **205** | **48** |
| FS decreases | **33** | **27** |

**Opposite point signs = 81/313 = 25.88%, across 36 distinct publications and 28 plant families.** Cases need not all be independent: one publication can contribute several species/populations/years/morphs/treatments. The equal-publication average fraction of discordant point cases among its eligible records is **23.83%** (84 publications), with an omit-one-publication range of **22.91–24.12%**. This is not a field prevalence estimate and is conditional on **both metrics being measured and having nonzero source-mean contrasts**; it is heavily subject to publication and measurement selection.

This direction mismatch is approximately symmetric in type (FS up/SPFR down **48**, FS down/SPFR up **33**). Neither a universal fruit-production bottleneck nor universal seed-filling deterioration follows.

## Is discordance biologically resolved?

**Do not claim 81 confidently detected tradeoffs.** Of the 81 opposite point-sign cases, 78 have compatible published N/SD columns for a rough two-independent-arm standard-error ratio. Only **4 cases from 4 distinct publications** pass a nominal z ≥ 1.96 in **both** marginal endpoints on that *approximate* screen. The screen is not a true simultaneous 95% interval, because treatment samples may share maternal plants, fruit set and seeds-per-fruit may have nonnormal/binomial distributions, the within-case/within-source covariance is unavailable and original N may describe differing observational scales. These 4 remain *candidates* for source-specific verification. The other 77 point cases cannot be considered confirmed reversals.

In contrast, a mean positive correlation of responses is perfectly compatible with occasional opposite point signs. An opposite sign is not a demonstrated compensatory allocation mechanism, evolutionary antagonism or negative within-individual covariance.

## Same-case third endpoint cross-check

For **44 cases from 9 publications** with simultaneous nonzero FS, SPFR and SPFL means:

- FS+, SPFR+, SPFL+: 28
- FS+, SPFR−, SPFL+: 9
- FS+, SPFR−, SPFL−: 3
- FS−, SPFR+, SPFL+: 1
- FS−, SPFR−, SPFL−: 3

The third response can align with one, but not necessarily both, component stages. The same-case triple sample is only 9 source publications; neither algebraic multiplication of marginal means nor a study-level pooled compensatory mechanism is justified.

## Heterogeneity candidate — scale of hand-pollen application

Among opposite/nonopposite FS–SPFR source cases, flower-level supplementation gives **20/117 (17.1%)** opposite cases across **43 publications**, while whole-plant supplementation gives **55/162 (34.0%)** across **29 publications**. Giving each publication equal weight for its eligible cases changes these descriptive frequencies to **22.1%** and **32.3%**, respectively.

**Crucial confounding:** only **one publication** in the eligible data reports both application levels. Thus this is **not** a within-study experimental comparison of flower versus whole-plant treatments, and cannot show that pollen addition to the whole plant *causes* developmental tradeoffs. Study, species, life history, habitat, power and outcome measurement could account for the difference. No general moderator or test significance is claimed.

## General ecological meaning

Across many source publications, the same pollen addition does **not** map to one uniquely defined response for all reproductive stages. An increase in the **probability of forming a fruit** is not identical to an increase in the **seed content conditional on having a fruit**. Resource supply, compatible pollen, quality–quantity effects and differential abortion are plausible mechanisms, but this source table alone cannot identify which is responsible. A mechanism requires synchronously matched plant/flower outcomes and experimental/physiological covariates.

This is broadly relevant to egwee's stronger, independently registered **fragmentation interaction→fitness** finding but not its causal validation. GloPL's supplement-treated and natural controls are intervention arms, while egwee's main matched observational corpus evaluates changes across fragmented landscapes; the two effect definitions cannot be pooled without an explicit causal estimand.

## Source, reproducibility, audit status

- Local study copy: \`evidence/meta_extraction/glopl_2018/GloPL_with_id.csv\`
- **Source encoding caveat:** original author Git blob \`d22fe333b19489c473e076dd173ed7a67b1afbf0\` is **legacy encoded** and cannot be represented byte-identically by the GitHub text connector. The normalized UTF-8 copy stored here is a *derived text version* with Git blob \`0809eaeee54e4375d26bacfe002787241f8ff72e\`, preserving 2,969 rows and the numeric table; source numeric validation is not equivalent to original byte-MD5 verification. See \`evidence/meta_extraction/glopl_2018/SOURCE_PROVENANCE.md\`.
- Reproducer \`scripts/audit_glopl_reproductive_stage_topology_20261019.py\`, workflow \`.github/workflows/glopl-stage-topology.yml\`. It writes case/study/family count JSON, all 84 eligible publication summaries and all 81 opposite point-sign records.
- \`submission_ready=false\` and frozen main manuscript remain unchanged. This is a retrospective global **mechanistic hypothesis generator**, not a novel fragmentation meta-analysis or an accepted publication conclusion.
