# Full GenoDive sample-ID source gate — Pseudoziziphus celata (2026-11-15)

**Verdict:** `UNVERIFIED_SEMANTIC_CROSSWALK_REQUIRED`. Public *genetic* source is **recovered**, but the molecular–survival join is **not yet identifiable** from literal sample IDs. **This is not a negative genetic/functional rescue effect.**

## Primary records and machine evidence

- Original article: Edwards et al., *Annals of Botany* 138:216–229 (2026 issue; online 2025), DOI [10.1093/aob/mcaf259](https://doi.org/10.1093/aob/mcaf259).
- Original public Figshare source [10.6084/m9.figshare.30290722](https://doi.org/10.6084/m9.figshare.30290722) version 1, full native dataset file `Copy of Genodive All Populations.2025` (Figshare file ID `58525312`).
- GenoDive native-format specification: [GenoDive 3 manual](https://www.patrickmeirmans.com/GenoDiveManual.pdf) and R `polysat::read.GenoDive` source-format documentation. Native first two lines declare sample/population/locus counts and the column header identifies the individual-name field; marker allele columns are excluded from this audit.
- New reproducible source-only script: `research/rescue_coupling/audit_ziziphus_genodive_sample_ids.py`; paper-level survival grain audit remains `ZIZIPHUS_GENOTYPE_SURVIVAL_ID_GATE_20261115.md`.
- First successful source run: [43694463687](https://github.com/zuizui0223/egwee/actions/runs/43694463687), artifact 14153264126.
- Second, additional full-population-name check: [43694749139](https://github.com/zuizui0223/egwee/actions/runs/43694749139), artifact `14153298306` (all checks success). It found **3/12** genotype population-name strings occurring among the **41** survival `popcode` labels. This is only literal label overlap, not a validated common identity or mapping for the other nine populations.

## Source-exact audit results

| Evidence item | Raw source result | Interpretation |
| --- | ---: | --- |
| Declared individual records | **1,120** | Matches independently published genotyped-transplant denominator |
| Actual nonempty sample-name records | **1,120** | Native header and data rows internally consistent |
| Unique sample-name labels | **1,120** | No duplicate textual sample name within this genotype source |
| Declared populations | **12** | Distinct translocation populations; do not equate with 41 `popcode` labels in the other file |
| Microsatellite loci | **12** | Count is metadata only; no genotype/allele cell was read |
| Published survival rows | **1,185** | Long/record structure; not 1,185 independent plants |
| Direct sample-name match to survival `plant_id` | **0** | Textual names are not a verified shared key |
| Direct sample-name match to survival `genotype` | **0** | The latter may be sibling-family code rather than molecular individual identifier |
| Direct sample-name match to survival `Rgenotype` | **0** | No validated mapping |
| Direct population-index + sample-name vs `popcode` + `plant_id` match | **0** | Population index and field code may use different naming conventions; no inferred biological equivalence |
| GenoDive population *name* vs survival `popcode` literal overlap | **3** of 12 genotype population names | Partial same-string population label matches only; membership and biological unit correspondence are NOT established |

Source digests:
- Complete GenoDive native source SHA-256: `acdaef526f52c72e1b88076dc79a236d6d5e24037d8bdea050182f9541f80d47`
- Published survival TSV source SHA-256: `17395280f02a5fb88810555237ae637c993279a23da0bc6179f1233ca5f75b59`

**Important source distinction:** Previous PR #54 examined `Zc_parentgenotypedata.xlsx` with only 59 XML rows (candidate parent panel), *not* the 1,120-individual GenoDive file. That explained why the original Genodive dataset was a necessary additional check.

## Biological meaning and safety ceiling

The original article identified 52 potential parents at 12 loci, genotyped 1,120 transplants and traced full-sib parentage; a handful of parental crosses contributed most offspring, while survival varied by sib group. The authors reported that genetic data-guided translocations produced a more even representation of full-sib groups but not higher genetic diversity. These are **published results**, not estimates recomputed here.

**The raw survival table has reused local `plant_id` labels** (40 distinct labels, 41 `popcode` values), and the most permissive candidate `popcode × plant_id` has only 98 keys, not 1,120 verified individuals. Further expanded identifiers also repeat. No crosswalk was exposed by exact literal string matching; matching based on length or guessed prefix is forbidden without source documentation.

Accordingly:
- The file provides true genotype/parentage information **at the published source level**, but no admissible same-individual G/W/F reanalysis yet.
- Survival is `W_survival`, **not `F_direct` ecological-function recovery**; the reproductive process limitation may be analyzed in a distinct same-family causal design only after the source provides the genetic-mate/compatible pollen data and matched biological units.
- If a population/sibship codebook can map transplants to the survival records, group-level descriptive or survival analyses may be possible. Nevertheless the original 2026 paper already studied sibship survival. The novelty for EGWEE must be a **cross-programme, preregistered gene-flow × direct-function interaction contrast**, not duplicating their reported survival association.
- Nothing in this experiment establishes the effect of adding migrants, changes in genetic load, or a general ecological-function recovery benefit without matching source intervention contrasts.

## Next admissibility gate

**Acquire/verify the source mapping for Figshare GenoDive `Individuals` identifiers → `ziziphus.survival.txt` `popcode`, `intro_yr`, `plant_id` or full-sib code.** Compare exact official population names and original R/analysis codebook before aligning individual records.

If no mapping can be verified, preserve `ID_LINKAGE_STOP` and expand the **independent empirical** candidate universe (not simulated seeds) with newly published 2026 genetic + demography studies, while screening for direct reproductive-function outcomes and independent source measures.

**Frozen outcome rule:** no marker allele calls, transplant survival event values, fitness effect directions or genome–function coefficients were read or estimated in this source audit.
