# QPF007 parentage–visitor-partner ID audit (source-only; no sexual-selection reanalysis)

**18 November 2026. Protocol source-only lock, before inspecting source-level parentage assignment rows beyond published schema and prior structural receipt.** This is an exploratory **postprimary** source-reconciliation operation nested within the *single* original Barbot et al. (2026) Brassica rapa study, and stacked on PR #88 / PR #85. It cannot add 16 independent natural systems to EGWEE or change the frozen 6-candidate source denominator.

## Published source and scientific novelty boundary

Barbot et al. (2026) *PLoS Biology*, DOI 10.1371/journal.pbio.3003579, original Zenodo 10.5281/zenodo.21628183. The authors already showed the contrast between observed pre-pollination mate access and postpollination genetic reproductive success, including 86.2% of detected paternal plants recovered under a large carry-over assumption. This is PRIOR ART. Our question here is whether the **published original genotype/paternity file is biologically joinable to the *same observational partner pairs*** at a source-certified field key without inventing source ID or experimental session labels.

The **existing source receipt** independently verified:
- 160 original unique `(session,ID_full)` main mother keys in 16 experimental sessions; `data_ABPOLL_ID_resume.txt` SHA256 `5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe`.
- 1,967 original stigma flower rows matching all 160 mother keys.
- `data_ABPOLL_ID_level_detID.txt` original 1,363 source pair rows in **18** session labels, **156** focal partner source keys, and only **138** focal keys overlapping original main table.
- `data_ABPOLL_fix10_paternities.txt` **1,099** original offspring/paternity rows; source keys `offspring_id`, `known_id`, `candidate_id` were seen but no session×mother mapping verified. SHA256 `984d60b26e870c58252b39177d923fa0707af6ea62acadfa9bf8f497da1ce6a6`.
- Pair file SHA256 `7f00bbe673eb849c11de5b7fcbeb2d2b60012765cde0f1f6bc25168dd6aedfc5`.
- README itself refers to `data_ABPOLL_ID_level_ID.txt`, but the actual publisher file is `...detID.txt`; that filename discrepancy is registered in PR #85, **not** silently repaired by interpreting rows.

## What the source-only check may inspect

1. Exact **case-sensitive** original columns, file byte sizes, original file SHA256 and row counts, original source `session`, `ID_full`, `ID_full_foc`, `ID_full_part`, `known_id`, `candidate_id` and `offspring_id` for ID-match comparisons, but do **not** read biological `seed_couple_on_foc`, visit contacts, offspring genotype, successful father categories, pollen or seed values.
2. Preserve the mother table's **16 session** keys; count mother `ID_full` string reuse between original sessions and singleton IDs. If reused, session-absent `known_id` and `candidate_id` remain nonunique even if they match a literal string.
3. Compare pairwise **exact session×focal ID** and **exact session×partner ID** against the main source. Record (a) common sessions, (b) orphan sessions, (c) rows with both source partner endpoints valid, (d) distinct directed pairs in that supported space, (e) repeated directed-pair rows, (f) exact source self pairs, and (g) source session×focal coverage. Never add a missing session to a pair row, map numbers between raw files by order, or interpret a pair with one absent endpoint as observed mating.
4. For original offspring paternity file, report only exact header and whether `known_id` / `candidate_id` strings have unambiguous literal matches to **globally unique** original maternal IDs; report ambiguous/no-match proportions and repeated offspring IDs **without revealing IDs or parentage outcomes**. Literal token equality does NOT prove that `known_id` has a maternal biological role unless the original authors' codebook explains it. Do not assume `candidate_id` is the true father rather than one of multiple candidate genotypes.
5. **No prediction, ecological effect, group association or realized father fraction** shall be computed from this audit. No original source rows, mother/site ID or private genotype published in derivative CI artifacts.

## Admission rule for any *future* realized-partner prediction (to be frozen separately, if possible)

- Only author-defined parentage record with unambiguous correct-mother and assigned-father roles; literal exact session and plant keys (or a separately source-verified one-to-one original ID→session mapping). No deduced session by similar numeric tokens, source order, treatment or offspring counts.
- Pairwise observational network and assigned genetic partners must have **same session and BOTH mother/father original IDs** source-certified.
- Require at least 12 of the original 16 source sessions with ≥3 matched focal mothers AND ≥10 distinct source directed pair rows per session and ≥80% eligible offspring assigned to uniquely mappable mother AND father identity, **before looking at any paternity effect or filtering coefficient**. If not met: `PARENTAGE_PARTNER_IDENTITY_STOP`, never turn a seemingly missing genetic father into an observed failure or estimate false mating.
- If it passes, freeze an **explicitly postprimary predictive / calibration target** *after* confirmed source codebook and only then inspect genetic identities. Since original Barbot paper already identified partner filtering, an actual novel paper requires an independent dataset/region and a generalization test, not merely replotting the original published 86.2%.

## Interpretation ceiling

Same-source partner-directed rows may reflect inferred contact via an assumed pollen carry-over; they are NOT direct observed transferred donor-specific pollen. Genotypic parentage is downstream outcome and may have sampling censoring (10 offspring per individual). A clear source-join gate protects previously observed Q/P versus genetic and seed-function divergences from dataset fusions.

This new source branch does not change either PR #88 157-mother genetic negative result, PR #85 145-mother seed exploratory result, egwee five natural-fragmentation clusters, PR #86 apple, PR #72/74 EuPPollNet, nor theoretical EGWE. No merges to main before any result and methodological review.
