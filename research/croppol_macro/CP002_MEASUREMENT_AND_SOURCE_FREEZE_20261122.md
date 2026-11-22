# CP002 — CropPol measurement and source-family audit
Date: 22 November 2026. Empirical EGWEE. Extends CP001 without changing its results.

## Purpose and chosen approach
The user asked to continue broad public-database macroecology. CP001 established
coverage; CP002 resolves what the measurements and source groups mean, then
counts the data remaining under explicit rules. Reusing the author's analysis
sample would be easy but would inherit exclusions tied to a honeybee-versus-wild-
insect question. Pooling every numeric yield/visitor cell would mix endpoints
and sampling methods. We therefore classify source metadata explicitly, preserve
separate measurement families, and audit conservative source blocking.

This is the implementer's choice under the standing proceed instruction, not a
new user-specified scientific preference. No model or biological association is
estimated in CP002. Subsequent modelling needs a separate frozen specification.

## Source and evidence
Retain the exact CP001 v2.1.0 file, commit, byte length, Git blob and 68-column
contract. Read source bytes in memory only. Author code and template metadata
may be inspected before freezing literal metadata dictionaries; record their
pinned paths and hashes. Previous presence counts are already known, and
published CropPol associations are known. No EGWEE response relationship has
been examined.

The template defines yield under natural pollinator exposure; its numerical
unit remains heterogeneous. The author selector is an instruction for the
dynamic Reilly analysis, not a universal quality flag. study_id2 groups years
when methods match and sometimes splits a common study by year/method.
Therefore neither selector nor study_id2 alone certifies our target sample.

## Bounded operations, fixed before live CP002 execution
1. Verify the original source and schema. Retain all 3,448 rows in accounting;
   never repair, deduplicate or average silently.
2. Decode only explicit bounded dictionaries for selector, taxonomic sampling
   scope, endpoint family and visit sampling/unit type. Unknown labels stay
   unknown. Do not echo arbitrary metadata, IDs, free text, contacts or values.
3. Keep primary yield and secondary yield separate. Classify primary labels as
   direct reproductive count/set, harvested mass per area/plant, product size/
   quality, visitation-derived pollen estimate, ambiguous proxy, or unresolved.
   No inferred-pollen endpoint is eligible for a visitor-to-output comparison.
   A label establishes a candidate class, not provenance of its construction.
4. Report separate candidate frames: numeric primary yield with a reviewed
   direct-output label; that plus numeric total visitation and a documented
   observation method/unit; the corresponding author-use-visits subset; and
   the separate author-use-abundance frame. Tabulate taxonomic scope rather
   than converting absent guilds to biological zero.
5. Build conservative metadata components: connect all rows with the same
   study_id2; additionally connect same year-stripped study-id stem and shared
   explicit publication DOI. Document any umbrella references separately and
   do not use generic unpublished/missing text as a shared identifier. Missing
   links remain unresolved. These are blocking components, not a proven count
   of independent research programmes. Record counts for each rule separately
   and for their union; require transitive closure.
6. Audit a nontrivial field-context baseline before prediction. Candidate
   covariates are management, field_size and plant_density, conditional on
   documented meaning. Within source component × crop × sampling year × exact
   primary-yield unit × visit unit × taxonomic scope, report block size and
   predictor completeness/variation only. Report all blocks and the prespecified
   subset with at least five complete rows and at least one varying baseline
   predictor. A group with only constant crop/year labels cannot count as a
   useful ranking baseline. Also report each covariate separately; do not choose
   a best-looking baseline after viewing scores.
7. Numeric outcome/predictor cells may be checked for finite syntax and relevant
   domain validity. Predictor distinctness may be checked for baseline
   feasibility. Do not calculate outcome distributions, correlations, effect
   signs, model scores or response-derived cutoffs. Never use held-out response
   mean, SD or maximum to normalize a future prediction target.
8. Return aggregate-only receipts, counts, classification coverage and explicit
   unresolved flags. Scientific status remains METADATA_AUDITED_NOT_MODEL_ADMISSION.
   Transport/schema failure must be nonzero with a saved safe receipt.

## Next-stage conditions and literature boundary
A future comparison needs verified source blocking, a meaningful varying
baseline, one direct-outcome family and fixed model/score definitions. A
within-held-out-source rank score can avoid incompatible numerical units, but
is not absolute yield forecasting. Presence and variation do not establish
covariate timing or remove confounding.

Reilly 2024 (10.1111/geb.13843), Turo 2024
(10.1038/s41559-024-02460-2) and Vezzani 2025
(10.1111/1365-2664.70042) already analyse yield-pollinator relationships.
Gimenez-Garcia 2023 (10.5194/we-23-99-2023) already holds authors/studies
out for VISITATION prediction. Do not claim the first held-out CropPol model.
Chabert et al. 2026 (10.1111/1365-2435.70269) explains confounding by flower
density and yield potential. Plant density is not flower density.
No causal pollinator-limitation claim is authorized by this audit.

## Delivery and boundaries
Update draft PR94 only. Preserve main, historical five-cluster fragmentation
results, Brassica/Silene branches and theoretical egwe. Do not contact authors.
Commit our code, tests, classification rules and aggregate results only.

## Execution record
- Specification committed before original CP002 row processing.
- Tests: source/metadata safety, no missing-to-zero conversion, transitive
  source blocking, method/unit separation and a genuinely varying baseline.
- Independent review before live run; retain exact run/head/source fingerprints.
