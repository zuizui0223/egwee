# Ecological Indicators submission readiness — 2026-09-05

## Current publication decision

- **Primary target:** *Ecological Indicators*.
- **Article role:** Original Research Paper centred on indicator/state evaluation methodology.
- **Title:** *Test the state before interpreting the residual: four empirical gates for ecological state indicators*.
- **Scientific source of truth:** `natural_data_gate_registry.json` plus locked records under `evidence/`.
- **No new analysis gate:** no pooled cross-system effect, endpoint change, proxy substitution, scaling rescue, or cross-origin refit is authorised for submission preparation.

## Submission spine

The paper is organised by inferential gate, not by organism:

1. endpoint-relevant measurement adequacy;
2. information-preserving representation;
3. transferable residual-context testing;
4. cross-study identifiability.

Seven natural-data analyses occupy distinct branches. Six negative/failed/representation-collapse system branches are tabulated as downstream inferences not licensed by the frozen evidence; *Oenothera harringtonii* is retained separately as a positive missing-coordinate diagnosis. The cross-origin STOP is synthesis-level, not a seventh system row.

## Submission files

- [x] authoritative manuscript spine;
- [x] complete methodological + natural-system bibliography;
- [x] five Highlights, each <=85 characters;
- [x] submission metadata and author-controlled placeholders;
- [x] Ecological Indicators cover letter;
- [x] deterministic Figure 1 four-gate workflow;
- [x] deterministic Figure 2 seven-system branch map;
- [x] deterministic graphical abstract;
- [x] Table 1 generated from `unreachable_six_systems.json`;
- [x] deterministic submission builder and SHA-256 manifest;
- [x] evidence-note provenance included without redistributing third-party raw data;
- [x] downstream EGC/EGWE headline-value firewall in the builder;
- [x] dedicated GitHub Actions submission workflow;
- [x] final rasterized visual QA of Figure 1, Figure 2 and graphical abstract;
- [x] Figure 1 right-edge branch-label clipping corrected after visual QA;
- [x] Figure 2 synthesis-boundary label / machine-ID spacing corrected after visual QA.

## Final submission-artifact QA

The final visual-QA workflow on head `658fe81bcfe9bf8f8365ffc6c0e973389af321ca` completed successfully as run `33901155115`. Its uploaded submission artifact was:

- artifact ID: `9947675062`;
- artifact name: `egwee-ecological-indicators-submission`;
- artifact digest: `sha256:0a36e6ec4331f93b4a870317845fb8c93f51b2658703ea1d2b6a679e07d3ebae`.

The artifact was downloaded, the three SVG displays were rasterized at high preview resolution, and the generated images were inspected directly. Figure 1 no longer clips `study/origin/protocol confounded`; Figure 2 cleanly separates `Synthesis-level boundary` from `cross_origin_convergence_not_identifiable_from_existing_archives`; the graphical abstract required no correction. The layout-only fixes were merged as PR #3, merge commit `22da5cfe51b6db04d293bd9cb4b7b5bf26c3df2f`.

This visual QA did not alter any scientific text, system assignment, effect estimate, endpoint, stop rule, bibliography, or claim ceiling.

## Live-policy checks

Elsevier's current general Highlights guidance specifies 3–5 bullets and <=85 characters per bullet. This contract is checked automatically in the submission workflow. The live *Ecological Indicators* portal/Guide for Authors must still be rechecked immediately before actual submission for any journal-specific changes, graphical-abstract requirements, declarations, and file-format rules.

## Author-only completion items

- [ ] author list and order;
- [ ] affiliations and ORCIDs;
- [ ] corresponding-author details;
- [ ] CRediT roles;
- [ ] funding and acknowledgements;
- [ ] competing-interest declaration;
- [ ] final AI/automated-tool disclosure;
- [ ] permanent archive DOI/reviewer-accessible code snapshot;
- [ ] final portal-specific formatting after live guide recheck.

## Merge gate

**Passed.** The four-gate manuscript contract, deterministic Ecological Indicators submission-bundle workflow, submission firewall, Highlights contract, uploaded artifact, and final rasterized visual QA have all completed successfully. Further scientific reopening is not required by the active manuscript claim.