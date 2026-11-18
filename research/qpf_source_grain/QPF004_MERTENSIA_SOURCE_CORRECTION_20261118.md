# QPF004 primary-source correction — *Mertensia ciliata*, not *Mimulus/Erythranthe ciliata*

**18 November 2026.** Source and independent biological-unit audit **only**. This corrects a taxon misidentification in the outcome-blind six-candidate Q–P–F registry of draft PR #66 without silently rewriting the original frozen programme. **No biological outcome coefficient, new Q–P–F effect, source-matched sample size, or extra independent system is claimed**.

## Correct primary source

- Gallagher, M. K. & Campbell, D. R. (2020), *Pollinator visitation rate and effectiveness vary with flowering phenology*, *American Journal of Botany* 107:445–455, [DOI 10.1002/ajb2.1439](https://doi.org/10.1002/ajb2.1439).
- Original public data package [Dryad DOI 10.7280/D19X0D](https://doi.org/10.7280/D19X0D); dataset page [source](https://datadryad.org/dataset/doi%3A10.7280/D19X0D). It explicitly identifies **`Mertensia ciliata` (Boraginaceae)**. The original PR #66 registry entry says **`Mimulus/Erythranthe ciliata`** (Phrymaceae): this is a **species/family error**, not a synonym. The six-source selection and prospective date are preserved; the corrected species must be used in all future analyses, source inventory lookups, and any eventual manuscript.
- Four original files: `gallagher&campbell_phenologyExperimentData.xlsx`, `gallagher&campbell_pollinatorEffectivenessData.xlsx` and their two corresponding non-spatial metadata PDFs. **The PDFs are catalogued, not analyzed** by the source-schema audit.

## Critical source architecture: these are two experiments, not 235 paired Q–P–F flowers

| Design | 2015 flowering-phenology manipulation | 2016 single-visit effectiveness |
|---|---|---|
| Biological unit | 40 flowering **potted plants**, 4 manipulated flowering-onset weeks (10 per week), nested in randomized arrays | 95 **visited ramets**, 235 marked visited flowers across two wild locations; some visited ramets have multiple flowers |
| Interaction Q | Repeated 30-minute observed visitor counts and floral display, by week/array/plant | Each ramet exposed to one observed insect visit with visitor taxon and marked flower(s); controls are distinct |
| Transfer P | Stigma pollen microscopy on a subsample averaging **5.2 ± 0.7 flowers per plant** | Same treatment programme samples stigma CP/HP; published Fig. 5 reports **62** pollen observations, *not* 235 |
| Function F | All tagged flowers' mature seeds aggregated to seeds per planted individual | Single-visit marked flower seed outcomes; published Fig. 5 has **232** seed observations, not necessarily the same 62 pollen samples |
| Outcome loss | Must confirm tagging/bagging, source seed eligibility and observation effort per plant | Exclude/record herbivory and accidental damage; 65 open-but-no-observed-visit and 74 continuously bagged control ramets |
| Strict join gate | Matched **potted plant ID × array × week**, not same blossom just because Q and P came from the same programme | Matched **ramet/marked flower ID × clone/treatment × site × visit type** among available pollen and seed observations — joint pair count **unknown until original XLSX checked** |

**2015 week-4 method issue:** the first 15 observed hours produced no visits, so cut stems were subsequently added to pots to increase displayed flowers, followed by another 15 observation hours. Thus the fourth-week encounter/flower-hour numerator/denominator is *partly under a changed floral-display intervention*. A clean natural seasonal comparison cannot silently treat the two blocks as identical floral exposure without recording that design change. This is a measured experimental provenance issue, not evidence of bias or a new pollination mechanism.

**2016 pollen and seed samples:** the published Fig. 5's N=62 for pollen and N=232 for seed count **cannot be added or assumed to overlap perfectly**. If the original source rows prove no shared ramet/marked-flower key, the outcome is a **SOURCE_JOIN_STOP**, not a new Q→P→F numeric null. Even for shared ramets, repeated marked flowers, clone-level relatedness, two collection sites and the open/bagged control arms must not be pseudoreplicated.

## The ecological result in the original paper is already known

The original authors report an approximately **five-fold** decline in observed visitation over four weeks, while experimental seed set did not decline significantly. They associate this with a shift toward a higher proportion of **bumblebee visits**, whose single visits deposited more conspecific pollen than solitary bees or flies. This is prior empirical evidence that **interaction quality/composition can compensate for changing interaction quantity**. It predates EGWEE and cannot be rebranded as a newly discovered Q–P–F law.

A related Gallagher–Campbell 2021 field experiment of *the same species/region*, [DOI 10.3389/fevo.2021.641693](https://doi.org/10.3389/fevo.2021.641693), with Dryad [10.7280/D16D7Z](https://doi.org/10.7280/D16D7Z), manipulated **flowering phenology × water availability** and measured visitor composition and reproductive output. That paper reports water availability having a stronger effect on seeds than phenology's effect on visits, but **direct compatible pollen transfer is not established by its abstract**. Do **not** count the related research as a second independent biological system, or infer identical tagged individual cohorts across the two datasets.

## Actual access gate and the next decisive evidence

`audit_mertensia_QPF004_public_source.py` checks the original published Dryad DOI/version metadata and original XLSX filenames, SHA/size manifest, and **first-row worksheet schema only** from officially advertised Dryad file links when available. It does not inspect original raw pollen, seeds, or visitation outcomes, does not read PDF contents, and does not invent joined flower/ramet records. On 401/403/429 or inaccessible original workbook it records an **access STOP**, not an ecological null.

**If both original XLSX files are obtained**, next check two separate workbooks for source treatment codes, unique plant/ramet/flower keys, nested controls, response missingness and actual overlap of same-unit Q, P and F, **before opening signed outcome relationships or preregistering a predictive transport test**. A 2015 visit and a 2016 pollen/seed assay are not observations on the same maternal flower merely because the source species is identical.

The original six-candidate frozen list in PR #66 remains at six, the existing *Oenothera* QPF001 original-source negative date-transport test and missing-fruit identification bounds remain unchanged, and nothing about the original meta-analysis or the mathematical EGWE theorem is modified. The strongest achievable source-only claim at present is an **evidence-supported taxonomic correction and a falsifiable cross-experiment joinability audit**, not a new ecological result.
