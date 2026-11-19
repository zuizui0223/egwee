# QPF007 post-codebook father/mother ID-membership diagnostic (role-verified, no contact-effect)

**2026-11-19. Postprimary, post-ID and post-author-code audit**, before the first mother–father dyad membership count computed by the new script. This is **not outcome-blind** to the underlying published father-assignment method: the source article explicitly reports 1,099 assigned genotyped seedlings at 80% CERVUS confidence and the original R code groups `candidate_id` in male offspring summaries and `known_id` in mothers' genotyped-seed summaries. The source-published R code at SHA256 `a8e47abb7b2b4e7d6f85574fa6444eddd35a2bf0537592eccb4354fabb2402e9` derives the session from the first five characters of `known_id`.

## Locked scope

At this stage, read **ID fields only** from original 160-mother (16 sessions), 1,363 directed pair-table rows (18 sessions), and 1,099 genotyped offspring father-assignment rows. Verify source Zenodo publisher manifest MD5 and exact original SHA256 for all three files. Require globally unique full maternal plant ID, source author R-role lines unchanged and proper explicit original session. Derive genetic mother session from the original maternal map and check the original author's five-character `known_id` rule, then verify whether each assigned paternal ID belongs to **the same original session**.

Report aggregate counts only: unique offspring-ID labels, any duplicate offspring labels, total within-session paternity assignments, unique (mother, father) assigned genetic pairs, self pairs and the number of genetic pairs whose **ID pair appears as a row** in the original directed `ID_full_foc`→`ID_full_part` table, in both orientations. No original mother, father, offspring or genotype labels may be emitted or committed.

**Critical denominator:** a row in the original 1,209 exact-ID pair table is *not* automatically an observed flower contact. The row may exist with zero visitation/count; that semantic status MUST be independently identified from the original pair-table field meanings and R code before computing observed-father recovery, calibration, precision, a null randomization or ecological association. No outcome effect is evaluated under this protocol; ID-pair membership itself is a **structural genetic outcome identity count**, not an outcome-blind registry test.

## Scientific status

Stop biological calibration when any assigned father/known mother source session is inconsistent, the source has duplicated offspring assignments, or the source pair table's observational-contact metric cannot be certified. An original offspring assignment rate at 80% CERVUS confidence does not imply that **every candidate pollen donor was genetically compatible** nor that genotyped offspring constitute all seeds. Paternity genotyping selected up to 10 viable seedlings per maternal plant, so sampling can artificially limit the number of known genetic mates.

Any future **novel** calculation would assess how much reported observational–genetic edge recovery exceeds a source-degree- and genetic-sampling-aware null across whole experimental sessions, preferably with independent biological programmes. The already published recovery under maximal carryover and pre/postpollination selection results from Barbot et al. (2026) are prior art, not an EGWEE discovery. With one experiment only, do not infer a universal fragmentation regime or genetic compatibility mechanism.

No changes to historical QPF001–QPF006 denominator, original QPF007 preregistered complete-case STOP, PR #88 exploratory genetic mate prediction, other egwee draft research PRs, theory egwe, or main.
