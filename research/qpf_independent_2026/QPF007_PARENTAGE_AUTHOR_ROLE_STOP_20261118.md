# QPF007 author-assignment semantics: provisional source STOP

Date: 2026-11-18 (source verification sequence); status: **AUTHOR_PARENTAGE_ROLE_UNCERTIFIED_STOP**, pending a verified published parentage codebook. This is not a biological effect, null result, or finished genotype/fertilization network.

## Evidence available

- Original Barbot et al. 2026 *Brassica rapa* Zenodo 10.5281/zenodo.21628183 metadata, original published files and SHA-verified mother/observed partner/parentage records are available.
- Actual source ID-only gate [44306123175](https://github.com/zuizui0223/egwee/actions/runs/44306123175) established globally unique 160 original mother ID strings, 1,209 exact original 16-session directed partner pairs (out of 1,363 published rows; 154 are other-session rows), and unique ID-string matches for 1,099 raw `known_id` and `candidate_id` fields.
- A preliminary publisher-analysis-code audit requested a filename `script_ABPOLL_main_analyses.R` not verified by the publisher's file list at that exact name; this **is a discovery/metadata mismatch, not proof the author supplied no scripts**. Source roster diagnosis is implemented in `audit_qpf007_published_author_code_roles.py`; until a real original script and its exact checksum and role semantics are certified, parentage remains unresolved.

## Non-negotiable scientific STOP

**The literal `candidate_id` string is not itself evidence of an assigned fertilizing father**. Likewise a literal `known_id` match is not, by itself, proof of mother versus control genotype role. No observed directed edge can be classified as a fertilization success or failure from this source audit alone.

The original authors have already investigated whether observed contacts correspond to realized genetic mating; their published 86.2% recovery under a particular pollen carry-over assumption is **PRIOR ART**, not a new EGWEE ecological discovery.

No original genotype, source individual rows, father assignment, per-pair seed counts, or visitation intensities were read in the ID-only audit. A new pairwise ecological claim requires an independently verified original author role codebook and explicit mother→father→offspring assignment, with source session harmonization and a separately frozen, outcome-blind estimand. This branch **does not** add independent natural populations, confirm any paternity-derived effect, or change the historical QPF six-source and original QPF007 145-mother coverage STOP.

## Work recorded

- Source interpretation lock `QPF007_PARENTAGE_PARTNER_SOURCE_FREEZE_20261118.md`.
- Structural audit `audit_qpf007_partner_parentage_ids.py`; verified [CI 44306123175](https://github.com/zuizui0223/egwee/actions/runs/44306123175).
- Original manuscript/source role review lock `QPF007_AUTHOR_CODE_PARENTAGE_ROLE_FREEZE_20261118.md`.
- Publisher source-code roster/role scanner `audit_qpf007_published_author_code_roles.py` with fail-closed codebook absence and no automatic role certification.
- No external source code redistribution; GitHub PR remains **DRAFT** stacked on PR #88.

**Current decision: STOP father-specific quantitative analysis.** This gate protects the earlier *stigma count → genotype-inferred mate number* prediction from being mislabeled as direct observational pollen father matching.


---

## Superseded 2026-11-19 role-evidence resolution — preserve original historical STOP

This file faithfully records an **earlier temporary source-role STOP**. That blocker was subsequently resolved by a **separate later source-code verification**, not by guessing a father from its `candidate_id` string. The published Zenodo README refers to `script_ABPOLL_main_analysis.R` (singular), but the **actual publisher record** exposes `script_ABPOLL_main_analyses.R` (plural). Publisher advertised MD5 and the full actual **297,463-byte R source SHA256 `a8e47abb7b2b4e7d6f85574fa6444eddd35a2bf0537592eccb4354fabb2402e9`** were verified by [CI 44460795179](https://github.com/zuizui0223/egwee/actions/runs/44460795179). Its original code derives `session` from the 5-character `known_id` prefix, groups `candidate_id` for original father/seed assignments, and `known_id` for original maternal genotyped offspring counts, consistently with the paper's CERVUS 80%-confidence assignment methods.

The follow-up source-hash gate [CI 44460795341](https://github.com/zuizui0223/egwee/actions/runs/44460795341) confirmed **1,099/1,099 assigned parent IDs in the same source session**, 391 distinct genetic mother–father pairs (88 selfing), and 361 genetic pairs with a corresponding **row** in the source partner table. These are source-role/identity findings, not evidence that all rows represent positive observed pollinator contact. The subsequent [`QPF007_CONTACT_GENETIC_PARENTAGE_NULL_RESULT_20261119.md`](QPF007_CONTACT_GENETIC_PARENTAGE_NULL_RESULT_20261119.md) reports a *later, separately frozen, exploratory* pair-specific contact and sire-assignment benchmark with true positive contact values and a source-parental-margin conditional null.

**Original snapshot intact:** The previous STOP was appropriate prior to codebook verification, but it is no longer the current biological-role blocker. Limits persist: CERVUS assignment is not error-free, paternal source genotype is not physically measured stigma pollen, the 16 sessions are one study, and the original author's broad mate filtering finding is prior art.
