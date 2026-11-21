# Molecular-to-functional conservation bridge — prospective design (2026-11-18)

Status: design-only, no new empirical effect or model-to-nature validation. Branch-only; do not alter the frozen five-cluster synthesis or active manuscript.

## Central test
Does a joint molecular compatibility × effective interaction state improve held-out prediction of future seed/recruitment function beyond census, ancestry, neutral diversity, and interaction marginals? Does a controlled genetic/pollen intervention recover function only when mating compatibility is limiting?

## Exact crosswalk and cautions
- D: flowering density, demographic stage, patch size; no SNP surrogate.
- I: visits, pollen deposition, pollen tube success; visit counts are not compatible fertilisation.
- G_neutral: genome-wide SNP heterozygosity, F_IS, ancestry, kinship; not identical to functional allele availability.
- G_compatibility: empirically validated S-genotypes or diallel-estimated mate compatibility; inference method flagged.
- C_pollen: paternity-based effective pollen donors, donor origins; not equivalent to landscape distance or model allele-mixing m.
- T: measured phenotype with validated genotype association; expression alone is not causality.
- F_direct: viable seed set and subsequent recruitment; distinguish general fitness W.
- Relational state: within-site joint distribution/covariance of I, G_compatibility, T, not merely their separate means.

## Source-first gate (no outcome peeking)
1. SMF001 Argentina anserina (Dryad 10.5061/dryad.pnvx0k6zm): controlled crosses, inferred S alleles, pollen tubes, outcross seeds; natural visitation same-grain unknown.
2. SMF002 Leavenworthia alabamica (Dryad 10.5061/dryad.2pj0j): field pollinators, S-locus and seed outcomes; maternal/year joins unverified.
3. SMF003 Rutidosis leptorrhynchoides (Young & Pickup 2010, doi:10.1111/j.1365-2664.2010.01798.x): seven population-level pollen deposition, mate compatibility and seed set; structured original seven-row data unverified.
4. SMF004 Spondias purpurea (doi:10.1016/j.biocon.2021.109007): genetic/paternity and functional observations currently not verified at common mother×time grain.

Only source metadata, sheets, headers, key types, units, dates, controls, access rights and provenance hashes may be inspected before freezing outcome model. Do not fabricate joins or infer missing values as zero.

## Prediction gate
Eligible grain: maternal plant or population × year/cohort with measured exposure and future F_direct. Lock train/test split by entire population/programme (not offspring or loci). Baseline M0: D + environment + ancestry + G_neutral + measured I. M1: M0 + validated G_compatibility + effective C_pollen + predeclared I×G compatibility and spatial alignment. Report held-out log score/NLL difference, bootstrap by independent population/programme, calibration and negative controls. If no aligned records, output NOT_IDENTIFIABLE.

## Intervention gate
Only if controlled within-/between-population pollen, compatibility, and direct seed function are recoverable with recipient controls. Prespecify genetic donor × ecological/pollinator treatment factorial when available. Compare direct F outcomes, neutral G, validated functional G, general W and D separately; prevent demographic supplementation being labeled genetic rescue. Genotype ancestry, ploidy, maternal and paternal donor effects and outbreeding depression must be audited. No meta-analysis until independent study denominators support it.

## Falsification
- M1 fails to improve held-out prediction: no supported transfer of relational state in this dataset.
- M1 improves only within studies, not leave-programme-out: nonportable, not general.
- Neutral heterozygosity improves while compatibility and F do not: marker improvement without demonstrated ecological-function recovery.
- Pollen/compatibility factorial fails: the hypothesized limiting process not supported under that design.
- No verified synchronized data: measurement non-identifiability, not ecological null.

## Conservation interpretation ceiling
Prioritize identifying the limiting ecological/mating process, then match intervention to bottleneck. Do not claim a universal genomic warning threshold, universal S-locus mechanism, natural AUC=0.927, or equivalence of pollen, individual and allele-frequency mixing. This is an independent design programme, not a re-analysis selected to repair Serapias-sensitive EGWEE significance.

Source anchors: research/compatibility_function/PRIMARY_PROGRAMMES_SOURCE_GATE_20261117.md; research/rescue_coupling/PLANT_PRIMARY_SOURCE_SCREEN_20261115.md; research/rescue_coupling/PROTOCOL_20261115.md; EGWE manuscript/theoretical_ecology_article.md.
