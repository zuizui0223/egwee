# Frozen-universe qualitative interaction–function audit — 2026-10-03

## Purpose

Ask whether the current quantitative interaction–function result is qualitatively echoed or contradicted by **already-screened fragmentation programmes that were excluded from quantitative synthesis for effect-unit, dispersion, covariance or access reasons**.

This audit does not search for new examples. Its denominator was frozen before coding outcome direction:

- the 7 design-passed programmes in `phase2_if_quantitative_gate_v1.csv` that failed quantitative admission;
- ML007 Hulting, an already-registered replicated fragmentation experiment whose published I/F direction is recoverable but whose covariance-aware quantitative effect was blocked.

Total qualitative denominator = **8 independent programmes**.

## Coding rule

Each source is coded only to the level explicitly supported by the paper/recovery record:

- `lower` / `higher` when the source reports a directional effect;
- `no_detected_*` when a source reports no statistically detected exposure effect;
- `similar` when the source explicitly describes output as similar among exposure classes;
- unresolved/unclear otherwise.

**No detected effect is never converted to effect = 0, equality, or biological coupling.**

Nested plants, flowers, seeds or species are not promoted to independent fragmentation replicates. No effect size is manufactured from published significance statements.

## Complete result

| system | interaction result | reproductive-function result | qualitative geometry |
|---|---|---|---|
| *Erica discolor* | no negative visitation effect | viable seeds not lower in small patches | resilient / no detected loss |
| *Haloxylon ammodendron* | visitation lower in fragmented habitat | natural seed set not detectably different | interaction loss / function not detected lower |
| *Caragana korshinskii* | visitation lower in fragmented habitat | natural seed-set habitat effect not significant | interaction loss / function not detected lower |
| *Lithraea molleoides* | no fragmentation effect on pollination level | no effect on seed set/progeny fitness | resilient / no detected loss |
| *Myrtus communis* | visitation highest in small patches; assemblage shifted | seed production rather similar | interaction increase/shift / function similar |
| *Phyteuma spicatum* | visitation higher in large experimental populations | seed production higher in large populations | concordant population-size effect |
| *Psychotria suterella* | visitor richness/frequency greater in fragments | fruit and seed output similar | interaction increase / function similar |
| Hulting five-species experiment | no detected edge/connectivity effect on pollination rate | seed production lower near edge in 4/5 species | qualitative hidden function loss |

## What this adds

The blocked-source denominator does **not** support a one-sided universal downstream failure rule.

Instead it broadens the scale-stable ecological conclusion:

> **Interaction quantity is not a monotonic or sufficient stand-alone proxy for reproductive function under fragmentation.**

Different frozen programmes show:

- interaction decline with reproductive output not detectably lower;
- interaction increase or assemblage change with reproductive output similar;
- no detected loss in either layer;
- concordant deterioration;
- qualitative hidden reproductive loss despite no detected pollination response.

This heterogeneity is exactly why the three quantitatively resolved downstream proxy-failure programmes should be treated as a repeated **failure mode**, not as an estimate of how fragmentation usually propagates.

## Relationship to the quantitative main result

The three representation-stable quantitative downstream mismatches remain the strongest resolved evidence:

- *Eucalyptus wandoo*;
- *Cardiopetalum calophyllum*;
- Kakamega *Acanthopale pubescens*.

The qualitative audit neither increments their quantitative denominator nor changes the 3-programme claim into a prevalence estimate.

Hulting supplies qualitative external support for hidden function loss, whereas Haloxylon, Caragana, Myrtus and Psychotria show the opposite lesson: interaction quantity can also decline or increase without an equivalent reproductive-function response.

Thus the broader ecological generalization is **proxy insufficiency / non-monotonic translation**, while the downstream asymmetry remains a narrower quantitative observation.

## Mechanistic implications

The source biology points to different filters rather than one common mechanism:

- *Haloxylon*: wind pollination buffers seed set despite reduced insect visitation;
- *Myrtus*: honeybee dominance and high visitation in small patches coexist with broadly similar seed production;
- *Psychotria*: visitor frequency increases in fragments while reproductive stages remain resilient in a connected landscape;
- Hulting: edge effects reduce flowering/seed production without a detected pollination-rate response;
- *Phyteuma*: population-size effects on visitation and seed production are concordant.

The prospective `interaction quantity → effective mating → reproductive function` design remains appropriate because it can distinguish these routes instead of assuming that visit abundance is the causal intermediate.

## Claim ceiling

Allowed:

- the complete frozen qualitative denominator contains multiple forms of I–F non-monotonicity as well as resilience and concordance;
- qualitative blocked evidence is consistent with interaction quantity being an insufficient stand-alone functional sentinel;
- Hulting qualitatively supports hidden function loss, while several other systems show buffering/resilience;
- the quantitative three-program downstream result remains distinct from qualitative corroboration.

Not allowed:

- count these eight programmes as quantitative replication;
- code no detected effects as zero;
- use the qualitative category frequencies as global prevalence estimates;
- claim all qualitative programmes show proxy failure;
- infer one common mechanism from the mixed directions.

## Sources / frozen provenance

- Phase-2 gate: `evidence/meta_extraction/phase2_if_quantitative_gate_v1.csv`
- Hulting registry/recovery: `evidence/meta_extraction/PS014_hulting_extraction_v1.csv` and `manuscript/HULTING_2025_CLUSTER_RECOVERY_RESULT.md`
- machine-readable audit: `evidence/meta_extraction/qualitative_external_if_audit_v1.csv`
