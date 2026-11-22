# CP002 — CropPol measurements, source blocking and baseline availability

**22 November 2026. Empirical EGWEE.**
**Decision: METADATA_AUDITED_NOT_MODEL_ADMISSION.**

## Main finding

The pinned database supports a substantially smaller, explicitly defined
visitor–production candidate set than the earlier presence-only count suggested.
There are **452 records from 19 provisional source components** with a reviewed
direct primary-output label, a documented timed observation label and the
author's use-visits annotation. Restricting the output to harvest mass per land
area leaves **121 records from five components**.

Requiring management, cropped-field area and plant density on the same records
leaves **38 records in two comparison blocks from just one source component**
for the area-mass target. A new-source comparison of that baseline against a
visitation extension cannot be evaluated with one source component. The broader
direct-output candidate set has only 43 jointly complete records from two
components. No predictive score, visitor–yield coefficient or biological effect
was estimated.

This is a limitation of this specified target and comparator in the pinned
release, not a finding that pollinators lack effects or that CropPol cannot
support other well-defined questions. A metadata classification is not proof
that the original measure was constructed as its label suggests.

## Source and execution

Controlling author release: CropPol v2.1.0, commit
`febec7dcc088ccf1bd721c41ce8dda87a2dcba1a`,
`Final_Data/CropPol_field_level_data.csv`.

- Original bytes: 2,195,393.
- Git blob SHA-1: `cd19a354741ac40428e6b94aa1ec2ee596ff0547`.
- Original-file SHA-256:
  `ecfa84d1f6a52f24f13b7096347a59f231e8cc77eef8692b0a0183ceca86f879`.
- Exact ordered header: 68 columns, unchanged from CP001.
- Production analysis commit:
  `0351a9e0d89f8013b767a6f8e1ee4430438444ff`.
