# EGWEE multilayer meta-analysis — extraction status

**Date:** 2026-09-11

This is an execution ledger, not a Results section. No pooled meta-analytic conclusion is authorised yet.

## Corpus state

- source-verified primary-study seeds: **15**
- candidate systems/programmes: **19**
- priority extraction queue: **8 studies**
- studies with first-pass endpoint extraction materialized: **6**
- currently `g_admissible` effects: **1**

The four-gate programme remains QC/provenance only. The active paper is the multilayer fragmentation meta-analysis.

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

This is one study/species effect with only three independent sites per habitat. It is therefore low precision and does not by itself establish a general layer effect. `scripts/check_brosimum_extraction.py` independently reconstructs this value in CI.

`N_ep=1/r_p` is retained only descriptively because it is the deterministic reciprocal of the same observation and would double-count the signal. Other Brosimum endpoints remain outside naive Hedges-g standardisation until their hierarchy is reconstructed or raw Figshare data (`10.6084/m9.figshare.22130177.v1`) are reanalysed.

## PS014 — Hulting et al. replicated fragmentation experiment

File: `evidence/meta_extraction/PS014_hulting_extraction_v1.csv`

- endpoint/layer records: **4** (`D` flowering likelihood, `D` flower abundance, `I` pollination rate, `F` seed production)
- quantitative primary effects admitted: **0 so far**
- raw dataset: Dryad `10.5061/dryad.bnzs7h4mb`

Published within-study pattern:

- flowering likelihood and flower production increased with distance from the habitat edge across all five species;
- pollination rate showed no detected response to connectivity or edge distance;
- seed production increased with distance from edge for four of five species.

This is a high-value candidate state-separation pattern (`D/F` respond while `I` does not), but the nonsignificant interaction result is **not coded as zero**. Species-specific coefficients/uncertainty or a hierarchy-preserving raw-data reanalysis are required. Dryad confirms that rows are nested observations: block → patch → plant → reproductive structure.

## PS011 — *Conospermum undulatum* contemporary pollen-flow layer

File: `evidence/meta_extraction/PS011_conospermum_2026_extraction_v1.csv`

- contemporary `C` pollen immigration and pollen-distance rows retained for the gradient stream;
- selfing retained as a mechanism/moderator, not a primary D/I/C/F/G response;
- offspring/seedling paternity/genotypes require population/maternal nesting in raw reanalysis;
- adult-genetic context is marked **descriptive duplicate**, linked to the standing adult cohort already represented by PS010/Delnevo et al. 2021 rather than counted as another independent adult-genetic effect.

The 2026 focal populations are all remnant/fragmented populations, so no post-hoc continuous/reference binary split is created. A source-defined isolation/matrix predictor is required for Fisher-z or model-based gradient extraction.

## PS015 — *Conospermum undulatum* interaction / pollen-quality layer

File: `evidence/meta_extraction/PS015_conospermum_2020_extraction_v1.csv`

Across eleven populations, native specialist visitation/effective pollinator representation increased with floral display/connectivity, whereas small isolated remnants had stronger pollen-quality limitation. This adds a same-study `D + I + T + F` gradient between the 2019 reproduction study and the later adult-genetic / contemporary-paternity layers.

The first-pass extraction stores only source-supported ranges/directions and model targets. No coefficient or variance is invented from narrative summaries. The study remains `model_contrast_pending_standardisation` until population-level coefficients/SE or raw data are recovered.

PS015 is priority **5** in the extraction queue. It is not row-joined with PS009/PS010/PS011; the four publications share a programme/system identity but retain separate observation IDs and years.

## PS012 — *Tillandsia intermedia* / *T. makoyana*

File: `evidence/meta_extraction/PS012_tillandsia_extraction_v1.csv`

The study sampled three continuous and three fragmented sites per species over three years. It provides a useful same-study contrast between interaction and reproduction:

- pollinator visitation rate was reported as similar between habitat conditions for both species;
- fruit set did not differ between habitats (`T. intermedia`: `F(1,4)=2.2`, `P=0.22`; `T. makoyana`: `F(1,4)=0.25`, `P=0.64`);
- 2011 seed set was `78±2.8%` continuous vs `79±2.7%` fragmented for *T. intermedia* and `86±2.4%` vs `77±4.1%` for *T. makoyana*; the latter habitat contrast was significant (`F(1,60)=4.3`, `P<0.05`);
- autonomous selfing capacity differed strongly (`AFI=0` in *T. intermedia*, `0.47` in *T. makoyana`) and is retained as a moderator/mechanism rather than a fragmentation response.

Crucially, the reported plant sample sizes (e.g. seed-set subsets `35/29` and `38/27`) are **not** used as independent fragmentation replicate counts because exposure is site-level. The correct independent habitat units are three continuous and three fragmented sites. Without site-level seed-set/visitation summaries or raw data, the apparently significant `T. makoyana` seed-set result is retained as `raw_reanalysis_required`, not converted into a plant-level Hedges `g`.

## Conospermum programme — empirical lag architecture

The source-verified programme now spans:

1. **2019:** population/floral support and reproductive function (`D/R/F`);
2. **2020:** pollinator visitation/effectiveness and pollen-quality limitation (`D/I/T/F`);
3. **2021:** standing adult genetics and historical connectivity (`G_adult/M`);
4. **2026:** contemporary pollen flow / offspring paternity (`C/G_offspring/M`).

This is a strong candidate natural analogue of the NEE state-separation idea: contemporary interaction/mating processes can shift while standing adult neutral genetics still records an older landscape. It is not yet a pooled or causal result because the four campaigns are temporally distinct and cannot be concatenated as one synchronized observation.

## Current inference boundary

Supported now:

- the corpus contains genuinely multilayer natural fragmentation studies;
- multiple studies expose cross-layer differences within the same system or experiment;
- published summaries require explicit hierarchy handling before standardized effects are admitted;
- one site-level standardized effect is already safely reconstructable (`PS004 r_p`, oriented `g=-2.32154`);
- Spondias and Tillandsia demonstrate why individual/offspring counts cannot automatically serve as fragmentation-level `n`;
- Hulting, Tillandsia and the Conospermum programme provide high-value empirical state-separation/lag targets for quantitative extraction.

Not supported yet:

- a pooled mean effect in any layer;
- an omnibus layer-difference test;
- `I-F`, `C-F`, or `G_adult-G_offspring` meta-analytic contrasts;
- moderator conclusions about mating system, movement mode, compensation or cohort history;
- empirical validation of a specific finite NEE operator.

## Next extraction order

1. recover PS015 Conospermum 2020 population-level coefficients/SE or raw data;
2. obtain/reanalyse PS004 Figshare data for additional site/maternal-tree-aware progeny-vigour and genetic effects;
3. obtain/reanalyse PS014 Dryad data for species-specific edge effects on flowering, pollination and seed production;
4. recover PS012 Tillandsia site-level visitation/seed-set summaries if available;
5. proceed to PS002 Magnolia and PS003 Serapias using their locked gradient streams.
