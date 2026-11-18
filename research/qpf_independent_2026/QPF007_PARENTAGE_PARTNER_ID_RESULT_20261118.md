# QPF007 original pair/parentage source-ID reconciliation (postprimary), 2026-11-18

**Status: ID-only joins verified; biological parentage role and assigned-father status not yet certified. NO mating/fitness coefficient computed.** Empirical egwee, one published Barbot et al. (2026) *Brassica rapa* manipulated pollinator experiment, *not* 16 independent natural ecosystems.

## Original published sources and provenance

Barbot et al., *Pollinator abundance shapes sexual selection in an angiosperm*, PLoS Biol. DOI [10.1371/journal.pbio.3003579](https://doi.org/10.1371/journal.pbio.3003579). Original [Zenodo 10.5281/zenodo.21628183](https://doi.org/10.5281/zenodo.21628183). Source fingerprinted files:

| Original source table | Original rows | Original SHA256 |
| --- | ---: | --- |
| Individual `data_ABPOLL_ID_resume.txt` | 160 | `5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe` |
| Directed pair `data_ABPOLL_ID_level_detID.txt` | 1,363 | `7f00bbe673eb849c11de5b7fcbeb2d2b60012765cde0f1f6bc25168dd6aedfc5` |
| Offspring paternity `data_ABPOLL_fix10_paternities.txt` | 1,099 | `984d60b26e870c58252b39177d923fa0707af6ea62acadfa9bf8f497da1ce6a6` |

Strict original file bytes, publisher record MD5 checksums, exact biological IDs and source-native session labels reproduced in [successful GitHub Actions run 44306123175](https://github.com/zuizui0223/egwee/actions/runs/44306123175). Script `audit_qpf007_partner_parentage_ids.py` outputs only source metadata/aggregate and **does not read or fit visit, pollen, seed, parentage assignment or genetic outcomes**.

## Actual structural results (ID-only)

| Question | Source-verified result |
| --- | ---: |
| Original individual main `session×ID_full` keys | **160** across **16 sessions** |
| `ID_full` that are globally unique even without session | **160/160** |
| Original observed/inferred directed pair rows | **1,363** across **18** session labels |
| Directed pair rows outside all 16 original main-study sessions | **154**, *not* mappable to main |
| Strict pair rows with BOTH exact `(session, focal)` and `(session, partner)` plant keys in main | **1,209** |
| Distinct source direct pairs in those rows | **1,209** (no duplicate directed keys) |
| Original focal mother source keys with both source partner IDs validated | **138** |
| Source sessions with >=3 focal mothers and >=10 valid directed pair records | **16/16** |
| Offspring paternity rows whose `known_id` string exactly matches a globally unique original plant ID | **1,099/1,099** |
| Offspring paternity rows whose `candidate_id` string exactly matches a globally unique original plant ID | **1,099/1,099** |

**Interpretation:** the earlier "raw paternity rows have no source-certified session×mother key" statement remains true **as an explicit role/join certification boundary**, but the new original code proves **literal 1-to-1 plant identifier lookup** is available for every raw paternity `known_id` and `candidate_id`. There is no duplication of mother ID strings across original sessions. The 154 extra directed pairs are a **source coverage difference**, not a biological negative absence of visits or reproduction; never fill them by guessed session or assume source pair rows reflect all 160 mothers.

The original authors already reported a pre/postpollination partner discordance and an 86.2% recovery of genetically identified fathers from observational mating contacts under their highest pollen carry-over assumption. This is **PRIOR ART**, not new EGWEE mate filtering discovery.

## Remaining nonadmission (important)

The **exact string match does not itself establish the original semantics** of `known_id` and `candidate_id`: the latter may be a scored candidate rather than the uniquely chosen father, and paternity measurements can be conditional on 10 genotyped offspring per maternal plant. Before computing a false-positive/false-negative contact–fertilization rate, inspect the verified author original analysis code and its assignment/mother roles, identify the source paternity sampling denominator, and confirm the directed focal/partner row roles. The source-only decision is **`AUTHOR_ROLE_AND_ASSIGNMENT_SEMANTICS_VERIFICATION_REQUIRED`**, not a green light to fit per-pair survival.

A separately version-frozen author-R-source codebook audit `QPF007_AUTHOR_CODE_PARENTAGE_ROLE_FREEZE_20261118.md` tests whether these biological roles can be verified from original author code, without executing that code or opening original phenotype values. Do not claim father identification as accomplished until that source meaning check passes.

## Scientific next gate if roles are source-confirmed

At least 12 source sessions with >=3 focal mother plants and >=10 valid direct pairs each, correct source mother/father roles, >=80% of original genotyped offspring assigned to a uniquely source-identifiable father. If any source-semantic component is unverified: STOP; no invented missing fathers or unobserved partners. Even a fully source-backed calibration within this **one original experimental study** must be called exploratory, not independent macroecological generalization, and cannot be promoted over the original authors' mechanism claims.

Parent PR #85 original 160 source frame and 145-seed coverage STOP, PR #88 157-mother genetic mate no-increment, historical five-cluster/17-effect natural fragmentation synthesis, EuPPollNet, CropPol, apple PR #86 and theoretical egwe all untouched. No source rows, genotype, mother ID, mating partner ID or reproductive values redistributed.