- [Original-source execution 44972392076](https://github.com/zuizui0223/egwee/actions/runs/44972392076)
  passed 33 scoped CP001/CP002 regression tests, source verification, metadata
  processing and aggregate-artifact upload.
- Artifact 14734291967, ZIP SHA-256:
  `a631061bedbc985b7b5d131a0b3d821a2a6c7494ccae44d08630458d52193455`.
  Root downloaded the ZIP, independently verified that digest and checked it
  contains only the expected aggregate receipt.
- Frozen-rule SHA-256 in the production receipt:
  `5810972ff5179dba661d78d630687fe9b5bbdaa4ae31559606db16ba55153979`.

The [original receipt](CP002_ORIGINAL_METADATA_RECEIPT_20261122.json),
[metadata rules](CP002_METADATA_RULES.json),
[reviewed DOI registry](CP002_SOURCE_DOI_REGISTRY.json), and
[source-evidence manifest](CP002_SOURCE_EVIDENCE_MANIFEST.json) are inspectable.
No original source rows, individual/site identifiers, coordinates, contacts,
genotypes or numerical biological measurements are redistributed.

## What the metadata actually says

The [pinned submission template](https://github.com/ibartomeus/CropPol/blob/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Template/Template_example_V10.ods)
defines primary yield broadly, under natural pollinator exposure, with kg/ha
preferred but other reproductive and crop-production measures permitted.
The shorter [attributes table](https://github.com/ibartomeus/CropPol/blob/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Metadata/data/metadata/attributes.csv)
does not fully define the author selector.

The metadata dictionary covers 53 primary-unit labels and 28 secondary-unit
labels, **including the missing marker in each count**. Full-label matching
matters: a label beginning with fruit set can instead describe the mass of
100 seeds or a contrast between pollination treatments. Already z-scored
endpoints remain explicitly transformed. Unspecified mass, container units,
thresholded quality and proxies are separate categories.

Among finite primary numeric cells, the classified families are:

| Primary family | Records |
|---|---:|
| Reproductive count or set | 888 |
| Harvest mass per area | 606 |
| Harvest mass per plant/tree/shrub | 76 |
| Harvest mass per whole field | 50 |
| Harvest mass for a fixed branch/head sample | 37 |
| Organ mass or quality component | 539 |
| Already transformed | 177 |
| Treatment contrast | 12 |

These categories are not pooled biological effect sizes. The five first families
form the broad direct-label candidate inventory. The area-mass frame is a
separate, narrower target. Secondary outcomes were classified separately and
never substituted for a missing or inconvenient primary outcome.

No unit label explicitly identifies a visitation-derived pollen estimate.
The authors' [methods](https://github.com/ibartomeus/CropPollinationModels/blob/bf209807bc359b7ce86156cd7ffd600ced06d1f2/methods.qmd)
exclude such estimated outcomes, but their absence from our candidates is not
certified by labels alone. That remains an original-source construction check.

### Visitation and abundance

The selector is a curated instruction for the Reilly dynamic analysis, not a
universal quality flag. Its exclusions include missing honeybee observations,
enclosures, traps and unresolved methods. A dataset excluded from that comparison
is not automatically invalid for another question.

The strict timed-observation frame requires a recorded focal-observation or
transect method, an explicit time denominator, numeric nonnegative total
visitation, and a known non-none taxonomic sampling scope. Plain visits,
floral counts without a time denominator, insect density, and generic
unspecified time units stay separate. Sweep-net records cannot become direct
timed observations merely because they occupy a visitation column.

The author's [processing script](https://github.com/ibartomeus/CropPollinationModels/blob/bf209807bc359b7ce86156cd7ffd600ced06d1f2/scripts/read_data.R)
documents the manual selector and scope-dependent handling of guild values.
We do not turn unrecorded guilds into observed zero. The source wild-bee fields
exclude Bombus; no unverified guild recombination was performed.

## Source groups: 145 analysis groups become 111 blocking components

The [join script](https://github.com/ibartomeus/CropPol/blob/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data/Supporting_R_scripts/add_dynamic_paper_variables_to_field_data_with_65_variables.R)
attaches study_id2 from an annotation workbook. The authors'
[original grouping code](https://github.com/ibartomeus/CropPollinationModels/blob/bf209807bc359b7ce86156cd7ffd600ced06d1f2/scripts/Original_analysis/HB%20vs%20WI%20analysis%20clean.R)
removes years, repairs labels and splits some common studies when methods or
papers differ. It therefore describes analytical consistency, not independent
programme identity.

The provenance audit matched all 220 workbook mappings and replayed the author
rule for all 222 study-label-by-year combinations. One additional study label
enters through the newer 68-column pipeline.

| Grouping rule | Components |
|---|---:|
| Author study_id2 alone | 145 |
| Add exact year-stripped study-ID links | 142 |
| Add vetted original-publication links, without year links | 113 |
| **Union of year and vetted original-publication links** | **111** |

Only 11 reviewed original or coordinated-study DOIs create publication edges.
Three cross-group synthesis references are explicitly excluded as automatic
original-programme links. A coordinated original field campaign is different
from a later synthesis containing unrelated campaigns. The full graph is built
before biological eligibility filtering, preserving transitive links even when
an intermediate record would fail an endpoint filter.

The largest component combines 13 author analysis groups. Shared author names,
emails, institutions or generic unpublished labels never create edges.

The graph remains incomplete as a map of independence: 42 author groups have no
parseable DOI anywhere; 407 records lack publication text; 659 lack a parseable
DOI. Different papers may reuse farms or campaigns. Sequentially incremented DOI
suffixes were also found within one existing group; these are not silently
repaired or treated as validated references. The 111 components are consequently
**provisional blocking units**, not 111 proven independent studies.

## Executed candidate counts

| Metadata/domain frame | Records | Author groups | Source components | Crops | Countries |
|---|---:|---:|---:|---:|---:|
| Whole source | 3,448 | 145 | 111 | 48 | 35 |
| Reviewed direct primary-output label | 1,657 | 84 | 64 | 37 | 28 |
| Above plus valid numeric total-visitation field | 986 | 40 | 29 | 20 | 17 |
| Above plus timed observation and recorded scope | 485 | 23 | 21 | 16 | 13 |
| Above plus author use-visits selector | **452** | **19** | **19** | **15** | **12** |
| Area-mass output within that strict visit frame | **121** | **5** | **5** | **5** | **5** |
| Reviewed-method author-use-abundance direct-output frame | 572 | 42 | 32 | 22 | 19 |

Frames overlap and must not be summed. The 33 timed-observation records outside
the strict author selector remain separately counted; they are not declared
biologically invalid. The abundance frame additionally requires a reviewed
sampling method and recorded taxonomic scope. It is not substituted for visits.

Zero is observed. Missing and non-finite values are not zero. No negative direct
primary outcomes, negative total visits, negative abundance or out-of-range
explicit primary percentages occurred in the admitted-label domain checks.
Signed transformed/contrast outcomes outside the candidate families are not
called errors simply because they can be negative.

## The baseline, rather than raw row count, is the immediate limitation

Field area is documented in hectares and plant density in plants per square
metre. Surveyed transect area is a different field and is never substituted for
cropped-field area. Plant density is not flower density. The source's generic
cleaning scripts do not establish whether original density measurements were
independently observed, calculated from spacing, or reconstructed from another
quantity, nor do they certify preharvest timing.

Comparison blocks keep source component, crop, sampling year, exact normalized
output unit, visit unit, observation method and recorded taxonomic scope
together. All blocks are counted before deleting records with missing baseline
covariates. A feasible block needs at least five complete unique candidate keys
and a varying baseline. The half-pair indicator asks whether at least half of
the field pairs differ in their baseline vector; it uses no outcome ordering.

| Candidate frame | Records | All blocks | Jointly complete records | Complete blocks with ≥5 keys and variation | Source components |
|---|---:|---:|---:|---:|---:|
| Strict direct-output/visit frame | 452 | 30 | **43** | 3 | **2** |
| Strict harvest mass per area | 121 | 8 | **38** | 2 | **1** |

All three complete blocks in the broader frame, and both in the area-mass frame,
also pass the half-pair indicator. But 27 of the 30 broader blocks and six of the
eight area-mass blocks have no jointly complete record.

| Baseline field | Available in strict direct frame | Available in area-mass frame |
|---|---:|---:|
| Management | 452 | 121 |
| Field area | 296 | 81 |
| Plant density | 58 | 53 |
| **All three on the same record** | **43** | **38** |

Availability alone is not a meaningful comparator. For example, management is
present throughout the strict frame but varies within qualifying blocks in only
six source components; within the area-mass frame it varies in only one.
A baseline containing only labels constant within each prediction block would
provide a weak comparison by construction.

## Independent verification and interpretation

A separate JavaScript implementation, without reading or importing the
production Python auditor, independently verified source hashes, the graph,
candidate counts and baseline completeness/variation. The
[independent recount](CP002_INDEPENDENT_RECOUNT_20261122.json) records its exact
rules and reconciliation history. Its initial broad abundance frame had 574
records; the production frame also screens recorded sampling methods. Applying
the same precommitted method rule excludes two records (one other and one
mixed sweep-net/other record), reproducing 572. The taxonomic-scope rule removes
none of those 574. Both definitions are retained, rather than overwriting the
initial discrepancy. The [independent implementation](validation/independent_cp002_recount.js)
is included for inspection. The receipt also distinguishes the initial specification
commit e225b82 from subsequent metadata-review amendments. The complete
production contract and reviewed implementation are committed at 0351a9e;
this work is metadata-informed, not an unseen-data preregistration.

Independent code review reproduced errors in baseline denominators, measurement
domains, missing taxonomic scope, duplicate accounting and missing-source
namespaces. They were fixed with failing-then-passing synthetic cases before
the production run. The resulting 33-test suite is scoped to CP001/CP002; it is
not a claim that an unrelated full-repository test suite was run.

## Prior work and the next useful work

Visitor–yield associations are already studied by
[Reilly 2024](https://doi.org/10.1111/geb.13843),
[Turo 2024](https://doi.org/10.1038/s41559-024-02460-2), and
[Vezzani 2025](https://doi.org/10.1111/1365-2664.70042).
Turo uses within-system LOOIC comparisons, so predictive model comparison itself
is not absent from the literature. Vezzani's normalization by a study-specific
observed maximum should not be copied into an unseen-source forecast.

[Author-held-out CropPol prediction already exists for visitation](https://doi.org/10.5194/we-23-99-2023),
with a [later CNN extension](https://doi.org/10.5194/we-24-81-2024).
A candidate contribution would therefore need to establish added yield-ranking
information from observed visits beyond an informative preharvest field-context
baseline, not claim the first held-out CropPol analysis.

The [2026 methodological commentary](https://doi.org/10.1111/1365-2435.70269)
explains how floral density and maternal resources can jointly affect visitation
and yield. Successful prediction would still not prove that adding pollinators
causes the corresponding yield change.

The next bounded curation task is to recover documented observation effort and
preharvest field-context information from the public source-processing records,
and check original endpoint construction. That task can expand a standardized
database without selecting sources by a favourable effect. This pinned
three-covariate, area-mass design is not run as a macroecological model with one
source component, and its criteria are not relaxed to manufacture a result.

All changes remain in draft PR94. Main, the historical five-cluster evidence,
Brassica/Silene results and theoretical egwe are unchanged.
