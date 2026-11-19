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
