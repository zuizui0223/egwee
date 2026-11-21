# CP001 — verified CropPol source coverage before predictive modelling

**21 November 2026. Executed original-source audit; no biological effect estimated.**
A pinned multi-study database is now available for the empirical project's
macroecological direction. Admission to a predictive analysis remains closed
until measurement and source-group definitions are reconciled.

## What was retrieved and verified

The [official CropPol v2.1.0 field file](https://github.com/ibartomeus/CropPol/blob/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data/CropPol_field_level_data.csv)
at commit `febec7dcc088ccf1bd721c41ce8dda87a2dcba1a` was read in memory.
Its 2,195,393 bytes match Git blob
`cd19a354741ac40428e6b94aa1ec2ee596ff0547`; actual file SHA256 is
`ecfa84d1f6a52f24f13b7096347a59f231e8cc77eef8692b0a0183ceca86f879`.
All 68 ordered column names match the author-code contract.

The [freeze](CP001_SOURCE_COVERAGE_FREEZE_20261121.md) was committed at
`13084a772c3fe1a409636dc925e9cc1f0ba98839` before original row processing.
The first live [run 44915335822](https://github.com/zuizui0223/egwee/actions/runs/44915335822)
at implementation head `4a7fcbac80d6944d48fde92d63a956150dd248c0` passed ten
offline regressions and original source/schema verification.

## Actual coverage of the pinned file

| Presence-only subset | Rows | Provisional study_id2 groups | Crops | Countries |
|---|---:|---:|---:|---:|
| Whole file | 3,448 | 145 | 48 | 35 |
| Numeric primary yield with a populated unit field | 2,545 | 104 | 40 | 31 |
| Above plus numeric data in a visit field | 1,710 | 53 | 23 | 21 |
| Above plus numeric data in an abundance field | 1,593 | 88 | 37 | 30 |
| Above plus observed pollinator richness | 1,168 | 66 | 34 | 26 |
| Numeric seed/fruit-count component plus a visit field | 266 | 14 | 10 | 7 |

Visit and abundance subsets overlap. A separately labelled exploratory coverage
check found **802 shared rows and 38 shared provisional groups**. They must not be
summed as separate observations or programmes. The 266-row subset uses only the
dedicated `fruits_per_plant`, `seeds_per_fruit` and `seeds_per_plant` columns;
it is not a census of all reproductive outcomes, some of which occur in yield
fields with differing units.

There are **221 distinct study_id labels**, **145 study_id2 labels**, and **222
study_id × sampling_year keys**. Every one of the 3,448 candidate
`study_id × site_id × sampling_year` keys is populated and unique. All
study_id-to-study_id2 mappings are consistent. These are identifier checks;
they do not prove that biological sites, samples, research teams or programmes
are independent.

The primary yield column has numeric values in **2,589 rows**, of which **44**
lack a unit entry. All inspected nonmissing numeric cells match numeric syntax.
Zeros are observed values. No response magnitudes, signs, averages,
correlations, model scores or coefficients were calculated.

## Independent verification

A second analyst used a separate Python CSV parser with finite-Decimal
presence checks, without reading or reusing the production auditor. The
original bytes, SHA256, all supplied full-file/key counts, and the visit,
abundance and dedicated seed/fruit-count subsets matched exactly.
[Independent recount receipt](CP001_INDEPENDENT_RECOUNT_20261121.json).

The production [aggregate receipt](CP001_ORIGINAL_COVERAGE_RECEIPT_20261121.json)
was downloaded from artifact 14711446319 through the supported GitHub artifact
API. Its ZIP SHA256 independently matched
`eb0e29cd6d55c51192d7201a1c8fd2e496c569702bd521c579b842b242a80d53`.
No source CSV or raw records are included in these receipts.

## Why these are not yet an admitted model sample

1. **Source independence.** study_id2 is an author-supplied grouping variable.
   Its consistent mapping is useful, but repeated years, shared samples and
   reused inputs from earlier syntheses still need source-family reconciliation.
   The 145 labels are not 145 newly verified independent experiments.
2. **Measurement definitions.** The bounded output vocabulary recognized no
   values of `use_visits_or_abundance`: all 3,448 entries fall into
   `<unreviewed_label>`. This is an unreviewed code convention, **not a claim
   that all values are missing**. The code must be decoded from author metadata
   or processing code before choosing a visitor measure. Likewise 1,990 yield-unit
   entries are unreviewed labels and 802 are missing; the limited vocabulary is
   deliberately not an endpoint classifier.
3. **Outcome meaning.** Populated yield-unit fields do not establish equivalent
   endpoints. Direct seed/fruit outcomes, harvested mass and inferred pollen
   scores need separate treatment. Visitor measurements can differ in methods
   and taxonomic coverage. Numeric syntax does not resolve these meanings.
4. **Prediction design.** A new whole-source holdout must be frozen only after
   that reconciliation. No random split of field rows, use of held-out response
   means/variances, or retrospective selection of a favourable endpoint is
   permitted. Confounding and selective data coverage remain limitations.

Thus the current decision is **SOURCE_COVERAGE_VERIFIED_NOT_MODEL_ADMISSION**.

## Relation to prior work and earlier EGWEE sources

[Allen-Perkins et al. 2022](https://doi.org/10.1002/ecy.3614) introduced CropPol;
[Reilly et al. 2024](https://doi.org/10.1111/geb.13843) already analysed
visitor–yield associations, using a 93-study filtered sample and reporting
2,321 site-years. Their earlier 202-study inventory, 137-study grouping and
93-study analysis have different version/grouping/inclusion meanings. The
current 221/145 labels are not a failed reproduction of those denominators.

The proposed added question concerns transport of prediction to withheld
sources, with novelty still to be assessed. This agricultural database does
not provide individual pollen-donor or sire identities and is not an
independent contact-to-sire replication of Brassica. The existing
fragmentation synthesis and theoretical egwe are unaffected.

The data-paper noncommercial CC BY-NC-SA statement, older metadata CC By label,
and repository software MIT label are retained separately. No blanket license
claim for raw data is made; this work provides original code and aggregate
receipts only.

## Review decisions and next bounded work

Independent code review found four consequential issues before source retrieval:
arbitrary categorical text could escape, some transport errors lacked receipts,
schema STOP discarded verified-byte evidence, and schema fingerprints/source
pins lacked an independent test. These were corrected in one regression pass.
The exact-source rule was also enforced by rejecting redirects before following
them. Ten tests pass; categorical outputs are bounded and unfamiliar labels
are counted without echoing their contents. The cost of that conservative
choice is incomplete category interpretation at this stage, explicitly shown
above.

Next: audit the author-defined source grouping and measurement-code dictionary;
freeze a direct-outcome family and one baseline/visitor predictive comparison;
then test whole-source transfer if enough independently traceable units remain.
The present gate is complete; model admission and effect estimation are not.

