# Interaction–function translation non-identifiability — 2026-10-03

## Question

Can the qualitative state of reproductive function be inferred uniquely from the qualitative response of interaction / pollen quantity under habitat fragmentation?

## Frozen evidence universe

The audit combines two **non-overlapping, already frozen** evidence tiers:

- 8 quantitatively admitted matched I–F programmes;
- 8 already-screened I–F programmes blocked from quantitative synthesis but with source-explicit qualitative response geometry.

Total mapped programmes = **16 independent source programmes**.

The two evidence tiers remain separate. Qualitative programmes do not become quantitative replications, and category counts are not used as prevalence estimates.

## Result: the mapping is many-to-many

The same qualitative interaction signal maps to multiple reproductive-function states.

### Interaction lower

Programmes with lower interaction / pollinator quantity include examples in which reproductive function is:

- **lower** — e.g. Chaco, Cardiopetalum, Pritchard, Phyteuma;
- **higher as a point estimate** — common milkweed and some Sevenello panels;
- **not detectably lower** — Haloxylon and Caragana.

### No detected interaction loss

Programmes with no detected interaction decline include:

- **no detected reproductive loss** — Erica and Lithraea;
- **lower reproductive function** — Hulting, where seed production declines near edges despite no detected pollination-rate edge/connectivity effect.

### Interaction higher

Programmes with higher interaction quantity include:

- **lower reproductive function** — Eucalyptus wandoo and Kakamega Acanthopale;
- **similar reproductive function** — Psychotria; Myrtus provides a related interaction-increase / assemblage-shift case with broadly similar seed production.

## Ecological interpretation

This is stronger than saying that visitation is noisy.

> **Interaction quantity is a non-identifying sentinel of reproductive function under fragmentation: the same upstream interaction signal can correspond to different downstream functional states.**

The implication is not that interaction monitoring is useless. Interaction quantity remains biologically informative, but it is insufficient **on its own** to diagnose reproductive function.

## Relation to the three quantitative proxy-failure anchors

The three representation-stable resolved downstream programmes remain the strongest quantitative evidence:

- Eucalyptus wandoo;
- Cardiopetalum calophyllum;
- Kakamega Acanthopale pubescens.

They establish a repeated **false-reassurance failure mode**: interaction quantity looks better than reproductive function.

The 16-programme translation map adds a different result. It shows that the broader I→F mapping is not one-to-one even when the quantitative admission filter is relaxed only to source-explicit qualitative geometry. Thus the proxy-failure signal is not simply an artefact of which programmes supplied reconstructable variances/covariances.

## Leave-one-programme-out robustness

The full 16-programme translation non-identifiability result is not carried by one source.

After deleting any single programme, the remaining map still contains **at least two interaction evidence states that map to multiple reproductive-function states**.

Thus the existence of a many-to-many translation structure is leave-one-programme-out robust within the frozen mixed-tier evidence universe.

The quantitative-only tier is weaker. Its category-level ambiguity is carried by the unresolved opposite-sign point estimate in common milkweed; removing that programme leaves no quantitative interaction category with more than one programme-level F category. This does **not** erase the three representation-stable quantitative false-reassurance anchors, which are a different claim based on resolved within-programme contrasts.

Therefore the hierarchy is:

1. **full 16-programme map:** robust existence of non-identifying translation;
2. **quantitative 8-programme map:** no robust category-frequency or multi-state mapping claim;
3. **quantitative resolved evidence:** three stable false-reassurance programmes.
## Why this is not a prevalence analysis

The evidence tiers differ in precision and estimand:

- quantitative admitted programmes have reconstructable effect size / uncertainty;
- qualitative blocked programmes have source-explicit direction or no-detected-effect statements only.

Therefore the map establishes **existence of multiple translation states**, not their population frequencies.

No 16-programme binomial test, contingency test or regime-frequency estimate is authorised.

## Mechanistic meaning

A many-to-many Q→F map is expected when unmeasured intermediate and direct pathways vary among systems:

- pollinator identity / per-visit effectiveness;
- compatible pollen and self/outcross composition;
- realised pollen-donor diversity;
- wind pollination or reproductive assurance;
- post-pollination filtering;
- direct landscape/resource effects on fruit/seed production.

The current registered quantitative I–F set directly measures effective mating quality in **0/8 programmes**, leaving the most likely intermediate conversion layer largely unobserved.

## Strongest paper-level statement

> **Habitat fragmentation does not map interaction quantity monotonically onto reproductive function. Across a frozen 16-programme evidence universe, identical qualitative interaction signals coexist with divergent reproductive outcomes.**

This is a statement about response translation and sentinel sufficiency, not a claim about one causal mechanism or global prevalence.

## Claim ceiling

Allowed:

- 16 independent frozen source programmes are represented: 8 quantitative and 8 qualitative-blocked;
- the same interaction signal occurs with multiple reproductive-function states;
- interaction quantity is insufficient as a stand-alone sentinel of reproductive function;
- three quantitative programmes provide representation-stable resolved false-reassurance examples;
- Hulting provides qualitative hidden-function-loss support;
- the qualitative blocked set also contains buffering, resilience and concordance, showing non-monotonic translation rather than a universal downstream rule.

Not allowed:

- frequencies in the 16-programme map estimate global ecological prevalence;
- qualitative blocked programmes are equivalent to quantitative replications;
- all fragmentation effects are non-monotonic;
- one missing effective-mating mechanism explains all systems;
- pollinator abundance or visitation has no conservation value.

## Machine-readable implementation

- `evidence/meta_extraction/if_translation_map_v1.csv`
- `scripts/check_if_translation_map.py`
