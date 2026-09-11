# EGWEE multilayer meta-analysis — extraction status

**Date:** 2026-09-11

This is an execution ledger, not a Results section. No pooled meta-analytic conclusion is authorised yet.

## Corpus state

- source-verified primary-study seeds: **14**
- candidate systems/programmes: **18**
- priority extraction queue: **7 studies**
- studies with first-pass endpoint extraction materialized: **3**

## PS001 — *Spondias purpurea*

File: `evidence/meta_extraction/PS001_spondias_extraction_v1.csv`

- raw/model endpoints recorded: **11**
- layers reached: `I`, `C`, `F`, `G_adult`, `G_offspring`
- `g_admissible`: **0**
- model contrasts pending compatible standardisation: at least **3**
- raw/cluster-aware reanalysis required: at least **6**

Reason: several published denominators describe lower-level trees, offspring/paternity events or individuals, while genetic dispersion is locus-level and reproductive analyses use site/random-effect structure. Naively combining these quantities would produce pseudo-replication.

This source triggered the pre-outcome effect-unit amendment `META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-11_EFFECT_UNITS.md`.

## PS004 — *Brosimum alicastrum*

File: `evidence/meta_extraction/PS004_brosimum_extraction_v1.csv`

- endpoint records: **8**
- layers reached: `C`, `F`, `G_adult`, `G_offspring`
- first `g_admissible` endpoint: **site-level multilocus correlated paternity (`r_p`)**

Table 3 supplies three continuous-site and three fragmented-site paternity-correlation estimates:

- continuous: `0.106, 0.164, 0.107`
- fragmented: `0.246, 0.208, 0.191`

Using sites—not seedlings—as the independent units:

- fragmented minus continuous Hedges `g = +2.32153761`
- because higher `r_p` means fewer effective sires / lower mating support, orientation multiplier = `-1`
- oriented effect = **`-2.32153761`**
- sampling variance = `1.10035878`; SE ≈ `1.04898`

This is one study/species effect with only three independent sites per habitat. It is therefore low precision and does not by itself establish a general layer effect.

`N_ep=1/r_p` is retained only descriptively because it is the deterministic reciprocal of the same observation and would double-count the signal.

Other Brosimum endpoints—pollen-flow distance, habitat-level genetic summaries and model-based progeny vigour—remain outside naive Hedges-g standardisation until their hierarchy is reconstructed or raw data are reanalysed. The article states that raw data are archived on Figshare (`10.6084/m9.figshare.22130177.v1`).

## PS014 — Hulting et al. replicated fragmentation experiment

File: `evidence/meta_extraction/PS014_hulting_extraction_v1.csv`

- endpoint/layer records: **4** (`D` flowering likelihood, `D` flower abundance, `I` pollination rate, `F` seed production)
- quantitative primary effects admitted: **0 so far**
- raw dataset: Dryad `10.5061/dryad.bnzs7h4mb`

The published experiment gives a particularly important within-study qualitative pattern:

- flowering likelihood and flower production increased with distance from the habitat edge across all five species;
- pollination rate showed no detected response to connectivity or edge distance;
- seed production increased with distance from edge for four of five species.

This is a direct candidate instance of cross-layer fragmentation discordance (`D/F` respond while `I` does not), but the null interaction effect is **not coded as zero**. Species-specific coefficients/uncertainty or a hierarchy-preserving raw-data reanalysis are required before meta-analysis admission.

Dryad documents the nesting variables (`block`, `patch`, `distance`, `species`, plant reproductive status, flowering structures and seed counts). Plant/structure rows are therefore not treated as independent landscape replicates.

## Current inference boundary

Supported now:

- the corpus contains genuinely multilayer natural fragmentation studies;
- published summaries require explicit hierarchy handling before standardized effects are admitted;
- at least one effect can already be reconstructed at the correct site level (`PS004 r_p`);
- the Hulting experiment supplies a strong candidate empirical state-separation pattern requiring quantitative extraction.

Not supported yet:

- a pooled mean effect in any layer;
- an omnibus layer-difference test;
- `I-F`, `C-F`, or `G_adult-G_offspring` meta-analytic contrasts;
- moderator conclusions about mating system, movement mode, compensation or cohort history;
- empirical validation of a specific finite NEE operator.

## Next extraction order

1. obtain/reanalyse PS004 Figshare data to recover site/maternal-tree-aware progeny-vigour and genetic effects where possible;
2. obtain/reanalyse PS014 Dryad data for species-specific edge effects on flowering, pollination and seed production;
3. extract PS011 *Conospermum* contemporary pollen-flow/offspring layer while preserving population/year linkage;
4. continue PS012 / PS002 / PS003 according to the locked queue.
